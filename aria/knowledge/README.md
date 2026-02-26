# ARIA Knowledge DB

규제 프레임워크 레퍼런스 — 원문 규정 기반 단일 진실 원천 (SSOT)

## 구조

```
regulations/
  fda-framework.md       — FDA 21 CFR, Product Code 체계, 510(k)/PMA/De Novo
  eu-mdr-framework.md    — EU MDR Annex VIII, 22 Rules, Conformity Assessment
  mfds-framework.md      — MFDS 의료기기법, 등급분류, 인허가 경로
shared/
  samd-classification.md — IMDRF SaMD 분류 (3관할권 공통)
  combination-products.md — 복합제품 PMOA/MDR Article 1(8-9)
  mfds-digital-classification.md — MFDS 디지털의료제품법 분류 규칙 (4-Gate, 7-digit, Risk Matrix)
```

## 출처 정책

- 모든 데이터는 원문 규정에서 직접 인용 (출처 명시 필수)
- 벤치마크 시나리오 답안 포함 금지
- 특정 제품명 하드코딩 금지
- 규칙과 프레임워크만 기술

## YAML Frontmatter 스키마

```yaml
---
last_updated: "YYYY-MM-DD"
sources:
  - "출처 URL 또는 문서명"
next_review: "YYYY-MM-DD"  # last_updated + 30일
---
```

## 갱신 절차

`/aria-knowledge-refresh` 스킬 실행 또는 session-start hook 알림 시 갱신.

## 스킬 참조 방법

각 스킬의 `references/` 디렉토리에서 `../../knowledge/regulations/` 경로로 참조.
