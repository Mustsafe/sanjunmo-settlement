# 백오피스 `prototype_clean/` 전수 정합성 스캔 리포트

- 생성 스크립트: `phase1_clean_and_audit.py`
- 목적: Phase 1 정제 결과 검증 및 Phase 2~4 도메인별 잔여 변수명(`snake_case`)·영문 ENUM(`UPPER_SNAKE_CASE`)·과거 용어(`Track G` 등) 타겟팅

## 1. 파일별 잔여 검출 요약

| 파일명 | 총 검출 건수 | 주요 검출 유형 및 토큰 샘플 |
| :--- | :---: | :--- |
| `00_WORKFLOW_GUIDE_baseline.html` | 22건 | `order_items`, `EVIDENCE_FILE, MANUAL_NOTE`, `refund_promo_burden_type`, `POST_TAX, PRE_TAX`, `PRE_TAX` |
| `ADMN-BOOK-001_baseline.html` | 25건 | `FIN_MANAGER`, `book_price_history, book_supply_type`, `book_supply_type`, `own_copyright_yn`, `OWN_PUBLISHED` |
| `ADMN-BRD-001_baseline.html` | **0건 (Clean)** | - |
| `ADMN-BRD-002_baseline.html` | 8건 | `ship_ordered_at`, `safe_park`, `ship_ordered_at`, `pass_lee`, `choi_san` |
| `ADMN-BRD-005_baseline.html` | 6건 | `FREE_LECTURE, FREQ_EXAM`, `FREE_LECTURE`, `FREQ_EXAM`, `ANSWER_SHEET`, `FREE_LECTURE` |
| `ADMN-CONF-001_baseline.html` | 1건 | `preview_token` |
| `ADMN-CONF-002_baseline.html` | 2건 | `term_code, user_agreements`, `terms_version_history` |
| `ADMN-CONF-003_baseline.html` | 2건 | `admin_root`, `admin_kim` |
| `ADMN-CONF-004_baseline.html` | 7건 | `INSPECT_REQ`, `INSPECT_REQ`, `INSPECT_REQ`, `is_marketing_agreed`, `is_marketing_agreed` |
| `ADMN-CONF-005_baseline.html` | 20건 | `ROLE_PARTNER_3PL, ROLE_PARTNER_COPYRIGHT, ROLE_PARTNER_INST`, `ROLE_PARTNER_INST`, `ROLE_PARTNER_COPYRIGHT`, `ROLE_PARTNER_3PL`, `ROLE_SUPER_ADMIN` |
| `ADMN-CONF-010_baseline.html` | 3건 | `MANUAL_NOTE`, `before_snapshot_json`, `after_snapshot_json` |
| `ADMN-DASH-001_baseline.html` | 11건 | `SUPER_ADMIN`, `OP_ADMIN`, `CS_ADMIN`, `LOGIS_ADMIN`, `OP_ADMIN, SETT_ADMIN, SUPER_ADMIN` |
| `ADMN-INST-001_baseline.html` | 22건 | `PENDING_REVIEW`, `contract_status`, `contract_id`, `contract_id`, `end_basis` |
| `ADMN-INST-002_baseline.html` | 11건 | `LUMPSUM_ADD, LUMP_SETTLE, REVENUE_SHARE`, `LUMP_SETTLE`, `LUMP_SETTLE`, `target_month`, `LUMP_SETTLE` |
| `ADMN-LOGIN-001_baseline.html` | **0건 (Clean)** | - |
| `ADMN-ORD-001_baseline.html` | 20건 | `ROLE_PARTNER_3PL`, `paid_amount`, `ship_ordered_at`, `paid_amount`, `Track G` |
| `ADMN-PROD-001_baseline.html` | **0건 (Clean)** | - |
| `ADMN-PROD-002_baseline.html` | 2건 | `FREQ_EXAM`, `FREQ_EXAM` |
| `ADMN-PROD-003_baseline.html` | **0건 (Clean)** | - |
| `ADMN-PROD-004_baseline.html` | 8건 | `FIN_MANAGER`, `book_discount_rate_limit`, `FIN_MANAGER`, `book_discount_rate_limit`, `FIN_MANAGER` |
| `ADMN-PROD-005_baseline.html` | 1건 | `package_product` |
| `ADMN-PROD-006_baseline.html` | 1건 | `instructor_display` |
| `ADMN-PROD-007_baseline.html` | 16건 | `FIN_MANAGER`, `INVENTORY_PURCHASE`, `goods_supply_type`, `PURCHASED_RESALE`, `DIRECT_SALE` |
| `ADMN-PROM-001_baseline.html` | 4건 | `html_content`, `css_content`, `js_content`, `html_content` |
| `ADMN-PROM-002_baseline.html` | 5건 | `user_coupon`, `user_coupon`, `cap_applied, order_discount`, `exclude_book`, `cap_applied, order_discount` |
| `ADMN-RFD-002_baseline.html` | 9건 | `dh_kang`, `yj_choi`, `order_item_id`, `order_item_id`, `SHIPPING_DEDUCT` |
| `ADMN-SETT-001_baseline.html` | **0건 (Clean)** | - |
| `ADMN-SETT-002_baseline.html` | 27건 | `CARRY_IN`, `MMG_ADJ`, `SUPPORT_CAP`, `PREPAY_OFFSET`, `LUMPSUM_ADD` |
| `ADMN-SETT-004_baseline.html` | 19건 | `pg_recon_unclassified_max`, `UNKNOWN_MISMATCH`, `pg_recon_tolerance_company`, `order_items`, `PURCHASED_RESALE, SHIPPING_FEE` |
| `ADMN-SETT-005_baseline.html` | 34건 | `①, ②`, `applied_month, origin_month`, `RATE_ERR`, `SHARE_ERR`, `REFUND_OMIT` |
| `ADMN-SETT-006_baseline.html` | 3건 | `mmg_promo_overlap_flag`, `mmg_promo_overlap_flag`, `cap_restore_on_refund` |
| `ADMN-SETT-007_baseline.html` | 9건 | `payee_is_author`, `PAYEE_SPLIT`, `payee_split_base`, `payee_id, split_ratio`, `payee_is_author` |
| `ADMN-SETT-008_baseline.html` | 14건 | `tax_type_cd`, `nts_tax_type_map`, `SIMPLIFIED_RECEIPT`, `SIMPLIFIED_INVOICE`, `PENDING_REVIEW` |
| `ADMN-SETT-009_baseline.html` | 19건 | `is_internal`, `own_copyright_yn`, `book_authors`, `own_copyright_yn`, `goods_master, item_type` |
| `ADMN-SETT-011_baseline.html` | 5건 | `ship_ordered_at, tracking_no`, `tracking_no`, `CANCELLED_BILLED`, `tracking_no`, `CANCELLED_BILLED` |
| `ADMN-USER-001_baseline.html` | 20건 | `sanjun_hong88`, `safety_kim26`, `park_jw90`, `lee_sjm77`, `choi_min33` |
| `ADMN-USER-007_baseline.html` | 21건 | `pii_unmask_ttl_seconds`, `destruction_hold`, `pii_destruction_field_map`, `rights_holder_id`, `destruction_hold` |

## 2. 파일별 상세 검출 내역 (라인 번호 기준)

### `00_WORKFLOW_GUIDE_baseline.html` (22건)
- **L590** [DB변수명_snake_case] `order_items` → `자체 주문 품목 ( order_items ) 원장과 결제대행사(PG) 입금 정산 내역`
- **L612** [영문코드_UPPER_SNAKE] `EVIDENCE_FILE, MANUAL_NOTE` → `증빙 파일 첨부 ( EVIDENCE_FILE ) / 수기 확인 소명 ( MANUAL_NOTE )`
- **L625** [DB변수명_snake_case] `refund_promo_burden_type` → `( refund_promo_burden_type : A/B/C) 연동`
- **L671** [영문코드_UPPER_SNAKE] `POST_TAX, PRE_TAX` → `세전 이월 계정 ( PRE_TAX )·세후 이월 계정 ( POST_TAX )·위탁 전용 잔액 모달`
- **L673** [영문코드_UPPER_SNAKE] `PRE_TAX` → `펌뱅킹 이체 실패 시 예약 해제 후 세전 이월 계정 ( PRE_TAX ) 적재 (QA D-13)`
- **L687** [DB변수명_snake_case] `origin_month` → `마감 취소 절대 금지  — 발생 원인 귀속월 ( origin_month )과 반영 기준월`
- **L688** [DB변수명_snake_case] `applied_month` → `( applied_month ) 분리`
- **L689** [영문코드_UPPER_SNAKE] `ACCOUNT_TRANSFER` → `100만원 초과 · 계정 간 대체 ( ACCOUNT_TRANSFER ) · 이행률 비례 정산`
- **L690** [영문코드_UPPER_SNAKE] `PRO_RATA` → `( PRO_RATA )은  재무책임자 2차 승인`
- **L746** [영문코드_UPPER_SNAKE] `ADMN_AUDIT_LOG` → `( ADMN_AUDIT_LOG )`
- **L833** [영문코드_UPPER_SNAKE] `POST_TAX, PRE_TAX` → `이월( PRE_TAX ) · 세후 이월( POST_TAX ) · 위탁 전용 잔액 분리 1회 조회 (재분할·재투입`
- **L836** [DB변수명_snake_case] `carryover_ledger` → `carryover_ledger)`
- **L881** [영문코드_UPPER_SNAKE] `LUMP_SETTLE` → `지원금 · 매절 대금 · 정액 수당 · 종료 일시정산( LUMP_SETTLE ) 가산`
- **L887** [영문코드_UPPER_SNAKE] `PRE_TAX` → `수취인 총액 역산, 원귀속  PRE_TAX  및 위탁 순액 별도 배열 전달)`
- **L897** [영문코드_UPPER_SNAKE] `VAT_EXCLUDED` → `매트릭스( 세무 판정 기준(13종) ) 적용 (부가세 별도  VAT_EXCLUDED  / 총액 역산`
- **L898** [영문코드_UPPER_SNAKE] `VAT_INCLUDED` → `VAT_INCLUDED , 원천세 2단 내림 절사)`
- **L909** [영문코드_UPPER_SNAKE] `PRE_TAX` → `RESERVED  예약) / 미달 시 세무 상태별 이월( PRE_TAX  /`
- **L910** [영문코드_UPPER_SNAKE] `POST_TAX` → `POST_TAX )`
- **L968** [DB변수명_snake_case] `origin_month` → `마감 취소 절대 금지 (10.1절). 발생 원인 귀속월 ( origin_month )과 반영 기준월`
- **L969** [DB변수명_snake_case] `applied_month` → `( applied_month )을 분리하고 4채널 증빙·원천세 정정 작업 (10.4절, 1:N 복수 작업 허용) 자동 생성`
- **L982** [DB변수명_snake_case] `payment_event_date` → `( payment_event_date IS NOT NULL )만 포함하며, 민감 정보 열람 후 30초`
- **L983** [DB변수명_snake_case] `pii_unmask_ttl_seconds` → `( pii_unmask_ttl_seconds ) 경과 시 자동 재마스킹 및 감사 로그 기록`

