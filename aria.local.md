# ARIA Local Playbook

조직별 규제 전략 및 설정을 위한 ARIA 플레이북 템플릿

**위치**: 이 파일을 **프로젝트 루트 디렉토리**에 복사하세요 (플러그인 디렉토리가 아님)
**용도**: 조직 특화 규제 선호사항, 벤치마크, 전략 설정
**참조**: SPEC-ARIA-001 Section S6

---

## Organization Profile (조직 프로필)

```yaml
# 회사명 및 규제 부서
company_name: "Your Company Name"
regulatory_department: "RA/QA Department"

# 주요 의료기기 유형
# Options: Active, Implantable, IVD, SaMD, Non-active
primary_device_types:
  - "Active"
  - "Implantable"

# 활성 시장
# Options: US, EU, Korea, Japan, China, Canada
active_markets:
  - "US"
  - "EU"
  - "Korea"
```

---

## Language Preference (언어 설정)

```yaml
# 출력 언어 설정
# Options: ko (Korean, default) | en (English)
# Reference: SPEC-ARIA-001 SR-008
output_language: ko
```

**설명**:
- `ko`: 모든 출력을 한국어로 생성 (기본값)
- `en`: 모든 출력을 영어로 생성
- 명령어 플래그 `--lang`이 우선순위를 가집니다

---

## Preferred Regulatory Pathways (선호 규제 경로)

### FDA (미국)

```yaml
# FDA 등급별 선호 경로
# Class I Options: 510(k) Exempt, 510(k)
fda_class_i_preferred: "510(k) Exempt"

# Class II Options: 510(k), De Novo
fda_class_ii_preferred: "510(k)"

# Class III Options: PMA, HDE
fda_class_iii_preferred: "PMA"

# 선호 전략 노트
fda_strategy_notes: "510(k) 경로 우선 고려. PMA는 임플란트만 해당."
```

### EU MDR (유럽)

```yaml
# 선호 Notified Body
# 예: TÜV SÜD, BSI, SGS, DEKRA
eu_preferred_notified_body: "TÜV SÜD"

# CE 마킹 접근 방식
# Options: Full QMS, Product-specific, Module-based
eu_ce_marking_approach: "Full QMS"

# 선호 전략 노트
eu_strategy_notes: "TÜV SÜD와 장기 파트너십. ISO 13485 인증 유지."
```

### MFDS (한국)

```yaml
# 선호 규제 경로
# Options: 인증, 허가, 신고
mfds_preferred_pathway: "인증"

# 선호 인증기관
# 예: 한국의료기기안전정보원, 한국산업기술시험원
mfds_preferred_certification_body: "한국의료기기안전정보원"

# 선호 전략 노트
mfds_strategy_notes: "인증 경로 우선. 2등급 이하는 신속 인증 활용."
```

---

## Classification Positions (분류 입장)

```yaml
# 조직의 표준 분류 입장
# 과거 결정 사례를 기록하여 일관성 유지

standard_positions:
  - device_type: "심전도 모니터"
    fda_class: "II"
    eu_mdr_class: "IIa"
    mfds_class: "2"
    rationale: "비침습, 진단 목적, 510(k) precedent 존재"

  - device_type: "혈당 측정기"
    fda_class: "II"
    eu_mdr_class: "IIb"
    mfds_class: "2"
    rationale: "체외 진단, 치료 결정 영향"

# 추가 입장 사례 기록
# ...
```

---

## Cost/Timeline Benchmarks (비용/일정 벤치마크)

```yaml
# 과거 프로젝트 실제 비용 (USD)
historical_costs:
  fda_510k_class_ii:
    consulting: 50000
    testing: 30000
    regulatory_fees: 12000
    total: 92000

  eu_mdr_class_iia:
    consulting: 60000
    testing: 40000
    notified_body: 25000
    total: 125000

  mfds_class_2:
    consulting: 30000
    testing: 20000
    certification_fees: 5000
    total: 55000

# 과거 프로젝트 실제 일정 (개월)
historical_timelines:
  fda_510k_class_ii: 12
  eu_mdr_class_iia: 18
  mfds_class_2: 9

# 선호 시험 기관
preferred_testing_labs:
  - "Intertek"
  - "TÜV Rheinland"
  - "한국산업기술시험원 (KTL)"
```

---

