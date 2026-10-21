# v5.4 정답지 정리 및 미사용 코드 정리 결과 리포트

> **작성일시:** 2026-10-21  
> **검증 대상 폴더:** `prototype/`, `prototype_clean/`  
> **검증 도구:** Playwright Chromium (1440px 뷰포트 E2E 자동 검수)  
> **백업 디렉터리:** `_archive/backup/v5_4_20261021_180243/`

---

## 1. 개요 및 주요 변경 사항

정답지는 독립된 화면(`ADMN-BRD-009`)이나 독립 탭이 아닌 **무료 콘텐츠(무료특강/빈출문제, `ADMN-BRD-006`)**의 한 유형으로 통합 관리(등록 시 제목에 `[정답지]` 태그 부착)하기로 결정되었습니다. 이에 따라 독립 탭 및 잔재 코드를 정리하고, 미실행 옛 코드 및 레거시 파일을 아카이빙했습니다.

### 세부 작업 내역
1. **`ADMN-BRD-005_baseline.html` 정답지 탭 및 기능 정리 (양쪽 폴더 동일 적용)**
   - 서브 탭 5개 중 `정답지 관리 (구 ADMN-BRD-009)` (`tab-btn-errata`) 제거 ➔ **4개 탭 체제**로 개편
     - 1) ⭐ 수강후기 관리 (강좌/별점)
     - 2) 🎓 합격수기 검수 관리 (합격증빙/회차)
     - 3) 🎬 무료특강 및 빈출문제 (ADMN-BRD-006)
     - 4) 🚨 커뮤니티/신고 관리 (ADMN-BRD-007/008)
   - `view-errata` 섹션 마크업, 모달 팝업(`modal-errata`), 더미데이터(`ERRATA_ITEMS`), 탭 전환 분기(`switchTab('errata')`), 전용 렌더링/저장 로직(`renderErrataTable`, `saveErrata`, `openErrataModal`, `deleteErrata`), URL 쿼리 파라미터 허용 목록(`?view=errata`) 완전 제거
   - 화면 제목 및 타이틀의 `"·정답지"` 문구 삭제
   - **예외 보존:** 합격수기 수험생 실기 수기 내용 중 `"정답지 해설을 반복 회독"`은 합격자 작성 원문이므로 화이트리스트 지정 보존
2. **`common-snb.js` 메뉴명 및 치환표 정리 (양쪽 폴더 동일 적용)**
   - `BRD-005` 메뉴명: `"후기 · 합격수기 · 정답지 · 무료특강 · 신고"` ➔ `"후기 · 합격수기 · 무료특강 · 신고"`
   - `PROM-002` 메뉴명: 괄호 제거 (`"(타겟 메시지 발송 · 내역)"` ➔ `"타겟 메시지 발송 · 내역"`)
   - `SETT-011` 메뉴명: 가운뎃점 표준화 (`"내부 정산 조회 (조회 전용)"` ➔ `"내부 정산 조회 · 조회 전용"`)
   - `prototype_clean/common-snb.js`: 구 문구 치환표(`SUBSTITUTION_TABLE`)에서 `ANSWER_SHEET`, `ADMN-BRD-009` 항목 제거
3. **`BOOK-001`, `PROD-003~006` 미실행 옛 SNB 코드 제거 (양쪽 폴더 동일 적용)**
   - 화면 하단 스크립트에 잔존하던 미호출 옛 코드 `MASTER_NAV_GROUPS` 배열 및 `renderMasterSnb()` 함수 정의 제거 (화면 렌더링 영향 0건)
4. **레거시 파일 아카이빙 (`git mv`)**
   - `prototype/patch_all_snb_v3.html` ➔ `_archive/legacy/prototype/patch_all_snb_v3.html`
   - `prototype_clean/patch_all_snb_v3.html` ➔ `_archive/legacy/prototype_clean/patch_all_snb_v3.html`
   - 프로토타입 활성 화면 수 총 38개에서 **37개**로 정규화
5. **E2E 검수 스크립트 기능 확장 (`scripts/qa/skill_playwright_e2e.py`)**
   - 명령줄 인자로 검수 대상 폴더를 지정할 수 있도록 개선: `python scripts/qa/skill_playwright_e2e.py [prototype_clean | prototype]` (기본값: `prototype_clean`)
