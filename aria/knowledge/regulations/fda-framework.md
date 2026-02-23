---
last_updated: "2026-02-23"
sources:
  - "FDA.gov guidance documents"
  - "Federal Register"
  - "21 CFR Parts 800-892"
  - "21st Century Cures Act"
  - "MDUFA V (FY2023-2027)"
next_review: "2026-03-23"
---

# FDA 의료기기 규제 프레임워크

## 1. Device Determination (의료기기 해당 여부 판단)

### 1.1 Section 201(h)(1) 의료기기 정의

FD&C Act Section 201(h)(1)에 따라, 제품이 **의료기기(device)**로 분류되려면 다음 세 가지 요건을 모두 충족해야 한다:
(출처: 21 U.S.C. § 321(h), FD&C Act Section 201(h))

1. **제품 형태 요건**: instrument, apparatus, implement, machine, contrivance, implant, in vitro reagent, 또는 이와 유사하거나 관련된 물품(article)이어야 한다.

2. **사용 목적(Intended Use) 요건**: 다음 목적 중 하나 이상에 해당해야 한다:
   - 질병(disease)의 진단, 치료, 완화, 처치, 또는 예방
   - 인체의 구조(structure) 또는 기능(function)에 영향을 미치는 용도

3. **작용 기전(Mechanism of Action) 요건**: 인체 내에서 또는 인체 표면에서 **화학적 작용(chemical action)**을 통해 주된 목적을 달성하지 않아야 하며, 주된 목적 달성이 **대사(metabolism)**에 의존하지 않아야 한다.

> 이 세 번째 요건이 의료기기와 의약품(drug)을 구분하는 핵심 기준이다.

### 1.2 General Wellness 제품 정책

FDA는 저위험(low-risk) General Wellness 제품에 대해 enforcement discretion 정책을 적용한다.
(출처: FDA Guidance "General Wellness: Policy for Low Risk Devices" 최종본, 2026.1.6 발행)

**2026년 1월 개정 주요 변경사항:**

- **센서 기반 웨어러블 기기** 관련 조항이 대폭 확대됨
- 혈압(blood pressure), 혈당(blood glucose), 혈중산소포화도(SpO₂), 심박변이도(HRV) 등 생리학적 파라미터를 측정하는 웨어러블 기기에 대한 구체적 기준 명시
- **혈압 측정 제품**의 경우: 2025년 중반 FDA Safety Communication을 통해, 혈압을 측정·추정하는 제품은 규제 대상 의료기기임을 명확히 함
- 센서 기반 웨어러블이 General Wellness 범주에 해당하려면: 임상적으로 사용되는 수치를 모방(mimic)하지 않아야 하며, 해당 수치가 임상적으로 검증(validate)되지 않은 경우여야 함

**General Wellness 해당 요건 (2가지 모두 충족 필요):**

| 요건 | 내용 |
|------|------|
| (1) 사용 목적 | 일반적 건강·웰빙(general wellness)과 관련된 주장만 가능; 특정 질병·상태의 진단·치료·예방 주장 불가 |
| (2) 위험 수준 | 사용자에게 저위험(low risk)이어야 함; 침습적(invasive) 제품 제외 |

### 1.3 Clinical Decision Support (CDS) 소프트웨어 제외 기준

21st Century Cures Act Section 3060(a)에 의해, FD&C Act Section 520(o)(1)(E)에 따른 CDS 소프트웨어는 의료기기 정의에서 제외될 수 있다.
(출처: FDA Guidance "Clinical Decision Support Software" 최종본, 2026.1.6 발행, 2026.1.29 재발행)

**CDS 제외를 위한 4가지 기준 (모두 충족 필요):**

1. **정보 표시 목적이 아닌 것**: 의료기기 데이터, 환자 기록, 또는 기타 의료정보의 표시(display), 분석(analysis), 또는 출력(printing)이 아닌 것
2. **의료 전문가 대상**: 의료 전문가(healthcare professional, HCP)를 대상 사용자로 의도
3. **투명성(Transparency)**: 해당 소프트웨어가 제공하는 권고(recommendation)의 근거(basis)를 의료 전문가가 독립적으로 검토(independently review)할 수 있도록 해야 함
4. **독립적 임상 판단**: 의료 전문가가 해당 소프트웨어의 출력에 의존하지 않고 독립적 임상 판단(independent clinical judgment)을 내리도록 의도

