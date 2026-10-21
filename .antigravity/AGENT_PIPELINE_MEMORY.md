# 안티그래비티 로컬 에이전트 — 역할 고정 및 영구 파이프라인 메모리

> **이 문서는 세션 압축·신규 세션에도 휘발되지 않는 영구 메모리다.**
> 에이전트는 **매 작업 시작 전 반드시** 이 문서와 `.antigravity/RULES.md`를 먼저 열람한다.
> 최초 등록: 2026-10-20 · 최종 갱신: 2026-10-21 (v6.2 기준)
>
> **2026-10-21 역할 재편 (v6.2):** 진단·패치·실행·검증·커밋은 Claude Code가 한곳에서 수행한다. 현행 작업 규칙은 루트 `CLAUDE.md`가 우선한다.
> 아래 0·1절과 `RULES.md`의 젠스파크/안티그래비티 역할 구분은 이력 보존용이다. 안티그래비티는 대량·기계적 작업(전체 E2E, 일괄 스캔)을 맡길 때만 쓴다.
> 구글 드라이브 동기화는 Apps Script(GitHub ↔ 공유 문서함 `04.설계서/정산시스템`)로 넘어가며 `sync_to_gdrive.ps1`은 실행하지 않는다.

---

## 0. 파이프라인 구조 및 AI 세션 공통 지침 (새 세션 시작 시 필독)

> **참조 문서:** 작업 착수 전 반드시 루트 `README.md`(프로젝트 아키텍처·표준 정책·화면 인벤토리, 현행 활성 37개)와 본 문서(`.antigravity/AGENT_PIPELINE_MEMORY.md`)를 함께 열람한다.

| 역할 | 주체 | 책임 |
| :--- | :--- | :--- |
| **기획·설계·패치 작성 AI** | **젠스파크 Chat / Opus** | 요구사항 분석, 정본 문서(`docs/`) 대조, **`prototype/` 및 `prototype_clean/` 동시 패치용 단일 Python 스크립트(`.py`) 작성** |
| **로컬 실행·검수 에이전트** | **안티그래비티 (Antigravity)** | 전달받은 패치 스크립트 원본 그대로 실행(R1), 실행 완료 스크립트 `_archive/scripts/` 이동, Playwright E2E 검수(`scripts/qa/skill_playwright_e2e.py`), Git·구글 드라이브 동기화 |

### 0-1. 기획/설계 AI (젠스파크 세션) 필수 작성 규칙
1. **단일 원스톱 스크립트 제공:** 로컬 파일(HTML/MD) 수정 시 여러 조각으로 나누지 않고 터미널에 한 번에 붙여넣어 실행할 수 있는 단일 명령어 블록으로 제공한다.
2. **`prototype/` & `prototype_clean/` 동시 패치:** 백오피스 HTML 수정 시 두 폴더의 성격 차이(`prototype/`은 상단 정책 배너 포함, `prototype_clean/`은 순수 서비스 UI)를 유지하면서 양쪽 폴더의 동명 파일에 동시 반영한다.
3. **문서 우선순위 및 화면설계서(`docs/screen_spec/`) 검증:**
   - 1순위: `README.md` 및 사용자의 실시간 지시 / 2순위: `docs/산준모닷컴 구축 통합 상세 설계서.md` 및 `docs/[산준모 정산시스템]_00~04.md` / 3순위(참고용): `docs/screen_spec/*.md`
   - `screen_spec/` 내의 원형 번호(`①~⑭`, `[마커 N]`)나 기획 설명 문구를 실제 프로토타입 UI에 노출하지 않으며, 가짜 상단 탭 스위처 대신 실제 SNB 및 화면 내 동선 버튼을 사용한다.

### 0-2. 운영 규칙 (2026-10-21 확정)

