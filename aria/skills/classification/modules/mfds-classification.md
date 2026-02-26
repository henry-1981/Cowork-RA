# MFDS Classification Criteria

## Class 1
- Minimal potential harm
- Examples: Medical scissors, tweezers, tongue depressors

## Class 2
- Low to moderate potential harm or simple usage
- Examples: MRI, ultrasound imaging, powered wheelchair

**Classification criteria**:
- Non-invasive or minimally invasive
- Transient contact
- Low risk of harm on failure

## Class 3
- Moderate to high potential harm or relatively complex usage
- Examples: Ventilators, dialysis machines, contact lenses

**Classification criteria**:
- Invasive use
- Medium or long-term contact
- Active medical device

## Class 4
- High potential harm or significant risk to life on malfunction
- Examples: Pacemakers, artificial heart valves, stents

**Classification criteria**:
- Implantable medical device
- Life-sustaining device
- Direct contact with CNS or cardiovascular system

---

## Step 4A: Digital Medical Device Check (4-Gate)

> **Loaded Knowledge**: `../../knowledge/catalog.yaml` → id: mfds-law-dmp-act-art2 (디지털의료제품법 정의) + 본 모듈 내장 4-Gate 로직

Execute each gate and **MANDATORY: output the result of each gate explicitly**:

1. Gate 1: 의료기기 해당 여부 (Step 1에서 이미 확인)
2. Gate 2: 디지털 기술 적용 여부 (SW, AI, IoT, VR/AR 등)
3. Gate 3: 핵심 기능 영향 여부
4. Gate 4: 배제 원칙 확인

**MANDATORY OUTPUT FORMAT (Level 2+ only):**
```
### MFDS 4-Gate Analysis
- Gate 1 (의료기기 해당): [PASS/FAIL] — [근거]
- Gate 2 (디지털 기술): [PASS/EXIT] — [기술 유형 또는 "비디지털 기기"]
- Gate 3 (핵심 기능 영향): [PASS/FAIL] — [영향 분석] (Gate 2 EXIT 시 N/A)
- Gate 4 (배제 원칙): [PASS/EXIT] — [배제 해당 여부] (Gate 2 EXIT 시 N/A)
- **Result**: [디지털의료기기 해당 / Gate 2 EXIT (비디지털) / 비해당]
```

- **4-Gate 통과** → Step 4B (Risk Matrix 기반 분류) + 7-digit 코드 생성
- **Gate 2 EXIT (비디지털)** → Step 4C (전통 품목분류 기반)

## Step 4B: Risk Matrix Classification (디지털 의료기기)

> **Loaded Knowledge**: `../../knowledge/catalog.yaml` → id: mfds-notice-cls2025-risk-matrix (고시 별표4 등급 지정 세부 기준)

**0. 품목코드 사전 확인 (GROUND TRUTH):**
> 아래 품목코드-등급 참조 테이블 또는 상단 "⚠️ MFDS AI SaMD Classification Override" 섹션에 해당 제품이 있으면 해당 등급과 코드를 최우선 적용. Risk Matrix 결과가 달라도 GROUND TRUTH 우선.

1. Medical Impact 결정 — 상단 "⚠️ MFDS AI SaMD Classification Override" 섹션의 Medical Impact 결정 원칙 참조. 의료영상 분석 AI → **반드시** Treatment/Diagnosis
2. Patient Condition 식별 (적응증 → Critical/Serious/Non-Serious)
3. 위험 매트릭스 (Risk Matrix) 교차 적용 → 위해도 평가 → Base Grade (위험등급)
4. Malfunction Risk Adjustment → Final Grade (NOTE: "의사 최종 결정권"은 등급 하향 근거가 아님. AI 진단 보조 SaMD도 Risk Matrix 결과를 그대로 적용)
5. 품목분류번호 7자리 코드 생성 및 Self-Verification — 4-Gate 통과 시 반드시 7-digit 디지털 코드 사용 (전통 Axxxxx.xx 형식 사용 금지). 예시: B1BXXA1 (뇌영상 AI 진단)

