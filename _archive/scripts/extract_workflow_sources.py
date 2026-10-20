# extract_workflow_sources.py
# 업무플로우 개편용 정본 추출 (읽기 전용 · HTML 미수정)
# 산출: .antigravity/WORKFLOW_REDESIGN_PLAN.md (없을 때만 생성)
#       .antigravity/reports/WORKFLOW_SOURCE_EXTRACT.md (화면 코드 대조)
#       .antigravity/reports/WORKFLOW_CURRENT_TEXT.md (현재 페이지 본문 텍스트)
import re
import sys
from pathlib import Path
from html.parser import HTMLParser
from collections import defaultdict

ROOT = Path.cwd()
DOCS = ROOT / "docs"
CLEAN = ROOT / "prototype_clean"
OUT_DIR = ROOT / ".antigravity" / "reports"
PLAN = ROOT / ".antigravity" / "WORKFLOW_REDESIGN_PLAN.md"
VOL03 = DOCS / "[산준모 정산시스템]_03_백오피스화면_외부연동_및_데이터사전.md"
B2C = DOCS / "산준모닷컴 구축 통합 상세 설계서.md"
README = ROOT / "README.md"
WF = CLEAN / "00_WORKFLOW_GUIDE_baseline.html"

BASE_RE = re.compile(r"ADMN-[A-Z]+-\d{3}")
RANGE_RE = re.compile(r"(ADMN-[A-Z]+-)(\d{3})\s*~\s*(?:ADMN-[A-Z]+-)?(\d{3})")


def read(p):
    return p.read_text(encoding="utf-8", errors="replace")


def codes_in(text):
    """단일 코드 + 범위 표기(ADMN-PROD-001 ~ ADMN-PROD-007) 확장"""
    found = set(BASE_RE.findall(text))
    for pre, a, b in RANGE_RE.findall(text):
        a, b = int(a), int(b)
        if 0 < b - a <= 20:
            found.update(f"{pre}{n:03d}" for n in range(a, b + 1))
    return found


def cells(row):
    return [c.strip().strip("*").strip() for c in row.strip().strip("|").split("|")]


def table_after(text, heading_kw):
    out, started = [], False
    for ln in text.splitlines():
        s = ln.strip()
        if not started:
            if s.startswith("#") and heading_kw in s:
                started = True
            continue
        if s.startswith("|"):
            out.append(s)
        elif out and s:
            break
    return out


def name_map(rows):
    m = {}
    for r in rows:
        c = cells(r)
        if len(c) >= 2 and BASE_RE.fullmatch(c[0]):
            m[c[0]] = c[1]
    return m


def b2c_pair_rows(text):
    """[A] 페어 매핑표 구간의 ADMN 포함 행 수집 ([B] 만나면 종료)"""
    rows, on, heading = [], False, ""
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith("#"):
            heading = s.lstrip("#").strip().strip("*")
        if "[A]" in s and ("매핑" in s or "페어" in s):
            on = True
            continue
        if on and "[B]" in s:
            on = False
            continue
        if on and s.startswith("|") and BASE_RE.search(s):
            rows.append((heading[:60], s[:260]))
    return rows


class TextDump(HTMLParser):
    BLOCK = {"p", "div", "li", "tr", "section", "header", "br", "summary", "ul", "ol", "table"}

    def __init__(self):
        super().__init__()
        self.skip = 0
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1
            return
        if tag in ("h1", "h2", "h3", "h4"):
            self.buf.append("\n\n" + "#" * int(tag[1]) + " ")
        elif tag in self.BLOCK:
            self.buf.append("\n")
        elif tag in ("td", "th"):
            self.buf.append(" | ")
        a = dict(attrs)
        tgt = ""
        m = re.search(r"goScreen\(['\"]([^'\"]+)['\"]\)", a.get("onclick") or "")
        if m:
            tgt = m.group(1)
        elif (a.get("href") or "").endswith(".html"):
            tgt = a["href"]
        if tgt:
            self.buf.append(f" [→{tgt}] ")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = max(0, self.skip - 1)
        elif tag in self.BLOCK or tag in ("h1", "h2", "h3", "h4"):
            self.buf.append("\n")

    def handle_data(self, data):
        if self.skip:
            return
        t = re.sub(r"\s+", " ", data)
        if t.strip():
            self.buf.append(t)

    def text(self):
        lines = [l.strip() for l in "".join(self.buf).splitlines()]
        out, blank = [], False
        for l in lines:
            if not l:
                if not blank:
                    out.append("")
                blank = True
            else:
                out.append(l)
                blank = False
        return "\n".join(out).strip()


