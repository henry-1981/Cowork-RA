# 공정경쟁규약 Compliance 개선 설계

> Date: 2026-02-28
> Status: Draft
> PR #27 (merged) 위에 개선

## 1. 목표

PR #27의 토픽 분리 기반 위에서:
- **DB**: 중복 제거 + 계층(규정/내부지침/해석) 역할 구분 + Checklist 원문 포함
- **Skill**: Interactive Compliance Check (Mode 3) 추가 — 대화형 체크리스트 + 서류 검토
- **판정 체계**: 맥락 기반 GREEN/YELLOW/RED 재정의

## 2. DB 구조 (접근 A: 토픽 내부 섹션 태깅)

### 2.1 토픽 파일 내부 구조

각 토픽 파일에 일관된 섹션 헤더로 계층을 구분. 모든 텍스트는 원문 verbatim, 섹션 헤더만 추가.

```markdown
# Art. N [토픽명]

## 규정 (Regulation)
### 공정경쟁규약 제N조
[규약 원문 verbatim]

### 세부운용기준 제N조
[세부기준 원문 verbatim]

## 심의위원회 내부지침 (Committee Guidance)
[내부지침 중 해당 Article 부분 verbatim]

## 규정 해설 (FAQ/Interpretation)
### FAQ #N: [질문]
**Q**: ...
**A**: ...
[해당 토픽 FAQ 전체 verbatim]

## Compliance Checklist
[안내서 원문의 Checklist 표 verbatim]
| 구분 | 내용 | 체크리스트 |
|------|------|-----------|
| ... | ... | 1. [질문] □ Yes □ No |
| 첨부자료 | ... | [목록] |
```

### 2.2 _index.yaml 구조

