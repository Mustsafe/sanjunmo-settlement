# ANTIGRAVITY AGENT RULES (영구 고정 — 매 작업 시작 전 필독)

> 상세 메모리: `.antigravity/AGENT_PIPELINE_MEMORY.md` (반드시 함께 열람)

## R1. 임의 코딩 금지
- 백오피스 HTML/JS/CSS 구현 및 패치 스크립트 작성 = 분석 AI(젠스파크 Chat) + 코딩 전담 AI(Opus)의 역할.
- 전달받은 Python 패치 스크립트(`.py`)는 **단 한 글자도 개조하지 않고 그대로 실행**한다.
- 실행 실패 시 스크립트를 수정하지 말고 오류 로그를 리포트로 반환한다.

## R2. 로컬 멀티 스킬 구축·실행 전담 (`scripts/qa/`, 읽기 전용 검수)
- Skill 1 `skill_static_lint.py` — `<script>` 추출 후 `node --check`, 깨진 href, 중복 ID, 빈 `<tbody>`
- Skill 2 `skill_jargon_scan.py` — 금지어·기획서 내부 암호·번역 중복어 전수 탐지
- Skill 3 `skill_cross_data_check.py` — 강사·도서 정가/요율/계약번호 화면 간 교차 대조
- Skill 4 `skill_playwright_e2e.py` — 모달 열기/닫기, 탭 전환, 레이아웃 겹침

## R3. 리포트 발행 및 동기화
- 결과는 `docs/*_REPORT.md`로 저장.
- 즉시 `git add -A && git commit && git push origin main`.
- 구글 드라이브 동기화: `pwsh -ExecutionPolicy Bypass -File sync_to_gdrive.ps1` 실행 (Windows 로컬).

## R4. 기준선
- prototype/·prototype_clean/ 38개 화면 동기화, ORD-001·PROD-003·PROD-005 면세(EXEMPT) 정합화,
  전 화면 모달 닫기 핫픽스, ADMN-SETT-006 개편 + 4대 제출 자료 반영 완료.
