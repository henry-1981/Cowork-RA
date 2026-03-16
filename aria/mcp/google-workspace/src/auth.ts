import { google } from "googleapis";

const SCOPES = [
  "https://www.googleapis.com/auth/documents",
  "https://www.googleapis.com/auth/drive",
];

let authInstance: InstanceType<typeof google.auth.GoogleAuth> | null = null;

export function getAuth() {
  if (!authInstance) {
    authInstance = new google.auth.GoogleAuth({ scopes: SCOPES });
  }
  return authInstance;
}