```yaml
title: 의료기기 거래에 관한 공정경쟁규약
source_documents:
  - 의료기기-리베이트-예방-및-공정경쟁을-위한-안내서2022-04
  - 붙임2-의료기기-공정경쟁규약심의위원회-내부지침-전문24-07-12-개정
  - 공정경쟁규약-주요-위반유형-및-사례23-5-2-1

sections:
  regulation: "## 규정 (Regulation)"
  committee_guidance: "## 심의위원회 내부지침 (Committee Guidance)"
  interpretation: "## 규정 해설 (FAQ/Interpretation)"
  checklist: "## Compliance Checklist"

topics:
  - file: topics/00-general.md
    title: 총칙 (목적, 기본원칙, 정의)
    articles: [1, 2, 3, 4]
    has_checklist: false
  - file: topics/01-용어정의.md
    title: 용어 정의
    articles: [3]
    has_checklist: false
  - file: topics/02-금품류제공제한.md
    title: 금품류 제공 제한
    articles: [5]
    operating_standard: [2]
    has_checklist: false
    procedure_required: [지출보고서]
  - file: topics/03-견본품.md
    title: 견본품
    articles: [6]
    operating_standard: [3]
    has_checklist: true
    faq_range: [7, 12]
    procedure_required: [지출보고서, 견본품수불대장]
    checklist_meta:
      total_questions: 11
      critical_questions: [1, 3]
      evidence_required:
        - "견본품 제공 신청서"
        - "수불대장"
  - file: topics/04-기부행위.md
    title: 기부행위
    articles: [7]
    operating_standard: [4]
    has_checklist: true
    faq_range: [13, 21]
    procedure_required: [지출보고서, 사전심의]
    checklist_meta:
      total_questions: 7
      critical_questions: [1, 2]
      evidence_required:
        - "기부 신청서"
        - "사전심의 결과서"
  - file: topics/05-학술대회개최지원.md
    title: 학술대회 개최·운영 지원
    articles: [8]
    operating_standard: [5]
    has_checklist: true
    faq_range: [22, 24]
    procedure_required: [사전심의, 지출보고서]
    checklist_meta:
      total_questions: 7
      critical_questions: [1, 3]
      evidence_required:
        - "사전심의 신청서"
        - "행사 프로그램"
        - "참가자 명단"
        - "비용 집행 내역서"
  - file: topics/06-학술대회참가지원.md
    title: 학술대회 참가 지원
    articles: [9]
    operating_standard: [6]
    has_checklist: true
    faq_range: [25, 27]
    procedure_required: [사전심의, 지출보고서]
    checklist_meta:
      total_questions: 10
      critical_questions: [1, 4]
      evidence_required:
        - "사전심의 신청서"
        - "참가 신청서"
        - "비용 집행 내역서"
  - file: topics/07-자사제품설명회.md
    title: 자사제품설명회
    articles: [10]
    operating_standard: [7]
    has_checklist: true
    faq_range: [28, 46]
    procedure_required: [사전심의, 지출보고서]
    checklist_meta:
      total_questions: 16
      critical_questions: [1, 3, 7]
      evidence_required:
        - "사전심의 신청서 사본"
        - "참가자 명단"
        - "비용 집행 내역서"
  - file: topics/08-교육훈련.md
    title: 교육·훈련
    articles: [11]
    operating_standard: [8]
    has_checklist: true
    faq_range: [48, 51]
    procedure_required: [사전심의, 지출보고서]
    checklist_meta:
      total_questions: 14
      critical_questions: [1, 2, 5]
      evidence_required:
        - "교육 계획서"
        - "참석자 명단"
        - "비용 집행 내역서"
  - file: topics/09-강연및자문.md
    title: 강연 및 자문
    articles: [12]
    operating_standard: [9]
    has_checklist: true
    faq_range: [54, 66]
    procedure_required: [사전심의, 지출보고서]
    checklist_meta:
      total_questions: 7
      critical_questions: [1, 3]
      evidence_required:
        - "강연/자문 계약서"
        - "대가 산정 근거"
  - file: topics/10-임상시험지원.md
    title: 임상시험 지원
    articles: [13]
    has_checklist: true
    faq_range: [67, 67]
    procedure_required: [지출보고서]
    checklist_meta:
      total_questions: 8
      critical_questions: [1, 2]
      evidence_required:
        - "임상시험 계약서"
        - "IRB 승인서"
  - file: topics/11-시장조사.md
    title: 시장조사
    articles: [14]
    operating_standard: [10]
    has_checklist: false
    faq_range: [70, 73]
    procedure_required: [지출보고서]
  - file: topics/12-시판후조사.md
    title: 시판후 조사
    articles: [15]
    operating_standard: [11]
    has_checklist: false
    faq_range: [74, 74]
    procedure_required: [지출보고서]
  - file: topics/13-시판후외임상활동.md
    title: 시판후 외 임상활동
    articles: [16]
    operating_standard: [12]
    has_checklist: false
    procedure_required: [지출보고서]
  - file: topics/14-전시및광고.md
    title: 전시 및 광고
    articles: [17]
    operating_standard: [13]
    has_checklist: false
    procedure_required: [지출보고서]
  - file: topics/15-규약의공정거래위원회신고.md
    title: 규약의 공정거래위원회 신고
    articles: [18]
    has_checklist: false
  - file: topics/16-공정경쟁규약심의위원회.md
    title: 공정경쟁규약 심의위원회
    articles: [19]
    has_checklist: false
  - file: topics/17-위반시제재사항.md
    title: 위반 시 제재사항
    articles: [20]
    operating_standard: [18]
    has_checklist: false

common_procedures:
  - name: 지출보고서
    guide: "지출보고서-작성-가이드라인.md"
    description: "경제적 이익 제공에 따른 지출보고서 (전 활동 공통)"
  - name: 사전심의
    description: "심의위원회 사전심의 신청"
  - name: 사후신고
    description: "활동 완료 후 사후신고"
```

### 2.3 중복 제거 원칙

- 원문이 여러 소스(안내서, 내부지침, 위반사례)에 중복 존재 시 → 최상위 규정 원문을 기준으로 하나만 유지
- FAQ에서 규약 조문을 재인용하는 부분은 FAQ 원문 그대로 유지 (FAQ 자체가 verbatim이므로)
- 안내서 배포본(요약판)은 원본 안내서와 중복 → 배포본 삭제, 원본만 유지

### 2.4 references/ 디렉토리 처리

PR #27에서 삭제 대상이었던 `aria/skills/compliance/references/` 3파일(regulation.md, activity-guide.md, faq.md)은 토픽 파일이 완전 대체하므로 제거.

## 3. Skill 설계: Mode 3 — Interactive Compliance Check

### 3.1 트리거

```
트리거 키워드: "심의 체크", "컴플라이언스 체크", "사전심의", "compliance check",
              "사후신고 준비", "활동 검토"
```

