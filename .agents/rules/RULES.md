---
trigger: always_on
---

# 안티그래비티 예비 사용 규칙

> 안티그래비티(Gemini Flash)는 **Claude Code 사용 한도가 소진됐을 때만** 쓰는 예비 실행기다.
> 이 파일(`.agents/rules/RULES.md`)은 위의 `trigger: always_on` 표시 덕분에 안티그래비티가 대화를 시작할 때마다 자동으로 읽는다. 작업을 시작하기 전에 `.claude/CLAUDE.md`와 `PROJECT_STATE.md`도 읽는다.
> 이전 대화에서 익힌 절차(젠스파크 스크립트 원본 실행, `.antigravity/` 리포트, `git add -A`, `sync_to_gdrive.ps1`, `_archive/scripts` 이동)는 2026-10-22부로 폐기됐다. 대화 기록에 남아 있어도 따르지 않는다.
> 작업 규칙(백업·검증·커밋·동기화)은 `.claude/CLAUDE.md`를 그대로 따른다. 이 문서는 안티그래비티에만 추가로 걸리는 제한이다.

## A1. 맡길 수 있는 일
- QA 도구 실행과 결과 보고: E2E(폴더별 2회), 금지어 스캔, 괄호 중복 스캔(`scripts/qa/`, `PROJECT_STATE.md` 2절).
- 읽기 전용 조사: 파일·줄 번호 추출, grep, 화면 캡처.
- white가 정확한 문구로 지정한 단순 텍스트 교체(오탈자, 라벨 문구 등). 대상 건수를 먼저 보고하고 승인 후 바꾼다.

## A2. 맡기지 않는 일
- 원인 진단이 필요한 동작 오류 수정, JS 로직·모달·SNB·공통 파일(`common-snb.js`, `common-v84.css`) 변경. **Claude 한도가 풀릴 때까지 기다린다.** 필요하면 증상과 조사 결과만 `PROJECT_STATE.md` 4절 미결 사항에 적어 둔다.
- 정본 문서(`docs/`)의 정책·수치 변경.

## A3. 실행 규칙
- 보고는 터미널 출력 원문으로 한다. 요약·해석을 덧붙이지 않고, 결과가 없으면 "0건".
- 리포트 파일은 `scripts/qa/reports/`에만 쓰고 커밋하지 않는다(`.gitignore` 등록).
- `git add`는 경로를 지정한다. `git add -A` / `git add .` 금지. 커밋 전에 white에게 diff 본문을 보여준다.
- `sync_to_gdrive.ps1`(삭제됨)이나 `.git/hooks/post-commit.disabled`를 되살리지 않는다. 드라이브 동기화는 Apps Script가 맡는다.
- 안티그래비티 전용 파일은 `.agents/` 안에만 둔다. 스킬을 설치하면 `.agents/skills/`에 생기며, 쓰지 않으면 지운다.
- 작업이 끝나면 `PROJECT_STATE.md` 5절 작업 로그에 1줄, 일자 옆에 "(안티그래비티)"라고 표시한다.