PLAN_MD = """# 업무플로우 페이지(00_WORKFLOW_GUIDE) 전면개편 플랜

> 새 세션은 이 파일만 읽고 이어서 작업한다. 결정이 바뀌면 이 파일을 먼저 갱신한다.

## 확정 결정
- clean 기준으로만 작업, 완료 후 prototype/ 동명 파일에 덮어쓰기 (이 페이지 한정 예외)
- 섹션 4개: 첫 화면(진입 카드 2장) / 운영 플로우(Set) / 정산 플로우(STAGE 01~04) / 화면 디렉터리
- 짙은 그라데이션 hero 제거. 공통 에셋·SNB 유지, 본문만 전용 레이아웃
- 예외 상황: 각 단계 하단, 점선 테두리 + 연주황 배경, 기본 접힘(details)
- DB 컬럼·상태값 코드 전면 제거, 한글 의미로 표기. 화면 코드는 회색 라벨로만
- 문장형 금지. 노드 = 할 일(동사형 12자 이내) / 화면(한글명 + 코드 라벨) / 결과 1줄 / 조건 칩 최대 2개
- 순서 없는 업무 묶음은 화살표 대신 '상황 → 처리' 짝 배치. 1:1 문의는 분기 그림
- 정산 계산 1~11단계는 STAGE 03 안 접힘 영역(한글 단계명 + 사용 화면만)
- 시나리오 치트시트 섹션 폐지, 각 단계 예외로 흡수
- 색: 운영=teal, 정산=pri(blue), 예외=warn. 기존 CSS 변수 재사용

## 미결
- Set 2(오프라인 계약·도서·패키지)를 정산 STAGE 01로 흡수할지
- 화면 코드·화면명 기준: 정본 docs/ 대조 결과(WORKFLOW_SOURCE_EXTRACT.md)로 확정
- SETT-010, CONF-006 정본 존재 여부

## 진행 단계
1. [ ] 정본 추출 리포트 생성 (extract_workflow_sources.py)
2. [ ] 노드 문구표 정본 대조·수정 → 본 파일 하단에 확정본 기록
3. [ ] white 확인
4. [ ] 마크업 패치 스크립트 (clean)
5. [ ] Playwright 검수 38/38
6. [ ] prototype/ 덮어쓰기

## 노드 문구표 (확정본)
(2단계 완료 후 기록)
"""


