import { google } from "googleapis";
import { getOAuth2Client } from "../auth.js";

export function getDriveClient() {
  return google.drive({ version: "v3", auth: getOAuth2Client() });
}