**2026년 1월 개정 핵심 변경사항:**

- **단일 치료 권고(single recommendation)에 대한 enforcement discretion**: 종전 가이던스에서는 "단일 권고만 제시하는 소프트웨어"도 규제 대상으로 보았으나, 개정판에서는 나머지 3개 기준을 모두 충족하고 시간-긴급(time-critical) 의사결정이 아닌 경우, enforcement discretion 적용
- **위험 점수(risk score)/확률(probability) 관련**: 위험 점수·확률을 제공하는 소프트웨어가 non-device CDS에 해당하지 않는다는 종전 문구 삭제
- 전반적으로 디지털 헬스 기술에 대한 규제 범위를 축소하는 방향

---

## 2. Classification System (분류 체계)

### 2.1 3-Tier 분류 체계

FDA는 의료기기를 위험도(risk)에 따라 3개 등급으로 분류한다.
(출처: 21 CFR Part 860, FD&C Act Section 513)

| 등급 | 비율 (약) | 위험 수준 | 규제 수준 | 주요 특징 |
|------|-----------|-----------|-----------|-----------|
| **Class I** | ~47% | 최저 위험 | General Controls | 대부분 510(k) 면제; 등록·목록(Registration & Listing), GMP, 라벨링 요건 적용 |
| **Class II** | ~43% | 중간 위험 | General Controls + Special Controls | 대부분 510(k) 필요; Special Controls(성능 표준, 환자 등록부 등) 적용 |
| **Class III** | ~10% | 최고 위험 | General Controls + PMA | 생명 유지·지원 기기 또는 질병·부상의 잠재적 비합리적 위험; PMA 필요 |

### 2.2 Product Code 체계

FDA CDRH는 약 **6,500개 이상의 Product Code**를 운용하며, 각 코드는 기기의 일반 유형(generic type)을 나타낸다.
(출처: FDA Guidance "Medical Device Classification Product Codes" 2013; FDA Product Code Classification Database)

- 7자리 코드의 앞 2자리는 **Medical Specialty Panel** 번호를 나타냄
- 약 1,700개의 generic device type이 16개 패널에 분류됨

### 2.3 16 Medical Specialty Panels

(출처: 21 CFR Parts 862-892)

| Panel # | CFR Part | Panel Name (전문 분야) |
|---------|----------|----------------------|
| 1 | Part 862 | Clinical Chemistry and Clinical Toxicology (임상화학·독성학) |
| 2 | Part 864 | Hematology and Pathology (혈액학·병리학) |
| 3 | Part 866 | Immunology and Microbiology (면역학·미생물학) |
| 4 | Part 868 | Anesthesiology (마취과) |
| 5 | Part 870 | Cardiovascular (심혈관) |
| 6 | Part 872 | Dental (치과) |
| 7 | Part 874 | Ear, Nose, and Throat (이비인후과) |
| 8 | Part 876 | Gastroenterology-Urology (소화기·비뇨기) |
| 9 | Part 878 | General and Plastic Surgery (일반·성형외과) |
| 10 | Part 880 | General Hospital and Personal Use (일반 병원·개인용) |
| 11 | Part 882 | Neurological (신경과) |
| 12 | Part 884 | Obstetrical and Gynecological (산부인과) |
| 13 | Part 886 | Ophthalmic (안과) |
| 14 | Part 888 | Orthopedic (정형외과) |
| 15 | Part 890 | Physical Medicine (물리의학) |
| 16 | Part 892 | Radiology (방사선과) |

### 2.4 General Controls vs Special Controls

(출처: FD&C Act Sections 501, 502, 510, 513, 516, 518, 519, 520)

**General Controls (모든 등급에 적용):**
- Establishment Registration & Device Listing (시설 등록·기기 목록)
- Quality System Regulation / QMSR (품질 시스템 규정)
- Labeling Requirements (라벨링 요건)
- Medical Device Reporting (MDR, 이상사례 보고)
- Premarket Notification (510(k)), 해당하는 경우
- Banned Devices (금지 기기)
- Repair, Replacement, Refund (수리·교환·환불)