6. **보류 항목**
   - `ADMN-CONF-005_baseline.html` 교재 저작권자 권한 문구 내 정답지 관련 언급은 사용자 결정 대기를 위해 현상 유지

---

## 2. 변경 파일 목록 (총 15개 수정, 2개 이동)

| 구분 | 파일 경로 | 변경 내용 요약 |
| :--- | :--- | :--- |
| **수정** | `prototype/ADMN-BRD-005_baseline.html` | 정답지 탭/모달/더미/함수 제거, 4개 탭 구성 |
| **수정** | `prototype_clean/ADMN-BRD-005_baseline.html` | 정답지 탭/모달/더미/함수 제거, 4개 탭 구성 |
| **수정** | `prototype/common-snb.js` | 메뉴명 라벨 3건 정렬 |
| **수정** | `prototype_clean/common-snb.js` | 메뉴명 라벨 3건 정렬 및 치환표 구 항목 삭제 |
| **수정** | `prototype/ADMN-BOOK-001_baseline.html` | 미실행 레거시 SNB 코드 77줄 제거 |
| **수정** | `prototype_clean/ADMN-BOOK-001_baseline.html` | 미실행 레거시 SNB 코드 77줄 제거 |
| **수정** | `prototype/ADMN-PROD-003_baseline.html` | 미실행 레거시 SNB 코드 77줄 제거 |
| **수정** | `prototype_clean/ADMN-PROD-003_baseline.html` | 미실행 레거시 SNB 코드 77줄 제거 |
| **수정** | `prototype/ADMN-PROD-004_baseline.html` | 미실행 레거시 SNB 코드 77줄 제거 |
| **수정** | `prototype_clean/ADMN-PROD-004_baseline.html` | 미실행 레거시 SNB 코드 77줄 제거 |
| **수정** | `prototype/ADMN-PROD-005_baseline.html` | 미실행 레거시 SNB 코드 77줄 제거 |
| **수정** | `prototype_clean/ADMN-PROD-005_baseline.html` | 미실행 레거시 SNB 코드 77줄 제거 |
| **수정** | `prototype/ADMN-PROD-006_baseline.html` | 미실행 레거시 SNB 코드 77줄 제거 |
| **수정** | `prototype_clean/ADMN-PROD-006_baseline.html` | 미실행 레거시 SNB 코드 77줄 제거 |
| **수정** | `scripts/qa/skill_playwright_e2e.py` | 폴더 인자 지원 파라미터화 |
| **수정** | `.antigravity/WORKFLOW_REDESIGN_PLAN.md` | v5.4 결정 사항 로그 기록 |
| **이동** | `prototype/patch_all_snb_v3.html` | `_archive/legacy/prototype/` 로 이동 |
| **이동** | `prototype_clean/patch_all_snb_v3.html` | `_archive/legacy/prototype_clean/` 로 이동 |

---

## 3. 검증 결과

### 3.1 Playwright E2E 기능 검수 (양쪽 폴더 전수 검수)
1. **`prototype_clean` 환경 검수 결과:**
   - 실행 명령: `python scripts/qa/skill_playwright_e2e.py prototype_clean`
   - 검수 화면 수: **37 / 37 PASS (100%)**
   - 콘솔 에러: 0건
2. **`prototype` 환경 검수 결과:**
   - 실행 명령: `python scripts/qa/skill_playwright_e2e.py prototype`
   - 검수 화면 수: **37 / 37 PASS (100%)**
   - 콘솔 에러: 0건

### 3.2 시각 검증 및 캡처
- **저장 위치:** [`.antigravity/reports/screens/v5_4_brd005.png`](screens/v5_4_brd005.png)
- **뷰포트 규격:** 1440 × 900 px
- **확인 사항:**
  - 상단 화면 타이틀 및 안내문구에서 정답지 삭제 확인
  - 상단 도메인 스위치 바에 4개 서브 탭(`수강후기`, `합격수기`, `무료특강 및 빈출문제`, `커뮤니티/신고`)만 노출되며 '정답지' 탭이 깔끔하게 제거됨 확인
  - 기본 활성화 탭(`수강후기`) 정상 렌더링 확인
