# 안티그래비티 로컬 에이전트 — 역할 고정 및 영구 파이프라인 메모리

> **이 문서는 세션 압축·신규 세션에도 휘발되지 않는 영구 메모리다.**
> 에이전트는 **매 작업 시작 전 반드시** 이 문서와 `.antigravity/RULES.md`를 먼저 열람한다.
> 최초 등록: 2026-10-20

---

## 0. 파이프라인 구조 (역할 분담)

| 역할 | 주체 | 책임 |
| :--- | :--- | :--- |
| 분석 AI | 젠스파크 Chat | 요구사항 분석, 기획서(SSOT) 대조, 패치 지시 |
| 코딩 전담 AI | Opus | 백오피스 HTML/JS/CSS 기능 구현, Python 패치 스크립트(`.py`) 작성 |
| **로컬 실행·검수 에이전트** | **안티그래비티 (본 에이전트)** | 패치 스크립트 원본 그대로 실행, 로컬 QA 스킬 구축·실행, 리포트 발행, Git·구글 드라이브 동기화 |

---

## 1. 핵심 역할과 금지 사항

### 1-1. 임의 코딩 금지 (Strict Rule)
- 백오피스 HTML/JS/CSS 기능 구현 및 패치 스크립트 작성은 외부의 **분석 AI(젠스파크 Chat) + 코딩 전담 AI(Opus)**가 수행한다.
- 안티그래비티는 전달받은 Python 패치 스크립트(`.py`)를 **단 한 글자도 임의로 개조하지 않고 그대로 실행**한다.
- 패치 실행 중 오류가 나면 스크립트를 고치지 말고, 오류 로그를 리포트로 발행하여 분석 AI에 반환한다.

### 1-2. 로컬 전용 멀티 스킬(Multi-Skill) 구축 및 실행 전담
로컬 OS/CLI 환경을 활용해 검증·자동화 스킬을 `scripts/qa/` 폴더에 모듈화하여 등록·실행한다.
(QA 스킬은 **읽기 전용 검수 도구**이며, 프로토타입 HTML을 수정하지 않는다.)

| 스킬 | 파일 | 기능 | 상태 |
| :--- | :--- | :--- | :--- |
| Skill 1 | `scripts/qa/skill_static_lint.py` | 38개 HTML 내 `<script>` 추출 → `node --check` 문법 검사, 깨진 링크(`href`), 중복 ID, 빈 `<tbody>` 초고속 스캔 | 미구축 |
| Skill 2 | `scripts/qa/skill_jargon_scan.py` | 금지어(`기출`, `정오표`, `Vimeo`, `80%`, `①~⑭`, `[마커`) 및 운영자가 이해할 수 없는 기획서 내부 암호(`C-01~04`, `H-01~05`, `D-1~16`, `P1.1~5.1`, `Pipeline`, `제N장`, `N.N절`, `_flag`, `_yn`, `_id`), 번역 중복어(`실결제금액(실결제금액)`) 정규식 전수 탐지 → `docs/JARGON_SCAN_REPORT.md` | **구축 완료** |
| Skill 3 | `scripts/qa/skill_cross_data_check.py` | 동일 강사(`RH-0025` 등)·동일 도서(`BK-2026-101` / `BOOK-2601`)의 정가·요율·계약번호 화면 간 불일치 파싱 대조 | 미구축 |
| Skill 4 | `scripts/qa/skill_playwright_e2e.py` | Playwright 기반 모달 열기/닫기, 탭 전환, 레이아웃 겹침 검수 | **구축 완료** |

### 1-3. 리포트 발행 및 Git / 구글 드라이브 동기화
1. 패치 실행 및 스킬 검수 결과를 `docs/` 하위 마크다운 리포트(예: `docs/QA_SCAN_REPORT.md`, `docs/JARGON_SCAN_REPORT.md`)로 저장한다.
2. 즉시 `git add -A && git commit -m "<type(scope): 설명>" && git push origin main` 수행.
3. 구글 드라이브 동기화: Windows 로컬에서 `pwsh -ExecutionPolicy Bypass -File sync_to_gdrive.ps1` 실행.
4. 분석 AI는 GitHub Raw URL로 리포트를 즉시 읽는다:
   `https://raw.githubusercontent.com/whiteceo/sanjunmo-settlement/main/docs/<REPORT>.md`

---