**Special Controls (Class II에 추가 적용):**
- Performance Standards (성능 표준)
- Postmarket Surveillance (시판 후 감시)
- Patient Registries (환자 등록부)
- Special Labeling Requirements (특수 라벨링)
- Guidance Documents (가이던스 문서)
- Premarket Data Requirements (시판 전 데이터 요건)

---

## 3. Regulatory Pathways (인허가 경로)

### 3.1 510(k) Premarket Notification

(출처: FD&C Act Section 510(k); 21 CFR Part 807 Subpart E; FDA 510(k) guidance documents)

510(k)는 시판하고자 하는 기기가 기존 합법적 시판 기기(predicate device)와 **실질적 동등성(substantial equivalence, SE)**이 있음을 입증하는 제도이다.

**3가지 유형:**

| 유형 | 특징 | 데이터 요건 |
|------|------|------------|
| **Traditional 510(k)** | 표준적 SE 입증; predicate와의 직접 비교 | 성능 데이터 포함 가능; 필요시 임상 데이터 |
| **Special 510(k)** | 기존 자사 기기의 설계 변경(design change)에 사용; risk analysis와 verification/validation 중심 | 설계 제어(design control) 문서; 제조자 본인 기기만 predicate 가능 |
| **Abbreviated 510(k)** | FDA-recognized consensus standard 또는 Special Controls guidance에 의존 | 적합성 선언(Declaration of Conformity) 또는 가이던스 준수 요약 |

**주요 수수료 (FY2025, MDUFA V):**
- 표준 수수료: $24,335
- 소기업(Small Business) 수수료: $6,084
(출처: Federal Register, Medical Device User Fee Rates for FY2025, 2024.7.31)

**eSTAR 요건:**
- 510(k) 제출 시 eSTAR(Electronic Submission Template And Resource) 사용이 사실상 표준화됨
- eSTAR v5.5가 현행 최신 버전
(출처: FDA eSTAR program page)

### 3.2 De Novo Classification

(출처: FD&C Act Section 513(f)(2); 21 CFR Part 860 Subpart D; FDA De Novo guidance)

De Novo는 **적합한 predicate가 없는** 신규 기기 중 저~중간 위험(low-to-moderate risk) 기기를 위한 경로이다. 승인 시 새로운 분류(Class I 또는 II)와 Product Code가 생성되어, 향후 유사 기기의 510(k) predicate로 사용 가능하다.

**핵심 통계:**
- 평균 검토 기간: 약 **420일** (2024년 기준, FDA Days 기준 150일 목표 대비 실제 소요 기간)
- 2024년 승인(grant) 건수: **47건**
(출처: Medical Device Academy De Novo review timeline analysis; MDDI Online 2024 FDA approval volume trends)

**eSTAR 의무화:**
- **2025년 10월 1일**부터 모든 De Novo 신청은 eSTAR 형식으로 전자 제출 의무화
- 해당 일자 이후 기존 형식(legacy format)으로 제출 시 Refuse to Accept (RTA) 사유
(출처: FDA De Novo final guidance; RAPS "FDA: De novo requests must be submitted electronically beginning October 2025" 2024.8)

### 3.3 Premarket Approval (PMA)

(출처: FD&C Act Section 515; 21 CFR Part 814; Federal Register FY2025/FY2026 user fee rates)

PMA는 **Class III** 기기에 적용되는 가장 엄격한 인허가 경로로, 안전성(safety)과 유효성(effectiveness)에 대한 과학적·규제적 검토이다.

**핵심 요건:**
- 임상시험(clinical trial) 데이터 필수 (대부분의 경우)
- 비임상 시험(bench testing, animal studies) 데이터
- 제조·품질 시스템 정보
- 라벨링 초안(proposed labeling)

**수수료:**
- FY2025 PMA 신청 수수료: **$540,783**
- FY2026 PMA 신청 수수료: **$579,272** (약 7% 증가)
- 소기업(Small Business) 감면 적용 가능
(출처: Federal Register, Medical Device User Fee Rates for FY2025, 2024.7.31; FY2026, 2025.7.30)

**PMA 보충(Supplement) 유형:**
- 180-day PMA Supplement (180일 보충)
- Real-Time PMA Supplement (실시간 보충)
- Special PMA Supplement — Changes Being Effected (변경 시행 중)
- 30-Day Notice
- Annual Report (연례 보고서)