### `ADMN-BOOK-001_baseline.html` (25건)
- **L658** [영문코드_UPPER_SNAKE] `FIN_MANAGER` → `재무/정산책임자 (FIN_MANAGER)`
- **L763** [DB변수명_snake_case] `book_price_history, book_supply_type` → `4대 도서 공급형태(book_supply_type) · 자사저작권(Pipeline 5.1) · 정가 이력(book_price_history) 정합성 원장`
- **L777** [DB변수명_snake_case] `book_supply_type` → `공급형태 코드 (book_supply_type)`
- **L778** [DB변수명_snake_case] `own_copyright_yn` → `자사저작권 (own_copyright_yn)`
- **L789** [영문코드_UPPER_SNAKE] `OWN_PUBLISHED` → `OWN_PUBLISHED (자사발행)`
- **L799** [영문코드_UPPER_SNAKE] `OWN_PUBLISHED` → `OWN_PUBLISHED (자사저작권)`
- **L812** [영문코드_UPPER_SNAKE] `NET_DEDUCT, VAT_INCLUDED` → `NET_DEDUCT (수수료 차감지급) · 수수료율  30%  ( VAT_INCLUDED ) · 6.6절 등식 적용`
- **L819** [영문코드_UPPER_SNAKE] `PURCHASED_RESALE` → `PURCHASED_RESALE (사입)`
- **L846** [DB변수명_snake_case] `book_price_history` → `[ADMN-BOOK-001-S1] 도서 정가 변경 이력(book_price_history) 및 위탁 수수료 스냅샷 검증`
- **L851** [DB변수명_snake_case] `book_supply_type, effective_from, effective_to` → `💡  [제6장 6.2절 정가 변경 이력 관리 원칙]  도서 정가가 개정판 등으로 인상·변경되더라도 과거 주문의 환불/반품(4단계  DEDUCT ) 시에는  원거래 주문 시점의 정가`
- **L858** [DB변수명_snake_case] `effective_from` → `적용 시작일 (effective_from)`
- **L859** [DB변수명_snake_case] `effective_to` → `적용 종료일 (effective_to)`
- **L914** [DB변수명_snake_case] `book_supply_ledger` → `Table: book_supply_ledger`
- **L921** [DB변수명_snake_case] `book_supply_type` → `전체 4대 공급형태 (book_supply_type)`
- **L922** [영문코드_UPPER_SNAKE] `OWN_PUBLISHED` → `OWN_PUBLISHED · 자사발행 (Pipeline 2.1 인세 / 5.1 지원금)`
- **L924** [영문코드_UPPER_SNAKE] `PURCHASED_RESALE` → `PURCHASED_RESALE · 매입 재판매 (외부정산 비대상 · SETT-009/011)`
- **L932** [설계마커_원문자] `①` → `① 계약원장(INST-001) 가채번 출발`
- **L933** [설계마커_원문자] `②` → `② 교재관리(PROD-004) 선등록 역매핑`
- **L934** [설계마커_원문자] `③` → `③ 공급원장(BOOK-001) 최초 채번`
- **L1038** [설계마커_원문자] `①` → `① 계약원장(ADMN-INST-001) 가채번 도서 불러오기`
- **L1055** [설계마커_원문자] `②` → `② 교재관리(ADMN-PROD-004) 선등록 SKU 원가 완성`
- **L1072** [설계마커_원문자] `③` → `③ 공급원장(ADMN-BOOK-001)에서 최초 신규 SKU 생성`
- **L1088** [설계마커_원문자] `①` → `[경로 ① 선택됨 — 계약원장 가채번(TMP-BK-2601) 바인딩 완료]`
- **L1253** [설계마커_원문자] `①` → `① 계약원장(ADMN-INST-001) 가채번 도서 불러오기`
- **L1299** [설계마커_원문자] `②` → `② 교재관리(ADMN-PROD-004) 선등록 원가 미입력 SKU 불러오기`

### `ADMN-BRD-002_baseline.html` (8건)
- **L558** [DB변수명_snake_case] `ship_ordered_at` → `ship_ordered_at  잠금 여부 실시간 조회 → 출고 전 주소 변경 or 출고지시 회수/반품검수 연결`
- **L684** [DB변수명_snake_case] `safe_park` → `박안전 (safe_park)`
- **L689** [DB변수명_snake_case] `ship_ordered_at` → `⚠️ 3PL 발주 엑셀 다운로드 완료( ship_ordered_at  기록)로 마이페이지 수정 차단됨`
- **L713** [DB변수명_snake_case] `pass_lee` → `이서연 (pass_lee · USR-0941)`
- **L742** [DB변수명_snake_case] `choi_san` → `최산안 (choi_san)`
- **L771** [DB변수명_snake_case] `jung_study` → `정수험 (jung_study)`
- **L855** [DB변수명_snake_case] `unopened_book_photo` → `unopened_book_photo.jpg (1.8MB)`
- **L946** [DB변수명_snake_case] `ship_ordered_at` → `상태: 🔒 출고지시 완료 ( ship_ordered_at = 2026-10-16 11:00:12 )`

### `ADMN-BRD-005_baseline.html` (6건)
- **L928** [영문코드_UPPER_SNAKE] `FREE_LECTURE, FREQ_EXAM` → `[ADMN-BRD-006] 무료특강 및 빈출문제 운영 정책:  사용자 웹  USER-FREE-001 ~ 003 에 노출되는 무료 학습 콘텐츠입니다. 콘텐츠 구분은  [무료특강 영상`
- **L944** [영문코드_UPPER_SNAKE] `FREE_LECTURE` → `무료특강 영상 (FREE_LECTURE)`
- **L946** [영문코드_UPPER_SNAKE] `FREQ_EXAM` → `빈출문제 해설 (FREQ_EXAM)`
- **L1019** [영문코드_UPPER_SNAKE] `ANSWER_SHEET` → `[ADMN-BRD-009] 교재 정답지 관리 (웹 에디터 적용):  수험서 교재별  [교재 정답지 및 상세 해설 ( ANSWER_SHEET )] 을 관리합니다. 등록/수정 시  리`
- **L1158** [영문코드_UPPER_SNAKE] `FREE_LECTURE` → `무료특강 영상 (FREE_LECTURE)`
- **L1160** [영문코드_UPPER_SNAKE] `FREQ_EXAM` → `빈출문제 해설 (FREQ_EXAM)`

### `ADMN-CONF-001_baseline.html` (1건)
- **L110** [DB변수명_snake_case] `preview_token` → `🖥️ 사용자 메인 미리보기 (?preview_token) ↗`

### `ADMN-CONF-002_baseline.html` (2건)
- **L623** [DB변수명_snake_case] `term_code, user_agreements` → `필수 동의 ·  user_agreements (term_code='T04')`
- **L973** [DB변수명_snake_case] `terms_version_history` → `• 저장 즉시 버전별 변경 이력( terms_version_history ) 및 관리자 보안 감사 로그( ADMN-CONF-006 )에 기록됩니다.`

### `ADMN-CONF-003_baseline.html` (2건)
- **L238** [DB변수명_snake_case] `admin_root` → `2026.10.16 14:20  최고관리자 (admin_root)  동시접속 제어 정책 (11/16 오픈 기준)  기기 UUID 2대 고정   동시접속 1세션 제어 (중복 시 기존`
- **L239** [DB변수명_snake_case] `admin_kim` → `2026.10.11 10:05  운영팀 (admin_kim)  워터마크 노출 시간 (displayDuration)  3초   5초 (이동 주기 10초)`

