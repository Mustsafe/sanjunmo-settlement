# 프로젝트 상태 — 산준모닷컴 정산·백오피스

> 이 문서는 **지금 어디까지 왔나**를 기록한다: 확정 기준, 기준선, 현재 상태·미결, 작업 로그.
> 작업 방법은 `.claude/CLAUDE.md`, 프로젝트 소개·정책·화면 목록은 `README.md`, 안티그래비티 예비 사용법은 `.agents/rules/RULES.md`.
> 최초 등록: 2026-10-20(`.antigravity/AGENT_PIPELINE_MEMORY.md`) · 2026-10-22 v6.7에서 저장소 루트로 옮기고 역할 규칙을 덜어냄 · 최종 갱신: 2026-10-22 (v6.17 기준)

---

## 1. 확정 기준

**문서 우선순위**
- 1순위: `README.md` 및 white의 실시간 지시
- 2순위: `docs/산준모닷컴 구축 통합 상세 설계서.md`, `docs/[산준모 정산시스템]_00~04.md`
- 3순위(참고용): `docs/screen_spec/*.md`

**프로토타입**
- `prototype/`은 기획 검수용(상단 정책 배너, 정책 문구·괄호 병기 유지), `prototype_clean/`은 운영 UI만. 기능 패치는 양쪽 동명 파일에, 표기 정리는 clean 우선이며 prototype/ 괄호 병기는 수정하지 않는다.
- 역할 그룹은 고정값이 아니라 운영자 권한 관리(CONF-005)에서 추가 · 수정 · 미사용하는 변수다(삭제 대신 미사용, 소속 계정 · 1:1 문의 분류가 쓰는 그룹은 미사용 차단). 최초값 8종: 최고 관리자 · CS담당자 · 물류팀 · 재무팀 · 강사 · 조교(화면설계서 v12 예시) + 저작권자 · 외부 3PL(README). 화면 표기는 이 이름으로 통일하고, 역할 그룹 · 1:1 문의 분류를 쓰는 화면은 이름을 직접 적지 않고 `common-master.js`(`SJM_MASTER`)에서 읽는다(2026-10-22 확정).
- 1:1 문의 분류의 담당 부서 큐는 역할 그룹 중 '1:1 문의 담당 큐'로 지정한 그룹이며 복수 선택 가능. 여러 부서 큐에 올라간 건도 먼저 답변 화면에 들어간 사람이 담당자(선점), 다른 사람이 처리 중인 건은 읽기 전용(BRD-002 · BRD-001 상품 Q&A, 2026-10-22 확정).
- 등록 · 상세(S1) 화면은 프로토타입에서 모달로 표현하고, 실제 개발은 화면설계서 v12의 별도 페이지 기준을 따른다(2026-10-22 확정).
- clean HTML 원문의 화면 코드(`ADMN-*`)는 지우지 않는다. 설계서·API·QA·권한의 공통 키라 원문에 남기고, 화면 표시는 `common-snb.js` 런타임 치환으로 가린다(2026-10-22 확정).
- `screen_spec/`의 원형 번호(`①~⑭`, `[마커 N]`)나 기획 설명 문구를 UI에 노출하지 않는다. 가짜 상단 탭 스위처 대신 실제 SNB와 화면 내 동선 버튼을 쓴다.
- 업무플로우 페이지(`00_WORKFLOW_GUIDE_baseline.html`)는 clean에서 작업 후 prototype/으로 덮어쓴다. 코드값 비노출, 화면 코드는 회색 라벨.
- SNB: 정본 9개 그룹 · 메뉴 44개(v6.10에서 BRD-007 추가), 양쪽 `SNB_GROUPS` 동일. 정본 명칭이 길면 축약 허용.
- 원천세·지급명세서 산출물은 SETT-009 4번 탭(`?view=taxreport`, 별도 화면 코드 없음 — SETT-010은 미사용). 감사 로그는 CONF-010 "시스템 감사 로그" 하나로 통합(구 CONF-006 운영자 작업 로그는 CONF-010 3번 탭 `?view=access`, CONF-006 결번). USER-007은 "민감 정보 보관·열람 통제"(10자 열람 사유 팝업 포함, 환불 수취계좌 암호화 보관)이며 "개인정보 · 보안 감사" 그룹. 합격환급 심사는 SETT-006으로 일원화(RFD-002의 RFD-001 뷰 제거). SETT-011은 3PL 물류비 대사(출고·수수료 / 배송비·반품 / 도서 매입 계산서 탭). 메뉴별 접근 권한은 CONF-005 RBAC 권한 매트릭스에 둔다(BRD-007은 CS 메뉴 비노출) (2026-10-22 확정).
- BRD 화면 번호는 화면설계서 v12 기준(2026-10-22 확정): 001 공지, 002 1:1 문의, 003 상품 Q&A, 004 학습 Q&A, 005 후기, 006 FAQ, 007 문의 분류, 009 당첨자, 010 무료콘텐츠. 파일은 BRD-001(공지·FAQ·상품 Q&A·학습 Q&A·당첨자 탭), BRD-002(1:1 문의 허브), BRD-005(수강후기·합격수기·무료특강 탭 3개), BRD-007(1:1 문의 분류 마스터, "사이트 · 약관 · 메시지 설정" 그룹, 운영 관리자 이상 전용 — BRD-002에서 바로가기).
- 정답지는 독립 화면이 아니라 운영자가 무료콘텐츠(BRD-010) 제목에 붙이는 표기. 1:1 문의는 BRD-002 한 곳에서만 처리. 학습 Q&A는 1차 오픈 카페 아웃링크지만 2차 고도화 대비로 관리 탭을 동작 상태로 유지. 커뮤니티/신고는 설계에 없어 제거. 자유게시판도 1차 범위 아님(2026-10-22 확정).
- 업무플로우 정산은 3단계(STAGE 01~03), 상시 감사는 STAGE 03 하위 상시 블록, 예외 케이스는 접힘으로 주 흐름과 분리.

