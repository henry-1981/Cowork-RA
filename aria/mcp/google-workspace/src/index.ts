import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { getDocsClient } from "./services/docs.js";
import { getDriveClient } from "./services/drive.js";
import { formatError } from "./errors.js";

const server = new McpServer({
  name: "google-workspace",
  version: "0.1.0",
});

// Tool 1: read_document
server.registerTool(
  "read_document",
  {
    description: "Read the full text content of a Google Doc",
    inputSchema: {
      docId: z.string().describe("Google Doc ID or URL (extracts ID automatically)"),
    },
  },
  async ({ docId }) => {
    try {
      const idMatch = docId.match(/\/d\/([a-zA-Z0-9_-]+)/);
      const resolvedId = idMatch ? idMatch[1] : docId;

      const docs = getDocsClient();
      const res = await docs.documents.get({ documentId: resolvedId });

      const body = res.data.body;
      if (!body?.content) {
        return { content: [{ type: "text" as const, text: JSON.stringify({ docId: resolvedId, text: "", error: "문서 본문이 비어있습니다." }) }] };
      }

      const textParts: string[] = [];
      for (const element of body.content) {
        if (element.paragraph?.elements) {
          for (const el of element.paragraph.elements) {
            if (el.textRun?.content) textParts.push(el.textRun.content);
          }
        }
        if (element.table) {
          for (const row of element.table.tableRows ?? []) {
            const cells = row.tableCells?.map(cell =>
              cell.content?.map(c =>
                c.paragraph?.elements?.map(e => e.textRun?.content ?? "").join("") ?? ""
              ).join("") ?? ""
            ) ?? [];
            textParts.push("| " + cells.join(" | ") + " |");
          }
        }
      }

      return {
        content: [{ type: "text" as const, text: JSON.stringify({ docId: resolvedId, title: res.data.title, text: textParts.join("") }) }],
      };
    } catch (error) {
      return { content: [{ type: "text" as const, text: JSON.stringify({ error: formatError(error) }) }], isError: true };
    }
  }
);

// Tool 2: inspect_template
server.registerTool(
  "inspect_template",
  {
    description: "Extract all {{placeholder}} field names from a Google Docs template",
    inputSchema: {
      docId: z.string().describe("Template Google Doc ID"),
    },
  },
  async ({ docId }) => {
    try {
      const docs = getDocsClient();
      const res = await docs.documents.get({ documentId: docId });

      const placeholders = new Set<string>();
      const body = res.data.body;
      if (body?.content) {
        const fullText = JSON.stringify(body.content);
        const matches = fullText.matchAll(/\{\{([^}]+)\}\}/g);
        for (const match of matches) {
          placeholders.add(match[1]);
        }
      }

      return {
        content: [{
          type: "text" as const,
          text: JSON.stringify({
            docId,
            title: res.data.title,
            placeholders: [...placeholders].sort(),
            count: placeholders.size,
          }),
        }],
      };
    } catch (error) {
      return { content: [{ type: "text" as const, text: JSON.stringify({ error: formatError(error) }) }], isError: true };
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
      folderId: z.string().optional().describe("Target Drive folder ID"),
    },
  },
  async ({ templateDocId, title, folderId }) => {
    try {
      const drive = getDriveClient();
      const res = await drive.files.copy({
        fileId: templateDocId,
        requestBody: {
          name: title,
          ...(folderId ? { parents: [folderId] } : {}),
        },
      });

      return {
        content: [{
          type: "text" as const,
          text: JSON.stringify({ docId: res.data.id, title }),
        }],
      };
    } catch (error) {
      return { content: [{ type: "text" as const, text: JSON.stringify({ error: formatError(error) }) }], isError: true };
    }
  }
);

// Tool 4: fill_fields (with unfilled placeholder detection)
server.registerTool(
  "fill_fields",
  {
    description: "Fill {{placeholder}} fields in a Google Doc and report any unfilled placeholders",
    inputSchema: {
      docId: z.string().describe("Google Doc ID to fill"),
      fields: z
        .record(z.string(), z.string())
        .describe('Map of field names to values, e.g. {"활동유형": "자사제품설명회"}'),
    },
  },
  async ({ docId, fields }) => {
    try {
      const docs = getDocsClient();

      const requests = Object.entries(fields).map(([key, value]) => ({
        replaceAllText: {
          containsText: { text: `{{${key}}}`, matchCase: true },
          replaceText: value,
        },
      }));

      const batchRes = await docs.documents.batchUpdate({
        documentId: docId,
        requestBody: { requests },
      });

      const replacedCount = batchRes.data.replies?.reduce(
        (sum, r) => sum + (r.replaceAllText?.occurrencesChanged ?? 0), 0
      ) ?? 0;

      // Scan for remaining unfilled placeholders
      const docRes = await docs.documents.get({ documentId: docId });
      const remaining = new Set<string>();
      if (docRes.data.body?.content) {
        const fullText = JSON.stringify(docRes.data.body.content);
        const matches = fullText.matchAll(/\{\{([^}]+)\}\}/g);
        for (const match of matches) remaining.add(match[1]);
      }

      return {
        content: [{
          type: "text" as const,
          text: JSON.stringify({
            docId,
            fieldsProvided: Object.keys(fields).length,
            replacementsApplied: replacedCount,
            unfilledFields: [...remaining].sort(),
            unfilledCount: remaining.size,
          }),
        }],
      };
    } catch (error) {
      return { content: [{ type: "text" as const, text: JSON.stringify({ error: formatError(error) }) }], isError: true };
    }
  }
);

// Tool 5: get_share_link (with GOOGLE_DOMAIN fallback)
server.registerTool(
  "get_share_link",
  {
    description: "Set sharing permissions and return the share link for a Google Doc",
    inputSchema: {
      docId: z.string().describe("Google Doc ID"),
      access: z
        .enum(["anyone", "domain"])
        .default("domain")
        .describe("Share scope: 'anyone' for public link, 'domain' for org-only"),
      role: z
        .enum(["reader", "commenter", "writer"])
        .default("reader")
        .describe("Permission role"),
    },
  },
  async ({ docId, access, role }) => {
    try {
      const drive = getDriveClient();
      const domain = process.env.GOOGLE_DOMAIN;

      const effectiveAccess = (access === "domain" && !domain) ? "anyone" : access;

      await drive.permissions.create({
        fileId: docId,
        requestBody: {
          type: effectiveAccess === "domain" ? "domain" : "anyone",
          role,
          ...(effectiveAccess === "domain" ? { domain } : {}),
        },
      });

      const link = `https://docs.google.com/document/d/${docId}/edit`;
      return {
        content: [{
          type: "text" as const,
          text: JSON.stringify({
            docId, link, access: effectiveAccess, role,
            ...(effectiveAccess !== access ? { warning: "GOOGLE_DOMAIN 미설정으로 'anyone' 공유로 전환됨" } : {}),
          }),
        }],
      };
    } catch (error) {
      return { content: [{ type: "text" as const, text: JSON.stringify({ error: formatError(error) }) }], isError: true };
    }
  }
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