### `ADMN-CONF-004_baseline.html` (7건)
- **L415** [영문코드_UPPER_SNAKE] `INSPECT_REQ` → `카카오 검수중 (INSPECT_REQ)`
- **L434** [영문코드_UPPER_SNAKE] `INSPECT_REQ` → `•  알림톡(ALIMTALK):  신규 템플릿 등록 시  작성초안(DRAFT) 으로 생성되며,  [카카오 검수 요청] 을 통해  검수중(INSPECT_REQ)  →  검수승인(AP`
- **L449** [영문코드_UPPER_SNAKE] `INSPECT_REQ` → `카카오 검수중 (INSPECT_REQ)`
- **L490** [DB변수명_snake_case] `is_marketing_agreed` → `[2]  광고성( AD ) 메시지 는 야간 시간대(20:50 ~ 익일 08:00) 즉시 발송이 자동 차단되며,  is_marketing_agreed = true  수신 동의 회원만`
- **L503** [DB변수명_snake_case] `is_marketing_agreed` → `마케팅 수신동의(is_marketing_agreed=Y) 회원 (985명)`
- **L622** [영문코드_UPPER_SNAKE] `INSPECT_REQ` → `카카오 검수중 (INSPECT_REQ)`
- **L665** [영문코드_UPPER_SNAKE] `INSPECT_REQ` → `📤 저장 후 카카오 검수 요청 (INSPECT_REQ)`

### `ADMN-CONF-005_baseline.html` (20건)
- **L342** [영문코드_UPPER_SNAKE] `ROLE_PARTNER_3PL, ROLE_PARTNER_COPYRIGHT, ROLE_PARTNER_INST` → `기존 단일 그룹이던 외부 파트너를 역할과 정산·업무 범위에 따라  [1] 파트너 강사( ROLE_PARTNER_INST ) ,  [2] 교재 저작권자/출판사( ROLE_PARTNE`
- **L347** [영문코드_UPPER_SNAKE] `ROLE_PARTNER_INST` → `ROLE_PARTNER_INST`
- **L352** [영문코드_UPPER_SNAKE] `ROLE_PARTNER_COPYRIGHT` → `ROLE_PARTNER_COPYRIGHT`
- **L357** [영문코드_UPPER_SNAKE] `ROLE_PARTNER_3PL` → `ROLE_PARTNER_3PL`
- **L368** [영문코드_UPPER_SNAKE] `ROLE_SUPER_ADMIN` → `[내부] 최고관리자 (ROLE_SUPER_ADMIN)`
- **L369** [영문코드_UPPER_SNAKE] `ROLE_FINANCE_ADMIN` → `[내부] 정산/재무 담당 (ROLE_FINANCE_ADMIN)`
- **L370** [영문코드_UPPER_SNAKE] `ROLE_OPS_ADMIN` → `[내부] 서비스/콘텐츠 운영 (ROLE_OPS_ADMIN)`
- **L371** [영문코드_UPPER_SNAKE] `ROLE_CS_ADMIN` → `[내부] 고객센터 CS 전담 (ROLE_CS_ADMIN)`
- **L372** [영문코드_UPPER_SNAKE] `ROLE_PARTNER_INST` → `[파트너] 강사 전용 (ROLE_PARTNER_INST)`
- **L373** [영문코드_UPPER_SNAKE] `ROLE_PARTNER_COPYRIGHT` → `[파트너] 교재 저작권자 (ROLE_PARTNER_COPYRIGHT)`
- **L374** [영문코드_UPPER_SNAKE] `ROLE_PARTNER_3PL` → `[파트너] 외부 물류 3PL (ROLE_PARTNER_3PL)`
- **L414** [영문코드_UPPER_SNAKE] `PARTNER_INST` → `파트너 강사 (PARTNER_INST)`
- **L416** [영문코드_UPPER_SNAKE] `PARTNER_3PL` → `외부 물류 3PL (PARTNER_3PL)`
- **L527** [영문코드_UPPER_SNAKE] `ROLE_SUPER_ADMIN` → `[내부] 최고관리자 (ROLE_SUPER_ADMIN)`
- **L528** [영문코드_UPPER_SNAKE] `ROLE_FINANCE_ADMIN` → `[내부] 정산/재무 관리자 (ROLE_FINANCE_ADMIN)`
- **L529** [영문코드_UPPER_SNAKE] `ROLE_OPS_ADMIN` → `[내부] 서비스/콘텐츠 운영자 (ROLE_OPS_ADMIN)`
- **L530** [영문코드_UPPER_SNAKE] `ROLE_CS_ADMIN` → `[내부] 고객센터 CS 전담 (ROLE_CS_ADMIN)`
- **L531** [영문코드_UPPER_SNAKE] `ROLE_PARTNER_INST` → `[외부 파트너] 강사 전용 (ROLE_PARTNER_INST — 본인 강좌 Q&amp;A 및 강의 정산서)`
- **L532** [영문코드_UPPER_SNAKE] `ROLE_PARTNER_COPYRIGHT` → `[외부 파트너] 교재 저작권자/출판사 (ROLE_PARTNER_COPYRIGHT — 도서 인세 정산서 및 정답지 관리)`
- **L533** [영문코드_UPPER_SNAKE] `ROLE_PARTNER_3PL` → `[외부 파트너] 외부 물류 3PL (ROLE_PARTNER_3PL — 교재 출고지시서 및 송장 등록)`

### `ADMN-CONF-010_baseline.html` (3건)
- **L341** [영문코드_UPPER_SNAKE] `MANUAL_NOTE` → `2차 승인 · PRE↔POST 대체 · MANUAL_NOTE`
- **L511** [DB변수명_snake_case] `before_snapshot_json` → `🔴 변경 전 스냅샷 ( before_snapshot_json )`
- **L517** [DB변수명_snake_case] `after_snapshot_json` → `🟢 변경 후 스냅샷 ( after_snapshot_json )`

### `ADMN-DASH-001_baseline.html` (11건)
- **L432** [영문코드_UPPER_SNAKE] `SUPER_ADMIN` → `최고관리자 (SUPER_ADMIN · 전 블록 열람)`
- **L433** [영문코드_UPPER_SNAKE] `OP_ADMIN` → `운영관리자 (OP_ADMIN · 전 블록 열람)`
- **L434** [영문코드_UPPER_SNAKE] `CS_ADMIN` → `CS담당자 (CS_ADMIN · 매출/통계 블록 마스킹)`
- **L435** [영문코드_UPPER_SNAKE] `LOGIS_ADMIN` → `물류담당자 (LOGIS_ADMIN · 출고/3PL 중심)`
- **L573** [영문코드_UPPER_SNAKE] `OP_ADMIN, SETT_ADMIN, SUPER_ADMIN` → `🔒 매출 열람 권한(SUPER_ADMIN / OP_ADMIN / SETT_ADMIN) 보유 역할에만 노출됩니다.`
- **L694** [DB변수명_snake_case] `cs_park` → `관리자 cs_park — 회원 명단 엑셀 다운로드 1,240건 (사유: 10월 수강만료 안내 발송)`
- **L700** [DB변수명_snake_case] `inst_lee` → `파트너 inst_lee@sanjunmo.com — 비밀번호 5회 오류 계정 자동 잠금`
- **L706** [DB변수명_snake_case] `sett_choi` → `관리자 sett_choi — 강사 주민등록번호 마스킹 해제 열람 (사유: 원천징수 영수증 대사)`
- **L898** [영문코드_UPPER_SNAKE] `TPL_PAY_DONE` → `TPL_PAY_DONE`
- **L906** [영문코드_UPPER_SNAKE] `EML_TERMS_NOTICE` → `EML_TERMS_NOTICE`
- **L914** [영문코드_UPPER_SNAKE] `TPL_DLV_START` → `TPL_DLV_START`

### `ADMN-INST-001_baseline.html` (22건)
- **L329** [영문코드_UPPER_SNAKE] `PENDING_REVIEW` → `만료 임박(30일 이내), 세무 판정 보류(PENDING_REVIEW), 작성 중(DRAFT) 계약을 필터링하여 조회하고, 클릭하여 상세 계약 조건·요율·개발지원금·선급금을 편집합`
- **L338** [DB변수명_snake_case] `contract_status` → `계약 상태 (contract_status)`
- **L381** [DB변수명_snake_case] `contract_id` → `⚠️  정산 매핑 미완료(적용 계약 미지정) 1건 감지:  적용 계약( contract_id )이 미지정된 강의·도서 SKU는 월간 정산 배치( ADMN-SETT-002 ) 인입이`
- **L391** [DB변수명_snake_case] `contract_id` → `적용 계약 (contract_id)`
- **L393** [DB변수명_snake_case] `end_basis` → `매핑 종료 기준 (end_basis)`
- **L404** [영문코드_UPPER_SNAKE] `CONTRACT_LINKED` → `CONTRACT_LINKED  (계약 종료일 동기화)`
- **L413** [영문코드_UPPER_SNAKE] `CONTRACT_LINKED` → `CONTRACT_LINKED  (계약 종료일 동기화)`
- **L419** [DB변수명_snake_case] `own_copyright_yn` → `『산준모 산업안전 실기 빈출문제집』 ( PROD-BK-1004  ·  own_copyright_yn=true )`
- **L422** [영문코드_UPPER_SNAKE] `CONTRACT_LINKED` → `CONTRACT_LINKED  (무기한)`
- **L834** [DB변수명_snake_case] `payment_method` → `지급 방식 (payment_method)`
- **L836** [영문코드_UPPER_SNAKE] `REVENUE_SHARE` → `매출연동 (REVENUE_SHARE)`
- **L838** [영문코드_UPPER_SNAKE] `LUMP_SUM` → `일시금 (LUMP_SUM)`
- **L842** [DB변수명_snake_case] `offset_type` → `상계 처리 유형 (offset_type)`
- **L845** [영문코드_UPPER_SNAKE] `NON_OFFSET` → `비상계 · 순수 지원 (NON_OFFSET)`
- **L853** [DB변수명_snake_case] `cap_type` → `한도 유형 (cap_type)`
- **L894** [DB변수명_snake_case] `on_termination_policy` → `약정 종료 처리 정책 (on_termination_policy)`
- **L897** [영문코드_UPPER_SNAKE] `LUMP_SETTLE` → `일시 정산 (LUMP_SETTLE)`
- **L898** [영문코드_UPPER_SNAKE] `PRO_RATA` → `이행률 정산 (PRO_RATA)`
- **L902** [DB변수명_snake_case] `cap_restore_on_refund` → `환불 시 한도 복원 (cap_restore_on_refund = true)`
- **L913** [영문코드_UPPER_SNAKE] `PREPAY_OFFSET` → `위 누계는 원장 조회 결과를 표현한 예시입니다. 동일 콘텐츠·동일 기간의 지원금 요율 합계는 자사 지분을 넘을 수 없습니다. 매출연동 지원금(Pipeline 5.1)은 월 최저보장`
- **L946** [DB변수명_snake_case] `agreement_id` → `BASIC은 agreement_id = NULL입니다. 마감 구간은 잠금 상태로 보존합니다.`
- **L2854** [영문코드_UPPER_SNAKE] `CLAIMED_ON_TERMINATION` → `•  금전 약정 비승계 및 해지 강제청구:  선급금 잔액 · 최저보장(MMG) · 전속계약금 · 개발지원금은 승계 계약으로 자동 이전되지 않으며, 중도 해지 시 미상계 선급금 잔액`