---

## 2. QA 도구 (`scripts/qa/`, 읽기 전용 — HTML을 수정하지 않음)

| 도구 | 파일 | 기능 | 상태 |
| :--- | :--- | :--- | :--- |
| 정적 문법 검사 | `skill_static_lint.py` | 인라인 `<script>` 문법(Node.js 파싱), 깨진 로컬 링크(SNB 포함), 중복 ID, 채우는 스크립트 없는 빈 `<tbody>`, 공통 에셋 `id` 규격 경고. 폴더 인자 선택(기본 양쪽), `--strict` → `scripts/qa/reports/STATIC_LINT_REPORT.md` | 구축 |
| 금지어 스캔 | `skill_jargon_scan.py` | 금지어(`기출`, `정오표`, `Vimeo`, `80%`, `①~⑭`, `[마커`)·기획서 내부 암호(`C-01~04`, `H-01~05`, `D-1~16`, `P1.1~5.1`, `_flag`, `_yn`, `_id` 등)·번역 중복어 탐지 → `scripts/qa/reports/JARGON_SCAN_REPORT.md` | 구축 |
| 화면 간 데이터 대조 | `skill_cross_data_check.py` | 권리자 코드(RH)↔이름 충돌, 같은 이름의 다른 코드, 계약(CON)↔권리자 불일치, 도서 코드(BK) 형식 혼재 · 같은 도서명의 다른 코드(참고: 한 코드의 여러 도서명). 기본 `prototype_clean`, `--strict` → `scripts/qa/reports/CROSS_DATA_CHECK_REPORT.md` | 구축 |
| E2E | `skill_playwright_e2e.py` | 모달 열기/닫기, 탭 전환, 레이아웃 겹침. 폴더 인자 필수(`prototype` / `prototype_clean`) → `scripts/qa/reports/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md` | 구축 |
| 괄호 중복 스캔 | `scan_paren_dup.py` | 렌더링 후 괄호 중복 탐지(양쪽) + clean 원문 `ADMN-` 코드 자리 집계 → `scripts/qa/reports/PAREN_DUP_*.md` | 구축 |

리포트 폴더 `scripts/qa/reports/`는 `.gitignore`에 등록돼 있다(실행할 때마다 새로 생성).

---

