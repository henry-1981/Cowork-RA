import { google } from "googleapis";
import { getAuth } from "../auth.js";

export function getDriveClient() {
  return google.drive({ version: "v3", auth: getAuth() });
}
