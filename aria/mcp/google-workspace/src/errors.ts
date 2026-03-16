export function formatError(error: unknown): string {
  if (error instanceof Error) {
    const msg = error.message;
    if (msg.includes("404")) return "문서를 찾을 수 없습니다. Doc ID를 확인해주세요.";
    if (msg.includes("403")) return "문서 접근 권한이 없습니다. 해당 문서에 대한 접근 권한을 확인해주세요.";
    if (msg.includes("429")) return "API 요청 한도 초과. 잠시 후 다시 시도해주세요.";
    return `Google API 오류: ${msg}`;
  }
  return "알 수 없는 오류가 발생했습니다.";
}
