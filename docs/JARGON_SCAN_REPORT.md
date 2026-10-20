# JARGON SCAN REPORT — 기획서 내부 암호 · SSOT 금지어 전수 스캔

- 생성 시각: `2026-10-20 15:24:02`
- 실행 스킬: `scripts/qa/skill_jargon_scan.py` (Skill 2, 읽기 전용)
- 스캔 대상: `prototype_clean/*.html` — **38개 화면**
- **[A] DOM 가시 텍스트 탐지: 333건** (텍스트 노드 + placeholder/title/alt/aria-label/버튼 value)
- **[B] JS 동적 렌더링 후보 탐지: 237건** (`<script>` 내 한글 포함 문자열 리터럴)
- 무결 화면(탐지 0건): 14개

> [A]는 정적 화면에 그대로 노출되는 텍스트이므로 우선 정비 대상이다. [B]는 innerHTML/모달 렌더링 시 노출될 수 있는 후보로, 분석 AI가 노출 여부를 판단한다.
> 본 스킬은 HTML을 수정하지 않는다. 치환 패치는 분석 AI + 코딩 AI가 작성한다.

## 1. 규칙별 탐지 요약

| 분류 | 규칙 | 설명 | [A] DOM | [B] JS | 대표 매칭어 |
| :--- | :--- | :--- | ---: | ---: | :--- |
| 내부암호 | CODE_C | C-01~04 (정산 케이스 코드) | 4 | 10 | `C-03`×5, `C-01`×4, `C-02`×3, `C-04`×2 |
| 내부암호 | CODE_H | H-01~05 (하드락 코드) | 0 | 0 | - |
| 내부암호 | CODE_D | D-1~16 (회귀테스트 코드) | 17 | 13 | `D-15`×7, `D-13`×5, `D-16`×5, `D-12`×4, `D-1`×4, `D-3`×2 |
| 내부암호 | CODE_P | P1.1~5.1 (Phase 코드) | 8 | 2 | `P5.1`×3, `P1.1`×2, `P2.1`×2, `P2.3`×2, `P2.2`×1 |
| 내부암호 | PIPELINE | Pipeline 표기 | 82 | 61 | `Pipeline 5.1`×42, `Pipeline 1.1`×27, `Pipeline 2.1`×23, `Pipeline 2.2`×22, `Pipeline 2.3`×20, `pipeline`×5 |
| 내부암호 | CHAPTER | 제N장 (기획서 장 번호) | 32 | 3 | `제14장`×6, `제6장`×5, `제8장`×4, `제4장`×3, `제13장`×3, `제3장`×3 |
| 내부암호 | SECTION | N.N절 (기획서 절 번호) | 135 | 83 | `5.2절`×17, `5.3절`×13, `8.3절`×12, `3.5절`×12, `17.5절`×11, `10.4절`×10 |
| 내부암호 | SNAKE_FLAG | *_flag DB 컬럼명 | 0 | 0 | - |
| 내부암호 | SNAKE_YN | *_yn DB 컬럼명 | 6 | 6 | `own_copyright_yn`×12 |
| 내부암호 | SNAKE_ID | *_id DB 컬럼명 | 14 | 4 | `contract_id`×5, `order_item_id`×4, `origin_settlement_id`×2, `payee_id`×2, `rights_holder_id`×2, `agreement_id`×1 |
| 금지어 | BAN_GICHUL | 기출 | 1 | 9 | `기출`×10 |
| 금지어 | BAN_ERRATA | 정오표 | 0 | 0 | - |
| 금지어 | BAN_VIMEO | Vimeo | 0 | 0 | - |
| 금지어 | BAN_80PCT | 80% | 3 | 18 | `80%`×21 |
| 금지어 | BAN_CIRCLED | ①~⑭ 원문자 번호 | 31 | 28 | `①`×19, `②`×18, `③`×13, `④`×6, `⑤`×2, `⑥`×1 |
| 금지어 | BAN_MARKER | [마커 표기 | 0 | 0 | - |
| 번역중복 | DUP_PAREN | 동일어 괄호 중복 (예: 실결제금액(실결제금액)) | 0 | 0 | - |

## 2. 화면별 탐지 요약

| 화면 | [A] DOM | [B] JS | 내부암호 | 금지어 | 번역중복 |
| :--- | ---: | ---: | ---: | ---: | ---: |
| `00_WORKFLOW_GUIDE_baseline.html` | 49 | 0 | 49 | 0 | 0 |
| `ADMN-BOOK-001_baseline.html` | 22 | 8 | 13 | 17 | 0 |
| `ADMN-BRD-001_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-BRD-002_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-BRD-005_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-CONF-001_baseline.html` | 0 | 1 | 1 | 0 | 0 |
| `ADMN-CONF-002_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-CONF-003_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-CONF-004_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-CONF-005_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-CONF-010_baseline.html` | 4 | 15 | 19 | 0 | 0 |
| `ADMN-DASH-001_baseline.html` | 3 | 0 | 1 | 2 | 0 |
| `ADMN-INST-001_baseline.html` | 26 | 4 | 29 | 1 | 0 |
| `ADMN-INST-002_baseline.html` | 8 | 15 | 21 | 2 | 0 |
| `ADMN-LOGIN-001_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-ORD-001_baseline.html` | 10 | 0 | 10 | 0 | 0 |
| `ADMN-PROD-001_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-PROD-002_baseline.html` | 2 | 0 | 2 | 0 | 0 |
| `ADMN-PROD-003_baseline.html` | 1 | 1 | 1 | 1 | 0 |
| `ADMN-PROD-004_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-PROD-005_baseline.html` | 0 | 1 | 1 | 0 | 0 |
| `ADMN-PROD-006_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-PROD-007_baseline.html` | 7 | 3 | 10 | 0 | 0 |
| `ADMN-PROM-001_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-PROM-002_baseline.html` | 1 | 0 | 1 | 0 | 0 |
| `ADMN-RFD-002_baseline.html` | 7 | 8 | 3 | 12 | 0 |
| `ADMN-SETT-001_baseline.html` | 6 | 31 | 32 | 5 | 0 |
| `ADMN-SETT-002_baseline.html` | 51 | 72 | 86 | 37 | 0 |
| `ADMN-SETT-004_baseline.html` | 12 | 6 | 18 | 0 | 0 |
| `ADMN-SETT-005_baseline.html` | 10 | 14 | 22 | 2 | 0 |
| `ADMN-SETT-006_baseline.html` | 0 | 4 | 0 | 4 | 0 |
| `ADMN-SETT-007_baseline.html` | 24 | 21 | 41 | 4 | 0 |
| `ADMN-SETT-008_baseline.html` | 13 | 10 | 23 | 0 | 0 |
| `ADMN-SETT-009_baseline.html` | 56 | 15 | 68 | 3 | 0 |
| `ADMN-SETT-011_baseline.html` | 0 | 0 | 0 | 0 | 0 |
| `ADMN-USER-001_baseline.html` | 1 | 0 | 1 | 0 | 0 |
| `ADMN-USER-007_baseline.html` | 20 | 8 | 28 | 0 | 0 |
| `patch_all_snb_v3.html` | 0 | 0 | 0 | 0 | 0 |

## 3. [A] DOM 가시 텍스트 상세 (우선 정비 대상)

### `00_WORKFLOW_GUIDE_baseline.html` — 49건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 478 | text | 내부암호 | SECTION | `8.3절` | … 업무 순서, 화면 간 데이터 인계 조건, 그리고 8.3절 1~11단계 통합 … |
| 494 | text | 내부암호 | SECTION | `16.2절` | 결번 ADMN-SETT-003 영구 제외 (16.2절) |
| 517 | text | 내부암호 | SECTION | `5.2절` | (5.2절) |
| 532 | text | 내부암호 | SECTION | `5.3절` | …급금 잔액 > 0원 계약은 분할 등록 원천 차단 (5.3절) |
| 550 | text | 내부암호 | SNAKE_YN | `own_copyright_yn` | own_copyright_yn = true |
| 551 | text | 내부암호 | PIPELINE | `Pipeline 2.1` | Pipeline 2.1 |
| 552 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | Pipeline 5.1 |
| 553 | text | 내부암호 | SECTION | `6.1절` | 판매 이력 발생 후 공급 형태 변경 하드락 차단 (6.1절) |
| 566 | text | 내부암호 | SECTION | `4.3절` | 합계 100.00% 충족 시에만 판매 차단 해제 (4.3절) |
| 567 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | Pipeline 5.1 |
| 595 | text | 내부암호 | SECTION | `8.2절` | 이내 시 단수차액 일괄 대체 (8.2절) |
| 629 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | Pipeline 5.1 |
| 629 | text | 내부암호 | CODE_C | `C-01` | …·C 공제는 5단계 한도 캡 적용 후 차감·복원 (C-01 흡수 방지) … |
| 631 | text | 내부암호 | SECTION | `15.3절` | 로 고정 (15.3절) |
| 645 | text | 내부암호 | SECTION | `17.5절` | 전환 효력일 불명 시 7월 1일 임의 가정 금지 (17.5절) |
| 673 | text | 내부암호 | CODE_D | `D-13` | ) 적재 (QA D-13) |
| 691 | text | 내부암호 | SECTION | `10.4절` | 4채널 증빙·원천세 정정 큐 (10.4절, 1:N 복수 허용) |
| 703 | text | 내부암호 | PIPELINE | `Pipeline 2.3` | Pipeline 2.3 |
| 706 | text | 내부암호 | SECTION | `18.4절` | … 18.4절) |
| 707 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | Pipeline 5.1 |
| 708 | text | 내부암호 | CHAPTER | `제14장` | 제14장 14.1절 |
| 708 | text | 내부암호 | SECTION | `14.1절` | 제14장 14.1절 |
| 732 | text | 내부암호 | SECTION | `3.1절` | …인 위탁자 포함) 주민등록번호 수집 필드 미노출 (3.1절) |
| 733 | text | 내부암호 | SECTION | `3.5절` | …기하고 정산 원장 금액은 계층 2(10년) 보존 (3.5절) |
| 749 | text | 내부암호 | CODE_D | `D-12` | …수), 수동 조정, 계정 대체, 지원금 한도 복원(D-12) 전수 기록 |
| 765 | text | 내부암호 | CHAPTER | `제6장` | 01권 제6장 6.1 ~ 6.6절 기준 |
| 765 | text | 내부암호 | SECTION | `6.6절` | 01권 제6장 6.1 ~ 6.6절 기준 |
| 812 | text | 내부암호 | PIPELINE | `Pipeline 2.1` | Pipeline 2.1 |
| 813 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | Pipeline 5.1 |
| 823 | text | 내부암호 | SECTION | `8.3절` | 3️⃣ 8.3절 통합 연산 엔진(1~11단계)과 백오피스 화면 데… |
| 824 | text | 내부암호 | CHAPTER | `제8장` | SSOT: 02권 제8장 8.3절 |
| 824 | text | 내부암호 | SECTION | `8.3절` | SSOT: 02권 제8장 8.3절 |
| 840 | text | 내부암호 | PIPELINE | `Pipeline 1.1` | Pipeline 1.1 |
| 840 | text | 내부암호 | PIPELINE | `Pipeline 2.1` | Pipeline 2.1 |
| 841 | text | 내부암호 | PIPELINE | `Pipeline 2.2` | Pipeline 2.2 |
| 841 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | Pipeline 5.1 |
| 842 | text | 내부암호 | PIPELINE | `Pipeline 2.3` | Pipeline 2.3 |
| 853 | text | 내부암호 | PIPELINE | `Pipeline 1.1` | Pipeline 1.1 |
| 864 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | Pipeline 5.1 |
| 875 | text | 내부암호 | CODE_P | `P1.1` | P1.1 |
| 875 | text | 내부암호 | CODE_P | `P2.1` | P2.1 |
| 940 | text | 내부암호 | SNAKE_YN | `own_copyright_yn` | own_copyright_yn = true |
| 943 | text | 내부암호 | PIPELINE | `Pipeline 2.1` | Pipeline 2.1 |
| 944 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | Pipeline 5.1 |
| 945 | text | 내부암호 | CODE_D | `D-15` | ) 시 선급금 상계 연동 (부록 D-15·D-16) |
| 945 | text | 내부암호 | CODE_D | `D-16` | ) 시 선급금 상계 연동 (부록 D-15·D-16) |
| 968 | text | 내부암호 | SECTION | `10.1절` | 마감 취소 절대 금지 (10.1절). 발생 원인 귀속월 ( |
| 969 | text | 내부암호 | SECTION | `10.4절` | )을 분리하고 4채널 증빙·원천세 정정 작업 (10.4절, 1:N 복수 작업 허용) 자동 생성 … |
| 977 | text | 내부암호 | CHAPTER | `제14장` | (자사/전체 정산 대조 및 제14장 신고 기초자료 추출) → 확인 필요 시 … |

