import { google } from "googleapis";
import { getAuth } from "../auth.js";

export function getDocsClient() {
  return google.docs({ version: "v1", auth: getAuth() });
}