### 3.2 전체 흐름

```
1. 사용자 활동 설명
     ↓
2. 활동유형 분류 (다중 매핑 허용)
   ├─ 단일 매핑 (확신도 HIGH) → 바로 3단계
   ├─ 다중 매핑 (확신도 MED) → "이 활동은 [A]와 [B] 성격을 모두 가집니다"
   │   → 사용자 확인 후 관련 토픽 모두 순차 진행
   └─ 불확실 (확신도 LOW) → 구분 기준 제시 + 사용자 선택
     ↓
3. 맥락 확인
   "현재 어떤 단계인가요?"
   (A) 활동 기획 중 — 사전 검토
   (B) 신고/심의 준비 중 — 제출 전 최종 점검
   (C) 이미 진행한 활동 — 사후 적정성 확인
     ↓
4. 토픽 파일 Read (다중 토픽일 경우 순차 Read)
     ↓
5. Checklist 순차 진행
   - 한 번에 1-2개 질문
   - 답변 옵션: Yes / No / 확인필요
   - 각 질문에 규정 근거 요약 (해당 Article 번호 + 핵심 내용)
   - No → 즉시 위반 가능성 + 시정 방향 안내
   - 확인필요 → 메모 후 계속 진행 (최종 판정에 영향)
     ↓
6. 판정 (GREEN/YELLOW/RED) — 맥락별 의미 차등 적용
     ↓
7. 후속 절차 안내 (공통: 지출보고서 + 활동별 고유 절차)
     ↓
8. 서류 검토 (선택)
   ├─ 현재 폴더 검색 → 파일 발견 시 파일명 제시 → 사용자 확인 필수
   ├─ 미발견 시 업로드 요청
   ├─ Read → 기본 검토 (필수항목 누락, 금액 한도, 양식 완성도)
   └─ "나중에" → 미검토 표시
     ↓
9. 최종 요약 (판정 + 절차 + 서류 상태)
```

### 3.3 판정 매트릭스

#### 맥락별 판정 의미

| 판정 | (A) 기획 검토 | (B) 신고 준비 | (C) 사후 확인 |
|------|-------------|-------------|-------------|
| GREEN | 규정 요건 부합. 후속 절차 안내 | 제출 요건 충족. 진행 가능 | 적정. 기록 보관 안내 |
| YELLOW | 조건부. 보완 사항 목록 제공 | 보완 후 제출 권장. 미비 항목 명시 | 일부 미비. 보완 조치 안내 |
| RED | 현재 구성으로는 불가. 재설계 필요 | 제출 불가. 근본적 재검토 필요 | 위반 가능. 시정 조치 검토 |

#### 판정 결정 조건 (Council 피드백 반영)

```
GREEN 조건 (모두 충족):
  - 필수질문 100% Yes
  - 필수증빙 확인 (사용자 답변 기준)
  - 분류확신도 HIGH
  - "확인필요" 답변 0건

YELLOW 조건 (하나 이상):
  - "확인필요" 답변 1건 이상
  - OR 필수증빙 미확인 항목 있음
  - OR 분류확신도 MED (다중 매핑)
  - OR No 답변이 있지만 severity: warning (시정 가능)

RED 조건 (하나 이상):
  - critical 질문에 No 답변
  - OR 다수의 No 답변 (3건 이상)
  - OR 분류확신도 LOW + 미해결
```

### 3.4 서류 검토 흐름 (Cowork 폴더 연동)

```
필요 서류 목록 확정 (Checklist + 후속 절차에서 도출)
     ↓
서류별 순차 처리:
     ↓
┌─ 1. 현재 폴더 검색 (Glob/파일명 패턴)
│    ├─ 발견 → "이 파일이 맞나요? [파일명]" → 사용자 확인 필수
│    │          ├─ Yes → 파일 Read → 검토 → 피드백
│    │          └─ No  → 업로드 요청
│    └─ 미발견 → "해당 서류를 업로드해 주세요"
│                 ├─ 업로드됨 → Read → 검토 → 피드백
│                 └─ "나중에" → YELLOW 유지, 미검토 표시
└─ 2. 다음 서류로 반복

검토 범위 (기본):
  - 필수 항목 누락 여부
  - 금액 한도 초과 여부
  - 양식 완성도 (주요 필드 기입 확인)
```