## Consultant/Notified Body Preferences (컨설턴트/인증기관 선호)

```yaml
# 선호 규제 컨설턴트
preferred_regulatory_consultants:
  - name: "ABC Regulatory Consulting"
    specialization: "FDA 510(k), PMA"
    contact: "contact@abc-regulatory.com"

  - name: "XYZ MedTech Advisors"
    specialization: "EU MDR"
    contact: "info@xyz-medtech.com"

# 선호 Notified Body (EU)
preferred_notified_bodies:
  - name: "TÜV SÜD"
    nb_number: "0123"
    specialization: "Active devices, Class IIa/IIb"

  - name: "BSI Group"
    nb_number: "0086"
    specialization: "Class III, Implantable"

# 선호 시험/인증 기관
preferred_certification_bodies:
  korea:
    - "한국의료기기안전정보원 (NIDS)"
    - "한국산업기술시험원 (KTL)"
  us:
    - "Intertek"
    - "TÜV Rheinland"
```

---

## Risk Tolerance (위험 선호도)

```yaml
# 조직 위험 선호도
# Options: conservative | moderate | aggressive
risk_appetite: conservative

# 위험 선호도 설명
# - conservative: 안전한 경로 우선 (510(k) over De Novo, 표준 준수 엄격)
# - moderate: 균형잡힌 접근 (위험-보상 평가)
# - aggressive: 혁신적 경로 추구 (De Novo, 신규 기술 적극 활용)

risk_strategy_notes: |
  보수적 접근. 검증된 경로 우선.
  신규 기술은 precedent 확보 후 진행.
  임상시험 데이터는 충분한 샘플 크기 확보.
```

---

## Custom Escalation Criteria (에스컬레이션 기준)

```yaml
# 법률 자문 필요 시점
legal_counsel_triggers:
  - "분류 등급이 모호한 경우"
  - "새로운 규제 해석이 필요한 경우"
  - "FDA Warning Letter 또는 규제 조치 발생 시"

# 외부 컨설턴트 개입 시점
external_consultant_triggers:
  - "De Novo 또는 PMA 경로 선택 시"
  - "EU MDR Class IIb/III 신규 제품"
  - "precedent가 없는 신기술"

# 이사회 보고 기준
board_notification_thresholds:
  cost_threshold_usd: 200000
  timeline_threshold_months: 24
  regulatory_risk_level: "HIGH"

  # 보고 필요 시나리오
  scenarios:
    - "PMA 경로 진행 결정"
    - "FDA 추가 정보 요청 (Additional Information)"
    - "Notified Body 승인 지연"
```

---

## Data Management (데이터 관리)

```yaml
# 데이터 보존 기간 (일)
# Reference: SPEC-ARIA-001 ER-016, S11.4
data_retention_days: 365

# 보존 기간 초과 데이터 경고 표시
warn_on_stale_data: true

# 데이터 관리 정책 노트
data_management_notes: |
  규제 요구사항:
  - FDA: 제품 단종 후 최소 2년
  - EU MDR: 시장 출시 후 10년 (이식형 15년)
  - MFDS: 의료기기법 보존 요구사항 준수

  조직 정책: 365일 (1년) 경과 시 경고 표시.
  수동 삭제 권장. 자동 삭제 없음.
```

---

## Version History (버전 이력)

```yaml
# 플레이북 버전 관리
playbook_version: "1.0.0"
last_updated: "2026-02-10"
updated_by: "RA Department"

# 변경 이력
change_log:
  - version: "1.0.0"
    date: "2026-02-10"
    changes: "초기 플레이북 생성"
```

---

## 사용 방법

1. **복사**: 이 템플릿을 프로젝트 루트에 `aria.local.md`로 복사
2. **편집**: 조직 정보 및 선호 설정 입력
3. **저장**: 파일 저장 (Git에 커밋 가능, 민감 정보 제외)
4. **자동 로드**: ARIA가 명령어 실행 시 자동으로 로드하여 적용

**참고**:
- `.aria/active_product.json`과 달리 `aria.local.md`는 팀 공유 가능
- 조직 규제 전략을 문서화하여 일관성 유지
- 정기적으로 업데이트하여 최신 상태 유지

---

**템플릿 버전**: 2.0.0
**SPEC 참조**: SPEC-ARIA-001 Section S6
**관련 문서**: README.md, CONNECTORS.md
