# v5.8 괄호 중복 마무리 결과 리포트

> **작성일시:** 2026-10-21  
> **대상 파일:** `prototype_clean/ADMN-BOOK-001_baseline.html`, `prototype_clean/ADMN-ORD-001_baseline.html`  
> **백업 디렉터리:** `_archive/backup/v5_8_20261021_203409/`  
> **검증 도구:** Playwright Chromium (1440px 뷰포트 E2E 자동 검수)

---

## 원문

### 1. patch_v5_8_paren_fix3.py 실행 터미널 출력
```
[OK] 수정 2개 파일 · 치환 3건 · 플랜 노트 추가 · 백업 _archive\backup\v5_8_20261021_203409
```

### 2. scan_paren_dup.py 재실행 터미널 출력
```
[A] prototype_clean: 1건
[A] prototype: 6건
[B] prototype_clean (ADMN-코드) 자리: 251건
[SIZE] PAREN_DUP_SCAN.md: 933자
[SIZE] PAREN_DUP_STATIC.md: 27468자
```

---

## 1. 괄호 중복 탐지 건수 추이 (PAREN_DUP_SCAN.md)

| 구분 | 최초 (v5.5 직후) | v5.6 (1차 보정) | v5.7 (2차 보정) | v5.8 (최종 마무리) | 누적 감소율 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`prototype_clean` 중복 건수** | 163건 | 36건 | 3건 | **1건** | **-99.4% (162건 해소)** |
| **`prototype` 중복 건수** | 6건 | 6건 | 6건 | 6건 | 0건 (정본 병기 유지) |
| **`PAREN_DUP_SCAN.md` 크기** | 16,909자 | 4,449자 | 1,152자 | 933자 | -15,976자 |

> **prototype_clean 잔여 1건:**
> - `ADMN-SETT-006_baseline.html`: `강사가 환급분 20만원을 정상 부담하며 플랫폼 보전금(120만원) 왜곡 없음`
>   - 금액 단위를 명시한 괄호 표기이므로 의도된 정상 문구로 유지.

---

## 2. E2E 검수 결과

| 대상 환경 | 실행 명령어 | 전체 화면 수 | PASS 수 | 콘솔 에러 수 | 판정 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **`prototype_clean`** | `python scripts/qa/skill_playwright_e2e.py prototype_clean` | 37개 | 37개 | 0건 | **PASS** |
| **`prototype`** | `python scripts/qa/skill_playwright_e2e.py prototype` | 37개 | 37개 | 0건 | **PASS** |

---

## 3. git diff --ignore-cr-at-eol --stat 출력 전문

```
 .antigravity/WORKFLOW_REDESIGN_PLAN.md      | 7 +++++++
 .antigravity/reports/PAREN_DUP_SCAN.md      | 4 +---
 prototype_clean/ADMN-BOOK-001_baseline.html | 2 +-
 prototype_clean/ADMN-ORD-001_baseline.html  | 4 ++--
 4 files changed, 11 insertions(+), 6 deletions(-)
```
