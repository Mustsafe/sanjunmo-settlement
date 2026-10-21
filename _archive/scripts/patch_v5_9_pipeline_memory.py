import sys, os, re, shutil, datetime
sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = os.path.join(ROOT, "_archive", "backup", f"v5_9_{TS}")
MEM = ".antigravity/AGENT_PIPELINE_MEMORY.md"

def read(p):
    with open(os.path.join(ROOT, p), "r", encoding="utf-8", newline="") as f:
        return f.read()

def write(p, t):
    with open(os.path.join(ROOT, p), "w", encoding="utf-8", newline="") as f:
        f.write(t)

SEC_0_2 = """

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
"""

SEC_2_ADD = """
- (2026-10-21) 업무플로우 페이지 v5 전면 개편 및 prototype/ 반영, SNB 9개 그룹·메뉴 43개 양쪽 정렬, 전 화면 브레드크럼 정본 그룹명 적용
- (2026-10-21) 정답지 독립 화면 폐지(BRD-005 탭 정리, CONF-005 저작권자 권한 문구 정리), 미실행 옛 SNB 코드 삭제
- (2026-10-21) clean 렌더링 괄호 중복 163건 → 1건(SETT-006 금액 표기, 정상 유지)
"""

SEC_5 = """

---

## 5. 현재 상태 및 다음 작업 (2026-10-21 · v5.8 기준)

**상태**
- 활성 화면 37개(양쪽 폴더). E2E `prototype_clean` 37/37, `prototype` 37/37 PASS, 콘솔 에러 0건.
- 괄호 중복: clean 1건(정상), prototype 6건(기획 검수용 기준으로 유지).

**미결 사항**
- clean HTML 원문의 `ADMN-` 코드 251자리: 런타임 치환으로 화면에는 안 보임. 원문 정리 여부 미정.
- ORD-001 "도서 인세 (+1권)": 원 문구 미확인 상태에서 정한 판단값.
- Skill 1(정적 문법 검사)·Skill 3(화면 간 데이터 대조) 미구축.
- README 화면 수 표기(38개) 갱신 여부 확인 필요.

**다음 세션 작업: 개별 HTML 점검 및 동작 오류 세부 수정**
1. white가 화면·증상을 지정(스크린샷 포함 가능).
2. 안티그래비티가 읽기 전용으로 해당 구간 원문·줄 번호 추출 → `.antigravity/reports/` 저장.
3. 젠스파크가 문구 기반 단일 패치 스크립트 작성(0-2 규칙).
4. 실행 → E2E 2회 + 해당 화면 Playwright 캡처로 확인.
"""

LOG_ADD = """| 2026-10-21 | 업무플로우 페이지 v5 clean 전면 개편(첫 화면 진입 카드 2장, 운영 3세트, 정산 3단계, 화면 디렉터리) | `prototype_clean/00_WORKFLOW_GUIDE_baseline.html`, 커밋 `6e74a31` |
| 2026-10-21 | v5.1~v5.3 SNB 정렬(SETT-010·CONF-006 메뉴 제거, USER-007 보안 그룹), 브레드크럼 정본 그룹명, prototype/ `SNB_GROUPS` 정렬, 업무플로우 prototype/ 덮어쓰기(6단계) | `prototype*/common-snb.js`, `prototype*/*.html`, 커밋 `3c8c53c` 외 |
| 2026-10-21 | v5.4 정답지 정리(BRD-005 탭 제거, 치환표 정리), 옛 SNB 코드 삭제, `patch_all_snb_v3.html` 보관(활성 37개), E2E 폴더 인자 추가 | `prototype*/ADMN-BRD-005_baseline.html`, `scripts/qa/skill_playwright_e2e.py` |
| 2026-10-21 | v5.5 CONF-005 저작권자 권한 정답지 문구 제거, E2E 스크립트 LF 복원 | `prototype*/ADMN-CONF-005_baseline.html`, 커밋 `3ed5618` |
| 2026-10-21 | v5.6~v5.8 clean 괄호 중복 정리(코드만 든 괄호 선제거, 원문 중복 수정) 163건 → 1건, `scan_paren_dup.py` 구축 | `prototype_clean/common-snb.js`, `prototype_clean/*.html`, 커밋 `790d650` 외 |
| 2026-10-21 | v5.9 파이프라인 메모리 갱신(운영 규칙 0-2, 현재 상태 5절) | `.antigravity/AGENT_PIPELINE_MEMORY.md` |
"""

errors = []
if not os.path.exists(os.path.join(ROOT, MEM)):
    print(f"[ABORT] {MEM} 파일 없음"); sys.exit(1)

raw = read(MEM)
nl = "\r\n" if "\r\n" in raw else "\n"
t = raw.replace("\r\n", "\n")

def rep(old, new):
    global t
    n = t.count(old)
    if n != 1:
        errors.append(f"문구 {n}건 (기대 1건): {old[:70]}")
        return
    t = t.replace(old, new)