### `ADMN-BOOK-001_baseline.html` — 22건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 762 | text | 내부암호 | CHAPTER | `제6장` | 제6장 6.1~6.6절 · v4.0.0 SSOT |
| 762 | text | 내부암호 | SECTION | `6.6절` | 제6장 6.1~6.6절 · v4.0.0 SSOT |
| 763 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | …태(book_supply_type) · 자사저작권(Pipeline 5.1) · 정가 이력(book_price_history… |
| 778 | text | 내부암호 | SNAKE_YN | `own_copyright_yn` | 자사저작권 (own_copyright_yn) |
| 791 | text | 내부암호 | PIPELINE | `Pipeline 2.1` | Pipeline 2.1 |
| 801 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | Pipeline 5.1 (개발지원금 모수 인입 · v4.0.0) |
| 811 | text | 내부암호 | PIPELINE | `Pipeline 2.2` | Pipeline 2.2 |
| 812 | text | 내부암호 | SECTION | `6.6절` | ) · 6.6절 등식 적용 |
| 831 | text | 내부암호 | SECTION | `6.1절` | 정산 비대상 (정산기준금 0원 고정 · 6.1절) |
| 851 | text | 내부암호 | CHAPTER | `제6장` | [제6장 6.2절 정가 변경 이력 관리 원칙] |
| 851 | text | 내부암호 | SECTION | `6.2절` | [제6장 6.2절 정가 변경 이력 관리 원칙] |
| 922 | text | 내부암호 | PIPELINE | `Pipeline 2.1` | OWN_PUBLISHED · 자사발행 (Pipeline 2.1 인세 / 5.1 지원금) |
| 923 | text | 내부암호 | PIPELINE | `Pipeline 2.2` | CONSIGNMENT · 위탁판매 도서 (Pipeline 2.2 수수료 차감/총액) |
| 932 | text | 금지어 | BAN_CIRCLED | `①` | ① 계약원장(INST-001) 가채번 출발 |
| 933 | text | 금지어 | BAN_CIRCLED | `②` | ② 교재관리(PROD-004) 선등록 역매핑 |
| 934 | text | 금지어 | BAN_CIRCLED | `③` | ③ 공급원장(BOOK-001) 최초 채번 |
| 1038 | text | 금지어 | BAN_CIRCLED | `①` | ① 계약원장(ADMN-INST-001) 가채번 도서 … |
| 1055 | text | 금지어 | BAN_CIRCLED | `②` | ② 교재관리(ADMN-PROD-004) 선등록 SKU… |
| 1072 | text | 금지어 | BAN_CIRCLED | `③` | ③ 공급원장(ADMN-BOOK-001)에서 최초 신규… |
| 1088 | text | 금지어 | BAN_CIRCLED | `①` | [경로 ① 선택됨 — 계약원장 가채번(TMP-BK-2601)… |
| 1253 | text | 금지어 | BAN_CIRCLED | `①` | ① 계약원장(ADMN-INST-001) 가채번 도서 … |
| 1299 | text | 금지어 | BAN_CIRCLED | `②` | ② 교재관리(ADMN-PROD-004) 선등록 원가 … |

### `ADMN-CONF-010_baseline.html` — 4건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 344 | text | 내부암호 | CODE_D | `D-12` | D-12 · 17장 · 6장 |
| 349 | text | 내부암호 | SECTION | `3.5절` | USER-007 · 3.5절 |
| 367 | text | 내부암호 | SECTION | `16.1절` | 전체 9대 감사 이벤트 보기 (16.1절) |
| 398 | text | 내부암호 | SECTION | `16.1절` | 감사 이벤트 구분 (16.1절 9대 항목) |

### `ADMN-DASH-001_baseline.html` — 3건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 546 | text | 내부암호 | CODE_D | `D-3` | D-3 |
| 606 | text | 금지어 | BAN_80PCT | `80%` | CDN 트래픽 80% 초과 시 주의 배지가 점등되며, 수동 점검 시 a… |
| 629 | text | 금지어 | BAN_80PCT | `80%` | · 80% 임계치 초과 · 응답 118ms |

### `ADMN-INST-001_baseline.html` — 26건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 369 | text | 내부암호 | CHAPTER | `제4장` | … 상품(강의 · 도서 SKU) 1계층 매핑 현황 (제4장 4.3절 · 제16장 16.1절) |
| 369 | text | 내부암호 | CHAPTER | `제16장` | … SKU) 1계층 매핑 현황 (제4장 4.3절 · 제16장 16.1절) |
| 369 | text | 내부암호 | SECTION | `4.3절` | …강의 · 도서 SKU) 1계층 매핑 현황 (제4장 4.3절 · 제16장 16.1절) |
| 369 | text | 내부암호 | SECTION | `16.1절` | … 1계층 매핑 현황 (제4장 4.3절 · 제16장 16.1절) |
| 381 | text | 내부암호 | SNAKE_ID | `contract_id` | contract_id |
| 391 | text | 내부암호 | SNAKE_ID | `contract_id` | 적용 계약 (contract_id) |
| 405 | text | 내부암호 | PIPELINE | `Pipeline 1.1` | 정상 인입 (Pipeline 1.1) |
| 414 | text | 내부암호 | PIPELINE | `Pipeline 2.1` | 정상 인입 (Pipeline 2.1) |
| 419 | text | 내부암호 | SNAKE_YN | `own_copyright_yn` | own_copyright_yn=true |
| 420 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | (자사 100% + 정종대 지원금 Pipeline 5.1 모수 인입) |
| 703 | text | 내부암호 | SECTION | `15.1절` | …랫폼사 100% 부담 (권리자 정산 차감 없음 · 15.1절) |
| 704 | text | 내부암호 | CODE_C | `C-01` | …ne 5.1) 4단계 비례차감 + 5단계 한도복원(C-01) |
| 704 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | 옵션 B · 매출연동 개발지원금(Pipeline 5.1) 4단계 비례차감 + 5단계 한도복원(C-01) |
| 705 | text | 내부암호 | PIPELINE | `Pipeline 1.1` | 옵션 C · 온라인 강좌 R/S(Pipeline 1.1) 4단계 차감 (MMG 적용월 이중부담 회피) |
| 824 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | 매출연동(Pipeline 5.1) · 정액 |
| 913 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | … 자사 지분을 넘을 수 없습니다. 매출연동 지원금(Pipeline 5.1)은 월 최저보장(MMG) 판정 모수에서 제외하되,… |
| 939 | text | 내부암호 | PIPELINE | `Pipeline 1.1` | 온라인 강좌 수익배분(Pipeline 1.1) |
| 946 | text | 내부암호 | SNAKE_ID | `agreement_id` | BASIC은 agreement_id = NULL입니다. 마감 구간은 잠금 상태로 보존… |
| 982 | text | 내부암호 | PIPELINE | `Pipeline 2.1` | 자사 발행 도서 인세(Pipeline 2.1) |
| 1066 | text | 내부암호 | PIPELINE | `Pipeline 2.2` | 위탁 도서 판매대금 정산(Pipeline 2.2) |
| 2847 | text | 내부암호 | CHAPTER | `제1장` | … 이상 발생 시 기존 요율 라인 직접 수정 차단 (제1장 스냅샷 보존 원칙): |
| 2851 | text | 내부암호 | CHAPTER | `제5장` | … 해지(TERMINATED) 전환 시 연쇄 통제 (제5장 5.4절 · 통합설계서 Set 2): |
| 2851 | text | 내부암호 | SECTION | `5.4절` | …TERMINATED) 전환 시 연쇄 통제 (제5장 5.4절 · 통합설계서 Set 2): |
| 2858 | text | 내부암호 | SECTION | `1.3절` | ※ 정본 근거: 제1권 1.3절 · 5.4절 · 통합 상세 설계서 3.2.2절 |
| 2858 | text | 내부암호 | SECTION | `5.4절` | ※ 정본 근거: 제1권 1.3절 · 5.4절 · 통합 상세 설계서 3.2.2절 |
| 2858 | text | 내부암호 | SECTION | `3.2.2절` | …제1권 1.3절 · 5.4절 · 통합 상세 설계서 3.2.2절 |

### `ADMN-INST-002_baseline.html` — 8건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 479 | text | 내부암호 | SECTION | `7.2절` | 📌 [7.2절 단일 책임 원칙 및 검수 범위] |
| 490 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | 7단계 이관 + Pipeline 5.1 약정 |
| 517 | text | 내부암호 | SECTION | `5.2절` | … · 종료 일시정산(LUMP_SETTLE) 규격 (5.2절) |
| 577 | text | 내부암호 | SECTION | `5.2절` | …정산(LUMP_SETTLE, 7단계) 연동 현황 (5.2절) |
| 590 | text | 내부암호 | SECTION | `5.2절` | 산출 기준 및 수식 (5.2절 · 8.3절 정본) |
| 590 | text | 내부암호 | SECTION | `8.3절` | 산출 기준 및 수식 (5.2절 · 8.3절 정본) |
| 624 | text | 내부암호 | SECTION | `5.2절` | * 5.2절 원칙: 위약금은 기 지급 소득의 정정이 아닌 신규… |
| 665 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | + Pipeline 5.1 매출연동 약정 |

### `ADMN-ORD-001_baseline.html` — 10건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 558 | text | 내부암호 | SECTION | `8.2절` | … 연동 파이프라인 (SET3-5 · 합의서 8.1~8.2절) |
| 621 | text | 내부암호 | SECTION | `8.2절` | 8.2절 · 24시간 기한 |
| 627 | text | 내부암호 | SECTION | `5.5절` | 5.5절 우편번호 판정 |
| 1087 | text | 내부암호 | SECTION | `6.1절` | 합의서 6.1절 · 8.1절 · 도서정가제 안분 공식 적용 |
| 1087 | text | 내부암호 | SECTION | `8.1절` | 합의서 6.1절 · 8.1절 · 도서정가제 안분 공식 적용 |
| 1115 | text | 내부암호 | PIPELINE | `Pipeline 1.1` | Pipeline 1.1 온라인 RS |
| 1132 | text | 내부암호 | PIPELINE | `Pipeline 2.1` | Pipeline 2.1 도서 인세 (+1권) |
| 1144 | text | 내부암호 | SECTION | `6.1절` | 도서정가제 & 정산 스냅샷 규칙 (합의서 6.1절 · 8.1절): |
| 1144 | text | 내부암호 | SECTION | `8.1절` | …정가제 & 정산 스냅샷 규칙 (합의서 6.1절 · 8.1절): |
| 1699 | text | 내부암호 | PIPELINE | `Pipeline 1.1` | )으로 확정되므로 정산 파이프라인(Pipeline 1.1)에서 강사 정산 기준금(정산 모수) 또한 0원으로… |

