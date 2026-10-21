# CLAUDE.md — 산준모닷컴 정산·백오피스

## 기본 원칙
- 모든 응답·진행 메시지·요약은 **한국어**로 작성한다.
- 작업 공간은 `D:\Work\` 이다. C 드라이브에 파일·패키지·메모리 등을 설치하거나 저장하지 않는다.
  - 임시 파일, 설정, 메모, 리포트는 모두 프로젝트 폴더(`D:\Work\Settlement\`) 안에 둔다.
  - 기억해야 할 사항은 이 `CLAUDE.md`에 추가한다.

## 작업 시작 전
1. `git pull origin main` — Apps Script가 구글 드라이브에서 고친 문서를 GitHub에 커밋하므로 반드시 먼저 받는다. 안 받으면 드라이브 수정분을 옛 버전으로 덮어쓸 수 있다.
2. 참고 문서
   - `README.md`: 아키텍처·표준 정책·화면 인벤토리
   - `.antigravity/AGENT_PIPELINE_MEMORY.md`: 확정 기준(0-2절), 현재 상태·미결 사항(5절), 작업 로그(4절)
3. 대형 HTML(1,000줄 이상)은 통째로 읽지 않고 grep으로 필요한 줄만 본다.

## 역할 (2026-10-21 재편)
| 주체 | 역할 |
| :--- | :--- |
| Claude Code | 진단, 패치 작성·실행, Playwright 검증, 커밋·푸시까지 한곳에서 수행 |
| 안티그래비티 | 사용량이 빠듯할 때만 대량·기계적 작업(양쪽 37개 화면 전체 E2E, 전 파일 일괄 스캔). 결과는 PASS/FAIL 합계와 FAIL 줄만 받는다. 리포트 편집 금지 |
| 젠스파크 | 이 프로젝트에서는 사용하지 않음 |
| 구글 드라이브 | 아래 "구글 드라이브 동기화" 참고 |

## 구글 드라이브 동기화 (2026-10-22 가동)
- Apps Script(`scripts/gas/sync_settlement.gs`)가 GitHub `main` ↔ 공유 문서함 `산준모 닷컴/04.설계서/정산시스템`을 6시간마다 양방향 동기화한다. `_archive/backup/`은 제외.
  - 드라이브에서 고친 파일은 `drive-sync:` 커밋으로 올라온다 → 작업 전 `git pull` 필수.
  - 양쪽이 같은 파일을 고치면 원래 이름엔 GitHub 버전, 드라이브 버전은 `_drive충돌_` 사본으로 남고 메일이 온다.
  - 동기화 스크립트를 고치면 `sync_settlement.gs`와 Apps Script 편집기 양쪽에 반영한다. 토큰(`GH_TOKEN`)은 스크립트 속성에만 둔다.
- 예전 방식은 쓰지 않는다.
  - `sync_to_gdrive.ps1`: 커밋마다 `04.설계서/docs`에 덮어쓰던 스크립트. v6.4에서 삭제(git 이력에만 있음). 되살려 실행하지 않는다.
  - 이 PC의 `.git/hooks/post-commit`은 `post-commit.disabled`로 꺼둠. 되살리지 않는다.
  - 예전 사본 폴더 `04.설계서/docs`는 2026-10-22 삭제했다. 이제 `04.설계서` 아래에는 `정산시스템/`(동기화 대상)과 `User_Wireframe/`(저장소와 무관)만 있다.

## 문서 정본 위치
- `docs/산준모닷컴 구축 통합 상세 설계서.md`는 프론트와 백오피스를 함께 다루는 상위 문서지만, 정본은 이 저장소 `docs/`에 둔다(드라이브에서는 `04.설계서/정산시스템/docs/`). 다른 곳에 사본을 만들지 않는다(2026-10-22 결정).
- 문서 우선순위는 메모리 문서 0-1절 3번을 따른다.

## 수정 작업 규칙
- 기능 패치는 `prototype/`·`prototype_clean/` 동명 파일에 동시 반영한다. 두 폴더의 성격 차이와 확정 기준은 메모리 문서 0-2절을 따른다.
- 줄 번호가 아니라 문구로 찾는다. 대상 건수가 기대값과 다르면 전체 중단하고 파일을 바꾸지 않는다.
- 스크립트로 일괄 수정할 때
  - 저장 전 `_archive/backup/v<버전>_<시각>/` 에 백업한다(`.gitignore` 등록, 로컬 전용).
  - 저장 후 Playwright로 해당 동작을 검증하고, 실패하면 원본으로 되돌린다.
  - 상단에 `sys.stdout.reconfigure(encoding="utf-8")`, 파일 입출력은 `newline=""`로 CRLF/LF를 보존한다.
  - 패치·진단 스크립트와 리포트는 저장소에 남기지 않는다. 검증 결과 요약은 커밋 메시지 본문과 메모리 문서 작업 로그에 적는다. 지난 산출물은 git 이력에서 꺼내 본다(2026-10-22 v6.4에서 `_archive/`, `.antigravity/reports/` 정리).
  - `.antigravity/reports/`는 QA 스크립트 출력 폴더로만 쓰며 `.gitignore`에 등록돼 있다.
- 화면 문구 검사는 HTML grep이 아니라 Playwright 렌더링 기준으로 한다(`prototype_clean/common-snb.js`가 로드 후 문구를 런타임 치환).

## 검증
- E2E(폴더별 2회, UTF-8 출력):
  - `PYTHONIOENCODING=utf-8 python scripts/qa/skill_playwright_e2e.py prototype`
  - `PYTHONIOENCODING=utf-8 python scripts/qa/skill_playwright_e2e.py prototype_clean`
- 기준선: 양쪽 37/37 PASS, 콘솔 에러 0건.

## 커밋 규칙
- 커밋 전에 white에게 diff 본문을 보여주고 승인을 받는다(작성자와 검수자가 같아진 데 대한 교차 검증).
- `git add`는 경로를 지정한다. `git add -A` / `git add .` 금지(로컬 백업·`.claude/`가 섞이는 것 방지).
- `main`에 직접 커밋한다. 메시지 형식: `v<버전> <화면 코드> <요약>`.
- 작업이 끝나면 메모리 문서 4절 작업 로그에 1줄, 상태가 바뀌면 5절도 갱신한다.

## 알려진 함정
- 공통 모달 닫기 핫픽스(`UNIVERSAL-MODAL-CLOSER-HOTFIX`, 각 HTML 두 번째 `<script>`)는 로드 시 모든 모달 백드롭에 인라인 `display:none !important`를 건다. `hidden` 클래스만 떼서 여는 모달은 열리지 않는다. 열 때 `open` 클래스를 붙이고 인라인 `display`를 지우고, 닫을 때 `open`을 뗀다(SETT-005 v6.0·v6.1 참고).