### 3.4 Breakthrough Device Program

(출처: FDA Breakthrough Devices Program page; FDA GovDelivery bulletin, 2025.12 업데이트)

Breakthrough Device 지정은 21st Century Cures Act (2016)에 의해 법제화된 제도로, 생명을 위협하거나 돌이킬 수 없는 쇠약(irreversibly debilitating) 질환·상태에 대해 더 효과적인 치료·진단을 제공하는 기기의 개발·검토를 가속화한다.

**누적 통계 (2025년 12월 31일 기준):**
- 총 Breakthrough Device 지정: **1,246건** (CDRH 1,226건 + CBER 20건)
- 총 마케팅 인가(marketing authorization): **185건** (CDRH 180건 + CBER 5건)
(출처: FDA Breakthrough Devices Program metrics, 2025.12.31 기준)

**FY2026 동향:**
- FY2026 1분기(2025.10-12): 42건 지정, 연간 168건 예상 속도
- 2025년 하반기 활발한 분야: 정형외과(13건 지정)
(출처: MedTech Dive "FDA breakthrough program starts FY2026 at steady pace" 2026)

**지정 기준:**
1. 생명을 위협하거나 돌이킬 수 없는 쇠약 질환·상태에 대한 기기
2. 다음 중 하나에 해당:
   - 해당 질환·상태에 대한 승인·허가 대안이 없음
   - 기존 승인·허가 대안 대비 중대한 이점(significant advantage) 제공

**혜택:**
- FDA와의 우선적 상호작용(prioritized interaction)
- Sprint Discussion 가능
- 검토 과정에서의 효율적 데이터 개발 지원
- 선임 관리자(senior management) 참여

---

## 4. AI/ML Software as a Medical Device (SaMD)

### 4.1 Predetermined Change Control Plan (PCCP)

(출처: FDA Final Guidance "Marketing Submission Recommendations for a Predetermined Change Control Plan for AI-Enabled Device Software Functions" 2024.12.4 발행)

PCCP는 AI 기반 의료기기의 **시판 후(post-market) 소프트웨어 변경**을 사전에 계획·승인받는 프레임워크이다.

**PCCP의 3가지 필수 구성요소:**

| 구성요소 | 내용 |
|----------|------|
| **1. Description of Modifications** | 사전에 결정된 변경 사항에 대한 상세 설명; 구체적이고 명확해야 함 |
| **2. Modification Protocol** | 변경 구현·검증·확인 방법론; 데이터 관리, 성능 평가 방법 포함 |
| **3. Impact Assessment** | 변경이 기기 안전성·유효성에 미치는 영향 평가; 위험 분석 포함 |

**초안 → 최종본 주요 변경사항:**
- 용어 변경: Machine Learning Device Software Functions (ML-DSFs) → **AI-Enabled Device Software Functions (AI-DSFs)**
- 버전 관리(version control) 섹션 신규 추가
- 사용 목적(indications for use) 변경도 PCCP에 포함 가능함을 명확화
  (예: 추가 기기·구성요소와의 사용 지정)
(출처: RAPS "Final FDA guidance on PCCP includes clarification on version control" 2024.12)

### 4.2 TPLC (Total Product Lifecycle) 가이던스

(출처: FDA Draft Guidance "AI-Enabled Device Software Functions: Lifecycle Management and Marketing Submission Recommendations" 2025.1.7 발행; Federal Register 2025-31543)

**핵심 내용:**
- AI 기반 기기의 전체 제품 수명 주기(설계 → 개발 → 시판 → 시판 후 → 폐기)에 걸친 관리 권고사항
- **투명성(Transparency)**: 사용자 중심의 투명성 전략을 설계 단계부터 포함할 것을 강조
- **편향(Bias) 관리**: TPLC 전반에 걸친 편향 평가·완화 전략 권고
- **설명가능성(Explainability)**: 안전성·유효성 입증의 핵심 요소로 투명성·설명가능성 강조
- 의견 제출 마감: 2025년 4월 7일

**상태:** 초안(Draft) — 시행을 위한 것이 아님(Not for Implementation)

### 4.3 AI/ML 기기 인가 현황