**핵심 원칙**: 파일 발견해도 반드시 사용자 확인 후 검토. 자동 판단 금지.

### 3.5 판정 출력 포맷

```
## 컴플라이언스 체크 결과

### 활동 유형: 자사제품설명회 (Art. 10)
### 맥락: 기획 검토 (활동 실행 전)

### 판정: YELLOW — 보완 후 진행 가능

### 체크 결과
| # | 항목 | 답변 | 상태 |
|---|------|------|------|
| 1 | 참석 대상이 자사 제품 사용 HCP로 한정? | Yes | OK |
| 2 | 1일 식음료 비용 10만원 이내? | Yes | OK |
| 3 | 사전심의 신청 완료? | 아직 | 주의 |

### 보완 사항
1. 사전심의 신청 필요 (Art.10 §2)
   → 심의위 제출 절차를 안내해 드릴까요?

### 후속 절차
- [ ] 사전심의 신청 → 심의위 제출
- [ ] 지출보고서 작성 (가이드라인 Ⅱ판 기준)
- [x] 참석자 명단 작성

### 서류 상태
| 서류 | 상태 | 비고 |
|------|------|------|
| 사전심의 신청서 | 미검토 | 심의 신청 후 검토 가능 |
| 참가자 명단 | 확인완료 | participants.xlsx (기본 검토 통과) |
| 비용 집행 내역서 | 미제출 | 업로드 필요 |

### Disclaimer
본 결과는 정보 제공 목적이며, 법적 효력이 없습니다.
최종 결정은 사내 컴플라이언스 책임자의 검토를 거쳐야 합니다.
```

### 3.6 Mode 간 연계

```
Mode 1 (Q&A) → Mode 3: "정확한 판단을 위해 체크리스트를 진행하시겠습니까?"
Mode 3 → Mode 2 (Report): "내부 보고용 문서를 생성해 드릴까요?"
```

공통 판정 엔진 1개 + UX만 모드별 분리. Mode 3이 사실 수집기, Mode 1/2는 표현 레이어.

## 4. Council 검토 반영 사항

| 출처 | 피드백 | 반영 |
|------|--------|------|
| Codex | 복합 활동 — 다중 Article 동시 적용 | 다중 매핑 + 순차 Read (3.2 Step 2) |
| Codex | Yes/No 외 상태 필요 | "확인필요" 옵션 추가 (3.2 Step 5) |
| Codex | GREEN 오판 리스크 | GREEN 조건 강화 (3.3) |
| Codex | Checklist 구조화 메타데이터 | _index.yaml에 checklist_meta (2.2) |
| Codex | 공통 판정 엔진 + 모드별 UX | Mode 간 연계 구조 (3.6) |
| Gemini | Mode 간 자연스러운 연계 | 1→3→2 시나리오 (3.6) |
| Gemini | Disclaimer 강화 | 출력 포맷에 필수 포함 (3.5) |
| Gemini | 복합 활동 edge case | 다중 매핑 (3.2 Step 2) |
| Gemini | "확인필요" 답변 처리 | 자동 YELLOW (3.3) |
| Zai | Mode 3 용도 명확화 | 맥락 확인 단계로 해결 (3.2 Step 3) |
| HB | 단순 규정도 후속 절차 필요 | 전 활동 공통 절차 안내 (3.2 Step 7) |
| HB | 서류 업로드 검토 | Cowork 폴더 연동 흐름 (3.4) |
| HB | 폴더 검색 → 확인 → 검토 | 사용자 확인 필수 원칙 (3.4) |

## 5. 구현 범위

### In Scope
- DB: 토픽 파일 내부 섹션 재구성 (중복 제거 + 계층 태깅 + Checklist 포함)
- DB: _index.yaml 확장 (역할 구분 + checklist_meta + procedure_required)
- DB: 지출보고서 가이드라인 파일 추가
- DB: 배포본(요약판) 삭제
- Skill: SKILL.md에 Mode 3 추가
- Skill: references/ 디렉토리 제거
- Skill: 판정 매트릭스 + 서류 검토 흐름

### Out of Scope (후속)
- 복잡한 조건부 분기 로직 (질문 간 의존성)
- 누적 금액/횟수 추적 (사용자별 이력 관리)
- 심화 서류 검토 (규정 조항별 대조, 위반사례 패턴 매칭)
- 규정 개정 시점별 적용 로직