**지시문 형식**
- 안티그래비티 지시문은 코드블럭 하나로 제공한다(모바일 복붙). 패치 스크립트는 별도 코드블럭.
- 읽기 전용 지시문 고정 문구: `[읽기 전용 · 파일 수정 금지] 결과를 원문 그대로(파일명+줄 번호) 저장, 요약·해석·복원 금지, 결과 없으면 "0건", 이전 리포트 문구 재사용 금지`
- 실행 지시 표준 순서: 원문 그대로 저장·실행 → `[ABORT]` 시 출력 전문 전달 → `[OK]` 시 E2E 2회(폴더별) + `git diff --ignore-cr-at-eol --stat` → `.antigravity/reports/V*_RESULT.md` 저장(스크립트 출력은 "원문" 제목 아래 그대로) → 스크립트 `_archive/scripts/` 이동 → commit·push·구글 드라이브 동기화 → 터미널 마지막 출력만 전달.

**패치 스크립트 작성 규칙 (젠스파크)**
- 줄 번호가 아닌 문구로 찾는다. 대상 건수가 기대값과 다르면 전체 `[ABORT]`, 파일 미변경.
- 모든 변경을 메모리에서 계산한 뒤 일괄 저장. 저장 전 `_archive/backup/v<버전>_<시각>/` 백업.
- 상단에 `sys.stdout.reconfigure(encoding="utf-8")`(CP949 깨짐 방지), 파일 입출력은 `newline=""`로 CRLF/LF 보존.
- 유지해야 할 예외 문구는 스크립트에 화이트리스트로 명시.
- 대형 파일은 젠스파크가 직접 읽지 않는다. 안티그래비티 추출 리포트(30,000자 이내, 원문·줄 번호)로 받는다.

**리포트 신뢰 기준**
- 안티그래비티 리포트의 요약·표에는 재작성·추정이 섞일 수 있다(v5.4에서 코드 번호·함수명 오기 확인). 판단 근거는 "원문" 제목 아래 터미널 출력과 git diff만 쓴다.
- `prototype_clean/`은 `common-snb.js`가 로드 후 문구를 런타임 치환한다. 화면 문구 검사는 HTML grep이 아니라 Playwright 렌더링 기준(`scan_paren_dup.py` 방식)으로 한다.

**리포트 읽기 경로 (젠스파크)**
- raw.githubusercontent.com이 400/잘림일 때: `https://cdn.jsdelivr.net/gh/whiteceo/sanjunmo-settlement@main/<경로>` 또는 커밋 해시 URL `https://raw.githubusercontent.com/whiteceo/sanjunmo-settlement/<hash>/<경로>`.