## 3. 완료된 작업 기준선
- `prototype/` 및 `prototype_clean/` 활성 37개 화면 동기화 완료 (2026-10-21 `patch_all_snb_v3.html` 보관 후 기준)
- `ADMN-ORD-001`, `PROD-003`, `PROD-005` 인강·교재 면세(`EXEMPT`) 정합화 완료
- 전 화면 모달 닫기 핫픽스(`common-v84.css`, `common-snb.js`) 완료
- `ADMN-SETT-006` 가로 100% 목록/검색필터/상세모달 개편 + 4대 제출 자료(합격증 사본, 산준모 카페 합격수기 아웃링크, 통장사본, 1금융권 실명계좌) 반영 완료
- (2026-10-21) 업무플로우 페이지 v5 전면 개편 및 prototype/ 반영, SNB 9개 그룹·메뉴 43개 양쪽 정렬, 전 화면 브레드크럼 정본 그룹명 적용
- (2026-10-21) 정답지 독립 화면 폐지(BRD-005 탭 정리, CONF-005 저작권자 권한 문구 정리), 미실행 옛 SNB 코드 삭제
- (2026-10-21) clean 렌더링 괄호 중복 163건 → 1건(SETT-006 금액 표기, 정상 유지)
- (2026-10-21) SETT-005 "신규 수동 조정 등록" 모달 3개 진입 경로(카드 버튼·상단 버튼·SETT-002 `?fromStmt=` 자동 오픈) 정상화

---

## 4. 현재 상태 및 다음 작업 (2026-10-22 · v6.17 기준)

**상태**
- 활성 화면 38개(양쪽 폴더). E2E `prototype_clean` 38/38, `prototype` 38/38 PASS (v6.10 기준), 콘솔 에러 0건.
- 괄호 중복: clean 1건(정상), prototype 6건(기획 검수용 기준으로 유지).
- 공통 모달 닫기 핫픽스(`UNIVERSAL-MODAL-CLOSER-HOTFIX`)의 함정은 `.claude/CLAUDE.md` "알려진 함정" 참고.

**미결 사항**
- 2단계 진행 예정(2026-10-22 white 지시): ① 거래처 관리 화면 신설(도서 · 상품 매입처, 물류 대행사 3PL, 이후 공급 파트너 — BOOK-001은 도서 한정이라 분리) ② 계정 소속 구분(내부 직원 / 권리자 — 계약 원장의 계약 당사자, 계약 유형으로 구분 / 거래처) — 외부 파트너는 역할 그룹과 다른 축 ③ 설계 문서 수정: 통합설계서 파트너 3분류(강사 · 저작권자 · 3PL)는 예시로 고치고 계약 유형 · 거래처 기준으로, 3PL을 권리자 계약 원장에 등재할 수 없는 문제 보완, 역할 그룹 관리 · 담당 선점 반영(통합설계서 · README 2.5 · 정산 02 · 03권, 개정 이력).

**다음 작업: 개별 HTML 점검 및 동작 오류 세부 수정**
1. white가 화면·증상을 지정(스크린샷 포함 가능).
2. Claude Code가 원인 진단 → 양쪽 폴더 패치 → 해당 동작 Playwright 검증 + E2E 2회.
3. diff를 white에게 보여주고 승인 후 커밋·푸시, 아래 작업 로그에 1줄.

---

## 5. 작업 로그
> 2026-10-22 v6.4에서 `_archive/`, `.antigravity/reports/`, 일회성 스크립트를 저장소에서 정리했다. 아래 표에 나오는 스크립트·리포트 중 지금 없는 파일은 git 이력에서 꺼내 본다(예: `git log --all -- <경로>` → `git show <커밋>^:<경로>`).