### `ADMN-INST-002_baseline.html` (11건)
- **L480** [영문코드_UPPER_SNAKE] `LUMPSUM_ADD, LUMP_SETTLE, REVENUE_SHARE` → `본 화면은  전속계약금 · 일시금/분할형 개발지원금 · 매절 대금 · 정액 수당 · 종료 시 일시정산( LUMP_SETTLE ) 의 당월 정산서(7단계  LUMPSUM_ADD ) `
- **L517** [영문코드_UPPER_SNAKE] `LUMP_SETTLE` → `2. 전속계약금 중도해지 일할 반환 · 종료 일시정산(LUMP_SETTLE) 규격 (5.2절)`
- **L539** [영문코드_UPPER_SNAKE] `LUMP_SETTLE` → `지원금 종료 시 일시정산 (LUMP_SETTLE)`
- **L550** [DB변수명_snake_case] `target_month` → `귀속월 (target_month)`
- **L577** [영문코드_UPPER_SNAKE] `LUMP_SETTLE` → `전속계약금 중도해지 일할 반환 산식(10단계 CLAIM) 및 지원금 종료 시 일시 정산(LUMP_SETTLE, 7단계) 연동 현황 (5.2절)`
- **L612** [DB변수명_snake_case] `on_termination_policy` → `on_termination_policy = LUMP_SETTLE  (한도형 총 한도 10,000,000원 − 기 소진 8,200,000원)`
- **L612** [영문코드_UPPER_SNAKE] `LUMP_SETTLE` → `on_termination_policy = LUMP_SETTLE  (한도형 총 한도 10,000,000원 − 기 소진 8,200,000원)`
- **L613** [영문코드_UPPER_SNAKE] `LUMPSUM_ADD, SUPPORT_CAP` → `* 본 화면(INST-002)에서 종료 일시정산 승인 시 7단계(LUMPSUM_ADD)로 1회 인입 + 5단계(SUPPORT_CAP) 한도 소진액 가산 후 종결 전이`
- **L616** [영문코드_UPPER_SNAKE] `LUMPSUM_ADD` → `7단계(LUMPSUM_ADD) 수당 라인 인입 대기  (MS-2026-006)`
- **L623** [DB변수명_snake_case] `penalty_base, penalty_calc_type` → `penalty_calc_type = MULTIPLE (200%) ,  penalty_base = TOTAL_AGREED ,  CUMULATIVE`
- **L623** [영문코드_UPPER_SNAKE] `TOTAL_AGREED` → `penalty_calc_type = MULTIPLE (200%) ,  penalty_base = TOTAL_AGREED ,  CUMULATIVE`

### `ADMN-ORD-001_baseline.html` (20건)
- **L540** [영문코드_UPPER_SNAKE] `ROLE_PARTNER_3PL` → `🚚 3PL 물류 격리 (ROLE_PARTNER_3PL)`
- **L559** [DB변수명_snake_case] `paid_amount` → `실결제금액(payment.paid_amount) 단일 원장 기준`
- **L579** [DB변수명_snake_case] `ship_ordered_at` → `ADMN-ORD-002  · 3PL 발주 엑셀 다운로드 즉시  ship_ordered_at 이 기록되며 관리자·고객 양쪽 배송지 수정이 하드락됩니다.`
- **L609** [DB변수명_snake_case] `paid_amount` → `조회 주문 건수 (실결제 합계)  ORD-001 · paid_amount`
- **L712** [레거시_트랙_표기] `Track G` → `일반상품 (Track G)`
- **L753** [DB변수명_snake_case] `paid_amount` → `전체  7 건  (2026.08.01~08.18 · 실결제  payment.paid_amount  기준 · 주문 라인 분리 표기)`
- **L797** [영문코드_UPPER_SNAKE] `ROLE_PARTNER_3PL` → `🔒  외부 물류 파트너(ROLE_PARTNER_3PL) 보안 격리 모드 활성:`
- **L955** [DB변수명_snake_case] `warehouse_cam_0044` → `첨부됨: warehouse_cam_0044.jpg`
- **L1053** [DB변수명_snake_case] `paid_amount` → `실결제금액 (paid_amount)`
- **L1128** [영문코드_UPPER_SNAKE] `ROYALTY_BOOK` → `ISBN  979-11-8921-01 · SKU: BK-2026-101  · 스냅샷:  ROYALTY_BOOK(인세도서)`
- **L1144** [DB변수명_snake_case] `book_supply_type_snapshot` → `📌  도서정가제 &amp; 정산 스냅샷 규칙 (합의서 6.1절 · 8.1절):  교재 라인(#2)에는 쿠폰·포인트 할인이  0원 으로 고정되며 패키지 할인은 강좌 라인(#1)에만 `
- **L1144** [영문코드_UPPER_SNAKE] `ROYALTY_BOOK` → `📌  도서정가제 &amp; 정산 스냅샷 규칙 (합의서 6.1절 · 8.1절):  교재 라인(#2)에는 쿠폰·포인트 할인이  0원 으로 고정되며 패키지 할인은 강좌 라인(#1)에만 `
- **L1306** [영문코드_UPPER_SNAKE] `PAY_DONE` → `결제완료 알림톡 발송 완료 (템플릿  PAY_DONE  · 수신자: 홍길동)`
- **L1332** [DB변수명_snake_case] `ship_ordered_at` → `⚠️  출고 지시 확정(Lock) 안내:  발주 엑셀 다운로드와 동시에 대상 주문 라인에  ship_ordered_at  및 배치번호( BATCH-20260818-02 )가 부여되`
- **L1692** [폐지화면_코드] `ADMN-ORD-003` → `🎟️ [ADMN-ORD-001-P4] 수강권 직권 부여 (0원 주문 생성 · 구 ADMN-ORD-003 통합)`
- **L1698** [폐지화면_코드] `ADMN-ORD-003` → `💡  폐지 화면(구 ADMN-ORD-003) 통합 및 정산 0원 처리 원칙:`
- **L1699** [DB변수명_snake_case] `paid_amount` → `CS 보상, 이벤트 당첨, 임직원/수험생 특수 승인에 따른 수강권 부여는 0원 주문(ORDER_TYPE:  DIRECT_GRANT )으로 즉시 인서트됩니다. 실결제금액( payme`
- **L1699** [영문코드_UPPER_SNAKE] `DIRECT_GRANT, ORDER_TYPE` → `CS 보상, 이벤트 당첨, 임직원/수험생 특수 승인에 따른 수강권 부여는 0원 주문(ORDER_TYPE:  DIRECT_GRANT )으로 즉시 인서트됩니다. 실결제금액( payme`
- **L1756** [폐지화면_코드] `ADMN-ORD-003` → `• 주문 유형:  DIRECT_GRANT  (수강권 직권부여 · 구 ADMN-ORD-003 통합)`
- **L1756** [영문코드_UPPER_SNAKE] `DIRECT_GRANT` → `• 주문 유형:  DIRECT_GRANT  (수강권 직권부여 · 구 ADMN-ORD-003 통합)`

### `ADMN-PROD-002_baseline.html` (2건)
- **L377** [영문코드_UPPER_SNAKE] `FREQ_EXAM` → `빈출특강 (FREQ_EXAM)`
- **L476** [영문코드_UPPER_SNAKE] `FREQ_EXAM` → `빈출특강 (FREQ_EXAM)`