**확정 기준**
- `prototype/`은 기획 검수용(정책 문구·괄호 병기 유지), `prototype_clean/`은 운영 UI만. 기능 패치는 양쪽, 표기 정리는 clean 우선이며 prototype/ 괄호 병기는 수정하지 않는다.
- 업무플로우 페이지(`00_WORKFLOW_GUIDE_baseline.html`)는 clean에서 작업 후 prototype/으로 덮어쓴다. 코드값 비노출, 화면 코드는 회색 라벨.
- SNB: 정본 9개 그룹 · 메뉴 43개, 양쪽 `SNB_GROUPS` 동일. 정본 명칭이 길면 축약 허용.
- SETT-010(원천세·지급명세서 산출물)은 SETT-009 내부 기능으로 별도 메뉴 아님. CONF-006(보안 감사로그)은 CONF-005 세 번째 탭(`?view=ADMN-CONF-006`). USER-007은 "개인정보 · 보안 감사" 그룹.
- 정답지는 독립 화면이 아니라 운영자가 무료 콘텐츠 제목에 붙이는 표기. BRD-009 폐지, BRD-005는 탭 4개.
- 업무플로우 정산은 3단계(STAGE 01~03), 상시 감사는 STAGE 03 하위 상시 블록, 예외 케이스는 접힘으로 주 흐름과 분리.

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
| Skill 1 | `scripts/qa/skill_static_lint.py` | 전 HTML 내 `<script>` 추출 → `node --check` 문법 검사, 깨진 링크(`href`), 중복 ID, 빈 `<tbody>` 초고속 스캔 | 미구축 |
| Skill 2 | `scripts/qa/skill_jargon_scan.py` | 금지어(`기출`, `정오표`, `Vimeo`, `80%`, `①~⑭`, `[마커`) 및 운영자가 이해할 수 없는 기획서 내부 암호(`C-01~04`, `H-01~05`, `D-1~16`, `P1.1~5.1`, `Pipeline`, `제N장`, `N.N절`, `_flag`, `_yn`, `_id`), 번역 중복어(`실결제금액(실결제금액)`) 정규식 전수 탐지 → `.antigravity/reports/JARGON_SCAN_REPORT.md` | **구축 완료** |
| Skill 3 | `scripts/qa/skill_cross_data_check.py` | 동일 강사(`RH-0025` 등)·동일 도서(`BK-2026-101` / `BOOK-2601`)의 정가·요율·계약번호 화면 간 불일치 파싱 대조 | 미구축 |
| Skill 4 | `scripts/qa/skill_playwright_e2e.py` | Playwright 기반 모달 열기/닫기, 탭 전환, 레이아웃 겹침 검수. 폴더 인자 필수: `python scripts/qa/skill_playwright_e2e.py prototype_clean` / `... prototype` (폴더별 2회) | **구축 완료** |
| Skill 5 | `scripts/qa/scan_paren_dup.py` | Playwright 렌더링 후 괄호 중복 탐지(양쪽 폴더) + clean 원문 `ADMN-` 코드 자리 집계 → `.antigravity/reports/PAREN_DUP_SCAN.md`, `PAREN_DUP_STATIC.md` | **구축 완료** |

### 1-3. 리포트 발행 및 Git / 구글 드라이브 동기화
1. 패치 실행 및 스킬 검수 결과를 `.antigravity/reports/` 하위 마크다운 리포트(예: `.antigravity/reports/QA_SCAN_REPORT.md`, `.antigravity/reports/JARGON_SCAN_REPORT.md`)로 저장한다.
2. 즉시 `git add -A && git commit -m "<type(scope): 설명>" && git push origin main` 수행.
3. 구글 드라이브 동기화: Windows 로컬에서 `pwsh -ExecutionPolicy Bypass -File sync_to_gdrive.ps1` 실행.
4. 분석 AI는 GitHub Raw URL로 리포트를 즉시 읽는다:
   `https://raw.githubusercontent.com/whiteceo/sanjunmo-settlement/main/.antigravity/reports/<REPORT>.md`

---

## 2. 완료된 작업 기준선 (Baseline)
- `prototype/` 및 `prototype_clean/` 활성 37개 화면 동기화 완료 (2026-10-21 `patch_all_snb_v3.html` 보관 후 기준)
- `ADMN-ORD-001`, `PROD-003`, `PROD-005` 인강·교재 면세(`EXEMPT`) 정합화 완료
- 전 화면 모달 닫기 핫픽스(`common-v84.css`, `common-snb.js`) 완료
- `ADMN-SETT-006` 가로 100% 목록/검색필터/상세모달 개편 + 4대 제출 자료(합격증 사본, 산준모 카페 합격수기 아웃링크, 통장사본, 1금융권 실명계좌) 반영 완료
- (2026-10-21) 업무플로우 페이지 v5 전면 개편 및 prototype/ 반영, SNB 9개 그룹·메뉴 43개 양쪽 정렬, 전 화면 브레드크럼 정본 그룹명 적용
- (2026-10-21) 정답지 독립 화면 폐지(BRD-005 탭 정리, CONF-005 저작권자 권한 문구 정리), 미실행 옛 SNB 코드 삭제
- (2026-10-21) clean 렌더링 괄호 중복 163건 → 1건(SETT-006 금액 표기, 정상 유지)
- (2026-10-21) SETT-005 "신규 수동 조정 등록" 모달 3개 진입 경로(카드 버튼·상단 버튼·SETT-002 `?fromStmt=` 자동 오픈) 정상화

