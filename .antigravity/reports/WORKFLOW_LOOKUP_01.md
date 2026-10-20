# 업무플로우 개편을 위한 정본 및 프로토타입 확인 리포트 (WORKFLOW_LOOKUP_01)

> 작성일시: 2026-10-21  
> 목적: 00_WORKFLOW_GUIDE 전면 개편을 위한 정본 대조 및 프로토타입 실사 확인 (읽기 전용 작업)

---

## 1. prototype_clean/common-snb.js 내 "SETT-010" 포함 줄 원문

- **파일 경로:** `prototype_clean/common-snb.js`
- **해당 줄 번호:** Line 74
- **원문:**
```javascript
        { code: "SETT-010", label: "원천세 · 지급명세서 신고 산출물", href: "ADMN-SETT-009_baseline.html?view=tax-report", screenCode: "ADMN-SETT-010" },
```
*(참고: `common-snb.js` 내에 "SETT-010"이 포함된 행은 위 Line 74 총 1줄입니다.)*

---

## 2. docs/ 전체에서 "ADMN-SETT-010" 등장 여부 및 원문

### 2.1 문자열 완전 일치 ("ADMN-SETT-010") 검색 결과
- `docs/` 디렉터리 내의 모든 마크다운(`.md`) 및 텍스트(`.txt`) 파일 전수 검색 결과: **0건 (문자열 완전 일치 없음)**
- 정본 설계서(`[산준모 정산시스템]_00~04.md`, `산준모닷컴 구축 통합 상세 설계서.md`) 및 `screen_spec/` 전체에 `"ADMN-SETT-010"`이라는 정식 화면 코드는 단독으로 표기된 바 없습니다.

### 2.2 선행 추출 스크립트(`extract_workflow_sources.py`) 매칭 원인 소명
- 선행 스크립트의 정규식 `RANGE_RE`(`(ADMN-[A-Z]+-)(\d{3})\s*~\s*(?:ADMN-[A-Z]+-)?(\d{3})`)가 화면 범위 표기인 **`ADMN-SETT-001~011`**을 자동 확장(`001`부터 `011`까지 생성)하면서 `ADMN-SETT-010`이 매칭 목록에 포함되었음.
- **해당 범위 표기 행 원문:**
  1. `docs/screen_spec/00_INDEX_화면설계서_라우팅맵.md` (Line 19):
     ```markdown
     | 08 | `08_정산관리_ADMN-SETT.md` | 정산 > 정산 관리 (ADMN-SETT-001~011) | 26개 | 185,649 |
     ```
  2. `docs/screen_spec/08_정산관리_ADMN-SETT.md` (Line 1):
     ```markdown
     # [화면설계서 v12 정본] 정산 > 정산 관리 (ADMN-SETT-001~011)
     ```

### 2.3 접두어 제외 구버전 표기 ("SETT-010") 검색 결과 (참고)
- 과거 작성된 구 화면설계서 초안(`screen_spec/`)에서 `ADMN-` 접두어 없이 `SETT-010`으로 언급된 이력은 3건 존재함:
  1. `docs/screen_spec/08_정산관리_ADMN-SETT.md` (Line 2776):
     ```markdown
     내부 정산 조회 화면 번호 — 합의서 SETT-009 vs 이 설계서 SETT-010 |
     ```
  2. `docs/screen_spec/screen_spec_all.txt` (Line 1044):
     ```text
     ...무료콘텐츠 관리(BRD-010)·내부 정산 조회(SETT-010) 화면 신설...
     ```
  3. `docs/screen_spec/screen_spec_all.txt` (Line 18269):
     ```html
     <td class="al"><b>내부 정산 조회 화면 번호</b> — 합의서 SETT-009 vs 이 설계서 SETT-010</td>
     ```

---

## 3. "docs/산준모닷컴 구축 통합 상세 설계서.md" 3.4.1 [A] 표 "1:1 문의" 포함 행 원문 전체