### `ADMN-PROD-002_baseline.html` — 2건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 558 | text | 내부암호 | SECTION | `4.2절` | ⚖️ 정산 1계층 권리자 매핑 안내 (합의서 4.2절 · 16.1절): |
| 558 | text | 내부암호 | SECTION | `16.1절` | …산 1계층 권리자 매핑 안내 (합의서 4.2절 · 16.1절): |

### `ADMN-PROD-003_baseline.html` — 1건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 1252 | text | 금지어 | BAN_80PCT | `80%` | …제공 3. 환급반 진도 기준: 각 차시별 러닝타임 80% 이상 재생 시 출석/진도 인정 |

### `ADMN-PROD-007_baseline.html` — 7건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 336 | text | 내부암호 | PIPELINE | `Pipeline 2.3` | …스터 (공급 형태 · 재고 · 일반 상품 판매매출 Pipeline 2.3) |
| 356 | text | 내부암호 | CHAPTER | `제18장` | 일반 상품 정산 · 세무 · 회계 규칙 (합의서 제18장 18.1절): |
| 356 | text | 내부암호 | SECTION | `18.1절` | …품 정산 · 세무 · 회계 규칙 (합의서 제18장 18.1절): |
| 358 | text | 내부암호 | PIPELINE | `Pipeline 2.3` | Pipeline 2.3 |
| 360 | text | 내부암호 | PIPELINE | `Pipeline 2.3` | TX-13 과세 · Pipeline 2.3 |
| 386 | text | 내부암호 | PIPELINE | `Pipeline 2.3` | Pipeline 2.3 |
| 540 | text | 내부암호 | PIPELINE | `Pipeline 2.3` | 일반 상품 판매매출(Pipeline 2.3) |

### `ADMN-PROM-002_baseline.html` — 1건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 932 | text | 내부암호 | SECTION | `8.1절` | 8.1절 연동 |

### `ADMN-RFD-002_baseline.html` — 7건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 673 | text | 금지어 | BAN_CIRCLED | `①` | ① 합격증 사본 이미지, ② 플랫폼 및 산준모 카페 … |
| 673 | text | 금지어 | BAN_CIRCLED | `②` | ① 합격증 사본 이미지, ② 플랫폼 및 산준모 카페 등록 합격수기 아웃링크 작… |
| 673 | text | 금지어 | BAN_CIRCLED | `③` | …폼 및 산준모 카페 등록 합격수기 아웃링크 작성, ③ 환급금 입금용 통장 사본, ④ 시중 1금융권 은행… |
| 673 | text | 금지어 | BAN_CIRCLED | `④` | …기 아웃링크 작성, ③ 환급금 입금용 통장 사본, ④ 시중 1금융권 은행명 및 실명 계좌번호 입력 수집… |
| 675 | text | 내부암호 | CODE_C | `C-01` | ADMN-SETT-006 C-01 |
| 785 | text | 내부암호 | SNAKE_ID | `order_item_id` | order_item_id |
| 1299 | text | 내부암호 | CODE_C | `C-01` | ADMN-SETT-006 C-01 |

### `ADMN-SETT-001_baseline.html` — 6건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 270 | text | 내부암호 | SECTION | `4.2절` | …핑 미완료')은 신규 결제·판매가 자동 차단됩니다(4.2절). 행 또는 |
| 280 | text | 내부암호 | PIPELINE | `Pipeline 1.1` | 온라인 강좌 (Pipeline 1.1) |
| 281 | text | 내부암호 | PIPELINE | `Pipeline 2.1` | 실물 도서 SKU (Pipeline 2.1 / 5.1) |
| 296 | @placeholder | 금지어 | BAN_GICHUL | `기출` | 예: 기출, CRS-1003, 정종대, PROD-BK... |
| 355 | text | 내부암호 | SECTION | `4.3절` | …분할하여 공백이나 100% 미달 구간을 탐지합니다(4.3절). |
| 362 | text | 내부암호 | SECTION | `16.1절` | 로 트랜잭션 저장합니다(16.1절). 모든 활성 기… |