---

## 3. 표준 작업 루틴 (매 세션)
1. `.antigravity/AGENT_PIPELINE_MEMORY.md`, `.antigravity/RULES.md`, `README.md` 열람 (`BACKOFFICE_ALIGNMENT_MASTER_PLAN.md`는 10-20 작업 로그 기준 `_archive/docs/` 보관)
2. `git pull origin main`
3. 전달받은 패치 스크립트를 **원본 그대로** 실행 (`python <patch>.py`)
4. QA 실행: `python scripts/qa/skill_playwright_e2e.py prototype_clean`, `python scripts/qa/skill_playwright_e2e.py prototype` (필요 시 `skill_jargon_scan.py`, `scan_paren_dup.py`)
5. `.antigravity/reports/*.md` 발행(실행 스크립트는 `_archive/scripts/` 이동) → commit → push → 구글 드라이브 동기화
6. 아래 작업 로그에 1줄 추가

---

## 5. 현재 상태 및 다음 작업 (2026-10-21 · v6.2 기준)

**상태**
- 활성 화면 37개(양쪽 폴더). E2E `prototype_clean` 37/37, `prototype` 37/37 PASS (v6.1 기준), 콘솔 에러 0건.
- 괄호 중복: clean 1건(정상), prototype 6건(기획 검수용 기준으로 유지).
- 공통 모달 닫기 핫픽스(`UNIVERSAL-MODAL-CLOSER-HOTFIX`)는 로드 시 모든 모달 백드롭에 인라인 `display:none !important`를 건다. `hidden` 클래스만 떼서 여는 모달(특히 `addEventListener`로 연결된 버튼)은 열리지 않으므로, 다른 화면의 "눌러도 반응 없음" 증상은 이 원인부터 확인한다(해결 방식: v6.0·v6.1).

**미결 사항**
- clean HTML 원문의 `ADMN-` 코드 251자리: 런타임 치환으로 화면에는 안 보임. 원문 정리 여부 미정.
- ORD-001 "도서 인세 (+1권)": 원 문구 미확인 상태에서 정한 판단값.
- Skill 1(정적 문법 검사)·Skill 3(화면 간 데이터 대조) 미구축.
- README 화면 수 표기(38개) 갱신 여부 확인 필요.
- 로컬 전용 백업 `_archive/backup/v6.0_*`, `v6.1_*`는 저장소에 올리지 않는다(`.gitignore` 미등록, `git add` 경로 지정으로 관리).
- Apps Script 양방향 동기화 설정 중: 공유 문서함 `04.설계서/정산시스템` 폴더 생성·이동 → `previewSync` 미리보기 확인 전. `sync_to_gdrive.ps1` 정리(삭제 또는 `_archive/`) 미정.

**다음 세션 작업: 개별 HTML 점검 및 동작 오류 세부 수정**
1. white가 화면·증상을 지정(스크린샷 포함 가능).
2. 안티그래비티가 읽기 전용으로 해당 구간 원문·줄 번호 추출 → `.antigravity/reports/` 저장.
3. 젠스파크가 문구 기반 단일 패치 스크립트 작성(0-2 규칙).
4. 실행 → E2E 2회 + 해당 화면 Playwright 캡처로 확인.

---

## 4. 작업 로그
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
| 2026-10-21 | v6.2 역할 재편(Claude Code 단일 체계) — 루트 `CLAUDE.md` 신설, 본 문서·`RULES.md`에 재편 안내 추가 | `CLAUDE.md`, `.antigravity/AGENT_PIPELINE_MEMORY.md`, `.antigravity/RULES.md` |
