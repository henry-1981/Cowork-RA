# ARIA Knowledge DB — Atomic Chunks Architecture

규제 원문 직접인용 기반 단일 진실 원천 (SSOT).

## 설계 원칙

1. **Verbatim Only**: 원문 그대로 저장. 요약/재구성/해석 금지
2. **Atomic Chunks**: 규정의 자연구조(조/별표/장) 단위로 분리
3. **Selective Loading**: `catalog.yaml`로 필요한 청크만 로드 (토큰 예산 관리)
4. **Source Traceability**: 모든 청크에 출처 메타데이터 필수

## 구조

```
knowledge/
├─ catalog.yaml              ← 전체 청크 인덱스 (스킬 진입점)
├─ README.md
├─ mfds/                     ← 식약처 (한국)
│  ├─ laws/                  ← 법률 (디지털의료제품법 등)
│  ├─ notices/               ← 고시 (분류등급지정 등)
│  └─ guidelines/            ← 가이드라인 (허가심사 등)
├─ fda/                      ← FDA (미국)
│  ├─ laws/                  ← 법률 (FD&C Act)
│  ├─ cfr/                   ← CFR (21 CFR 등)
│  └─ guidance/              ← Guidance Documents
├─ eu/                       ← EU
│  ├─ regulations/           ← 규정 (MDR 2017/745)
│  ├─ mdcg/                  ← MDCG 가이던스
│  └─ guidelines/            ← 기타 가이드라인
└─ imdrf/                    ← IMDRF
   └─ documents/             ← IMDRF 문서
```

## 레거시 파일 (마이그레이션 중)

아래 디렉토리는 Atomic Chunks 전환 완료 시까지 보존:
- `regulations/` — 기존 프레임워크 파일 (fda/eu-mdr/mfds-framework.md)
- `shared/` — 기존 공유 파일 (samd-classification.md, combination-products.md, mfds-digital-classification.md)

전환 완료 후 별도 커밋으로 삭제 예정.

## 청크 파일 작성 가이드

### 템플릿

```markdown
---
id: <catalog의 id와 동일>
source:
  title: "<공식 문서명>"
  authority: "<발행 기관 + 문서 번호>"
  section: "<해당 조항/별표/장>"
  url: "<법령정보센터 등 공식 URL>"
  retrieved: YYYY-MM-DD
language: ko|en
---

(원문 그대로 — 해석/요약/재구성 금지)
```

### 규칙

- **원문 직접인용만 허용**: LLM이 요약하거나 재구성한 텍스트 저장 금지
- **출처 메타데이터 필수**: source 블록의 모든 필드를 빠짐없이 기재
- **표는 마크다운으로 변환**: 원문 표의 구조와 내용을 정확히 보존
- **id는 catalog.yaml과 동일**: 청크 파일의 id가 catalog 항목의 id와 일치해야 함

## catalog.yaml 항목 추가 절차

1. 청크 파일을 해당 jurisdiction/doc_type 디렉토리에 생성
2. `catalog.yaml`의 `chunks:` 배열에 항목 추가:

```yaml
- id: mfds-law-dmp-act-art2
  title: "디지털의료제품법 제2조 (정의)"
  jurisdiction: mfds
  doc_type: law
  topics: [determination, classification]
  keywords: [디지털의료제품, 정의, 의료기기]
  path: mfds/laws/digital-medical-products-act/art-2-definitions.md
  tokens: 500
```

3. 파일 경로가 실제 존재하는지 확인
4. 토큰 수는 `wc -w` × 1.3으로 추정

## 국가(Jurisdiction) 추가 절차

1. `knowledge/` 하위에 국가 디렉토리 생성 (예: `japan/`)
2. 국가별 doc_type 서브디렉토리 생성 (법률/고시/가이드라인에 맞게)
3. 원문 PDF/HTML에서 3-Agent 파이프라인으로 추출·검증
4. `catalog.yaml`에 항목 추가
5. 관련 스킬의 Knowledge DB references 블록에 catalog 필터 조건 추가

## 스킬 참조 방법

스킬은 직접 경로 대신 `catalog.yaml`을 통해 청크를 로드한다:

```
1. Read ../../knowledge/catalog.yaml
2. Filter: jurisdiction={target} AND topics contains {current_skill}
3. Read matched chunk paths
```

## 갱신 절차

`/aria-knowledge-refresh` 스킬 실행 또는 session-start hook 알림 시:
- 원문 소스의 변경사항 감지
- 변경 감지 시 3-Agent 파이프라인으로 재추출·검증
- catalog.yaml의 last_updated 갱신