def main():
    missing = [str(p) for p in (VOL03, B2C, README, WF) if not p.exists()]
    if missing:
        print("[ERROR] 필수 파일 없음:", *missing, sep="\n  ")
        sys.exit(1)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 0. 플랜 파일
    if PLAN.exists():
        print(f"[SKIP] 플랜 파일 이미 존재: {PLAN.relative_to(ROOT)}")
    else:
        PLAN.write_text(PLAN_MD, encoding="utf-8")
        print(f"[OK] 플랜 파일 생성: {PLAN.relative_to(ROOT)}")

    v03 = read(VOL03)
    b2c = read(B2C)

    # 1. 03권 화면 대조표 / 코드값 사전
    t03 = table_after(v03, "용어·화면 대조표")
    n03 = name_map(t03)
    n03dict = name_map(table_after(v03, "코드값 사전"))

    # 2. 통합 설계서 [A] 페어 매핑표
    pairs = b2c_pair_rows(b2c)
    b2c_codes = set()
    for _, r in pairs:
        b2c_codes |= codes_in(r)

    # 3. docs 전체 코드 인덱스
    idx = defaultdict(set)
    for md in DOCS.rglob("*.md"):
        rel = md.relative_to(DOCS).as_posix()
        short = "screen_spec/" + md.name[:28] if "screen_spec" in rel else md.name[:34]
        for c in codes_in(read(md)):
            idx[c].add(short)

    # 4. SNB + HTML 파일
    snb_codes, snb_ctx = set(), {}
    snb_files = list(CLEAN.rglob("common-snb.js"))
    for f in snb_files:
        for ln in read(f).splitlines():
            for m in re.finditer(r"\b(?:ADMN-)?([A-Z]{3,5}-\d{3})\b", ln):
                code = "ADMN-" + m.group(1)
                snb_codes.add(code)
                if code not in snb_ctx:
                    snb_ctx[code] = re.sub(r"\s+", " ", ln.strip())[:160]
    html_codes = set()
    for p in CLEAN.glob("*.html"):
        html_codes |= codes_in(p.name)

    readme_codes = codes_in(read(README))

    # 5. 대조표
    allc = sorted(set(n03) | set(n03dict) | b2c_codes | readme_codes | snb_codes | html_codes)
    ck = lambda s, c: "✓" if c in s else "–"

    R = ["# 업무플로우 개편용 정본 추출 리포트", "",
         "> extract_workflow_sources.py 자동 생성 · 읽기 전용", ""]
    R += ["## 1. 03권 용어·화면 대조표 (원문)", ""] + (t03 or ["(미검출)"]) + [""]
    R += ["## 2. 화면 코드 통합 대조", "",
          "| 코드 | 03 대조표 화면명 | 03 코드값사전 명칭 | 통합설계서[A] | README | SNB | HTML 파일 | docs 등장 파일 수 |",
          "| :--- | :--- | :--- | :-: | :-: | :-: | :-: | :-: |"]
    for c in allc:
        R.append(f"| {c} | {n03.get(c, '')} | {n03dict.get(c, '')} | {ck(b2c_codes, c)} | "
                 f"{ck(readme_codes, c)} | {ck(snb_codes, c)} | {ck(html_codes, c)} | {len(idx.get(c, ()))} |")
    R += ["", "## 3. 불일치 요약", ""]
    canon = set(n03) | set(n03dict) | b2c_codes
    R.append(f"- SNB에 있으나 정본(03권·통합설계서[A])에 없음: {', '.join(sorted(snb_codes - canon)) or '없음'}")
    R.append(f"- 정본에 있으나 README에 없음: {', '.join(sorted(canon - readme_codes)) or '없음'}")
    R.append(f"- 정본에 있으나 SNB에 없음: {', '.join(sorted(canon - snb_codes)) or '없음'}")
    diff = [f"{c}: 대조표 '{n03[c]}' / 코드값사전 '{n03dict[c]}'"
            for c in sorted(set(n03) & set(n03dict)) if n03[c] not in n03dict[c]]
    R.append("- 03권 내부 명칭 불일치: " + ("; ".join(diff) if diff else "없음"))
    R += ["", "## 4. 통합설계서 [A] 페어 매핑표 행", ""]
    if pairs:
        R += [f"- [{h}] {r}" for h, r in pairs]
    else:
        R.append("(미검출 — '[A]' + '매핑/페어' 표제 패턴 불일치. 표제 형식 확인 필요)")
    R += ["", "## 5. SNB 코드별 첫 등장 라인", ""]
    R.append(f"SNB 파일: {', '.join(str(f.relative_to(ROOT)) for f in snb_files) or '미발견'}")
    R += [f"- {c}: `{snb_ctx[c]}`" for c in sorted(snb_ctx)]
    R += ["", "## 6. docs 내 코드 등장 파일 (정본 외 코드만)", ""]
    for c in sorted(set(idx) - canon):
        R.append(f"- {c}: {', '.join(sorted(idx[c]))}")

    rep = OUT_DIR / "WORKFLOW_SOURCE_EXTRACT.md"
    rep.write_text("\n".join(R), encoding="utf-8")

    # 6. 현재 페이지 본문
    td = TextDump()
    td.feed(read(WF))
    cur = OUT_DIR / "WORKFLOW_CURRENT_TEXT.md"
    cur.write_text("# 00_WORKFLOW_GUIDE_baseline.html (clean) 현재 본문 텍스트\n\n" + td.text(), encoding="utf-8")

    for p in (rep, cur):
        size = len(read(p))
        warn = "  [WARN] 30,000자 초과 — 분할 필요" if size > 30000 else ""
        print(f"[OK] {p.relative_to(ROOT)} ({size:,}자){warn}")
    print(f"     대조 코드 {len(allc)}개 · 03대조표 {len(n03)} · [A]행 {len(pairs)} · SNB {len(snb_codes)} · HTML {len(html_codes)}")


if __name__ == "__main__":
    main()
