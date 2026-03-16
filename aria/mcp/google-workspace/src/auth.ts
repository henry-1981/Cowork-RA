import { existsSync, readFileSync, writeFileSync, mkdirSync } from "fs";
import { join } from "path";
import { homedir } from "os";

const CONFIG_DIR = join(homedir(), ".config", "google-workspace-mcp");
const CONFIG_PATH = join(CONFIG_DIR, "config.json");

export interface MpcConfig {
  webAppUrl: string;
  userEmail: string;
}

/**
 * Load config from ~/.config/google-workspace-mcp/config.json
 * or from environment variables.
 */
export function loadConfig(): MpcConfig | null {
  // Environment variables take priority
  if (process.env.APPS_SCRIPT_URL && process.env.USER_EMAIL) {
    return {
      webAppUrl: process.env.APPS_SCRIPT_URL,
      userEmail: process.env.USER_EMAIL,
    };
  }

  if (existsSync(CONFIG_PATH)) {
    return JSON.parse(readFileSync(CONFIG_PATH, "utf-8"));
  }

  return null;
}

/**
 * Save config to ~/.config/google-workspace-mcp/config.json
 */
export function saveConfig(config: MpcConfig): void {
  mkdirSync(CONFIG_DIR, { recursive: true });
  writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
}

/**
 * Check if the MCP is configured (has web app URL and user email).
 */
export function isConfigured(): boolean {
  return loadConfig() !== null;
}

/**
 * Call the Google Apps Script web app.
 */
export async function callAppsScript(
  action: string,
  params: Record<string, unknown> = {}
): Promise<unknown> {
  const config = loadConfig();
  if (!config) {
    throw new Error(
      "설정이 필요합니다. setup 도구를 먼저 실행해주세요."
    );
  }

  const body = {
    action,
    userEmail: config.userEmail,
    ...params,
  };

  const response = await fetch(config.webAppUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    redirect: "follow",
  });

  if (!response.ok) {
    throw new Error(`Apps Script 호출 실패: ${response.status} ${response.statusText}`);
  }

  const text = await response.text();
  try {
    return JSON.parse(text);
  } catch {
    throw new Error(`Apps Script 응답 파싱 실패: ${text.substring(0, 200)}`);
  }
}