### `ADMN-PROD-004_baseline.html` (8건)
- **L693** [영문코드_UPPER_SNAKE] `FIN_MANAGER` → `재무/정산책임자 (FIN_MANAGER)`
- **L781** [DB변수명_snake_case] `book_discount_rate_limit` → `산준모 판매 교재는  도서정가제 할인 0% 정책( book_discount_rate_limit = 0% ) 으로 정가와 판매가가 동일하게 고정되며, ISBN 도서로서  부가세 면세`
- **L955** [영문코드_UPPER_SNAKE] `FIN_MANAGER` → `· 단위 공급원가:  🔒 마스킹 (FIN_MANAGER 전용)`
- **L1196** [DB변수명_snake_case] `book_discount_rate_limit` → `book_discount_rate_limit = 0% (할인 불가)`
- **L1223** [영문코드_UPPER_SNAKE] `FIN_MANAGER` → `🔒 매입원가 마스킹 (FIN_MANAGER 전용)`
- **L1237** [DB변수명_snake_case] `is_preorder` → `3. 예약판매( is_preorder ) · 재고 수량 · 판매 상태 제어`
- **L1245** [DB변수명_snake_case] `is_preorder` → `예약판매 설정 ( is_preorder )`
- **L1253** [DB변수명_snake_case] `release_date` → `출고 예정일 ( release_date )  *`

### `ADMN-PROD-005_baseline.html` (1건)
- **L647** [DB변수명_snake_case] `package_product` → `Table: package_product`

### `ADMN-PROD-006_baseline.html` (1건)
- **L587** [DB변수명_snake_case] `instructor_display` → `Table: instructor_display`

### `ADMN-PROD-007_baseline.html` (16건)
- **L340** [영문코드_UPPER_SNAKE] `FIN_MANAGER` → `재무 권한(FIN_MANAGER) 시뮬레이션 (사입원가 열람)`
- **L358** [영문코드_UPPER_SNAKE] `INVENTORY_PURCHASE` → `ADMN-SETT-001 에서  자사 권리자 100%로 자동 매핑 되어  일반 상품 판매매출( Pipeline 2.3 ) 로 집계되며, 매입 대금은 정산 엔진(펌뱅킹)을 거치지 않`
- **L402** [DB변수명_snake_case] `goods_supply_type` → `공급 형태 ( goods_supply_type )`
- **L406** [영문코드_UPPER_SNAKE] `PURCHASED_RESALE` → `매입 재판매 (PURCHASED_RESALE)`
- **L407** [영문코드_UPPER_SNAKE] `DIRECT_SALE` → `자사 직접 판매 (DIRECT_SALE)`
- **L451** [영문코드_UPPER_SNAKE] `FIN_MANAGER` → `사입 원가는 대외비로 재무 권한(FIN_MANAGER) 외 **** 마스킹`
- **L465** [DB변수명_snake_case] `goods_supply_type` → `공급 형태 ( goods_supply_type )`
- **L512** [영문코드_UPPER_SNAKE] `PURCHASED_RESALE` → `매입 재판매 (PURCHASED_RESALE)`
- **L513** [영문코드_UPPER_SNAKE] `DIRECT_SALE` → `자사 직접 판매 (DIRECT_SALE)`
- **L539** [DB변수명_snake_case] `is_internal` → `자사 권리자(주식회사 엘캠퍼스 · is_internal=true) 100.00% 자동 매핑`
- **L566** [영문코드_UPPER_SNAKE] `DIRECT_SALE` → `재무 권한 외 열람 시 마스킹 · 자사 직접 판매(DIRECT_SALE) 선택 시 비활성`
- **L570** [영문코드_UPPER_SNAKE] `INVENTORY_PURCHASE` → `INVENTORY_PURCHASE  (재고 매입 계정 🔒) &nbsp;·&nbsp;`
- **L587** [DB변수명_snake_case] `goods_stock_log` → `수정 모드에서 현재고 직접 덮어쓰기 불가 — 반드시 [재고 조정] 레이어를 통해 증감 수량과 사유를 `goods_stock_log`에 기록해야 합니다.`
- **L618** [DB변수명_snake_case] `safety_helmet_keyring_main` → `첨부 파일:  safety_helmet_keyring_main.jpg  (1.2MB)  파일 변경`
- **L691** [DB변수명_snake_case] `goods_stock_log` → `조정 저장 (goods_stock_log 적재)`
- **L702** [DB변수명_snake_case] `goods_stock_log` → `입출고 이력 원장 조회 (ADMN-PROD-007-P2 · goods_stock_log)`

### `ADMN-PROM-001_baseline.html` (4건)
- **L582** [DB변수명_snake_case] `html_content` → `📄 HTML (html_content)`
- **L583** [DB변수명_snake_case] `css_content` → `🎨 CSS (css_content)`
- **L584** [DB변수명_snake_case] `js_content` → `⚡ JS (js_content)`
- **L586** [DB변수명_snake_case] `html_content` → `현재 편집 컬럼: promotion.html_content`

### `ADMN-PROM-002_baseline.html` (5건)
- **L420** [DB변수명_snake_case] `user_coupon` → `user_coupon`
- **L583** [DB변수명_snake_case] `user_coupon` → `저장 테이블: coupon · user_coupon`
- **L630** [DB변수명_snake_case] `cap_applied, order_discount` → `• 정률 쿠폰이라도  실제 감면액은 200,000원을 넘지 못합니다  — 결제 시  FLOOR(MIN(base × rate, 200000, base))  강제 연산 및  order`
- **L645** [DB변수명_snake_case] `exclude_book` → `시스템 강제 (coupon.exclude_book = 1)`
- **L923** [DB변수명_snake_case] `cap_applied, order_discount` → `• Cap이 작동해 감면액이 깎인 주문은  order_discount.cap_applied = 1  기록 및 정산( ADMN-SETT-002 ) 시  실감면액 기준 으로 배분됩니다`

### `ADMN-RFD-002_baseline.html` (9건)
- **L696** [DB변수명_snake_case] `dh_kang` → `강도현   dh_kang`
- **L710** [DB변수명_snake_case] `yj_choi` → `최유진   yj_choi`
- **L757** [DB변수명_snake_case] `order_item_id` → `[1] 주문 기본 정보 및 환불 대상 품목( order_item_id ) 선택`
- **L769** [DB변수명_snake_case] `order_item_id` → `품목코드 ( order_item_id )`
- **L1261** [영문코드_UPPER_SNAKE] `SHIPPING_DEDUCT` → `SHIPPING_DEDUCT (실물 교재 반품 회수택배비 3,000원 사후 추가 차감)`
- **L1262** [영문코드_UPPER_SNAKE] `PG_DIFF_ADJ` → `PG_DIFF_ADJ (연동 PG사 부분취소 정산 차액 보정)`
- **L1263** [영문코드_UPPER_SNAKE] `LECTURE_PRORATE_ADJ` → `LECTURE_PRORATE_ADJ (강좌 수강일수/가중평균 진도율 재산정 차액 보정)`
- **L1264** [영문코드_UPPER_SNAKE] `MINUS_POINT_ADJ` → `MINUS_POINT_ADJ (환불 복원 LIFO / 마이너스 포인트 부채 사후 보정)`
- **L1284** [DB변수명_snake_case] `applied_month, origin_month` → `기 마감된 정산월 귀속분인 경우 차월 전기오류수정(origin_month / applied_month) 조정 라인 자동 생성 요청`

### `ADMN-SETT-002_baseline.html` (27건)
- **L994** [영문코드_UPPER_SNAKE] `CARRY_IN` → `1단계: 전월 이월 호출 ( CARRY_IN )`
- **L1001** [영문코드_UPPER_SNAKE] `MMG_ADJ` → `3단계: 월 최저보장 보정 ( MMG_ADJ )`
- **L1003** [영문코드_UPPER_SNAKE] `SUPPORT_CAP` → `5단계: 지원금 한도 캡 판정 ( SUPPORT_CAP )`
- **L1009** [영문코드_UPPER_SNAKE] `PREPAY_OFFSET` → `6단계: 선급금 상한선 상계 ( PREPAY_OFFSET )`
- **L1010** [영문코드_UPPER_SNAKE] `LUMPSUM_ADD` → `7단계: 비정기 약정금 가산 ( LUMPSUM_ADD )`
- **L1011** [영문코드_UPPER_SNAKE] `PAYEE_SPLIT` → `8단계: 수취인별 지분 분할 ( PAYEE_SPLIT )`
- **L1137** [설계마커_원문자] `①` → `① 확정·환불 순누계`
- **L1138** [설계마커_원문자] `②` → `② 한도 소진액 누계`
- **L1139** [설계마커_원문자] `③` → `③ 실제 현금송금 누계`
- **L1236** [설계마커_원문자] `①, ②` → `① [수취] 도서 판매대금 면세 계산서 ② [당사 발행] 위탁 수수료 과세 세금계산서`
- **L1240** [영문코드_UPPER_SNAKE] `NET_DEDUCT` → `위탁 실지급: 2,900,000원   (수수료 차감지급 NET_DEDUCT)`
- **L1257** [영문코드_UPPER_SNAKE] `PRE_TAX` → `이름만으로 자동 매핑하지 않고 지급 지시 식별자로 대조합니다.  마감 후 송금 실패 시 마감 원장(Locked)이나 지원금 한도를 되돌리지 않고, 지급 예약(RESERVED)만 해`
- **L1274** [DB변수명_snake_case] `payment_status` → `지급 상태 (payment_status)`
- **L1344** [영문코드_UPPER_SNAKE] `UNKNOWN_MISMATCH` → `UNKNOWN_MISMATCH = 0건  (7.4절)`
- **L1360** [영문코드_UPPER_SNAKE] `PENDING_REVIEW` → `PENDING_REVIEW = 0건  (전 수취인 DECIDED)`
- **L1372** [DB변수명_snake_case] `carryover_ledger` → `7.4절 carryover_ledger`
- **L1914** [DB변수명_snake_case] `carryover_ledger` → `| 이월 원장(carryover_ledger) 7.4절 마감 연속성 검증`
- **L1943** [영문코드_UPPER_SNAKE] `POST_TAX, PRE_TAX` → `전체 계정 (PRE_TAX / POST_TAX / CONSIGNMENT)`
- **L1944** [영문코드_UPPER_SNAKE] `PRE_TAX` → `세전 이월 계정 (PRE_TAX · 1단계 합산/상쇄)`
- **L1945** [영문코드_UPPER_SNAKE] `POST_TAX` → `세후 지급대기 계정 (POST_TAX · 11단계 합산)`
- **L1946** [영문코드_UPPER_SNAKE] `CONSIGNMENT_BAL` → `위탁 도서 전용 잔액 (CONSIGNMENT_BAL)`
- **L1955** [설계마커_원문자] `①` → `① 전기말 기초 이월 잔액 (Opening)`
- **L1960** [설계마커_원문자] `②` → `② 당월 정산 합산/상쇄 해소로 인한 원장 변동`
- **L1965** [설계마커_원문자] `③` → `③ 당월 신규 차월이월 적재액 (New Carry-Out)`
- **L1970** [설계마커_원문자] `④` → `④ 당기말 차월 이월 잔액 (Closing)`
- **L1972** [설계마커_원문자] `①, ②, ③, ④` → `7.4절 연속성 등식: ① + ② + ③ = ④ (100% 일치)`
- **L1995** [영문코드_UPPER_SNAKE] `CARRY_IN` → `※ 정본 근거: 제1권 7.3절(최소 지급/청구 하한) · 7.4절(이월 원장 마감 연속성 등식) · 제2권 8.3절 1단계(CARRY_IN) 및 11단계(PAYOUT)`

