import { google } from "googleapis";
import { getOAuth2Client } from "../auth.js";

export function getDocsClient() {
  return google.docs({ version: "v1", auth: getOAuth2Client() });
}