(출처: FDA "AI-Enabled Medical Devices" 목록; The Imaging Wire 2025.12; JAMA Network Open systematic review)

**누적 인가 현황 (2025년 12월 기준):**

| 항목 | 수치 |
|------|------|
| 총 AI/ML 인가 기기 수 | **1,356건 이상** |
| 방사선과(Radiology) 비중 | **약 77%** (약 1,039건) |
| 심혈관(Cardiovascular) | 2위 |
| 기타 전문 분야 | 신경과, 안과, 혈액학 등 |

**인가 경로별 분포:**
- 대다수 510(k) 경로 사용
- 신규 AI 기기는 De Novo 경로도 활용
- Class III AI 기기의 경우 PMA 필요
- PCCP는 510(k), De Novo, PMA 모든 경로에서 포함 가능

**연도별 추이:**
- 2023년: 방사선과 비중 80%
- 2024년: 방사선과 비중 73%
- 2025년 상반기: 방사선과 비중 78%
- 2025년 하반기: 방사선과 비중 75%

### 4.4 AI/ML SaMD 규제 주요 고려사항

**SaMD 정의:**
Software as a Medical Device(SaMD)는 하드웨어 의료기기의 일부가 아닌, **독립적으로(stand-alone)** 의료 목적으로 사용되는 소프트웨어를 의미한다.
(출처: IMDRF "Software as a Medical Device: Possible Framework for Risk Categorization and Corresponding Considerations" 2014)

**AI/ML SaMD 특수 고려사항:**

1. **Locked vs Adaptive Algorithm**:
   - Locked Algorithm: 시판 후 변경 없음; 일반적 510(k)/PMA 경로 적용
   - Adaptive Algorithm (Continuously Learning): 실사용 데이터로 지속 학습; PCCP가 핵심 도구

2. **Good Machine Learning Practice (GMLP):**
   - FDA/Health Canada/MHRA 공동 발표 (2021.10)
   - 10개 기본 원칙(Guiding Principles)
   - 데이터 관리, 모델 학습, 성능 평가, 투명성 등 포괄

3. **Real-World Performance (RWP) Monitoring:**
   - 시판 후 실사용 데이터 기반 성능 모니터링
   - 편향 감지 및 성능 저하(performance degradation) 추적

---

## 5. Quality System & Recent Regulatory Changes

### 5.1 QMSR (Quality Management System Regulation)

(출처: Federal Register "Medical Devices; Quality Management System Regulation Technical Amendments" 2025.12.4; 21 CFR Part 820)

**시행일: 2026년 2월 2일**

QMSR은 기존 Quality System Regulation(QSR, 21 CFR Part 820)을 대체하는 역사적 규정 개편이다.

**핵심 변경사항:**

| 항목 | QSR (기존) | QMSR (신규) |
|------|-----------|-------------|
| 구조 | 15개 Sub-part (A-O) | **2개 Sub-part (A, B)** |
| 기반 표준 | FDA 독자 요건 | **ISO 13485:2016 참조 도입(incorporation by reference)** |
| 검사 방법 | QSIT (Quality System Inspection Technique) | **새로운 검사 프로세스 (Compliance Program 7382.850)** |
| 국제 조화 | 부분적 | ISO 13485와 실질적 조화(harmonization) |

**중요 유의사항:**
- ISO 13485:2016 준수만으로는 QMSR 요건을 완전히 충족하지 **않음**
- QMSR은 ISO 13485를 기반으로 하되, 추가적인 FDA 고유 요건(applicable regulatory requirements)을 포함
- 기존 QSR의 대부분 요건이 철회(withdrawn)되고, ISO 13485:2016 참조로 대체됨
(출처: AAMI "QMSR: Understanding Part 820.10" 2025; Morgan Lewis "February 2, 2026 Is Quickly Approaching" 2024.10)

### 5.2 LDT (Laboratory Developed Test) 규칙 철회

(출처: U.S. District Court for the Eastern District of Texas, ACLA v. FDA & AMP v. FDA, 2025.3.31; Federal Register LDT rule rescission, 2025.9)

**경과:**