### `ADMN-SETT-004_baseline.html` (19건)
- **L508** [DB변수명_snake_case] `pg_recon_unclassified_max` → `(pg_recon_unclassified_max = 0건)`
- **L513** [영문코드_UPPER_SNAKE] `UNKNOWN_MISMATCH` → `미분류( 원인 미분류 불일치 (UNKNOWN_MISMATCH) ) 상태의 거래가 1건이라도 존재하면 금액(1원 여부)과 무관하게 해당 거래 귀속 권리자의 정산 마감을 차단합니다.`
- **L525** [DB변수명_snake_case] `pg_recon_tolerance_company` → `(pg_recon_tolerance_company = 1,000원)`
- **L543** [DB변수명_snake_case] `order_items` → `매입 재판매 도서( 매입 재판매 도서 (PURCHASED_RESALE) ) 및 사은품( 강좌 부속·사은품 (BUNDLED) ), 배송비( SHIPPING_FEE )는 정산 엔진 비`
- **L543** [영문코드_UPPER_SNAKE] `PURCHASED_RESALE, SHIPPING_FEE` → `매입 재판매 도서( 매입 재판매 도서 (PURCHASED_RESALE) ) 및 사은품( 강좌 부속·사은품 (BUNDLED) ), 배송비( SHIPPING_FEE )는 정산 엔진 비`
- **L598** [영문코드_UPPER_SNAKE] `UNKNOWN_MISMATCH` → `UNKNOWN_MISMATCH (미분류)`
- **L599** [영문코드_UPPER_SNAKE] `TIMING_GAP` → `TIMING_GAP (기간 귀속차)`
- **L600** [영문코드_UPPER_SNAKE] `PARTIAL_CANCEL_PENDING` → `PARTIAL_CANCEL_PENDING (부분취소 대기)`
- **L601** [영문코드_UPPER_SNAKE] `PG_FEE_DIFF` → `PG_FEE_DIFF (PG 수수료 차감차)`
- **L602** [영문코드_UPPER_SNAKE] `REFUND_TIMING_DIFF` → `REFUND_TIMING_DIFF (환불 처리 시차)`
- **L647** [DB변수명_snake_case] `order_item_id` → `주문 품목(order_item_id) 단위 3계층 과·면세 분할 승인 및 도서정가제 안분 대사 (8.1절)`
- **L649** [DB변수명_snake_case] `book_discount_rate_limit` → `복합 결제(MIXED) 시 교재 정가 할인 0% 고정(`book_discount_rate_limit = 0%`) → 순수 강좌 결제 풀 안분 → 마지막 강좌 잔여 차액 배정 규칙 `
- **L658** [DB변수명_snake_case] `order_item_id` → `주문번호 / 품목 ID (order_item_id)`
- **L659** [DB변수명_snake_case] `item_type` → `품목명 / 유형 (item_type)`
- **L694** [금지어_기출_정오표] `기출문제` → `[자사저작권] 정종대 산업안전 필기 기출문제집  BOOK (OWN_PUBLISHED)`
- **L694** [영문코드_UPPER_SNAKE] `OWN_PUBLISHED` → `[자사저작권] 정종대 산업안전 필기 기출문제집  BOOK (OWN_PUBLISHED)`
- **L705** [영문코드_UPPER_SNAKE] `GOODS_ITEM` → `산준모 합격 타이머 스톱워치  GOODS_ITEM`
- **L716** [영문코드_UPPER_SNAKE] `SHIPPING_FEE` → `도서·굿즈 묶음 배송비  SHIPPING_FEE`
- **L771** [영문코드_UPPER_SNAKE] `TIMING_GAP` → `2026-10 (TIMING_GAP 소명)`

### `ADMN-SETT-005_baseline.html` (34건)
- **L498** [설계마커_원문자] `①, ②` → `①  월간 정산 및 집행( ADMN-SETT-002 ) 에서 특정 정산서를 선택해  [수동 조정 등록] 으로 진입하면 해당 정산서가 자동 바인딩되며, ② 우측 상단  [+ 신규 수`
- **L499** [DB변수명_snake_case] `applied_month, origin_month` → `마감 확정( Locked = True )된 월은 해제하지 않으며,  원 발생 귀속월( origin_month )과 반영 기준월( applied_month )을 분리 해 미마감 당월`
- **L553** [영문코드_UPPER_SNAKE] `RATE_ERR` → `요율 오류 (RATE_ERR)`
- **L554** [영문코드_UPPER_SNAKE] `SHARE_ERR` → `지분율 오류 (SHARE_ERR)`
- **L555** [영문코드_UPPER_SNAKE] `REFUND_OMIT` → `환불 반영 누락 (REFUND_OMIT)`
- **L556** [영문코드_UPPER_SNAKE] `ACCOUNT_TRANSFER` → `계정 간 대체 (ACCOUNT_TRANSFER)`
- **L557** [영문코드_UPPER_SNAKE] `BOOK_SUPPLY_ERR` → `도서 공급 형태 오등록 (BOOK_SUPPLY_ERR)`
- **L558** [영문코드_UPPER_SNAKE] `PRO_RATA` → `지원금 이행률 정산 (PRO_RATA)`
- **L559** [영문코드_UPPER_SNAKE] `CONSIGN_FEE_ERR` → `위탁 수수료율 오류 (CONSIGN_FEE_ERR)`
- **L560** [영문코드_UPPER_SNAKE] `TAX_TYPE_ERR` → `과세유형 오인 (TAX_TYPE_ERR)`
- **L701** [DB변수명_snake_case] `origin_month, origin_settlement_id` → `원 정산서( origin_settlement_id )를 선택하면 수취인 세무 유형과 원 발생 귀속월( origin_month )이 자동 바인딩되며, 마감된 월은 미마감 당월( 20`
- **L709** [DB변수명_snake_case] `origin_settlement_id` → `참조 원 정산서 선택 (origin_settlement_id · 필수)`
- **L729** [DB변수명_snake_case] `adj_reason_code` → `조정 사유 구분 (adj_reason_code · 10.2절 표준 13종)`
- **L731** [영문코드_UPPER_SNAKE] `RATE_ERR` → `요율 오류 (RATE_ERR)`
- **L732** [영문코드_UPPER_SNAKE] `SHARE_ERR` → `지분율 오류 (SHARE_ERR)`
- **L733** [영문코드_UPPER_SNAKE] `REFUND_OMIT` → `환불 반영 누락 (REFUND_OMIT)`
- **L734** [영문코드_UPPER_SNAKE] `PREPAY_OFFSET_ERR` → `선급금 상계액 오류 (PREPAY_OFFSET_ERR)`
- **L735** [영문코드_UPPER_SNAKE] `MMG_CALC_ERR` → `최저보장 보전금 산출 오류 (MMG_CALC_ERR)`
- **L736** [영문코드_UPPER_SNAKE] `SUPPORT_CAP_ERR` → `지원금 한도 판정 오류 (SUPPORT_CAP_ERR · 2차승인 필수)`
- **L737** [영문코드_UPPER_SNAKE] `PRO_RATA` → `지원금 해지 이행률 정산 (PRO_RATA · 2차승인 필수)`
- **L738** [영문코드_UPPER_SNAKE] `ACCOUNT_TRANSFER` → `세전·세후 계정 간 대체 (ACCOUNT_TRANSFER · 2차승인 필수)`
- **L739** [영문코드_UPPER_SNAKE] `TAX_TYPE_ERR` → `과세유형 오인 (TAX_TYPE_ERR)`
- **L740** [영문코드_UPPER_SNAKE] `WITHHOLDING_RATE_ERR` → `원천징수 세율 오류 (WITHHOLDING_RATE_ERR)`
- **L741** [영문코드_UPPER_SNAKE] `BOOK_COUNT_DIFF` → `도서 확정 판매 부수 차이 (BOOK_COUNT_DIFF)`
- **L742** [영문코드_UPPER_SNAKE] `BOOK_SUPPLY_ERR` → `도서 공급 형태 오등록 (BOOK_SUPPLY_ERR)`
- **L743** [영문코드_UPPER_SNAKE] `CONSIGN_FEE_ERR` → `위탁 수수료율 오류 (CONSIGN_FEE_ERR)`
- **L750** [DB변수명_snake_case] `origin_month` → `원 발생 귀속월 (origin_month)`
- **L754** [DB변수명_snake_case] `applied_month` → `반영 기준월 (applied_month · 미마감월 고정)`
- **L768** [DB변수명_snake_case] `adj_account_type` → `이월/반영 계정 구분 (adj_account_type)`
- **L770** [영문코드_UPPER_SNAKE] `PRE_TAX` → `세전 계정 (PRE_TAX · 과세표준 반영)`
- ... 외 4건

