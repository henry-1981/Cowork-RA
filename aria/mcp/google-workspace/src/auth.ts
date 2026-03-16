import { google } from "googleapis";
import { OAuth2Client } from "google-auth-library";
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "fs";
import { join } from "path";
import { homedir } from "os";
import { createServer } from "http";

const SCOPES = [
  "https://www.googleapis.com/auth/documents",
  "https://www.googleapis.com/auth/drive",
];

const TOKEN_DIR = join(homedir(), ".config", "google-workspace-mcp");
const TOKEN_PATH = join(TOKEN_DIR, "tokens.json");

let oauth2Client: OAuth2Client | null = null;

/**
 * Load OAuth client credentials from oauth-client.json or environment variables.
 */
function loadClientCredentials(): { clientId: string; clientSecret: string } {
  // Environment variables take priority
  if (process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET) {
    return {
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    };
  }

  // Fall back to oauth-client.json
  const candidates = [
    join(process.cwd(), "oauth-client.json"),
    join(__dirname, "..", "oauth-client.json"),
  ];

  for (const path of candidates) {
    if (existsSync(path)) {
      const raw = JSON.parse(readFileSync(path, "utf-8"));
      // Support both flat format and Google's downloaded format
      const installed = raw.installed ?? raw.web ?? raw;
      return {
        clientId: installed.client_id,
        clientSecret: installed.client_secret,
      };
    }
  }

  throw new Error(
    "OAuth 클라이언트 설정을 찾을 수 없습니다. oauth-client.json 파일을 배치하거나 GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET 환경변수를 설정해주세요."
  );
}

/**
 * Get or create the OAuth2 client singleton.
 */
export function getOAuth2Client(): OAuth2Client {
  if (oauth2Client) return oauth2Client;

  const { clientId, clientSecret } = loadClientCredentials();
  oauth2Client = new google.auth.OAuth2(
    clientId,
    clientSecret,
    "http://localhost:0/callback" // port is set dynamically during auth flow
  );

  // Load saved tokens if they exist
  if (existsSync(TOKEN_PATH)) {
    const tokens = JSON.parse(readFileSync(TOKEN_PATH, "utf-8"));
    oauth2Client.setCredentials(tokens);
  }

  // Auto-refresh: save new tokens when refreshed
  oauth2Client.on("tokens", (tokens) => {
    const existing = existsSync(TOKEN_PATH)
      ? JSON.parse(readFileSync(TOKEN_PATH, "utf-8"))
      : {};
    const merged = { ...existing, ...tokens };
    mkdirSync(TOKEN_DIR, { recursive: true });
    writeFileSync(TOKEN_PATH, JSON.stringify(merged, null, 2));
  });

  return oauth2Client;
}

/**
 * Check if the user has valid (or refreshable) credentials.
 */
export function isAuthenticated(): boolean {
  const client = getOAuth2Client();
  return !!(client.credentials.access_token || client.credentials.refresh_token);
}

/**
 * Run the OAuth2 authorization flow.
 * Opens a local HTTP server, returns the auth URL for the user to visit.
 * Waits for the callback, exchanges code for tokens, and saves them.
 */
export async function authenticate(): Promise<{ authUrl: string; waitForCallback: () => Promise<void> }> {
  const { clientId, clientSecret } = loadClientCredentials();

  return new Promise((resolve, reject) => {
    const tempServer = createServer();
    tempServer.listen(0, () => {
      const port = (tempServer.address() as { port: number }).port;
      const redirectUri = `http://localhost:${port}/callback`;

      const client = new google.auth.OAuth2(clientId, clientSecret, redirectUri);

      const authUrl = client.generateAuthUrl({
        access_type: "offline",
        scope: SCOPES,
        prompt: "consent",
      });

      const waitForCallback = (): Promise<void> =>
        new Promise((resolveWait, rejectWait) => {
          const timeout = setTimeout(() => {
            tempServer.close();
            rejectWait(new Error("인증 시간 초과 (5분). 다시 시도해주세요."));
          }, 300_000);

          tempServer.on("request", async (req, res) => {
            if (!req.url?.startsWith("/callback")) {
              res.writeHead(404);
              res.end();
              return;
            }

            const url = new URL(req.url, `http://localhost:${port}`);
            const code = url.searchParams.get("code");
            const error = url.searchParams.get("error");

            if (error) {
              res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
              res.end("<h1>인증 실패</h1><p>Google 인증이 거부되었습니다. 창을 닫아주세요.</p>");
              clearTimeout(timeout);
              tempServer.close();
              rejectWait(new Error(`Google 인증 거부: ${error}`));
              return;
            }

            if (!code) {
              res.writeHead(400);
              res.end("Missing code");
              return;
            }

            try {
              const { tokens } = await client.getToken(code);
              mkdirSync(TOKEN_DIR, { recursive: true });
              writeFileSync(TOKEN_PATH, JSON.stringify(tokens, null, 2));

              // Update the singleton
              oauth2Client = client;
              oauth2Client.setCredentials(tokens);

              res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
              res.end("<h1>인증 완료!</h1><p>이 창을 닫고 ARIA로 돌아가세요.</p>");
              clearTimeout(timeout);
              tempServer.close();
              resolveWait();
            } catch (err) {
              res.writeHead(500, { "Content-Type": "text/html; charset=utf-8" });
              res.end("<h1>토큰 교환 실패</h1><p>다시 시도해주세요.</p>");
              clearTimeout(timeout);
              tempServer.close();
              rejectWait(err);
            }
          });
        });

      resolve({ authUrl, waitForCallback });
    });

    tempServer.on("error", reject);
  });
}