### `ADMN-SETT-002_baseline.html` — 51건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 983 | text | 내부암호 | SECTION | `8.3절` | 🚀 [8.3절 SSOT] 통합 순방향 연산 엔진 (1~11단계)… |
| 985 | text | 내부암호 | CHAPTER | `제13장` | …림(Floor) 및 마지막 수취인 총액 역산 원칙(제13장)을 준수하며, 마감 확정 전 재실행 시 기존 당월… |
| 1057 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | 2. 개발지원금(Pipeline 5.1) 소진 원장 (확정·한도소진·실지급 3분리 · 5… |
| 1057 | text | 내부암호 | SECTION | `5.2절` | …1) 소진 원장 (확정·한도소진·실지급 3분리 · 5.2절) |
| 1059 | text | 내부암호 | SECTION | `7.2절` | … 대량이체 추출 및 은행 결과 파일 1:1 대사 (7.2절) |
| 1075 | text | 내부암호 | PIPELINE | `Pipeline 1.1` | 온라인 강좌 수익배분 (Pipeline 1.1) |
| 1076 | text | 내부암호 | PIPELINE | `Pipeline 2.1` | 자사 발행 도서 인세 (Pipeline 2.1) |
| 1077 | text | 내부암호 | PIPELINE | `Pipeline 2.2` | 위탁 도서 판매대금 정산 (Pipeline 2.2) |
| 1078 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | 매출연동 개발지원금 (Pipeline 5.1) |
| 1103 | text | 내부암호 | SECTION | `6.5절` | 통합 정산서 상세 (6.5절 · 8.3절) |
| 1103 | text | 내부암호 | SECTION | `8.3절` | 통합 정산서 상세 (6.5절 · 8.3절) |
| 1121 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | 매출연동 개발지원금(Pipeline 5.1) 소진 원장 — 확정·환불 순누계 / 한도 소진액… |
| 1121 | text | 내부암호 | SECTION | `5.2절` | …누계 / 한도 소진액 / 실제 송금 누계 3분리 (5.2절 · 8.3절 5단계) |
| 1121 | text | 내부암호 | SECTION | `8.3절` | … 소진액 / 실제 송금 누계 3분리 (5.2절 · 8.3절 5단계) |
| 1137 | text | 금지어 | BAN_CIRCLED | `①` | ① 확정·환불 순누계 |
| 1138 | text | 금지어 | BAN_CIRCLED | `②` | ② 한도 소진액 누계 |
| 1139 | text | 금지어 | BAN_CIRCLED | `③` | ③ 실제 현금송금 누계 |
| 1192 | text | 내부암호 | CHAPTER | `제12장` | … 면세 계산서 수취 추적 게이트웨이 (6.5절 · 제12장) |
| 1192 | text | 내부암호 | SECTION | `6.5절` | …발행 및 위탁 면세 계산서 수취 추적 게이트웨이 (6.5절 · 제12장) |
| 1236 | text | 금지어 | BAN_CIRCLED | `①` | ① [수취] 도서 판매대금 면세 계산서 |
| 1236 | text | 금지어 | BAN_CIRCLED | `②` | ② [당사 발행] 위탁 수수료 과세 세금계산서 |
| 1255 | text | 내부암호 | CODE_D | `D-13` | …결과 파일 1:1 식별자 매핑 (7.2절 · QA D-13) |
| 1255 | text | 내부암호 | SECTION | `7.2절` | … 리스트 및 은행 결과 파일 1:1 식별자 매핑 (7.2절 · QA D-13) |
| 1261 | text | 내부암호 | CODE_D | `D-13` | 🧪 [QA D-13 시연] 은행 계좌오류 송금 실패 시뮬레이션 |
| 1273 | text | 내부암호 | SECTION | `7.2절` | 원천징수·상계 사건 기록 (7.2절) |
| 1307 | text | 내부암호 | SECTION | `16.1절` | 16.1절 · 7.4절 필수 규격 |
| 1307 | text | 내부암호 | SECTION | `7.4절` | 16.1절 · 7.4절 필수 규격 |
| 1344 | text | 내부암호 | SECTION | `7.4절` | (7.4절) |
| 1372 | text | 내부암호 | SECTION | `7.4절` | 7.4절 carryover_ledger |
| 1914 | text | 내부암호 | SECTION | `7.4절` | \| 이월 원장(carryover_ledger) 7.4절 마감 연속성 검증 |
| 1935 | text | 내부암호 | PIPELINE | `Pipeline 2.2` | 한국소방학회 (PY-0031 · 위탁 도서 Pipeline 2.2) |
| 1955 | text | 금지어 | BAN_CIRCLED | `①` | ① 전기말 기초 이월 잔액 (Opening) |
| 1960 | text | 금지어 | BAN_CIRCLED | `②` | ② 당월 정산 합산/상쇄 해소로 인한 원장 변동 |
| 1965 | text | 금지어 | BAN_CIRCLED | `③` | ③ 당월 신규 차월이월 적재액 (New Carry-O… |
| 1970 | text | 금지어 | BAN_CIRCLED | `④` | ④ 당기말 차월 이월 잔액 (Closing) |
| 1972 | text | 내부암호 | SECTION | `7.4절` | 7.4절 연속성 등식: ① + ② + ③ = ④ (100%… |
| 1972 | text | 금지어 | BAN_CIRCLED | `①` | 7.4절 연속성 등식: ① + ② + ③ = ④ (100% 일치) |
| 1972 | text | 금지어 | BAN_CIRCLED | `②` | 7.4절 연속성 등식: ① + ② + ③ = ④ (100% 일치) |
| 1972 | text | 금지어 | BAN_CIRCLED | `③` | 7.4절 연속성 등식: ① + ② + ③ = ④ (100% 일치) |
| 1972 | text | 금지어 | BAN_CIRCLED | `④` | 7.4절 연속성 등식: ① + ② + ③ = ④ (100% 일치) |
| 1995 | text | 내부암호 | SECTION | `7.3절` | ※ 정본 근거: 제1권 7.3절(최소 지급/청구 하한) · 7.4절(이월 원장 마… |
| 1995 | text | 내부암호 | SECTION | `7.4절` | …근거: 제1권 7.3절(최소 지급/청구 하한) · 7.4절(이월 원장 마감 연속성 등식) · 제2권 8.3절… |
| 1995 | text | 내부암호 | SECTION | `8.3절` | …7.4절(이월 원장 마감 연속성 등식) · 제2권 8.3절 1단계(CARRY_IN) 및 11단계(PAYOUT… |
| 2024 | text | 내부암호 | PIPELINE | `Pipeline 2.2` | 한국소방학회 (PY-0031 · 위탁 도서 Pipeline 2.2) |
| 2056 | text | 내부암호 | CHAPTER | `제6장` | 📊 제6장 6.5절 통합 정산 요약 및 과세표준 vs 실지급… |
| 2056 | text | 내부암호 | SECTION | `6.5절` | 📊 제6장 6.5절 통합 정산 요약 및 과세표준 vs 실지급액 대조 … |
| 2057 | text | 내부암호 | CHAPTER | `제13장` | …,4) 유지 후 라인 합산 1회 Floor 절사 (제13장) |
| 2069 | text | 내부암호 | CHAPTER | `제8장` | ⚙️ 제8장 8.3절 1~11단계 정산 연산 워터폴 및 세액·… |
| 2069 | text | 내부암호 | SECTION | `8.3절` | ⚙️ 제8장 8.3절 1~11단계 정산 연산 워터폴 및 세액·상계 산식… |
| 2093 | text | 내부암호 | CHAPTER | `제9장` | 제9장 · 제11장 매트릭스 |
| 2093 | text | 내부암호 | CHAPTER | `제11장` | 제9장 · 제11장 매트릭스 |

### `ADMN-SETT-004_baseline.html` — 12건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 542 | text | 내부암호 | CHAPTER | `제8장` | 📌 [제8장 8.2절 · 통합설계서 표 5.1-A 토스페이먼츠… |
| 542 | text | 내부암호 | SECTION | `8.2절` | 📌 [제8장 8.2절 · 통합설계서 표 5.1-A 토스페이먼츠 5대 결… |
| 580 | text | 내부암호 | SECTION | `8.1절` | … 3계층 과·면세 분할 및 도서정가제 안분 검증 (8.1절) |
| 581 | text | 내부암호 | SECTION | `8.2절` | …. 가상계좌 · 실시간 계좌이체 복구 시차 점검 (8.2절) |
| 647 | text | 내부암호 | SECTION | `8.1절` | …층 과·면세 분할 승인 및 도서정가제 안분 대사 (8.1절) |
| 647 | text | 내부암호 | SNAKE_ID | `order_item_id` | 주문 품목(order_item_id) 단위 3계층 과·면세 분할 승인 및 도서정가제 … |
| 658 | text | 내부암호 | SNAKE_ID | `order_item_id` | 주문번호 / 품목 ID (order_item_id) |
| 679 | text | 내부암호 | PIPELINE | `Pipeline 1.1` | Pipeline 1.1 (정종대 외) |
| 690 | text | 내부암호 | PIPELINE | `Pipeline 1.1` | Pipeline 1.1 (정종대) |
| 701 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | 인세 Bypass → Pipeline 5.1 모수 |
| 712 | text | 내부암호 | PIPELINE | `Pipeline 2.3` | Pipeline 2.3 (자사 매출 전용) |
| 736 | text | 내부암호 | SECTION | `8.2절` | …금 대기 스냅샷 및 월말/월초 귀속월 분리 대사 (8.2절) |

### `ADMN-SETT-005_baseline.html` — 10건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 497 | text | 내부암호 | CHAPTER | `제10장` | 📌 [UX 진입 경로 및 마감 불변성 원칙 (제10장)] |
| 498 | text | 금지어 | BAN_CIRCLED | `①` | ① |
| 498 | text | 금지어 | BAN_CIRCLED | `②` | 으로 진입하면 해당 정산서가 자동 바인딩되며, ② 우측 상단 |
| 536 | text | 내부암호 | SECTION | `10.4절` | 2. [10.4절] 4채널 증빙 정정 분기 및 원천세 수정신고(채널… |
| 572 | text | 내부암호 | SECTION | `10.3절` | 승인 단계 (10.3절) |
| 597 | text | 내부암호 | SECTION | `10.4절` | [10.4절 정본] 수동 조정에 따른 4채널 증빙·원천세 정정… |
| 635 | text | 내부암호 | SECTION | `10.4절` | 10.4절 도서 공급형태 오등록 규칙: 기지급·신고 없으므로… |
| 701 | text | 내부암호 | SNAKE_ID | `origin_settlement_id` | origin_settlement_id |
| 709 | text | 내부암호 | SNAKE_ID | `origin_settlement_id` | 참조 원 정산서 선택 (origin_settlement_id · 필수) |
| 729 | text | 내부암호 | SECTION | `10.2절` | 조정 사유 구분 (adj_reason_code · 10.2절 표준 13종) |

### `ADMN-SETT-007_baseline.html` — 24건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 333 | text | 내부암호 | CODE_D | `D-1` | 16.1절 · D-1 |
| 333 | text | 내부암호 | SECTION | `16.1절` | 16.1절 · D-1 |
| 338 | text | 내부암호 | SECTION | `5.3절` | 5.3절 하드락 |
| 361 | text | 내부암호 | SECTION | `5.3절` | 🚨 선급금 미종결로 분할 차단된 계약 (5.3절) |
| 376 | text | 내부암호 | SECTION | `5.3절` | 선급금 원장 상태 (5.3절 상호차단) |
| 410 | text | 내부암호 | CHAPTER | `제4장` | 1) 정산 항목별 2계층 수취인 분할 적용 여부 (제4장 4.1절 · 제8장 8.3절 8단계) |
| 410 | text | 내부암호 | CHAPTER | `제8장` | …계층 수취인 분할 적용 여부 (제4장 4.1절 · 제8장 8.3절 8단계) |
| 410 | text | 내부암호 | SECTION | `4.1절` | …산 항목별 2계층 수취인 분할 적용 여부 (제4장 4.1절 · 제8장 8.3절 8단계) |
| 410 | text | 내부암호 | SECTION | `8.3절` | …취인 분할 적용 여부 (제4장 4.1절 · 제8장 8.3절 8단계) |
| 424 | text | 내부암호 | SNAKE_ID | `payee_id` | payee_id |
| 425 | text | 내부암호 | CODE_D | `D-1` | Case 7 / D-1 / D-2 |
| 425 | text | 내부암호 | CODE_D | `D-2` | Case 7 / D-1 / D-2 |
| 428 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | 5단계 확정 매출연동 개발지원금 (Pipeline 5.1) 및 7단계 비정기 가산금 |
| 431 | text | 내부암호 | SECTION | `4.1절` | 4.1절 / 13.1절 |
| 431 | text | 내부암호 | SECTION | `13.1절` | 4.1절 / 13.1절 |
| 437 | text | 내부암호 | SECTION | `5.3절` | 5.3절 상호 차단 |
| 443 | text | 내부암호 | CODE_D | `D-3` | 부록 D-3 / Case 3-B |
| 489 | text | 내부암호 | SECTION | `4.1절` | [계약 선택 안내 (4.1절 · 5.3절)] |
| 489 | text | 내부암호 | SECTION | `5.3절` | [계약 선택 안내 (4.1절 · 5.3절)] |
| 489 | text | 내부암호 | SECTION | `5.3절` | 미상계 선급금 잔액이 남아 있는 계약(5.3절) |
| 505 | text | 내부암호 | SECTION | `5.3절` | 선급금 잔액 (5.3절) |
| 525 | text | 내부암호 | SECTION | `4.1절` | …취인 선택 모달 (계약 합의 당사자 일치 원칙 · 4.1절) |
| 530 | text | 내부암호 | CHAPTER | `제4장` | [제4장 4.1절 계약 합의 당사자 일치 원칙] |
| 530 | text | 내부암호 | SECTION | `4.1절` | [제4장 4.1절 계약 합의 당사자 일치 원칙] |

### `ADMN-SETT-008_baseline.html` — 13건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 469 | text | 내부암호 | CHAPTER | `제17장` | 📌 [제17장 국세청 오픈API 연동 및 선관주의 보존 원칙] |
| 471 | text | 내부암호 | SECTION | `7.3절` | …인더를 중단하고 미지급 정산금을 강제 정산 트리거(7.3절)로 이관 |
| 508 | text | 내부암호 | SECTION | `17.3절` | …무 매트릭스(TX-05~TX-11) 매핑 설정표 (17.3절) |
| 509 | text | 내부암호 | SECTION | `17.6절` | …트워크 장애 재시도 큐 및 배치 스케줄 파라미터 (17.6절 · 부록 B) |
| 569 | text | 내부암호 | SECTION | `17.3절` | …cd) ↔ 세무 판정 매트릭스 자동 매핑 설정표 (17.3절 · 읽기 전용) |
| 574 | text | 내부암호 | SECTION | `17.1절` | 수기 과세유형 선택 금지 (17.1절) |
| 584 | text | 내부암호 | SECTION | `17.3절` | 자동 연결 매트릭스 케이스 및 예외 규칙 (17.3절 정본) |
| 641 | text | 내부암호 | SECTION | `17.6절` | … 파라미터(부록 B) 및 지수 백오프 재시도 큐 (17.6절) |
| 654 | text | 내부암호 | SECTION | `17.5절` | 운영 통제 규칙 (17.5절 · 17.6절 · 부록 B) |
| 654 | text | 내부암호 | SECTION | `17.6절` | 운영 통제 규칙 (17.5절 · 17.6절 · 부록 B) |
| 1220 | text | 내부암호 | SECTION | `17.5절` | 17.5절 하드락 |
| 1231 | text | 내부암호 | SECTION | `17.5절` | ⚠️ 17.5절 하드락 규칙: |
| 1272 | text | 내부암호 | SECTION | `17.5절` | ✔ 17.5절 행 분할 승인 및 PENDING_REVIEW 해제… |

### `ADMN-SETT-009_baseline.html` — 56건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 297 | text | 내부암호 | SECTION | `18.4절` | … 🔒 [권한 분리 및 외부 유출 차단 원칙 (18.4절 · 5.2절 · Case 11·12)] … |
| 297 | text | 내부암호 | SECTION | `5.2절` | …한 분리 및 외부 유출 차단 원칙 (18.4절 · 5.2절 · Case 11·12)] |
| 300 | text | 내부암호 | PIPELINE | `Pipeline 2.3` | 일반 상품 판매매출(Pipeline 2.3, |
| 300 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | 되며, 매출연동 개발지원금(Pipeline 5.1) 확정액은 외부 공동권리자 지분을 침해하지 않고 |
| 318 | text | 내부암호 | CODE_P | `P1.1` | P1.1 수익배분 + P2.1 인세 + P2.2 위탁 + … |
| 318 | text | 내부암호 | CODE_P | `P2.1` | P1.1 수익배분 + P2.1 인세 + P2.2 위탁 + P5.1 지원금 |
| 318 | text | 내부암호 | CODE_P | `P2.2` | P1.1 수익배분 + P2.1 인세 + P2.2 위탁 + P5.1 지원금 |
| 318 | text | 내부암호 | CODE_P | `P5.1` | … 수익배분 + P2.1 인세 + P2.2 위탁 + P5.1 지원금 |
| 321 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | Pipeline 5.1 |
| 326 | text | 내부암호 | PIPELINE | `Pipeline 2.3` | 일반 소비재 매출 (Pipeline 2.3) |
| 340 | text | 내부암호 | SECTION | `18.4절` | … 파이프라인별 전사 손익 · 권리자/자사 대조표 (18.4절) |
| 341 | text | 내부암호 | CODE_D | `D-15` | …Pipeline 5.1) 차감 검증 (5.2절 · D-15·16) |
| 341 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | 2. 자사 지분 내 개발지원금(Pipeline 5.1) 차감 검증 (5.2절 · D-15·16) |
| 341 | text | 내부암호 | SECTION | `5.2절` | … 개발지원금(Pipeline 5.1) 차감 검증 (5.2절 · D-15·16) |
| 342 | text | 내부암호 | PIPELINE | `Pipeline 2.3` | 3. 일반 소비재(Pipeline 2.3) 및 비인입 도서(Case 11·12) 명세 |
| 343 | text | 내부암호 | CHAPTER | `제14장` | 4. 월별·연간 세무 신고 기초 산출물 센터 (제14장 14.1절) |
| 343 | text | 내부암호 | SECTION | `14.1절` | …월별·연간 세무 신고 기초 산출물 센터 (제14장 14.1절) |
| 352 | text | 내부암호 | PIPELINE | `Pipeline 1.1` | 온라인 강좌 수익배분 (Pipeline 1.1) |
| 353 | text | 내부암호 | PIPELINE | `Pipeline 2.1` | 자사 발행 도서 인세 및 자사저작권 (Pipeline 2.1) |
| 354 | text | 내부암호 | PIPELINE | `Pipeline 2.2` | 위탁 도서 판매대금 정산 (Pipeline 2.2) |
| 355 | text | 내부암호 | PIPELINE | `Pipeline 2.3` | 일반 상품 판매매출 (Pipeline 2.3 · 소비재) |
| 356 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | 매출연동 개발지원금 (Pipeline 5.1) |
| 362 | text | 내부암호 | CHAPTER | `제13장` | …(Floor) 및 마지막 수취인 총액 역산 적용 (제13장) |
| 370 | text | 내부암호 | PIPELINE | `Pipeline` | 정산 입력 구분 (Pipeline) |
| 376 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | (Pipeline 5.1 · 자사부담) |
| 390 | text | 내부암호 | CODE_D | `D-15` | … 내 차감 및 잔여 귀속 대사 (5.2절 · 부록 D-15 · D-16) |
| 390 | text | 내부암호 | CODE_D | `D-16` | … 잔여 귀속 대사 (5.2절 · 부록 D-15 · D-16) |
| 390 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | 🛡️ 개발지원금(Pipeline 5.1) 자사 지분('RH-INTERNAL') 내 차감 … |
| 390 | text | 내부암호 | SECTION | `5.2절` | …INTERNAL') 내 차감 및 잔여 귀속 대사 (5.2절 · 부록 D-15 · D-16) |
| 397 | text | 내부암호 | CODE_D | `D-15` | … 📌 [규격 검증 1] 부록 D-15 · 자사 저작권 도서('own_copyright_… |
| 397 | text | 내부암호 | SNAKE_YN | `own_copyright_yn` | … 검증 1] 부록 D-15 · 자사 저작권 도서('own_copyright_yn = true') 외부 강사 지원금 차감 … |
| 400 | text | 내부암호 | PIPELINE | `Pipeline 2.1` | ) 100.00%로 매핑됩니다. 인세(Pipeline 2.1) 외부 지급은 0원으로 Bypass하되, 약정된 … |
| 407 | text | 내부암호 | PIPELINE | `Pipeline 2.1` | 외부 저자 인세 (Pipeline 2.1 · |
| 407 | text | 내부암호 | SNAKE_YN | `own_copyright_yn` | own_copyright_yn = true |
| 411 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | 정종대 개발지원금 차감 (Pipeline 5.1 · 요율 15%) |
| 422 | text | 내부암호 | CODE_D | `D-16` | … 📌 [규격 검증 2] 부록 D-16 · 공동권리 강좌에서 제3자(기여자) 지원금 차감… |
| 436 | text | 내부암호 | PIPELINE | `Pipeline 5.1` | 기여자 최그래픽 지원금 차감 (Pipeline 5.1 · 기준금 × 5% · 지분율 미곱) |
| 457 | text | 내부암호 | SECTION | `5.2절` | 재원 충족 판정 (5.2절) |
| 465 | text | 내부암호 | PIPELINE | `Pipeline 2.1` | Pipeline 2.1 모수 |
| 476 | text | 내부암호 | PIPELINE | `Pipeline 1.1` | Pipeline 1.1 모수 |
| 491 | text | 내부암호 | PIPELINE | `Pipeline 2.3` | 📦 일반 상품 판매매출(Pipeline 2.3 · TX-13) 및 매입 재판매 도서(Case 1… |
| 492 | text | 내부암호 | CHAPTER | `제18장` | 제18장 18.1~18.4절 · Case 11 · Case… |
| 492 | text | 내부암호 | SECTION | `18.4절` | 제18장 18.1~18.4절 · Case 11 · Case 12 정합 |
| 496 | text | 내부암호 | PIPELINE | `Pipeline 2.3` | 는 일반 상품 판매매출(Pipeline 2.3)로 인입하여 1단계 상위 공식에서 |
| 516 | text | 내부암호 | PIPELINE | `Pipeline 2.3` | 일반 상품 판매매출 (Pipeline 2.3) |
| 528 | text | 내부암호 | PIPELINE | `Pipeline 2.3` | 일반 상품 판매매출 (Pipeline 2.3) |
| 537 | text | 내부암호 | CODE_P | `P2.3` | 승인월 P2.3 차감 반영 |
| 571 | text | 내부암호 | CHAPTER | `제14장` | …및 부가가치세 신고 기초 산출물 자동 추출 센터 (제14장 14.1절) |
| 571 | text | 내부암호 | SECTION | `14.1절` | …치세 신고 기초 산출물 자동 추출 센터 (제14장 14.1절) |
| 578 | text | 내부암호 | CHAPTER | `제14장` | 산출물 명칭 (제14장 14.1절 규격) |
| 578 | text | 내부암호 | SECTION | `14.1절` | 산출물 명칭 (제14장 14.1절 규격) |
| 616 | text | 내부암호 | SNAKE_ID | `order_item_id` | order_item_id |
| 616 | text | 금지어 | BAN_CIRCLED | `①` | ) 기준 ① 교육용역 면세(제26조 제1항 제6호), ② 도서… |
| 616 | text | 금지어 | BAN_CIRCLED | `②` | …기준 ① 교육용역 면세(제26조 제1항 제6호), ② 도서 재화 면세(제26조 제1항 제8호), ③ 저… |
| 616 | text | 금지어 | BAN_CIRCLED | `③` | …, ② 도서 재화 면세(제26조 제1항 제8호), ③ 저작권 인적용역 면세(제15호 계통, 정산 라인 … |
| 618 | text | 내부암호 | CODE_P | `P2.3` | …00원 / 도서면세 17,180,000원 / 과세(P2.3) 3,300,000원 |

### `ADMN-USER-001_baseline.html` — 1건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 1415 | text | 내부암호 | SNAKE_ID | `cafe_member_id` | users.cafe_member_id IS NOT NULL |

### `ADMN-USER-007_baseline.html` — 20건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 306 | text | 내부암호 | CHAPTER | `제3장` | 제3장 3.2절 |
| 306 | text | 내부암호 | SECTION | `3.2절` | 제3장 3.2절 |
| 330 | text | 내부암호 | SECTION | `3.4절` | …정보 마스킹 열람 및 증빙 사본 통제 (3.1 ~ 3.4절) |
| 331 | text | 내부암호 | SECTION | `3.5절` | …한 3계층 분리 및 개인정보 필드 파기 스케줄러 (3.5절) |
| 342 | text | 내부암호 | SECTION | `3.1절` | 법인/개인사업자 (주민등록번호 수집 금지 · 3.1절) |
| 355 | text | 내부암호 | SECTION | `3.1절` | 주체 유형 및 수집 근거 (3.1절) |
| 358 | text | 내부암호 | SECTION | `3.3절` | 프라이빗 S3 증빙 사본 (3.3절) |
| 370 | text | 내부암호 | CHAPTER | `제3장` | … 분리 및 개인정보 필드 분리 파기 워크스페이스 (제3장 3.5절) |
| 370 | text | 내부암호 | SECTION | `3.5절` | …및 개인정보 필드 분리 파기 워크스페이스 (제3장 3.5절) |
| 375 | text | 내부암호 | SECTION | `3.5절` | 📌 [3.5절 파기와 보존의 충돌 해소 원칙] |
| 376 | text | 내부암호 | SNAKE_ID | `rights_holder_id` | rights_holder_id |
| 401 | text | 내부암호 | SECTION | `3.5절` | 코드 수정 없는 테이블 기반 통제 (3.5절) |
| 411 | text | 내부암호 | SECTION | `3.5절` | 계층 1 만료 시 처리 방식 (3.5절) |
| 421 | text | 내부암호 | SNAKE_ID | `rights_holder_id` | rights_holder_id |
| 494 | text | 내부암호 | CHAPTER | `제3장` | …-007] 민감 정보 열람 사유 입력 통제 팝업 (제3장 3.4절) |
| 494 | text | 내부암호 | SECTION | `3.4절` | …] 민감 정보 열람 사유 입력 통제 팝업 (제3장 3.4절) |
| 539 | text | 내부암호 | SECTION | `3.3절` | … 뷰어 (Presigned URL 임시 렌더링 · 3.3절) |
| 554 | text | 내부암호 | SECTION | `3.5절` | … 3계층 필드 분리 파기 배치 실행 결과 보고서 (3.5절) |
| 572 | text | 내부암호 | SECTION | `3.5절` | ⚖️ 3계층 데이터 분리 파기 대조표 (기획서 3.5절 · 개인정보보호법 제21조 & 상법 제33조) |
| 610 | text | 내부암호 | SNAKE_ID | `settlement_recipient_id` | settlement_recipient_id |

## 4. [B] JS 동적 렌더링 후보 상세

### `ADMN-BOOK-001_baseline.html` — 8건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 1453 | js-string | 금지어 | BAN_GICHUL | `기출` | 2026 산업안전기사 필기 10개년 과년도 기출해설집 |
| 1472 | js-string | 금지어 | BAN_GICHUL | `기출` | 2026 건설안전기사 필기 핵심이론 + 과년도 기출 |
| 1601 | js-string | 금지어 | BAN_CIRCLED | `①` | ① 계약원장 가채번 |
| 1602 | js-string | 금지어 | BAN_CIRCLED | `②` | ② PROD-004 선등록 |
| 1603 | js-string | 금지어 | BAN_CIRCLED | `③` | ③ 공급원장 직결 |
| 1725 | js-string | 금지어 | BAN_CIRCLED | `①` | [경로 ① 선택됨 — 계약원장 가채번(TMP-BK-2601)… |
| 1729 | js-string | 금지어 | BAN_CIRCLED | `②` | [경로 ② 선택됨 — 교재관리(ADMN-PROD-004) 선… |
| 1733 | js-string | 금지어 | BAN_CIRCLED | `③` | [경로 ③ 선택됨 — 도서 공급 원장 최초 신규 SKU 채번… |

### `ADMN-CONF-001_baseline.html` — 1건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 460 | js-string | 내부암호 | CODE_D | `D-15` | 2026 제3회 실기 시험 D-15 파이널 모의고사 특강 |

### `ADMN-CONF-010_baseline.html` — 15건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 549 | js-string | 내부암호 | CODE_D | `D-12` | …LETED → ACTIVE) 및 한도 복원 (부록 D-12) |
| 571 | js-string | 내부암호 | CODE_D | `D-12` | ACTIVE (유효 복귀 · 부록 D-12) |
| 582 | js-string | 내부암호 | SECTION | `7.3절` | …POST_TAX) 이월 계정 간 대체 2차 승인 (7.3절) |
| 611 | js-string | 내부암호 | SECTION | `3.4절` | 민감 정보(주민번호·계좌번호) 마스킹 해제 열람 (3.4절 · TTL 30초) |
| 638 | js-string | 내부암호 | SECTION | `4.3절` | …lecture_instructors) 변경 저장 (4.3절) |
| 666 | js-string | 내부암호 | SECTION | `4.1절` | …취인 분할 지분율(payee_splits) 등록 (4.1절 · Case 7) |
| 696 | js-string | 내부암호 | SECTION | `7.2절` | …금 수기 소명(MANUAL_NOTE) 검수 승인 (7.2절) |
| 724 | js-string | 내부암호 | SECTION | `17.5절` | …과세유형 전환 감지 승인 및 신규 버전 행 추가 (17.5절) |
| 755 | js-string | 내부암호 | SECTION | `5.2절` | … 이행률 정산(PRO_RATA) 수동 조정 승인 (5.2절) |
| 785 | js-string | 내부암호 | SECTION | `3.5절` | …드 분리 파기 및 계층 2 정산원장 비식별 보존 (3.5절) |
| 835 | js-string | 내부암호 | SECTION | `16.1절` | …저작자 지위(payee_is_author) 전환 (16.1절) |
| 858 | js-string | 내부암호 | SECTION | `3.3절` | …resigned URL 발급 열람 (5분 만료 · 3.3절) |
| 877 | js-string | 내부암호 | SECTION | `6.2절` | …= true) 신규 SKU 등록 및 가채번 매칭 (6.2절) |
| 877 | js-string | 내부암호 | SNAKE_YN | `own_copyright_yn` | 자사 저작권 도서(own_copyright_yn = true) 신규 SKU 등록 및 가채번 매칭 … |
| 879 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | …결 및 자사 저작권 100% + 정종대 개발지원금(Pipeline 5.1) 모수 설정 |

### `ADMN-INST-001_baseline.html` — 4건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 1316 | js-string | 내부암호 | SNAKE_YN | `own_copyright_yn` | [자사저작권] 정종대 산업안전 필기 기출문제집 (own_copyright_yn=true) |
| 1316 | js-string | 금지어 | BAN_GICHUL | `기출` | [자사저작권] 정종대 산업안전 필기 기출문제집 (own_copyright_yn=true) |
| 2607 | js-string | 내부암호 | SNAKE_YN | `own_copyright_yn` | [v4.0.0 대표 사례] 자사저작권 도서(own_copyright_yn=true) 매출연동 지원금 15% + 선급금 상계… |
| 2746 | js-string | 내부암호 | PIPELINE | `Pipeline` | … 만료 D-Day 적용 정산 조항 (Pipeline) 세무 판정 · 국세청 … |

### `ADMN-INST-002_baseline.html` — 15건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 727 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | …권 도서+강좌] 정종대 산업안전 필기 개발지원금 (Pipeline 5.1) |
| 801 | js-string | 금지어 | BAN_GICHUL | `기출` | 산업안전 필기 10개년 기출 해설집 집필 지원금 (2/2회차 완강·출간 마일스… |
| 817 | js-string | 금지어 | BAN_GICHUL | `기출` | 2026-10-10 필기 기출 해설 강의 45강 전 차시 런칭 및 LMS 업로드… |
| 984 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | …roved.toLocaleString()}원 + Pipeline 5.1 매출연동 약정 활성화 ${rsApprovedCo… |
| 1025 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | Pipeline 5.1 (R/S 1회) ${item.rateText} |
| 1085 | js-string | 내부암호 | SECTION | `6.4절` | ⚖️ [6.4절 · TX-03 매절(권리 양도) 세무 근거 통제]… |
| 1093 | js-string | 내부암호 | SECTION | `5.2절` | …SHARE) 지원금 약정 체결 1회 필수값 검증 (5.2절 · 7.2절) ${item.t… |
| 1093 | js-string | 내부암호 | SECTION | `7.2절` | …지원금 약정 체결 1회 필수값 검증 (5.2절 · 7.2절) ${item.targetCo… |
| 1130 | js-string | 내부암호 | SECTION | `7.2절` | … 🔒 [7.2절] 마일스톤 검수 승인 3대 필수 게이트 판정 … |
| 1156 | js-string | 내부암호 | SECTION | `7.2절` | … 이원화 검수 방식 선택 (7.2절) … |
| 1291 | js-string | 내부암호 | CHAPTER | `제17장` | 국세청 API 연동(제17장) |
| 1319 | js-string | 내부암호 | SECTION | `7.0절` | [7.0절 마감 상태별 인입 통제]\n선택하신 '${tMon… |
| 1339 | js-string | 내부암호 | SECTION | `7.0절` | [7.0절 마감 상태별 인입 통제]\n선택하신 '${tMon… |
| 1351 | js-string | 내부암호 | SECTION | `7.2절` | [7.2절 담당자 수기 소명형 검수 규칙]\n수기 검수(내부… |
| 1372 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | 매출연동(Pipeline 5.1) 지원금 약정 1회 검수 승인 (${item.ta… |

### `ADMN-PROD-003_baseline.html` — 1건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 1913 | js-string | 내부암호 | SECTION | `4.2절` | 기획서 4.2절 정책에 따라 ADMN-SETT-001의 1계층 지… |

### `ADMN-PROD-005_baseline.html` — 1건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 1883 | js-string | 내부암호 | SECTION | `4.2절` | 기획서 4.2절에 따라 패키지에 포함된 모든 단과 강좌의 ADMN… |

### `ADMN-PROD-007_baseline.html` — 3건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 867 | js-string | 내부암호 | PIPELINE | `Pipeline 2.3` | …Badge} TX-13 · Pipeline 2.3 ${stBadge} … |
| 933 | js-string | 내부암호 | PIPELINE | `Pipeline 2.3` | …스터 (공급 형태 · 재고 · 일반 상품 판매매출 Pipeline 2.3) |
| 1046 | js-string | 내부암호 | PIPELINE | `Pipeline 2.3` | …. (자사 권리자 100% 매핑 · TX-13 · Pipeline 2.3) |

### `ADMN-RFD-002_baseline.html` — 8건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 1922 | js-string | 금지어 | BAN_CIRCLED | `①` | … 대조 및 4대 증빙 미완료 — 승인 잠금] 위 ① 합격증 사본, ② 통장 사본(1금융권 실명계좌),… |
| 1922 | js-string | 금지어 | BAN_CIRCLED | `②` | …빙 미완료 — 승인 잠금] 위 ① 합격증 사본, ② 통장 사본(1금융권 실명계좌), ③ 산준모 카페/… |
| 1922 | js-string | 금지어 | BAN_CIRCLED | `③` | …합격증 사본, ② 통장 사본(1금융권 실명계좌), ③ 산준모 카페/플랫폼 합격수기 아웃링크 확인 체크박… |
| 1972 | js-string | 금지어 | BAN_CIRCLED | `①` | … ① 합격증 사본 이미지 대조 … |
| 1972 | js-string | 금지어 | BAN_CIRCLED | `②` | … ② 환급금 입금용 통장 사본 · 시중 1금융권 실명계… |
| 1972 | js-string | 금지어 | BAN_CIRCLED | `③` | … ③ 플랫폼 및 산준모 카페 등록 합격수기 아웃링크 확… |
| 1972 | js-string | 금지어 | BAN_CIRCLED | `④` | … ④ 환급금 산출 및 정산 분담 연동 명세 … |
| 1972 | js-string | 금지어 | BAN_CIRCLED | `⑤` | … ⑤ 최종 심사 판정 선택 * … |

### `ADMN-SETT-001_baseline.html` — 31건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 458 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | 온라인 강좌 수익배분 (Pipeline 1.1) |
| 470 | js-string | 내부암호 | PIPELINE | `Pipeline 2.1` | 자사 발행 도서 인세 (Pipeline 2.1) |
| 480 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | 온라인 강좌 수익배분 (Pipeline 1.1) |
| 492 | js-string | 금지어 | BAN_GICHUL | `기출` | 정종대 산업안전 실전 기출특강 |
| 493 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | 온라인 강좌 수익배분 (Pipeline 1.1) |
| 497 | js-string | 금지어 | BAN_GICHUL | `기출` | 1강. 기출 핵심 문제풀이 Part 1 |
| 498 | js-string | 금지어 | BAN_GICHUL | `기출` | 2강. 기출 핵심 문제풀이 Part 2 |
| 505 | js-string | 내부암호 | PIPELINE | `Pipeline 2.1` | 자사 발행 도서 인세 (Pipeline 2.1) |
| 514 | js-string | 금지어 | BAN_GICHUL | `기출` | 정종대 산업안전 필기 기출문제집 (자사저작권 보유 도서 · 정종대 지원금 1… |
| 515 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | …_copyright_yn=true) → 개발지원금(Pipeline 5.1) |
| 515 | js-string | 내부암호 | SNAKE_YN | `own_copyright_yn` | 자사 도서(own_copyright_yn=true) → 개발지원금(Pipeline 5.1) |
| 535 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | 위탁 도서 판매대금 정산 (Pipeline 2.2) |
| 604 | js-string | 내부암호 | SNAKE_YN | `own_copyright_yn` | 자사 저작권 보유 도서(own_copyright_yn=true) 자사 100% 자동 매핑 |
| 612 | js-string | 내부암호 | SECTION | `4.2절` | 1계층 권리자 매핑 미완료 상태로 신규 결제 차단(4.2절) |
| 657 | js-string | 내부암호 | CHAPTER | `제6장` | …되며 별도 1계층 인세 지분 매핑 대상이 아닙니다(제6장 6.1절). |
| 657 | js-string | 내부암호 | SECTION | `6.1절` | …도 1계층 인세 지분 매핑 대상이 아닙니다(제6장 6.1절). |
| 660 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | …MENT)는 1계층 인세 지분 매핑 대상이 아니며 Pipeline 2.2로 별도 정산합니다. |
| 674 | js-string | 내부암호 | SNAKE_ID | `contract_id` | ${idx+1}행: 유효 계약(contract_id) 바인딩이 필요합니다. |
| 715 | js-string | 내부암호 | SECTION | `5.2절` | … 지분 0% 구간: 지원금 0원 미발생 예외 적용(5.2절). |
| 739 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | 위탁정산 분리(Pipeline 2.2) |
| 832 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | … 현재 매핑된 권리자 개발지원금(Pipeline 5.1) 판매 게이트 작업 … |
| 943 | js-string | 내부암호 | CODE_D | `D-15` | …ypass되지 않고 지원금 모수로 정상 인입됩니다(D-15·D-16). |
| 943 | js-string | 내부암호 | CODE_D | `D-16` | …되지 않고 지원금 모수로 정상 인입됩니다(D-15·D-16). |
| 943 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | … 수취인( 정종대 강사 )의 매출연동 개발지원금( Pipeline 5.1 , 요율 15%, 상계 허용 CONDITIONA… |
| 943 | js-string | 내부암호 | SNAKE_YN | `own_copyright_yn` | [v4.0.0 자사 저작권 보유 도서 (own_copyright_yn = true)] 저작권이 당사(엘캠퍼스)에 있으… |
| 948 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | …도서는 1계층 지분 매핑 대상이 아니며 위탁 정산(Pipeline 2.2)으로 직접 처리됩니다. |
| 955 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | [연결된 매출연동 개발지원금(Pipeline 5.1)] ${p.supportAgreements.ma… |
| 955 | js-string | 내부암호 | SECTION | `5.2절` | …침해하지 않고 자사 귀속 지분 내에서만 차감됩니다(5.2절). |
| 961 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | …ternalShare)} 개발지원금(Pipeline 5.1) 요율 ${pct(lastSlice.suppor… |
| 968 | js-string | 내부암호 | SNAKE_ID | `contract_id` | … 상태 권리자 (1계층) 바인딩 계약 (contract_id) 1계층 지분율 적용 시작일 종… |
| 1076 | js-string | 내부암호 | SNAKE_ID | `contract_id` | … 바인딩 계약 선택 (contract_id NOT NULL) … |

### `ADMN-SETT-002_baseline.html` — 72건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 1445 | js-string | 내부암호 | SECTION | `6.5절` | …기 이월액(+45,000원) 합산]에 기인합니다 (6.5절). |
| 1487 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | 위탁 도서 판매대금 정산 (Pipeline 2.2 · 수수료 차감지급) |
| 1510 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | 위탁 도서 판매대금(Pipeline 2.2)은 원천징수 비대상이며, 수수료 차감 후 지급(N… |
| 1510 | js-string | 내부암호 | SECTION | `6.6절` | …100,000원)를 차감한 실정산액을 지급합니다 (6.6절 · 8.3절 9단계). |
| 1510 | js-string | 내부암호 | SECTION | `8.3절` | …원)를 차감한 실정산액을 지급합니다 (6.6절 · 8.3절 9단계). |
| 1520 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | 매출연동 개발지원금 단독 (Pipeline 5.1 · 무한도형) |
| 1542 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | …금액(72,000원)을 세전 계정(PRE_TAX, Pipeline 5.1 전용 구분)으로 차월 이월합니다 (7.3~7.4절… |
| 1542 | js-string | 내부암호 | SECTION | `7.4절` | … 5.1 전용 구분)으로 차월 이월합니다 (7.3~7.4절). |
| 1550 | js-string | 내부암호 | CODE_D | `D-11` | … 청구 트리거 발동 (10단계 CLAIM · QA D-11) |
| 1574 | js-string | 내부암호 | CODE_D | `D-11` | …과 무관하게 소액 미상계 선급금(-50,000원, D-11) 및 전속계약금 세후 일할 반환액(-4,768,7… |
| 1622 | js-string | 내부암호 | PIPELINE | `pipeline` | … ${s.pipelineText} ${s.step8T… |
| 1665 | js-string | 내부암호 | SECTION | `6.5절` | … 💡 [6.5절 과세표준 ↔ 실지급액 차액 사유 자동 명시] … |
| 1665 | js-string | 내부암호 | SECTION | `8.3절` | …📊 1단계 ~ 11단계 순방향 단방향 연산 명세 (8.3절 SSOT 정본) … |
| 1747 | js-string | 내부암호 | PIPELINE | `pipeline` | … ${s.payeeName} ${s.pipelineText} ${s.bankInf… |
| 1852 | js-string | 내부암호 | CODE_D | `D-13` | 🧪 [QA D-13 검증 완료] 펌뱅킹 실패 시 마감 원장(Locke… |
| 2261 | js-string | 금지어 | BAN_80PCT | `80%` | 정종대 (주권리자 80%) |
| 2264 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | Pipeline 1.1 (온라인 강좌 수익배분) |
| 2282 | js-string | 금지어 | BAN_80PCT | `80%` | 정종대 (주권리자 80%) |
| 2285 | js-string | 내부암호 | PIPELINE | `Pipeline 2.1` | Pipeline 2.1 (자사 발행 도서 인세) |
| 2306 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | Pipeline 2.2 (위탁 도서 판매대금) |
| 2327 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | Pipeline 1.1 (일시 특강·콘텐츠 용역) |
| 2330 | js-string | 내부암호 | CODE_D | `D-13` | …완료 후 수취인 계좌번호 오기재로 송금 실패(QA D-13) → 이중 과세 방지를 위해 세후(POST_TAX… |
| 2348 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | Pipeline 1.1 (선급금 해지 강제청구) |
| 2351 | js-string | 내부암호 | CODE_C | `C-03` | … 환수 청구 전환하여 선급금 원장 잔액 0원 종결(C-03·C-04) |
| 2351 | js-string | 내부암호 | CODE_C | `C-04` | …구 전환하여 선급금 원장 잔액 0원 종결(C-03·C-04) |
| 2375 | js-string | 금지어 | BAN_80PCT | `80%` | 정종대 (주권리자 · 2계층 지분 80%) |
| 2376 | js-string | 금지어 | BAN_80PCT | `80%` | 개인 면세사업자 (수취인 분할 80% · 원천징수 3.3% + 계산서 역발행) |
| 2383 | js-string | 금지어 | BAN_80PCT | `80%` | …001 \| 1계층 단독 100% → 2계층 정종대 80% / (주)산준교육 20% |
| 2384 | js-string | 금지어 | BAN_80PCT | `80%` | … 전체 당월 상계 -1,500,000원 중 정종대(80%) 귀속분 -1,200,000원 (기말 잔액 2,0… |
| 2396 | js-string | 금지어 | BAN_80PCT | `80%` | 8단계 수취인 분할(80%) 후 과세표준 5,915,000원(계산서 역발행 … |
| 2396 | js-string | 금지어 | BAN_80PCT | `80%` | …5,000원(계산서 역발행 금액) − 선급금 상계(80% 귀속분) 1,200,000원 − 원천징수세액(3.… |
| 2398 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | Pipeline 1.1 (강좌 수익배분) |
| 2405 | js-string | 내부암호 | PIPELINE | `Pipeline 2.1` | OWN_PUBLISHED (자사발행 인세 · Pipeline 2.1) |
| 2408 | js-string | 내부암호 | PIPELINE | `Pipeline 5.1` | 매출연동 개발지원금 (Pipeline 5.1) |
| 2411 | js-string | 금지어 | BAN_80PCT | `80%` | …상계 -1,500,000원 → 8단계 수취인 분할(80%) 적용 시 정종대 귀속 상계액 -1,200,000… |
| 2414 | js-string | 금지어 | BAN_80PCT | `80%` | 본인 귀속 80% (과세표준 5,915,000원 / 선급금상계 -1… |
| 2425 | js-string | 금지어 | BAN_80PCT | `80%` | 과세표준 7,393,750×80%=5,915,000원 / 상계 후 잔액 5,893,… |
| 2425 | js-string | 금지어 | BAN_80PCT | `80%` | …15,000원 / 상계 후 잔액 5,893,750×80%=4,715,000원 |
| 2430 | js-string | 금지어 | BAN_CIRCLED | `①` | 복합 증빙(TX-08): ① 면세 계산서 역발행 공급가액 5,915,000원 … |
| 2430 | js-string | 금지어 | BAN_CIRCLED | `②` | … 역발행 공급가액 5,915,000원 승인완료 + ② 사업소득 원천징수(3.3%, 195,190원) 동… |
| 2432 | js-string | 금지어 | BAN_80PCT | `80%` | …6-10-31 19:05] 재무팀 김회계: 정종대(80%) / 산준교육(20%) 2계층 분할 및 선급금 1… |
| 2469 | js-string | 금지어 | BAN_80PCT | `80%` | 주권리자 80% 귀속 |
| 2492 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | CON-2026-014 \| 위탁 도서(Pipeline 2.2) 수수료 차감지급(NET_DEDUCT, 수수료율 … |
| 2505 | js-string | 내부암호 | SECTION | `6.6절` | …) = 위탁 순정산 실지급액 1,820,000원 (6.6절 품목별 구성요소 등식 100% 일치) |
| 2509 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | CONSIGNMENT (위탁도서 · Pipeline 2.2 · NET_DEDUCT) |
| 2515 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | 위탁 도서 출고 기준 위탁 순액 산출 (Pipeline 2.2) |
| 2520 | js-string | 금지어 | BAN_CIRCLED | `①` | 양방향 증빙(TX-11/TX-12): ① 당사→한국소방학회 위탁수수료 과세 세금계산서(공급… |
| 2520 | js-string | 금지어 | BAN_CIRCLED | `②` | …9,091 / 세액 70,909) 정발행 완료 \| ② 한국소방학회→당사 도서 면세 계산서 수취 대기 |
| 2522 | js-string | 내부암호 | SECTION | `6.6절` | [2026-10-31 19:18] 재무팀 이검수: 6.6절 품목별 배분 등식(판매대금 260만 − 위탁순액 … |
| 2550 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | Pipeline 1.1 (일시 용역) |
| 2581 | js-string | 내부암호 | CODE_C | `C-02` | C-02·C-03 가드레일: 3단계 MMG 보전금(800,… |
| 2581 | js-string | 내부암호 | CODE_C | `C-03` | C-02·C-03 가드레일: 3단계 MMG 보전금(800,000원)… |
| 2599 | js-string | 내부암호 | CODE_C | `C-02` | NON_OFFSET (선급금 상계 절대 금지 · C-02/C-03) |
| 2599 | js-string | 내부암호 | CODE_C | `C-03` | …OFFSET (선급금 상계 절대 금지 · C-02/C-03) |
| 2611 | js-string | 내부암호 | CODE_C | `C-03` | 중도해지 미상계 선급금 강제 환수청구 분리 발행 (C-03·C-04) |
| 2611 | js-string | 내부암호 | CODE_C | `C-04` | …미상계 선급금 강제 환수청구 분리 발행 (C-03·C-04) |
| 2616 | js-string | 내부암호 | CODE_C | `C-02` | …1 19:30] 법무·재무 합동검토: v4.0.0 C-02/C-03 가드레일에 따라 비상계 MMG(80만원)… |
| 2616 | js-string | 내부암호 | CODE_C | `C-03` | …30] 법무·재무 합동검토: v4.0.0 C-02/C-03 가드레일에 따라 비상계 MMG(80만원)는 선급금… |
| 2731 | js-string | 내부암호 | PIPELINE | `pipeline` | …ntLabel} ${r.pipeline} … |
| 2768 | js-string | 내부암호 | PIPELINE | `pipeline` | …riginMonth} ${r.pipeline.replace(/Pipeline [0-9.]+ /… |
| 2768 | js-string | 내부암호 | PIPELINE | `Pipeline` | … ${r.pipeline.replace(/Pipeline [0-9.]+ /g, '')} … |
| 2861 | js-string | 금지어 | BAN_CIRCLED | `①` | ① 전월 세전 이월(1단계) ${f… |
| 2861 | js-string | 금지어 | BAN_CIRCLED | `②` | …} ② 당월 발생(2·3·7단계) ${… |
| 2861 | js-string | 금지어 | BAN_CIRCLED | `③` | …} ③ 환불·반품·옵션B 공제(4단계) … |
| 2861 | js-string | 금지어 | BAN_CIRCLED | `④` | …} ④ 수취인 과세표준 (증빙 기준) … |
| 2861 | js-string | 금지어 | BAN_CIRCLED | `⑤` | …} ⑤ 선급금상계 · 세후이월 가감 $… |
| 2861 | js-string | 금지어 | BAN_CIRCLED | `⑥` | …} ⑥ 세액(${fmt(sc.taxAmount)}) 반영… |
| 2887 | js-string | 내부암호 | SECTION | `6.5절` | 📐 [6.5절 과세표준 vs 실지급액 차액 검증 등식] ${c… |
| 2939 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | … [테이블 B] 온라인 강좌 수익배분 산출 명세 (Pipeline 1.1) 정산기준금 DECIMA… |
| 2980 | js-string | 내부암호 | PIPELINE | `Pipeline 2.1` | … 📚 [테이블 C] 교재 저작권 인세(Pipeline 2.1) · 위탁 도서 판매대금(Pipeline 2.2)… |
| 2980 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | …(Pipeline 2.1) · 위탁 도서 판매대금(Pipeline 2.2) 산출 명세 3PL 출고… |
| 2980 | js-string | 내부암호 | PIPELINE | `Pipeline` | …재명 공급 형태 (Pipeline) 출고 / 반품 … |

### `ADMN-SETT-004_baseline.html` — 6건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 873 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | Pipeline 2.2 (위탁 도서) |
| 892 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | Pipeline 1.1 (온라인 강좌) |
| 911 | js-string | 내부암호 | PIPELINE | `Pipeline 2.1` | Pipeline 2.1 (자사발행 도서) |
| 930 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | Pipeline 1.1 (온라인 강좌) |
| 1171 | js-string | 내부암호 | PIPELINE | `pipeline` | … 연결 파이프라인 ${r.pipeline} 3계층 과·면세 구성 … |
| 1171 | js-string | 내부암호 | SECTION | `8.2절` | … 차이 원인 코드 분류 (8.2절 표준 코드) … |

### `ADMN-SETT-005_baseline.html` — 14건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 881 | js-string | 내부암호 | SECTION | `7.3절` | [7.3절 · 10.3절] 세전·세후 계정 간 대체 전표는 … |
| 881 | js-string | 내부암호 | SECTION | `10.3절` | [7.3절 · 10.3절] 세전·세후 계정 간 대체 전표는 금액 크기와 무… |
| 908 | js-string | 내부암호 | SECTION | `10.4절` | [10.4절 도서 오등록 특칙] 전월에 인세가 지급·신고된 바… |
| 931 | js-string | 내부암호 | SECTION | `5.2절` | [5.2절 · 10.3절] 계약 해지 시 지원금 이행률 정산… |
| 931 | js-string | 내부암호 | SECTION | `10.3절` | [5.2절 · 10.3절] 계약 해지 시 지원금 이행률 정산(PRO_RAT… |
| 951 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | 위탁 정산금 (Pipeline 2.2) |
| 1082 | js-string | 내부암호 | SECTION | `10.3절` | … 승인 통제 규칙 (10.3절) ${item.requireRe… |
| 1082 | js-string | 내부암호 | SECTION | `10.4절` | … 🔗 [10.4절] 자동 분기된 증빙 · 원천세 정정 채널 (1:N… |
| 1219 | js-string | 내부암호 | SECTION | `10.4절` | [10.4절 도서 오등록 특칙] 기지급·신고 이력 없을 시 당… |
| 1225 | js-string | 내부암호 | SECTION | `10.3절` | • 승인 경로 판정 (10.3절): ${approvalText} … |
| 1225 | js-string | 내부암호 | SECTION | `10.4절` | … • 자동 연결 증빙 정정 채널 (10.4절): ${channelText} |
| 1238 | js-string | 내부암호 | SECTION | `10.2절` | [10.2절 필수 입력 통제]\n수동 조정 소명 내용(adj_… |
| 1292 | js-string | 내부암호 | SECTION | `10.4절` | 10.4절 기준 세무 매트릭스 정정 채널 자동 연결됨 |
| 1329 | js-string | 내부암호 | SECTION | `10.2절` | [10.2절 필수 입력 통제]\n수동 조정 소명 내용(adj_… |

### `ADMN-SETT-006_baseline.html` — 4건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 1101 | js-string | 금지어 | BAN_CIRCLED | `①` | … ① 합격증 사본 이미지 📎 … |
| 1101 | js-string | 금지어 | BAN_CIRCLED | `②` | … ② 플랫폼 · 산준모 카페 수기 링크 … |
| 1101 | js-string | 금지어 | BAN_CIRCLED | `③` | … ③ 환급금 입금용 통장 사본 … |
| 1101 | js-string | 금지어 | BAN_CIRCLED | `④` | … ④ 시중 1금융권 은행 · 실명계좌 … |

### `ADMN-SETT-007_baseline.html` — 21건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 549 | js-string | 금지어 | BAN_80PCT | `80%` | 2026 산업안전기사 정종대 통합계약 — 주권리자 80% : (주)산준교육 에이전시 20% (SETT-00… |
| 565 | js-string | 금지어 | BAN_80PCT | `80%` | 주권리자 정종대 80% 귀속 (2026-10 과세표준 5,915,000원… |
| 568 | js-string | 금지어 | BAN_80PCT | `80%` | …계약 체결 시 주권리자 정종대(PY-0025-A, 80%) 및 공동서명 에이전시 (주)산준교육(PY-002… |
| 596 | js-string | 내부암호 | SECTION | `16.1절` | …기사 기본서 저작권 및 강의 계약 (상속 승계 · 16.1절) |
| 613 | js-string | 내부암호 | CODE_D | `D-1` | …분할협의서 기준 자녀 40% (이전 원거래 환불은 D-1 스냅샷 적용) |
| 670 | js-string | 내부암호 | SECTION | `5.3절` | …3,500,000원 존재 (선급금 원장 미종결 — 5.3절 상호 차단) |
| 681 | js-string | 내부암호 | SECTION | `5.3절` | 선급금 미종결 계약으로 원 권리자 100% 고정 (5.3절) |
| 870 | js-string | 내부암호 | SECTION | `4.1절` | … • 계약서 등록 공동 서명인 풀(4.1절): ${c.coSigners.map(cs => |
| 906 | js-string | 내부암호 | SECTION | `4.1절` | ✅ [4.1절 정합성 통과] 공동 서명 수취인 분할 비율 합계가… |
| 915 | js-string | 내부암호 | SECTION | `4.1절` | … 수취인 (공동 서명인 그룹 · 4.1절) 사업자/소득 구분 및 … |
| 915 | js-string | 내부암호 | SECTION | `16.1절` | … 저작자 본인 여부 / 승계 확정일 (16.1절) 2계층 분할 비율 (%… |
| 915 | js-string | 금지어 | BAN_80PCT | `80%` | …30% (강사:소속사 표준) 80% : 20% 60% : 40%… |
| 970 | js-string | 내부암호 | CODE_D | `D-1` | …ccessionDate} (이전 환불은 원 스냅샷 D-1) |
| 991 | js-string | 내부암호 | SECTION | `13.3절` | …무 독립 판정 미리보기 (Case 7 · 13.2~13.3절) … |
| 991 | js-string | 내부암호 | SECTION | `13.3절` | … 배분 순번 (13.3절 정렬) 수취인 … |
| 991 | js-string | 내부암호 | SECTION | `13.2절` | …할 비율 산출 공식 (13.2절 총액 역산) 8단계 … |
| 991 | js-string | 내부암호 | SNAKE_ID | `payee_id` | …split_ratio) 내림차순 → 수취인 식별자(payee_id) 오름차순 · 선행 수취인 내림(Floor) … |
| 1060 | js-string | 내부암호 | SECTION | `5.3절` | 저장 하드락 (5.3절) 선택 계약( ${c.id} )… |
| 1072 | js-string | 내부암호 | SECTION | `4.1절` | …계약( ${c.id} ): 공동 서명 당사자 일치(4.1절) · 선급금 미보유(5.3절) · 분할 합계 10… |
| 1072 | js-string | 내부암호 | SECTION | `5.3절` | …동 서명 당사자 일치(4.1절) · 선급금 미보유(5.3절) · 분할 합계 100.00% 검증 통과 … |
| 1254 | js-string | 내부암호 | SECTION | `5.3절` | [5.3절 차단] 선급금 미종결 계약에는 수취인 분할을 저장… |

### `ADMN-SETT-008_baseline.html` — 10건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 801 | js-string | 내부암호 | SECTION | `17.5절` | 2026-09-28 폐업 확인됨. 17.5절에 따라 미승인 증빙 리마인더를 즉시 중단하고, 미… |
| 801 | js-string | 내부암호 | SECTION | `7.3절` | …즉시 중단하고, 미지급 정산금은 강제 정산 트리거(7.3절) 대상으로 선정함. 수취 계산서 확보 불가 시 채… |
| 834 | js-string | 내부암호 | SECTION | `17.3절` | 국세청 과세유형 코드 05(비영리법인) 응답. 17.3절 규칙에 따라 인세 라인은 후보 TX-09, 강의 … |
| 896 | js-string | 내부암호 | SECTION | `17.3절` | 17.3절 공급 성격 우선 규칙: 매입처의 과세유형은 일반과… |
| 1018 | js-string | 내부암호 | SECTION | `17.5절` | … 🔄 [17.5절] 과세유형 전환 확인 및 신규 유효일자 버전 행 … |
| 1038 | js-string | 내부암호 | SECTION | `17.3절` | … 🟣 [17.3절] 비영리법인·고유번호 단체(05·06) 세무 판정… |
| 1058 | js-string | 내부암호 | SECTION | `17.5절` | 🚨 [17.5절 폐업 사업자 후속 통제 작동 중] … |
| 1058 | js-string | 내부암호 | SECTION | `7.3절` | … 2) 미지급 정산금 잔액은 강제 정산 트리거(7.3절) 에 의해 최소 지급 하한(100,000원)과 무… |
| 1110 | js-string | 내부암호 | SECTION | `17.5절` | [17.5절 효력일 통제]\n전환 효력 시작일자가 비어 있습니… |
| 1149 | js-string | 내부암호 | SECTION | `17.5절` | ✔ [17.5절 행분할 승인] [${r.partnerName}] … |

### `ADMN-SETT-009_baseline.html` — 15건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 661 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | 온라인 강좌 수익배분 (Pipeline 1.1) |
| 680 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | 온라인 강좌 수익배분 (Pipeline 1.1) |
| 682 | js-string | 내부암호 | CODE_D | `D-16` | 2026 위험물산업기사 실기 시뮬레이션 특강 (D-16) |
| 691 | js-string | 내부암호 | CODE_P | `P5.1` | 최그래픽 P5.1 지원금 (5% · 자사몫 차감) |
| 699 | js-string | 내부암호 | PIPELINE | `Pipeline 1.1` | 온라인 강좌 수익배분 (Pipeline 1.1) |
| 718 | js-string | 내부암호 | PIPELINE | `Pipeline 2.1` | 자사 발행 도서 인세 (Pipeline 2.1) |
| 737 | js-string | 내부암호 | PIPELINE | `Pipeline 2.1` | 자사저작권 도서 + 개발지원금 (Pipeline 2.1 / 5.1) |
| 739 | js-string | 내부암호 | CODE_D | `D-15` | [자사저작권] 정종대 산업안전 실기 빈출문제집 (D-15) |
| 748 | js-string | 내부암호 | CODE_P | `P5.1` | 정종대 P5.1 지원금 15% (CONDITIONAL) |
| 756 | js-string | 내부암호 | PIPELINE | `Pipeline 2.2` | 위탁 도서 판매대금 정산 (Pipeline 2.2) |
| 767 | js-string | 내부암호 | SECTION | `5.2절` | 지원금 모수 제외 (5.2절) |
| 794 | js-string | 내부암호 | PIPELINE | `Pipeline 2.3` | 일반 상품 판매매출 (Pipeline 2.3 · 소비재) |
| 805 | js-string | 내부암호 | SECTION | `18.3절` | 지원금 모수 제외 (18.3절) |
| 934 | js-string | 내부암호 | CHAPTER | `제14장` | [제14장 14.1절 산출물] '${filename}' 파일… |
| 934 | js-string | 내부암호 | SECTION | `14.1절` | [제14장 14.1절 산출물] '${filename}' 파일을 생성하여… |

### `ADMN-USER-007_baseline.html` — 8건

| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |
| ---: | :--- | :--- | :--- | :--- | :--- |
| 700 | js-string | 내부암호 | SECTION | `3.1절` | 3.1절 최소 수집 원칙 — 법인은 주민등록번호 미수집 |
| 702 | js-string | 내부암호 | SECTION | `3.1절` | 미수집 (법인사업자 필드 미노출 · 3.1절) |
| 703 | js-string | 내부암호 | SECTION | `3.1절` | 미수집 (법인사업자 필드 미노출 · 3.1절) |
| 976 | js-string | 내부암호 | SECTION | `3.4절` | [3.4절 감사 통제] 열람 사유를 최소 10자 이상 구체적… |
| 1014 | js-string | 내부암호 | SECTION | `3.3절` | ✅ [3.3절 임시 서명 URL(Presigned URL) 발급… |
| 1052 | js-string | 내부암호 | SECTION | `3.4절` | [3.4절 자동 재마스킹] 30초(pii_unmask_ttl… |
| 1113 | js-string | 내부암호 | SECTION | `3.5절` | 3.5절 계층 1 개인정보 필드 분리 파기 승인 실행 |
| 1120 | js-string | 내부암호 | SECTION | `3.5절` | [3.5절 분리 파기 완료] ${item.id}의 개인식별 … |

## 5. 무결 화면 (탐지 0건)

- `ADMN-BRD-001_baseline.html`
- `ADMN-BRD-002_baseline.html`
- `ADMN-BRD-005_baseline.html`
- `ADMN-CONF-002_baseline.html`
- `ADMN-CONF-003_baseline.html`
- `ADMN-CONF-004_baseline.html`
- `ADMN-CONF-005_baseline.html`
- `ADMN-LOGIN-001_baseline.html`
- `ADMN-PROD-001_baseline.html`
- `ADMN-PROD-004_baseline.html`
- `ADMN-PROD-006_baseline.html`
- `ADMN-PROM-001_baseline.html`
- `ADMN-SETT-011_baseline.html`
- `patch_all_snb_v3.html`

