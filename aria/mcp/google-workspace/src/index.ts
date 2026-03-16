import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { isConfigured, saveConfig, callAppsScript } from "./auth.js";
import { formatError } from "./errors.js";

const server = new McpServer({
  name: "google-workspace",
  version: "0.3.0",
});

// Tool 0: setup
server.registerTool(
  "setup",
  {
    description:
      "Configure the Google Workspace MCP with Apps Script web app URL and user email. Run once per user.",
    inputSchema: {
      webAppUrl: z
        .string()
        .url()
        .describe("Google Apps Script web app URL (from deployment)"),
      userEmail: z
        .string()
        .email()
        .describe("User's company Google email address"),
    },
  },
  async ({ webAppUrl, userEmail }) => {
    try {
      saveConfig({ webAppUrl, userEmail });

      // Verify connection by calling ping
      const result = await callAppsScript("ping");

      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify({
              configured: true,
              userEmail,
              message: "설정 완료. Google Workspace MCP를 사용할 수 있습니다.",
              ping: result,
            }),
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify({ error: formatError(error) }),
          },
        ],
        isError: true,
      };
    }
  }
);

// Tool 1: read_document
server.registerTool(
  "read_document",
  {
    description: "Read the full text content of a Google Doc",
    inputSchema: {
      docId: z
        .string()
        .describe("Google Doc ID or URL (extracts ID automatically)"),
    },
  },
  async ({ docId }) => {
    try {
      const idMatch = docId.match(/\/d\/([a-zA-Z0-9_-]+)/);
      const resolvedId = idMatch ? idMatch[1] : docId;

      const result = await callAppsScript("readDocument", {
        docId: resolvedId,
      });
      return {
        content: [{ type: "text" as const, text: JSON.stringify(result) }],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify({ error: formatError(error) }),
          },
        ],
        isError: true,
      };
    }
  }
);

// Tool 2: inspect_template
server.registerTool(
  "inspect_template",
  {
    description:
      "Extract all {{placeholder}} field names from a Google Docs template",
    inputSchema: {
      docId: z.string().describe("Template Google Doc ID"),
    },
  },
  async ({ docId }) => {
    try {
      const result = await callAppsScript("inspectTemplate", { docId });
      return {
        content: [{ type: "text" as const, text: JSON.stringify(result) }],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify({ error: formatError(error) }),
          },
        ],
        isError: true,
      };
    }
  }
);

// Tool 3: copy_template
server.registerTool(
  "copy_template",
  {
    description: "Copy a Google Docs template to create a new document",
    inputSchema: {
      templateDocId: z.string().describe("Source template Google Doc ID"),
      title: z.string().describe("Title for the new document"),
      folderId: z
        .string()
        .optional()
        .describe("Target Drive folder ID"),
    },
  },
  async ({ templateDocId, title, folderId }) => {
    try {
      const result = await callAppsScript("copyTemplate", {
        templateDocId,
        title,
        folderId,
      });
      return {
        content: [{ type: "text" as const, text: JSON.stringify(result) }],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify({ error: formatError(error) }),
          },
        ],
        isError: true,
      };
    }
  }
);

// Tool 4: fill_fields
server.registerTool(
  "fill_fields",
  {
    description:
      "Fill {{placeholder}} fields in a Google Doc and report any unfilled placeholders",
    inputSchema: {
      docId: z.string().describe("Google Doc ID to fill"),
      fields: z
        .record(z.string(), z.string())
        .describe(
          'Map of field names to values, e.g. {"활동유형": "자사제품설명회"}'
        ),
    },
  },
  async ({ docId, fields }) => {
    try {
      const result = await callAppsScript("fillFields", { docId, fields });
      return {
        content: [{ type: "text" as const, text: JSON.stringify(result) }],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify({ error: formatError(error) }),
          },
        ],
        isError: true,
      };
    }
  }
);

// Tool 5: get_share_link
server.registerTool(
  "get_share_link",
  {
    description:
      "Set sharing permissions and return the share link for a Google Doc",
    inputSchema: {
      docId: z.string().describe("Google Doc ID"),
      access: z
        .enum(["anyone", "domain"])
        .default("domain")
        .describe("Share scope"),
      role: z
        .enum(["reader", "commenter", "writer"])
        .default("reader")
        .describe("Permission role"),
    },
  },
  async ({ docId, access, role }) => {
    try {
      const result = await callAppsScript("getShareLink", {
        docId,
        access,
        role,
      });
      return {
        content: [{ type: "text" as const, text: JSON.stringify(result) }],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify({ error: formatError(error) }),
          },
        ],
        isError: true,
      };
    }
  }
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