### `ADMN-SETT-006_baseline.html` (3건)
- **L475** [DB변수명_snake_case] `mmg_promo_overlap_flag` → `⚠️ [15.2절 · 부록 B] MMG 보전금 &amp; 합격 환급반 차감 동시 발생 감지 ( mmg_promo_overlap_flag = true )`
- **L511** [DB변수명_snake_case] `mmg_promo_overlap_flag` → `mmg_promo_overlap_flag = true`
- **L625** [DB변수명_snake_case] `cap_restore_on_refund` → `cap_restore_on_refund = true 연동`

### `ADMN-SETT-007_baseline.html` (9건)
- **L335** [DB변수명_snake_case] `payee_is_author` → `승계 확정일 기준 저작자 본인 여부(payee_is_author) 전환`
- **L406** [영문코드_UPPER_SNAKE] `PAYEE_SPLIT` → `⚖️ 8단계(PAYEE_SPLIT) 분할 대상 포함·제외 매트릭스 및 변경 감사 이력`
- **L415** [DB변수명_snake_case] `payee_split_base` → `2계층 분할 여부 ( payee_split_base )`
- **L424** [DB변수명_snake_case] `payee_id, split_ratio` → `라인별로  내림(라인 세전액 × 분할 비율)  산출 후 마지막 수취인( split_ratio  내림차순 →  payee_id  오름차순)에게 총액 역산 잔여액 배정`
- **L430** [DB변수명_snake_case] `payee_is_author` → `기본 R/S와 합산하지 않고 라인 단위로 독립 분할·절사한 뒤, 9단계에서 수취인별 세무 유형 및  payee_is_author  지위 독립 적용`
- **L434** [영문코드_UPPER_SNAKE] `PREPAY_OFFSET` → `6단계 선급금 상계액 ( PREPAY_OFFSET )`
- **L440** [영문코드_UPPER_SNAKE] `POST_TAX, PRE_TAX` → `전월 이월액 ( PRE_TAX  세전 미지급 /  POST_TAX  세후 지급대기) 및 전속계약금 반환액`
- **L448** [영문코드_UPPER_SNAKE] `ADMN_AUDIT_LOG` → `2) 2계층 수취인 분할 지분율 변경 · 상속 승계 감사 로그 ( ADMN_AUDIT_LOG )`
- **L484** [DB변수명_snake_case] `active_contracts` → `🔍 대상 계약 검색 및 선택 (유효 계약 마스터  active_contracts )`

### `ADMN-SETT-008_baseline.html` (14건)
- **L569** [DB변수명_snake_case] `tax_type_cd` → `국세청 과세유형 코드(tax_type_cd) ↔ 세무 판정 매트릭스 자동 매핑 설정표 (17.3절 · 읽기 전용)`
- **L571** [DB변수명_snake_case] `nts_tax_type_map` → `코드에 문자열을 하드코딩하지 않고 설정 테이블( nts_tax_type_map )로 관리하며, 도서 재화 공급(위탁자·매입처)은 과세유형과 무관하게 도서 면세( TX-11 )를 우`
- **L598** [영문코드_UPPER_SNAKE] `SIMPLIFIED_RECEIPT` → `간이과세자-영수증발급 ( SIMPLIFIED_RECEIPT )`
- **L605** [영문코드_UPPER_SNAKE] `SIMPLIFIED_INVOICE` → `간이과세자-세금계산서발급 ( SIMPLIFIED_INVOICE )`
- **L614** [영문코드_UPPER_SNAKE] `PENDING_REVIEW` → `개인 사업자는  TX-08  (면세 계산서 역발행) /  법인(법인번호 보유)은 인적용역 면세 배제 → 후보 TX-09 또는 TX-07 부여 후  세무 판정 보류(PENDING_R`
- **L619** [영문코드_UPPER_SNAKE] `NON_PROFIT_ORG` → `비영리·고유번호 단체 ( NON_PROFIT_ORG )`
- **L621** [영문코드_UPPER_SNAKE] `PENDING_REVIEW` → `인세·매절은 후보  TX-09 , 강의·약정·지원금은 후보  TX-07  부여 후   세무 판정 보류(PENDING_REVIEW) 로 격리 (마감 차단)`
- **L660** [DB변수명_snake_case] `nts_check_validity_days` → `nts_check_validity_days`
- **L666** [DB변수명_snake_case] `nts_batch_chunk_size, nts_batch_interval_ms` → `nts_batch_chunk_size / nts_batch_interval_ms`
- **L672** [DB변수명_snake_case] `nts_retry_max_count` → `nts_retry_max_count`
- **L678** [DB변수명_snake_case] `nts_periodic_check_schedule` → `nts_periodic_check_schedule`
- **L1231** [DB변수명_snake_case] `tax_type_change_dt` → `⚠️ 17.5절 하드락 규칙:  국세청 API 응답의  tax_type_change_dt 가 빈값("")일 때 7월 1일 등으로 일괄 가정하는 것을 엄격히 금지하며, 수취한 정정 `
- **L1254** [영문코드_UPPER_SNAKE] `CLOSED_BY_TRANSITION` → `CLOSED_BY_TRANSITION`
- **L1272** [영문코드_UPPER_SNAKE] `PENDING_REVIEW` → `✔ 17.5절 행 분할 승인 및 PENDING_REVIEW 해제 확정`

### `ADMN-SETT-009_baseline.html` (19건)
- **L300** [DB변수명_snake_case] `is_internal` → `본 화면은  자사 계정(주식회사 엘캠퍼스,  is_internal = true ) 귀속분 과  일반 상품 판매매출(Pipeline 2.3,  TX-13 ) 을 외부 권리자 지급액과`
- **L397** [DB변수명_snake_case] `own_copyright_yn` → `📌 [규격 검증 1] 부록 D-15 · 자사 저작권 도서(`own_copyright_yn = true`) 외부 강사 지원금 차감`
- **L400** [DB변수명_snake_case] `book_authors` → `정종대 강사 집필  [자사저작권] 산업안전 실기 빈출문제집(PROD-BK-1004) 은 저작권이 당사에 귀속되어  book_authors 에 자사( RH-INTERNAL ) 100`
- **L407** [DB변수명_snake_case] `own_copyright_yn` → `외부 저자 인세 (Pipeline 2.1 ·  own_copyright_yn = true )`
- **L496** [DB변수명_snake_case] `goods_master, item_type` → `•  일반 소비재( goods_master ,  item_type = GOODS_ITEM ) 는 일반 상품 판매매출(Pipeline 2.3)로 인입하여 1단계 상위 공식에서  공급`
- **L496** [영문코드_UPPER_SNAKE] `GOODS_ITEM` → `•  일반 소비재( goods_master ,  item_type = GOODS_ITEM ) 는 일반 상품 판매매출(Pipeline 2.3)로 인입하여 1단계 상위 공식에서  공급`
- **L497** [영문코드_UPPER_SNAKE] `INVENTORY_PURCHASE, PURCHASED_RESALE` → `•  사입 도서( 매입 재판매 도서 (PURCHASED_RESALE) , Case 11)  및  사은품 도서( 강좌 부속·사은품 (BUNDLED) ) 는 권리자 정산 파이프라인에 `
- **L518** [DB변수명_snake_case] `item_type` → `사입 재판매 (PURCHASED_RESALE)  item_type = GOODS_ITEM`
- **L518** [영문코드_UPPER_SNAKE] `GOODS_ITEM, PURCHASED_RESALE` → `사입 재판매 (PURCHASED_RESALE)  item_type = GOODS_ITEM`
- **L530** [영문코드_UPPER_SNAKE] `PURCHASED_RESALE` → `사입 재판매 (PURCHASED_RESALE)  원 판매 스냅샷 대칭 역참조`
- **L542** [DB변수명_snake_case] `book_supply_type_snapshot` → `매입 재판매 도서 (PURCHASED_RESALE)  book_supply_type_snapshot`
- **L542** [영문코드_UPPER_SNAKE] `PURCHASED_RESALE` → `매입 재판매 도서 (PURCHASED_RESALE)  book_supply_type_snapshot`
- **L560** [영문코드_UPPER_SNAKE] `MARKETING_EXPENSE` → `300,000원  (판촉비 · MARKETING_EXPENSE)`
- **L588** [DB변수명_snake_case] `payment_event_date, pending_negative_base, taxable_base` → `taxable_base IS NOT NULL  및 원천징수 사건 성립( payment_event_date IS NOT NULL ) 확정 라인만 집계. 지급 하한 미달 보류( PRE`
- **L588** [영문코드_UPPER_SNAKE] `PRE_TAX` → `taxable_base IS NOT NULL  및 원천징수 사건 성립( payment_event_date IS NOT NULL ) 확정 라인만 집계. 지급 하한 미달 보류( PRE`
- **L602** [DB변수명_snake_case] `income_clause` → `기타소득 중  인적용역 일시 제공( income_clause = C19 ) 라인만 한정 추출 . 원고료·인세( C15 ), 저작권 승계( C05 ), 사례금( C17 )은 법령상 `
- **L609** [영문코드_UPPER_SNAKE] `POST_TAX, PRE_TAX` → `대여금 방식 선급금 상계( LOAN ), 세후 지급대기 이월( POST_TAX ) 합산, 지급 하한 미달 보류( PRE_TAX ), 전속계약금 세후 반환,  재화 공급(원천징수 비`
- **L616** [설계마커_원문자] `①, ②, ③` → `주문 품목( order_item_id ) 기준 ① 교육용역 면세(제26조 제1항 제6호), ② 도서 재화 면세(제26조 제1항 제8호), ③ 저작권 인적용역 면세(제15호 계통, `
- **L616** [DB변수명_snake_case] `order_item_id` → `주문 품목( order_item_id ) 기준 ① 교육용역 면세(제26조 제1항 제6호), ② 도서 재화 면세(제26조 제1항 제8호), ③ 저작권 인적용역 면세(제15호 계통, `

