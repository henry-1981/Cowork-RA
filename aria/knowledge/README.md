# ARIA Knowledge DB

규제 원문 직접인용 기반 단일 진실 원천 (SSOT).

## 설계 원칙

1. **Verbatim Only**: 원문 그대로 저장. 요약/재구성/해석 금지
2. **Atomic Chunks**: 규정의 자연구조(조/별표/장/Part/Section) 단위로 분리
3. **Selective Loading**: 필요한 청크만 로드 (토큰 예산 관리)
4. **Source Traceability**: 모든 청크에 출처 메타데이터 필수

## 구조

```
knowledge/
├─ fda/                      ← FDA 원문 DB (648 files)
│  ├─ 01-statute/fdc-act-title21-chap9-subchapV/  — FD&C Act (117 sections + _index.yaml)
│  ├─ 02-regulation/21cfr-subchapter-h/           — 21 CFR Parts 800-898 (35 parts + _index.yaml)
│  └─ 03-guidance/                                — FDA Guidance Documents (494 files)
├─ eu/                       ← EU 원문 DB (413 files)
│  ├─ 01-regulation/mdr-2017-745/                 — MDR 2017/745 (123 Articles + 17 Annexes)
│  ├─ 01-regulation/ivdr-2017-746/                — IVDR 2017/746 (113 Articles + 15 Annexes)
│  ├─ 02-mdcg/                                    — MDCG 가이던스 (135 files)
│  └─ 03-meddev/                                  — MEDDEV 레거시 (4 files)
├─ mfds/                     ← MFDS 원문 DB (52 files)
│  ├─ 01-법령/01-의료기기법/
│  ├─ 01-법령/02-체외진단의료기기법/
│  ├─ 01-법령/03-디지털의료제품법/
│  ├─ 01-법령/04-공정경쟁규약/
│  └─ 02-가이드라인/
├─ regulations/              ← 레거시 (보존만, 참조 제거됨)
│  ├─ fda-framework.md
│  ├─ eu-mdr-framework.md
│  └─ mfds-framework.md
└─ shared/
   ├─ samd-classification.md
   ├─ combination-products.md
   └─ mfds-digital-classification.md
```

## 출처 정책

- 모든 데이터는 원문 규정에서 직접 인용 (출처 명시 필수)
- 벤치마크 시나리오 답안 포함 금지
- 특정 제품명 하드코딩 금지
- 규칙과 프레임워크만 기술

## 갱신 절차

`/aria-knowledge-refresh` 스킬 실행 또는 session-start hook 알림 시 갱신.

## 스킬 참조 방법

각 스킬의 Knowledge DB references에서 `../../knowledge/` 경로로 참조.