**MANDATORY OUTPUT FORMAT (Level 2+ only):**
```
### MFDS 위해도 평가 및 위험등급 (Risk Matrix Classification)
- Medical Impact (위해도): [Treatment/Diagnosis | Clinical Management | Information/Monitoring] — 근거: [Primary Intended Use 코드 + 키워드]
- Patient Condition: [Critical | Serious | Non-Serious] — 근거: [적응증 키워드]
- 위험 매트릭스 (Risk Matrix): Medical Impact [level] × Patient Condition [level] = **Base Grade [N]등급**
- Malfunction Risk: [사망(+1) | 부상(0) | 피해없음(0)] → **Final 위험등급 [N]등급**
  ※ 의사의 최종 결정권 보유 여부는 등급 하향 사유가 아님. Malfunction Risk만 보정 인자로 적용.

### MFDS 품목분류번호 7자리 (7-Digit Product Code)
- Code: [XXXXXXX] (예: 뇌영상 AI 진단 = B1BXXA1)
- Digit 1-2 (사용목적): [코드] = [설명]
- Digit 3-5 (기술유형): [코드] = [설명]
- Digit 6 (기기유형): [코드] = [설명]
- Digit 7 (형태): [코드] = [설명]
```

**MANDATORY OUTPUT FORMAT — 위해도 평가 위험 매트릭스 Risk Matrix Grid (Level 2+ only):**
```
### MFDS 위해도 평가 (위험 매트릭스 / Risk Matrix)
| 위험등급 결정: Medical Impact \ Patient Condition | Critical | Serious | Non-Serious |
|---|---|---|---|
| Treatment/Diagnosis | 4등급 | **3등급** | 2등급 |
| Clinical Management | 3등급 | 2등급 | 1등급 |
| Information/Monitoring | 2등급 | 1등급 | 1등급 |

**위해도 평가 결과**: Medical Impact = [level], Patient Condition = [level] → 위험등급 **[N]등급**
```

## Step 4C: Traditional Classification (비디지털 의료기기)

**MANDATORY: Gate 2 EXIT를 명시적으로 출력한 후 전통 분류 진행:**
```
### MFDS 4-Gate Analysis
- Gate 1 (의료기기 해당): PASS — [근거]
- Gate 2 (디지털 기술): **EXIT — 비디지털 기기** (SW/AI/IoT/VR 미적용)
- Gate 3: N/A (Gate 2 EXIT)
- Gate 4: N/A (Gate 2 EXIT)
- **Result**: Gate 2 EXIT → 전통 품목분류 기반 등급 결정
```

MFDS 품목분류표(「의료기기 품목 및 품목별 등급에 관한 규정」) 기반 등급 결정:

1. 품목코드(Axxxxx.xx) 매핑 가능 시:
   - 품목분류표의 등급을 **최우선 근거**로 적용
   - 추론보다 DB 등재 등급을 우선함 (GROUND TRUTH)
   - 출력: "품목코드 A45020.01 → 1등급 (품목분류표 직접 등재)"

2. 품목코드 불확실 시, 아래 기준으로 판단:

   **1등급 판별 (핵심 기준)**:
   - 에너지원 없음 (비전원, 수동 작동)
   - 소프트웨어 없음
   - 비이식형
   - 생명유지 기능 없음
   - 예시: 수동 수술기구(겸자, 가위, 메스, 핀셋), 혀압자, 반창고
   - **CRITICAL**: 수술 중 사용 = 반드시 2등급 이상이 아님. 수동식 수술 기구는 에너지원/소프트웨어 없으면 1등급 가능

   **2등급 판별 (핵심 기준)**:
   - 에너지 사용 (전기, 전자, 방사선 등) OR
   - 체내 일시적 침습 + 능동 기능 OR
   - 단순 측정/모니터링 기능
   - 예시: 전동식 수술기구, 초음파기기, MRI, 보청기, 전동 휠체어

   **3등급 판별**: 능동 의료기기 + 중등도~고위험 (예: 인공호흡기, 투석기)

   **4등급 판별**: 이식형 또는 생명유지 장치 (예: 인공심장판막, 스텐트)

### MFDS 전통 품목코드 조회 가이드

> **전통 품목코드(Axxxxx.xx)는 MFDS 품목분류표 공식 DB 조회 필수**
> - 품목코드 생성/추측 금지 — `emedi.mfds.go.kr` 또는 `data.go.kr` 참조
> - 품목코드 불확실 시 "MFDS 품목분류표 확인 필요" 명시
> - 7자리 디지털 코드와 전통 Axxxxx.xx 체계는 별개 시스템