| 일자 | 작업 | 산출물 |
| :--- | :--- | :--- |
| 2026-10-20 | 역할 고정 메모리 생성, Skill 2(금지어·내부 암호 스캐너) 구축 및 최초 스캔 | `.antigravity/RULES.md`, `.antigravity/AGENT_PIPELINE_MEMORY.md`, `scripts/qa/skill_jargon_scan.py`, `.antigravity/reports/JARGON_SCAN_REPORT.md` |
| 2026-10-20 | `patch_missing_3_features.py` 실행 — USER-004 진도율 보정 원장(카드 4·5번)·USER-006 태그 생성/그룹-태그 연결(카드 1·2번)·RFD-003-S2 별도 보정 거래, prototype/·prototype_clean/ 동기 적용 | `prototype*/ADMN-USER-001_baseline.html`, `prototype*/ADMN-RFD-002_baseline.html`, `.antigravity/reports/JARGON_SCAN_REPORT.md` |
| 2026-10-20 | `hotfix_ssr_initial_rows.py` 실행 — USER-001 차시·보정이력·그룹 3개 테이블 SSR 초기 행 내장 및 Skill 4(Playwright E2E 검수기) 구축·38/38 PASS 검증 | `prototype*/ADMN-USER-001_baseline.html`, `scripts/qa/skill_playwright_e2e.py`, `.antigravity/reports/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md` |
| 2026-10-20 | `fix_rfd002_ssr_row.py` 실행 — RFD-002 보정 거래 원장(m3f-rfd-adj-body) SSR 초기 행 내장 완료, 38/38 PASS 유지 | `prototype*/ADMN-RFD-002_baseline.html`, `.antigravity/reports/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md` |
| 2026-10-20 | `clean_all_jargon_zero.py` (v2) 실행 — JS 100% 보호형 DOM 가시 텍스트 기획서 암호·금지어 일괄 정제 (333건➔37건, 89% 감축, 38/38 ALL PASS 유지) | `prototype*/*.html`, `.antigravity/reports/JARGON_SCAN_REPORT.md`, `.antigravity/reports/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md` |
| 2026-10-20 | `clean_remaining_jargon_v3.py` 실행 — 잔여 DOM 34건 및 고정 문자열 핀셋 정제 (DOM 잔여 3건으로 99.1% 종결, 28개 화면 무결, 38/38 ALL PASS 유지) | `prototype*/*.html`, `.antigravity/reports/JARGON_SCAN_REPORT.md`, `.antigravity/reports/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md` |
| 2026-10-20 | `update_book_discount_policy.py` 실행 — 도서정가제 기본할인 최대 10% 허용 및 실결제액 기준 정산/인세/무료배송 반영, 위탁도서 모수선택권 정본·프로토타입 전수 동기화 (38/38 ALL PASS 유지) | `README.md`, `docs/*.md`, `prototype*/*.html`, `.antigravity/reports/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md` |
| 2026-10-20 | `sync_all_docs_book_policy_v2.py` 실행 — 잔여 기획서(01/03/04/B2C) 및 ADMN-INST-001 위탁도서 정산모수 선택 UI/정책 동기화 (38/38 ALL PASS 유지) | `docs/*.md`, `prototype*/*.html`, `.antigravity/reports/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md` |
| 2026-10-20 | Set 1~4 통합설계서 재구조화 플랜 수립 및 사본(v4.0_통합본) AI 거버넌스 헤더 주입 (`fix_step0_and_add_header.py`) | `docs/SET1_TO_4_ALIGNMENT_PLAN.md`, `docs/산준모닷컴 구축 통합 상세 설계서_v4.0_통합본.md`, `README.md` |
| 2026-10-20 | Set 1 통합설계서 3단 통폐합(v4.0_통합본) 및 구매적립(적립 P) vs 무상(무상 P) 포인트 용어 표준화 전수 반영 (`execute_set1_alignment_v2.py`, 38/38 ALL PASS) | `docs/산준모닷컴 구축 통합 상세 설계서_v4.0_통합본.md`, `docs/SET1_TO_4_ALIGNMENT_PLAN.md`, `prototype*/*.html`, `.antigravity/reports/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md` |
| 2026-10-20 | Set 2 통합설계서 3단 통폐합(v4.0_통합본) 및 ADMN-PROD-003 1계층 지분(100%) vs 계약 R/S 요율(35%) 분리 정합성 패치 (`execute_set2_alignment.py`, 38/38 ALL PASS) | `docs/산준모닷컴 구축 통합 상세 설계서_v4.0_통합본.md`, `docs/SET1_TO_4_ALIGNMENT_PLAN.md`, `prototype*/ADMN-PROD-003_baseline.html`, `.antigravity/reports/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md` |
| 2026-10-20 | Set 3 통합설계서 3단 통폐합(v4.0_통합본) 및 토스페이먼츠 5대 결제수단·3PL·부분환불 정합성 패치 (`execute_set3_alignment.py`, 38/38 ALL PASS) | `docs/산준모닷컴 구축 통합 상세 설계서_v4.0_통합본.md`, `docs/SET1_TO_4_ALIGNMENT_PLAN.md`, `.antigravity/reports/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md` |
| 2026-10-20 | Set 4 통합설계서 3단 통폐합(v4.0_통합본) 완결(구 4·5장 전수 흡수 3장 체제) 및 15개 프로토타입('정답지'·4대 세무증빙정정·국세청 수기예외 등) 동기화 (`execute_set4_alignment.py`, 38/38 ALL PASS) | `docs/산준모닷컴 구축 통합 상세 설계서_v4.0_통합본.md`, `docs/SET1_TO_4_ALIGNMENT_PLAN.md`, `prototype*/*.html`, `.antigravity/reports/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md` |
| 2026-10-20 | 작업용 플랜 2건(SET1_TO_4, BACKOFFICE) 및 구버전 설계서 원본 `_archive/docs/`로 보관, v4.0 통합본을 대표 정본(`산준모닷컴 구축 통합 상세 설계서.md`)으로 확정 (docs 폴더 클린업 완결) | `docs/*.md`, `_archive/docs/*.md`, `README.md`, `sync_to_gdrive.ps1` |
| 2026-10-21 | 업무플로우 페이지 v5 clean 전면 개편(첫 화면 진입 카드 2장, 운영 3세트, 정산 3단계, 화면 디렉터리) | `prototype_clean/00_WORKFLOW_GUIDE_baseline.html`, 커밋 `6e74a31` |
| 2026-10-21 | v5.1~v5.3 SNB 정렬(SETT-010·CONF-006 메뉴 제거, USER-007 보안 그룹), 브레드크럼 정본 그룹명, prototype/ `SNB_GROUPS` 정렬, 업무플로우 prototype/ 덮어쓰기(6단계) | `prototype*/common-snb.js`, `prototype*/*.html`, 커밋 `3c8c53c` 외 |
| 2026-10-21 | v5.4 정답지 정리(BRD-005 탭 제거, 치환표 정리), 옛 SNB 코드 삭제, `patch_all_snb_v3.html` 보관(활성 37개), E2E 폴더 인자 추가 | `prototype*/ADMN-BRD-005_baseline.html`, `scripts/qa/skill_playwright_e2e.py` |
| 2026-10-21 | v5.5 CONF-005 저작권자 권한 정답지 문구 제거, E2E 스크립트 LF 복원 | `prototype*/ADMN-CONF-005_baseline.html`, 커밋 `3ed5618` |
| 2026-10-21 | v5.6~v5.8 clean 괄호 중복 정리(코드만 든 괄호 선제거, 원문 중복 수정) 163건 → 1건, `scan_paren_dup.py` 구축 | `prototype_clean/common-snb.js`, `prototype_clean/*.html`, 커밋 `790d650` 외 |
| 2026-10-21 | v5.9 파이프라인 메모리 갱신(운영 규칙 0-2, 현재 상태 5절) | `.antigravity/AGENT_PIPELINE_MEMORY.md` |
| 2026-10-21 | v6.0 SETT-005 신규 수동 조정 모달 표시 수정 — `#newAdjModal` ID 우선 표시 CSS 1줄, `openNewAdjModal()`에서 인라인 display 잠금 해제(상단 버튼 포함), 검증 T1~T5 PASS, E2E 양쪽 37/37 | `prototype*/ADMN-SETT-005_baseline.html`, `.antigravity/reports/V6.0_RESULT.md`, 커밋 `9768b9d` |
| 2026-10-21 | v6.1 SETT-002 → SETT-005 `?fromStmt=` 자동 오픈 수정 — 열 때 `open` 클래스 부여·닫을 때 제거(핫픽스 로드 시점 잠금 예외), 검증 T1~T7 PASS, E2E 양쪽 37/37 | `prototype*/ADMN-SETT-005_baseline.html`, `.antigravity/reports/V6.1_RESULT.md`, 커밋 `2645a08` |
| 2026-10-21 | v6.1-c SETT-005 진단 리포트 4개·진단 스크립트 4개 삭제, v6.0 백업 추적 해제(로컬 유지) | 커밋 `eb18c45` |
| 2026-10-21 | v6.2 역할 재편(Claude Code 단일 체계) — 루트 `CLAUDE.md` 신설, 본 문서·`RULES.md`에 재편 안내 추가 | `CLAUDE.md`, `.antigravity/AGENT_PIPELINE_MEMORY.md`, `.antigravity/RULES.md`, 커밋 `f132a42` |
| 2026-10-22 | v6.3 드라이브 동기화 전환 — Apps Script 양방향 동기화 가동(정산시스템 폴더 221개 파일, GitHub blob 해시 전수 일치 확인), post-commit hook 비활성화, `sync_to_gdrive.ps1` 보관 | `scripts/gas/sync_settlement.gs`, `_archive/scripts/sync_to_gdrive.ps1`, `CLAUDE.md`, 커밋 `d7ee6ed`·`a683e3b` |
| 2026-10-22 | v6.4 완료 산출물 정리 — `_archive/` 144개(예전 백업·패치 스크립트·구 설계서 등), `.antigravity/reports/` 37개, `WORKFLOW_REDESIGN_PLAN.md`, 루트 일회성 py 2개, `extract_paren_src.py` 삭제(추적 파일 304 → 119개). `_archive/backup/`·`.antigravity/reports/` `.gitignore` 등록, `scan_paren_dup.py` 리포트 폴더 자동 생성, `CLAUDE.md`를 `.claude/CLAUDE.md`로 이동 | `.gitignore`, `.claude/CLAUDE.md`, `scripts/qa/scan_paren_dup.py`, 커밋 `75f6221` |
| 2026-10-22 | v6.5 GitHub Pages 첫 화면을 `prototype_clean/` 업무플로우 가이드로 변경(기획 검수용 `prototype/`은 주소 직접 입력으로 접근) | `index.html`, 커밋 `525f4e0` |
| 2026-10-22 | v6.6 드라이브 예전 사본 `04.설계서/docs` 삭제(white 직접, 통합 설계서는 저장소 정본과 동일 확인 후). 저장소에 없던 `정산 및 계약 기획 합의서_V4.0.0_FINAL.md`도 white가 삭제. 통합 설계서 정본은 저장소 `docs/`로 확정 | `.claude/CLAUDE.md`, 커밋 `b9fe822` |
| 2026-10-22 | v6.7 문서 역할 확정 — `README.md`(무엇)·`.claude/CLAUDE.md`(어떻게)·`.claude/PROJECT_STATE.md`(어디까지)로 분리. 메모리 문서를 이 파일로 옮기며 젠스파크/안티그래비티 역할·절차 절 삭제, 안티그래비티 예비 사용 규칙을 `.agents/rules/RULES.md`(자동 로드 위치)로 재작성, 젠스파크 사용 종료. 폴더 원칙 확정: 도구 전용 파일은 도구가 정한 점 폴더(`.claude/`, `.agents/`), 공용 파일은 그 밖. `PROJECT_STATE.md` 루트로, QA 리포트 `scripts/qa/reports/`로, 미사용 스킬(`.agents/skills/` 2개, `skills-lock.json`)과 `.antigravity/` 삭제 | `.claude/CLAUDE.md`, `PROJECT_STATE.md`, `.agents/rules/RULES.md`, `scripts/qa/*.py`, `.gitignore`, 커밋 `9749ea4` |
| 2026-10-22 | v6.8 안티그래비티 규칙 자동 로드 — 안티그래비티 확인 결과 `.agents/rules/RULES.md`가 대화 시작 때 읽히지 않음(문서상 `trigger: always_on`만 무조건 로드). RULES.md에 `trigger: always_on` 추가, 폐기된 예전 절차를 따르지 않는다는 문구 추가. 안티그래비티 지식 저장소에 예전 절차 없음 확인 | `.agents/rules/RULES.md` |
| 2026-10-22 | v6.9 BRD 화면 번호를 화면설계서 v12 기준으로 정렬 — BRD-001 FAQ 002→006·당첨자 010→009, 1:1 문의 탭 제거(BRD-002로 일원화), 학습 Q&A 답변 버튼 동작 수정, BRD-005 무료특강 006→010·설계에 없던 커뮤니티/신고 탭 제거(2026-10-19 `3944e59`에서 문서 없이 추가된 것), clean 치환표 BRD-004 "수험 자료실" 오표기 수정. 통합설계서·README 번호 동기화. Playwright 41/41, E2E 양쪽 37/37 ×2 | `prototype*/ADMN-BRD-001·005_baseline.html`, `prototype_clean/common-snb.js`, `docs/산준모닷컴 구축 통합 상세 설계서.md`, `README.md`, `PROJECT_STATE.md` |
| 2026-10-22 | v6.10 상품 Q&A·문의 분류 화면 추가 — BRD-001에 상품 Q&A 탭(BRD-003: 상품 ID 자동 매핑 목록, 미답변·문의일 오름차순 기본 진입, 문의 유형·담당·상태·공개 필터와 교재/강좌 필터, 담당자 일괄 지정·선택 숨김, 파손 다발 배너, 주문 연결·답변 모달), 새 화면 BRD-007 1:1 문의 분류(대·소분류 마스터, 자동 채번·코드 잠금, 자동 배정 화면·담당 부서 큐, 오류 문구 4종, 사용/미사용 일괄 변경, 대분류 관리, 변경 이력, `?id=` 수정 진입). SNB 44개(사이트 · 약관 · 메시지 설정 그룹), BRD-002에 바로가기. clean에서 숨는 `.info-callout`·`.policy-banner` 대신 `.ctx-note`·`.access-notice` 사용. Playwright 97/97, E2E 양쪽 38/38 ×2 | `prototype*/ADMN-BRD-001·002·007_baseline.html`, `prototype*/common-snb.js`, `README.md`, `PROJECT_STATE.md`, `.claude/CLAUDE.md` |
| 2026-10-22 | v6.11 자유게시판 1차 범위 제외 — 통합설계서 프론트 매핑에서 자유게시판 제거, USER-001 블랙리스트 후보 샘플의 삭제된 신고 탭 흔적(RPT-101·103, 자유게시판 비속어) 교체. 통합설계서 Set 4 [B]에 상품 Q&A(BRD-003, BRD-001 탭) 명세 추가, 문의 분류(BRD-007) 운영 관리자 전용 명시. 통합설계서 Ver. 3.2.1로 개정 이력 추가(v6.9~v6.11 본문 변경분). E2E 양쪽 38/38 ×2 | `docs/산준모닷컴 구축 통합 상세 설계서.md`, `prototype*/ADMN-USER-001_baseline.html`, `PROJECT_STATE.md` |
| 2026-10-22 | v6.12 README 4절 화면 인벤토리 재작성 — 실제 38개 파일을 SNB 9개 그룹 순서로, 파일별로 함께 담는 화면 코드와 결번·폐지 목록 정리. 4절 미결에 첫 화면설계서 점검에서 찾은 코드 충돌(합격환급 심사 이중, 감사 로그 CONF-006/010, USER-007 뜻, SETT-011 범위, SETT-010 미정의, 치환표 SETT-003)과 BRD 권한·S1 페이지 차이 기록 | `README.md`, `PROJECT_STATE.md` |
| 2026-10-22 | v6.13 미결 코드 충돌 정리(white 결정) — ① 합격환급 심사 SETT-006 일원화: RFD-002의 RFD-001 뷰·심사 모달·S1 업그레이드 블록 제거, `?view=pass`는 SETT-006으로 이동 ② 감사 로그 CONF-010 통합: CONF-010 "시스템 감사 로그"로 개명, 3번 탭에 운영자 접근·권한·다운로드 로그(구 CONF-006) 이전, CONF-005 탭은 바로가기로, `?view=ADMN-CONF-006`은 CONF-010으로, CONF-005 권한 매트릭스에 BRD-007(CS 메뉴 비노출)·CONF-010 행 추가 ③ SETT-011을 v12 기준 3PL 물류비 대사로 새로 작성(출고·수수료 대사 — 스코어카드·불일치 붉은 표시·처리 결과+메모 필수·대사 완료 잠금, 배송비·반품 대사 — 반품 귀책 CS 판정, 도서 매입 계산서 대조 — 수취 상태 4종·폐업 매입처 경고, `?tab=` 유지, 10월 명세서 미수령 빈 상태) ④ USER-007 "민감 정보 보관·열람 통제"로 정의 통일, SETT-010 미사용 명시, SETT-009 `?view=tax-report` 처리 추가, clean 치환표 SETT-003 항목 제거. 문서: 03권 대조표·16.1(USER-007·CONF-010·SETT-011), 00권 인덱스, 01권 v4.0.1 개정 이력, 통합설계서 Ver. 3.2.2, README. Playwright 48/48 + v6.10 회귀 97/97, E2E 양쪽 38/38 ×2 | `prototype*/ADMN-RFD-002·USER-001·SETT-006·CONF-001·002·005·010·SETT-009·011_baseline.html`, `prototype*/00_WORKFLOW_GUIDE_baseline.html`, `prototype*/common-snb.js`, `docs/*.md`, `README.md`, `PROJECT_STATE.md` |
| 2026-10-22 | v6.14 남은 미결 처리 — S1 화면은 프로토타입 모달·개발은 v12 별도 페이지, clean 원문 화면 코드 유지를 확정 기준으로 기록. ORD-001 교재 라인 문구 '도서 인세 (+1권)' → '자사 발행 도서 인세 · 판매 1권 집계'(prototype은 'Pipeline 2.1' 접두 유지). QA 도구 2종 구축: `skill_static_lint.py`(문법·링크·중복 ID·빈 tbody·에셋 규격, 오류 0건), `skill_cross_data_check.py`(권리자·계약·도서 대조). 대조 결과에 따라 v6.10·v6.13에서 넣은 도서 샘플 코드를 기존 형식(BK-2026-NNN)으로 정렬(BRD-001 → 103·204·206, SETT-011 → 201~206). 기존 데이터의 `김안전` RH-0012/0019 혼용과 공통 에셋 id 미준수 4개 화면은 미결로 기록 | `prototype*/ADMN-ORD-001·BRD-001·SETT-011_baseline.html`, `scripts/qa/skill_static_lint.py`, `scripts/qa/skill_cross_data_check.py`, `PROJECT_STATE.md`, `.claude/CLAUDE.md` |
| 2026-10-22 | v6.15 마지막 미결 2건 처리 — 샘플 권리자 코드 일원화(white: 임의 생성 데이터라 어느 쪽이든 일원화만): 김안전 = RH-0019, 산준교육(콘텐츠·에이전시·법인) = RH-0012로 통일. SETT-007·USER-007은 두 코드를 맞바꿔 쓰고 있어 교환, SETT-004·CONF-010은 김안전 자리만 RH-0019로. 공통 에셋 `id`(README 3.2) 누락 4개 화면(BRD-001·005, CONF-004·005) 보완. 데이터 대조 오류 1→0, 정적 검사 에셋 경고 8→0, E2E 양쪽 38/38 ×2, Playwright 48/48·97/97 | `prototype*/ADMN-SETT-004·007·USER-007·CONF-010·BRD-001·005·CONF-004·005_baseline.html`, `PROJECT_STATE.md`, `.claude/CLAUDE.md` |
| 2026-10-22 | v6.16 BRD-001·BRD-005 머리말을 공통 구조로 통일 — 두 화면만 공통 상단 바 없이 자체 page-header를 본문에 두고 `#v4-page-body`에 `main-container`가 없어, 공통 CSS가 본문 여백을 0으로 만들며 제목이 SNB 옆 맨 위에 붙던 문제. `header.top-bar.v4-gen3-topbar`(그룹 › 코드 · 제목, 오른쪽 이동 버튼) + `#v4-page-body.main-container`로 바꾸고 설명은 본문 첫 줄(`.page-desc`)로 이동, 탭 전환 시 제목 변경용 id 유지. BRD-001 초기 제목·BRD-005 이동 버튼의 '문의'(v6.9에서 없앤 탭) 문구 정리, 상단 바 버튼 밑줄 제거. 본문 시작 위치 x=288·y=82로 다른 화면과 동일, E2E 양쪽 38/38 ×2, Playwright BRD 회귀 통과, 정적·대조 오류 0 | `prototype*/ADMN-BRD-001·005_baseline.html`, `PROJECT_STATE.md` |
| 2026-10-22 | v6.17 역할 그룹을 변수로 관리 · 담당 부서 큐 연동 · 담당 선점(1단계) — 공통 기준정보 `common-master.js`(역할 그룹 최초 8종 · 메뉴 권한 · 1:1 문의 분류, 관리 화면에서 바꾼 값을 브라우저에 저장해 다른 화면이 읽음) 신설. CONF-005를 공통 구조로 새로 작성: 관리자 계정(역할 그룹 복수 부여) · 역할 그룹 · 권한(그룹 추가 · 수정 · 미사용, 메뉴별 읽기 · 쓰기 · 엑셀 편집, 저장 전 영향 확인 — 바뀌는 메뉴 · 영향 계정 · 담당 큐 참조 분류, 사용 중 그룹 미사용 차단, 변경 이력). BRD-007 담당 부서 큐를 역할 그룹에서 읽고 라우팅 변경 확인 창 · 소분류 40자. BRD-002 담당자 칸 · 상태 4종(접수 · 처리중 · 답변완료 · 보류) · 진입 시 선점 · 동시 잠금 · 관리자 재배정 · 내 담당 필터. BRD-001 상품 Q&A 담당 부서를 역할 그룹으로, 처리자 선점. DASH-001 역할 미리보기를 권한 매트릭스 기준으로. CONF-004 머리말 공통 상단 바로. 화면 부서 표기 통일(정산팀 · 재무회계팀 → 재무팀, CS팀 · 고객감동팀 → CS담당자, 상품팀 · 운영팀 → 최고 관리자, 최고관리자 → 최고 관리자 등 13개 화면). 남은 옛 합격환급 심사(RFD-001) 참조를 SETT-006으로. Playwright 83/83 · 회귀 97/97, E2E 양쪽 38/38 ×2, 정적 · 대조 오류 0 | `prototype*/common-master.js`, `prototype*/ADMN-CONF-005·BRD-007·BRD-002·BRD-001·DASH-001·CONF-004 외 부서 표기 화면`, `prototype*/common-snb.js`, `README.md`, `PROJECT_STATE.md`, `.claude/CLAUDE.md` |