### `ADMN-SETT-011_baseline.html` (5건)
- **L119** [DB변수명_snake_case] `ship_ordered_at, tracking_no` → `백오피스 출고 원장( ADMN-ORD-002  송장번호  tracking_no ,  ship_ordered_at  확정분)과 계약 택배 대리점의 월간 운임 청구서(엑셀)를 대조합니`
- **L332** [DB변수명_snake_case] `tracking_no` → `송장번호 (tracking_no)`
- **L357** [영문코드_UPPER_SNAKE] `CANCELLED_BILLED` → `출고지시 회수건 청구 (CANCELLED_BILLED)`
- **L483** [DB변수명_snake_case] `tracking_no` → `1. 업로드 파일의  운송장번호 와 백오피스 출고 원장( ADMN-ORD-002.tracking_no )을 1:1 대조합니다.`
- **L484** [영문코드_UPPER_SNAKE] `CANCELLED_BILLED` → `2. 발송 전  출고지시 회수(취소)  처리된 주문에 발급되었던 가송장이 청구된 경우  CANCELLED_BILLED 로 자동 분류하여 과오청구를 차단합니다.`

### `ADMN-USER-001_baseline.html` (20건)
- **L601** [DB변수명_snake_case] `sanjun_hong88` → `sanjun_hong88`
- **L615** [DB변수명_snake_case] `safety_kim26` → `safety_kim26`
- **L629** [DB변수명_snake_case] `park_jw90` → `park_jw90`
- **L646** [DB변수명_snake_case] `lee_sjm77` → `lee_sjm77`
- **L660** [DB변수명_snake_case] `choi_min33` → `choi_min33`
- **L677** [DB변수명_snake_case] `jung_sky20` → `jung_sky20`
- **L733** [DB변수명_snake_case] `admin_access_log` → `클릭 즉시  admin_access_log 에 계정·일시·IP·대상 회원번호가 기록됩니다.`
- **L745** [DB변수명_snake_case] `is_locked` → `로그인 실패 0회 (is_locked=false)`
- **L781** [DB변수명_snake_case] `is_marketing_agreed` → `( users.is_marketing_agreed = true  · 2026.08.19 동의 · 하단 [변경사항 저장] 시 반영)`
- **L798** [영문코드_UPPER_SNAKE] `SUPER_ADMIN` → `비밀번호 수동 초기화 (SUPER_ADMIN)`
- **L1057** [DB변수명_snake_case] `admin_kim` → `CS 김상담 (admin_kim)`
- **L1064** [DB변수명_snake_case] `admin_lee` → `재무 이정산 (admin_lee)`
- **L1250** [DB변수명_snake_case] `cafe_member_id` → `users.cafe_member_id IS NOT NULL`
- **L1305** [DB변수명_snake_case] `unpaid_points_blacklist` → `마이너스 포인트 부채 잠금 (unpaid_points_blacklist)`
- **L1379** [DB변수명_snake_case] `admin_kim` → `요청 관리자:  admin_kim (김운영 · 회원관리팀)`
- **L1403** [DB변수명_snake_case] `admin_access_log` → `선택한 항목 조합이 그대로  admin_access_log 에 기록됩니다.`
- **L1570** [영문코드_UPPER_SNAKE] `TPL_CS_GUIDE` → `[TPL_CS_GUIDE] 1:1 고객센터 안내 및 처리 결과 통지 (SENS 승인완료)`
- **L1571** [영문코드_UPPER_SNAKE] `TPL_VBANK_ISSUED` → `[TPL_VBANK_ISSUED] 가상계좌 입금 계좌 및 기한 재안내 (SENS 승인완료)`
- **L1572** [영문코드_UPPER_SNAKE] `TPL_DLV_START` → `[TPL_DLV_START] 교재 출고 및 송장번호 개별 안내 (SENS 승인완료)`
- **L1573** [영문코드_UPPER_SNAKE] `TPL_RFD_DONE` → `[TPL_RFD_DONE] 환불 처리 완료 안내 (SENS 승인완료)`

### `ADMN-USER-007_baseline.html` (21건)
- **L313** [DB변수명_snake_case] `pii_unmask_ttl_seconds` → `pii_unmask_ttl_seconds = 30초  경과 시 자동 잠금`
- **L321** [DB변수명_snake_case] `destruction_hold` → `계층 3 파기 보류 예외 (`destruction_hold`)  분리 보관`
- **L332** [DB변수명_snake_case] `pii_destruction_field_map` → `3. 개인정보 파기 필드 매핑 (`pii_destruction_field_map`) 및 열람 이력`
- **L376** [DB변수명_snake_case] `rights_holder_id` → `•  계층 1(개인식별정보: 국세기본법 법정신고기한 + 5년)  기한이 도래하면 주민등록번호·신분증 사본·연락처·주소만 복구 불가능하게 파기하고,  계층 2(계약서 및 회계 정산 `
- **L377** [DB변수명_snake_case] `destruction_hold` → `•  계층 3(파기 보류 예외,  destruction_hold = true ) : 미상계 선급금 잔액 존재, 미소진 지원금 한도( ACTIVE ), 대손 채권, 세무조사·소송 진`
- **L387** [DB변수명_snake_case] `destruction_hold` → `계층 3 파기 보류 (`destruction_hold`) 사유`
- **L400** [DB변수명_snake_case] `pii_destruction_field_map` → `🗂️ 개인정보 파기 필드 매핑 설정표 (`pii_destruction_field_map`) 및 당일 열람 로그`
- **L404** [DB변수명_snake_case] `pii_destruction_field_map` → `1) 필드별 파기 · 비식별 전환 · 원장 영구 보존 매핑 (`pii_destruction_field_map`)`
- **L417** [DB변수명_snake_case] `rights_holders, rrn_encrypted` → `rights_holders.rrn_encrypted`
- **L421** [DB변수명_snake_case] `rights_holder_id` → `영향 없음 ( rights_holder_id  조인 유지)`
- **L424** [DB변수명_snake_case] `bank_account_enc, rights_holders` → `rights_holders.bank_account_enc`
- **L431** [DB변수명_snake_case] `holder_name, rights_holders` → `rights_holders.holder_name`
- **L438** [DB변수명_snake_case] `id_cards` → `s3://private-bucket/id_cards/*`
- **L445** [DB변수명_snake_case] `settlement_statements` → `settlement_statements.*`
- **L454** [영문코드_UPPER_SNAKE] `ADMN_AUDIT_LOG` → `2) 민감 정보 열람 및 파기 실행 감사 로그 (`ADMN_AUDIT_LOG` 실시간 적재 내역)`
- **L482** [DB변수명_snake_case] `pii_unmask_ttl_seconds` → `부록 B 파라미터:  pii_unmask_ttl_seconds = 30초  · 암호화:  AES-256 (AWS KMS)`
- **L500** [DB변수명_snake_case] `pii_unmask_ttl_seconds` → `요청하신 항목은 AES-256 암호화 보호 대상입니다. 열람 또는 사본 다운로드 시  작업자 ID, IP, 열람 시각, 입력 사유가 시스템 감사 로그( ADMN-CONF-010 )`
- **L565** [DB변수명_snake_case] `admin_settle_mgr` → `•  실행 승인자:  admin_settle_mgr (박정산 / ROLE_FINANCE_ADMIN)`
- **L565** [영문코드_UPPER_SNAKE] `ROLE_FINANCE_ADMIN` → `•  실행 승인자:  admin_settle_mgr (박정산 / ROLE_FINANCE_ADMIN)`
- **L566** [DB변수명_snake_case] `destruction_hold` → `•  처리 결과:  대상 1건 정상 처리, 예외 보류( destruction_hold ) 1건 안전 격리(미파기 유지)`
- **L610** [DB변수명_snake_case] `settlement_recipient_id` → `• 권리자 대체 식별자 ( settlement_recipient_id )`