## 2. 완료된 작업 기준선 (Baseline)
- `prototype/` 및 `prototype_clean/` 38개 화면 동기화 완료
- `ADMN-ORD-001`, `PROD-003`, `PROD-005` 인강·교재 면세(`EXEMPT`) 정합화 완료
- 전 화면 모달 닫기 핫픽스(`common-v84.css`, `common-snb.js`) 완료
- `ADMN-SETT-006` 가로 100% 목록/검색필터/상세모달 개편 + 4대 제출 자료(합격증 사본, 산준모 카페 합격수기 아웃링크, 통장사본, 1금융권 실명계좌) 반영 완료

---

## 3. 표준 작업 루틴 (매 세션)
1. `docs/AGENT_PIPELINE_MEMORY.md`, `.antigravity/RULES.md`, `README.md`, `docs/BACKOFFICE_ALIGNMENT_MASTER_PLAN.md` 열람
2. `git pull origin main`
3. 전달받은 패치 스크립트를 **원본 그대로** 실행 (`python <patch>.py`)
4. QA 스킬 실행 (예: `python scripts/qa/skill_jargon_scan.py`)
5. `docs/*_REPORT.md` 발행 → commit → push → 구글 드라이브 동기화
6. 아래 작업 로그에 1줄 추가

---

## 4. 작업 로그
| 일자 | 작업 | 산출물 |
| :--- | :--- | :--- |
| 2026-10-20 | 역할 고정 메모리 생성, Skill 2(금지어·내부 암호 스캐너) 구축 및 최초 스캔 | `.antigravity/RULES.md`, `docs/AGENT_PIPELINE_MEMORY.md`, `scripts/qa/skill_jargon_scan.py`, `docs/JARGON_SCAN_REPORT.md` |
| 2026-10-20 | `patch_missing_3_features.py` 실행 — USER-004 진도율 보정 원장(카드 4·5번)·USER-006 태그 생성/그룹-태그 연결(카드 1·2번)·RFD-003-S2 별도 보정 거래, prototype/·prototype_clean/ 동기 적용 | `prototype*/ADMN-USER-001_baseline.html`, `prototype*/ADMN-RFD-002_baseline.html`, `docs/JARGON_SCAN_REPORT.md` |
| 2026-10-20 | `hotfix_ssr_initial_rows.py` 실행 — USER-001 차시·보정이력·그룹 3개 테이블 SSR 초기 행 내장 및 Skill 4(Playwright E2E 검수기) 구축·38/38 PASS 검증 | `prototype*/ADMN-USER-001_baseline.html`, `scripts/qa/skill_playwright_e2e.py`, `docs/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md` |
| 2026-10-20 | `fix_rfd002_ssr_row.py` 실행 — RFD-002 보정 거래 원장(m3f-rfd-adj-body) SSR 초기 행 내장 완료, 38/38 PASS 유지 | `prototype*/ADMN-RFD-002_baseline.html`, `docs/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md` |
| 2026-10-20 | `clean_all_jargon_zero.py` (v2) 실행 — JS 100% 보호형 DOM 가시 텍스트 기획서 암호·금지어 일괄 정제 (333건➔37건, 89% 감축, 38/38 ALL PASS 유지) | `prototype*/*.html`, `docs/JARGON_SCAN_REPORT.md`, `docs/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md` |
| 2026-10-20 | `clean_remaining_jargon_v3.py` 실행 — 잔여 DOM 34건 및 고정 문자열 핀셋 정제 (DOM 잔여 3건으로 99.1% 종결, 28개 화면 무결, 38/38 ALL PASS 유지) | `prototype*/*.html`, `docs/JARGON_SCAN_REPORT.md`, `docs/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md` |
| 2026-10-20 | `update_book_discount_policy.py` 실행 — 도서정가제 기본할인 최대 10% 허용 및 실결제액 기준 정산/인세/무료배송 반영, 위탁도서 모수선택권 정본·프로토타입 전수 동기화 (38/38 ALL PASS 유지) | `README.md`, `docs/*.md`, `prototype*/*.html`, `docs/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md` |
| 2026-10-20 | `sync_all_docs_book_policy_v2.py` 실행 — 잔여 기획서(01/03/04/B2C) 및 ADMN-INST-001 위탁도서 정산모수 선택 UI/정책 동기화 (38/38 ALL PASS 유지) | `docs/*.md`, `prototype*/*.html`, `docs/PLAYWRIGHT_FUNCTIONAL_AUDIT_REPORT.md` |
| 2026-10-20 | Set 1~4 통합설계서 재구조화 플랜 수립 및 사본(v4.0_통합본) AI 거버넌스 헤더 주입 (`fix_step0_and_add_header.py`) | `docs/SET1_TO_4_ALIGNMENT_PLAN.md`, `docs/산준모닷컴 구축 통합 상세 설계서_v4.0_통합본.md`, `README.md` |
