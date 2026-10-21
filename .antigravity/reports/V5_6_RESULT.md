# v5.6 괄호 중복 1차(런타임 치환 순서 보정) 결과 리포트

> **작성일시:** 2026-10-21  
> **대상 파일:** `prototype_clean/common-snb.js`  
> **백업 디렉터리:** `_archive/backup/v5_6_20261021_201146/prototype_clean/common-snb.js`  
> **검증 도구:** Playwright Chromium (1440px 뷰포트 E2E 자동 검수)

---

## 원문

### 1. patch_v5_6_paren_strip.py 실행 터미널 출력
```
[OK] prototype_clean/common-snb.js 수정 · 백업 _archive\backup\v5_6_20261021_201146\prototype_clean\common-snb.js
  - 프렐류드 추가, 훅 4곳 삽입: transformText, cleanString, walkAndClean, runEnhancedClean
  - [WARN] node 없음 — 문법 검사는 E2E로 대체
```

### 2. scan_paren_dup.py 재실행 터미널 출력
```
[A] prototype_clean: 36건
[A] prototype: 6건
[B] prototype_clean (ADMN-코드) 자리: 251건
[SIZE] PAREN_DUP_SCAN.md: 4449자
[SIZE] PAREN_DUP_STATIC.md: 27468자
```

---

## 1. 괄호 중복 탐지 건수 비교 (PAREN_DUP_SCAN.md)

| 구분 | v5.5 직후 (패치 전) | v5.6 적용 후 (1차 보정) | 변동 |
| :--- | :---: | :---: | :---: |
| **`prototype_clean` 중복 건수** | 163건 | **36건** | **-127건 (77.9% 감소)** |
| **`prototype` 중복 건수** | 6건 | 6건 | 0건 (동일) |
| **`PAREN_DUP_SCAN.md` 파일 크기** | 16,909자 | 4,449자 | -12,460자 |

---

## 2. E2E 검수 결과

| 대상 환경 | 실행 명령어 | 전체 화면 수 | PASS 수 | 콘솔 에러 수 | 판정 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **`prototype_clean`** | `python scripts/qa/skill_playwright_e2e.py prototype_clean` | 37개 | 37개 | 0건 | **PASS** |
| **`prototype`** | `python scripts/qa/skill_playwright_e2e.py prototype` | 37개 | 37개 | 0건 | **PASS** |

---

## 3. git diff --ignore-cr-at-eol --stat 출력 전문

```
 .antigravity/WORKFLOW_REDESIGN_PLAN.md |   5 ++
 .antigravity/reports/PAREN_DUP_SCAN.md | 135 +--------------------------------
 prototype_clean/common-snb.js          |  60 +++++++++++++++
 3 files changed, 69 insertions(+), 131 deletions(-)
```