def ins_before(pattern, block):
    global t
    m = list(re.finditer(pattern, t))
    if len(m) != 1:
        errors.append(f"위치 {len(m)}건 (기대 1건): {pattern}")
        return
    i = m[0].start()
    t = t[:i] + block.rstrip("\n") + t[i:]

rep("> 최초 등록: 2026-10-20", "> 최초 등록: 2026-10-20 · 최종 갱신: 2026-10-21 (v5.8 기준)")
rep("38개 화면 인벤토리", "화면 인벤토리, 현행 활성 37개")
rep("| 38개 HTML 내 `<script>`", "| 전 HTML 내 `<script>`")
rep("| Skill 4 | `scripts/qa/skill_playwright_e2e.py` | Playwright 기반 모달 열기/닫기, 탭 전환, 레이아웃 겹침 검수 | **구축 완료** |",
    "| Skill 4 | `scripts/qa/skill_playwright_e2e.py` | Playwright 기반 모달 열기/닫기, 탭 전환, 레이아웃 겹침 검수. 폴더 인자 필수: `python scripts/qa/skill_playwright_e2e.py prototype_clean` / `... prototype` (폴더별 2회) | **구축 완료** |\n"
    "| Skill 5 | `scripts/qa/scan_paren_dup.py` | Playwright 렌더링 후 괄호 중복 탐지(양쪽 폴더) + clean 원문 `ADMN-` 코드 자리 집계 → `.antigravity/reports/PAREN_DUP_SCAN.md`, `PAREN_DUP_STATIC.md` | **구축 완료** |")
rep("결과를 `docs/` 하위 마크다운 리포트(예:", "결과를 `.antigravity/reports/` 하위 마크다운 리포트(예:")
rep("sanjunmo-settlement/main/docs/<REPORT>.md", "sanjunmo-settlement/main/.antigravity/reports/<REPORT>.md")
rep("- `prototype/` 및 `prototype_clean/` 38개 화면 동기화 완료",
    "- `prototype/` 및 `prototype_clean/` 활성 37개 화면 동기화 완료 (2026-10-21 `patch_all_snb_v3.html` 보관 후 기준)")
rep("1. `.antigravity/AGENT_PIPELINE_MEMORY.md`, `.antigravity/RULES.md`, `README.md`, `docs/BACKOFFICE_ALIGNMENT_MASTER_PLAN.md` 열람",
    "1. `.antigravity/AGENT_PIPELINE_MEMORY.md`, `.antigravity/RULES.md`, `README.md` 열람 (`BACKOFFICE_ALIGNMENT_MASTER_PLAN.md`는 10-20 작업 로그 기준 `_archive/docs/` 보관)")
rep("4. QA 스킬 실행 (예: `python scripts/qa/skill_jargon_scan.py`)",
    "4. QA 실행: `python scripts/qa/skill_playwright_e2e.py prototype_clean`, `python scripts/qa/skill_playwright_e2e.py prototype` (필요 시 `skill_jargon_scan.py`, `scan_paren_dup.py`)")
rep("`docs/*_REPORT.md` 발행", "`.antigravity/reports/*.md` 발행(실행 스크립트는 `_archive/scripts/` 이동)")

ins_before(r"\n+---\n+## 1\. 핵심 역할과 금지 사항", SEC_0_2)
ins_before(r"\n+---\n+## 3\. 표준 작업 루틴", SEC_2_ADD)
ins_before(r"\n+---\n+## 4\. 작업 로그", SEC_5)

if errors:
    print("[ABORT]")
    for e in errors:
        print("  " + e)
    print("파일 미변경. 이 출력 전문을 분석 AI에 그대로 전달하세요.")
    sys.exit(1)

t = t.rstrip("\n") + "\n" + LOG_ADD

dst = os.path.join(BACKUP, MEM)
os.makedirs(os.path.dirname(dst), exist_ok=True)
shutil.copy2(os.path.join(ROOT, MEM), dst)
write(MEM, t.replace("\n", nl))
print(f"[OK] {MEM} 갱신 · 치환 10건 · 섹션 삽입 3건 · 로그 6행 · 백업 {os.path.relpath(BACKUP, ROOT)}")

print("[CHECK] README.md 내 '38' 포함 줄 (수정 안 함)")
if os.path.exists(os.path.join(ROOT, "README.md")):
    hits = [(i, l.rstrip()) for i, l in enumerate(read("README.md").splitlines(), 1) if "38" in l]
    for i, l in hits:
        print(f"  L{i}: {l[:160]}")
    if not hits:
        print("  0건")
print("[CHECK] docs/BACKOFFICE_ALIGNMENT_MASTER_PLAN.md 존재:",
      os.path.exists(os.path.join(ROOT, "docs", "BACKOFFICE_ALIGNMENT_MASTER_PLAN.md")))