- **파일 경로:** `docs/산준모닷컴 구축 통합 상세 설계서.md`
- **해당 줄 번호:** Line 381
- **원문 전체 (자르지 않은 정본):**

| **1:1 문의 분기 허브 · 커뮤니티 · 정답지** | • `USER-BRD-001~003` : 공지사항 · FAQ · 1:1 문의 접수<br>• `USER-BRD-004` : 학습 Q&A (1차 오픈: **산준모 공식 네이버 카페 질문게시판 아웃링크**)<br>• `USER-BRD-005` : 수강·합격후기<br>• `USER-BRD-006` : 무료 콘텐츠 시리즈 **'정답지'** 다운로드/열람<br>• `USER-BRD-007~010` : 시험일정/합격률 · 자유게시판 · 이벤트 당첨자 발표 | • `ADMN-BRD-001/003` : 공지사항 · FAQ 카테고리 및 **1:1 문의 유형(이관 타겟 매핑) 관리**<br>• `ADMN-BRD-002` : **1:1 문의 5대 유형 분기·부서 이관 통합 CS 허브**<br>• `ADMN-BRD-005` : 수강·합격후기 검수 및 베스트 후기 **무상 포인트(`무상 P`)** 보상 지급<br>• `ADMN-BRD-006` : **'정답지'** 콘텐츠 등록·관리<br>• `ADMN-BRD-007~010` : 시험일정 · 게시판 · 당첨자 경품(포인트/기프티콘/실물) 지급 원장 | • 1:1 문의 유형에 매핑된 라우팅 속성에 따라 환불(`RFD-002-S1`), 배송 Lock(`ORD-001-S1`), 동시접속 세션 초기화(`USER-003`), 합격환급(`SETT-006`), 학습질문 카페 안내로 즉시 분기<br>• 구 `'정오표'` 및 `'교재 정답지'` 명칭을 폐기하고 무료 교재형 콘텐츠 시리즈 고유명사 **`'정답지'`**로 통일 |

---

## 4. prototype_clean/ 폴더 내 .html 파일 전체 목록 (총 38개)

1. `00_WORKFLOW_GUIDE_baseline.html`
2. `ADMN-BOOK-001_baseline.html`
3. `ADMN-BRD-001_baseline.html`
4. `ADMN-BRD-002_baseline.html`
5. `ADMN-BRD-005_baseline.html`
6. `ADMN-CONF-001_baseline.html`
7. `ADMN-CONF-002_baseline.html`
8. `ADMN-CONF-003_baseline.html`
9. `ADMN-CONF-004_baseline.html`
10. `ADMN-CONF-005_baseline.html`
11. `ADMN-CONF-010_baseline.html`
12. `ADMN-DASH-001_baseline.html`
13. `ADMN-INST-001_baseline.html`
14. `ADMN-INST-002_baseline.html`
15. `ADMN-LOGIN-001_baseline.html`
16. `ADMN-ORD-001_baseline.html`
17. `ADMN-PROD-001_baseline.html`
18. `ADMN-PROD-002_baseline.html`
19. `ADMN-PROD-003_baseline.html`
20. `ADMN-PROD-004_baseline.html`
21. `ADMN-PROD-005_baseline.html`
22. `ADMN-PROD-006_baseline.html`
23. `ADMN-PROD-007_baseline.html`
24. `ADMN-PROM-001_baseline.html`
25. `ADMN-PROM-002_baseline.html`
26. `ADMN-RFD-002_baseline.html`
27. `ADMN-SETT-001_baseline.html`
28. `ADMN-SETT-002_baseline.html`
29. `ADMN-SETT-004_baseline.html`
30. `ADMN-SETT-005_baseline.html`
31. `ADMN-SETT-006_baseline.html`
32. `ADMN-SETT-007_baseline.html`
33. `ADMN-SETT-008_baseline.html`
34. `ADMN-SETT-009_baseline.html`
35. `ADMN-SETT-011_baseline.html`
36. `ADMN-USER-001_baseline.html`
37. `ADMN-USER-007_baseline.html`
38. `patch_all_snb_v3.html`