| 시점 | 사건 |
|------|------|
| 2024.5 | FDA, LDT에 대한 enforcement discretion 단계적 폐지 최종 규칙(final rule) 발표 |
| 2025.3.31 | 텍사스 동부 연방지방법원, FDA의 LDT 최종 규칙을 **위법(unlawful)**으로 판단하여 무효화(vacate) |
| 2025.9 | FDA, 공식적으로 LDT 최종 규칙 **철회(rescind)** — 2024년 5월 규칙 이전 상태로 복귀 |

**현재 상태:**
- FDA는 LDT에 대한 **enforcement discretion 정책을 유지**
- LDT는 510(k) 허가 또는 FDA 승인 없이 사용 가능 (기존 관행 유지)
- HHS는 법원 판결에 대해 항소하지 않기로 결정
(출처: Sidley Austin "FDA's Laboratory-Developed Test Rule Struck Down" 2025.4; FDA Law Blog "FDA Formally Rescinds the LDT Final Rule" 2025.8)

### 5.3 MDUFA V (Medical Device User Fee Amendments, FY2023-2027)

(출처: MDUFA V Five-Year Financial Plan, FDA 2025 update; Federal Register FY2025, FY2026 user fee rates)

MDUFA V는 2022년에 재인가(reauthorized)되어 **FY2023-FY2027** (2022.10.1 ~ 2027.9.30) 기간 동안 적용된다.

**주요 수수료 비교:**

| 수수료 항목 | FY2025 | FY2026 | 변동률 |
|------------|--------|--------|--------|
| PMA 신청 | $540,783 | $579,272 | +7.1% |
| 510(k) 신청 | $24,335 | (약 $26,000 예상) | +약 7% |
| 시설 등록(Establishment Registration) | $9,280 | $9,760 | +5.2% |

**FY2026 총 수입 목표:** $427,833,000 (법정 기준액 $366,486,300 × 인플레이션 조정 계수 1.167391)
(출처: Federal Register 2025-14412, "Medical Device User Fee Rates for Fiscal Year 2026" 2025.7.30)

**Small Business 감면:**
- PMA: 표준 수수료의 25% 적용
- 510(k): 표준 수수료의 25% 적용
- 자격 요건: 직원 수, 매출액 기준 충족 필요

---

## 6. 참고: 주요 디지털 헬스 규제 프레임워크 요약

### 6.1 FDA Digital Health 정책 체계

(출처: FDA Digital Health Center of Excellence; 각 가이던스 문서)

| 가이던스/규정 | 상태 | 발행일/시행일 | 핵심 내용 |
|--------------|------|-------------|-----------|
| General Wellness Guidance | **최종(Final)** | 2026.1.6 | 센서 기반 웨어러블 관련 확대; 혈압 제품 기준 명확화 |
| CDS Guidance | **최종(Final)** | 2026.1.6 (재발행 1.29) | 단일 권고 enforcement discretion; 위험 점수 관련 문구 삭제 |
| PCCP Guidance | **최종(Final)** | 2024.12.4 | AI-DSF 명칭 변경; 버전 관리 추가; 사용 목적 변경 포함 가능 |
| TPLC/AI-DSF Guidance | **초안(Draft)** | 2025.1.7 | 투명성·편향 관리; TPLC 전반 권고 |
| QMSR (21 CFR Part 820) | **시행(Effective)** | 2026.2.2 | ISO 13485 참조 도입; QSR 대체 |

### 6.2 인허가 경로 선택 흐름도 (간략)

```
기기 해당 여부 판단
├── General Wellness → FDA 규제 면제
├── CDS 4기준 충족 → 의료기기 정의 제외
└── 의료기기(Device)
    ├── Class I → 대부분 510(k) 면제; 등록·목록만
    ├── Class II
    │   ├── Predicate 있음 → 510(k)
    │   └── Predicate 없음 → De Novo
    └── Class III → PMA
        └── (Breakthrough Device 지정 가능)
    └── AI/ML → 상기 경로 + PCCP 포함 가능
```

---

> **면책 조항(Disclaimer):** 이 문서는 규제 프레임워크에 대한 일반적 안내를 제공하며, 법적 자문을 대체하지 않습니다. 구체적인 제품의 규제 전략은 반드시 규제 전문가(Regulatory Affairs professional)와 상의하십시오. 모든 정보는 문서에 명시된 출처에 기반하며, 규정은 수시로 변경될 수 있으므로 FDA.gov에서 최신 정보를 확인하십시오.
