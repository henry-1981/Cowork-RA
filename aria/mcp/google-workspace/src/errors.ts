export function formatError(error: unknown): string {
  if (error instanceof Error) {
    const msg = error.message;
    if (msg.includes("설정이 필요")) return msg;
    if (msg.includes("Apps Script 호출 실패")) return msg;
    if (msg.includes("Apps Script 응답 파싱")) return msg;
    return `오류: ${msg}`;
  }
  return "알 수 없는 오류가 발생했습니다.";
}
