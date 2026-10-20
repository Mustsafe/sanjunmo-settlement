# update_plan_v1_1_and_extract_markup_base.py
# 1) WORKFLOW_REDESIGN_PLAN.md 갱신 (Set 2 흡수 확정 · STAGE 04 → STAGE 03 하위 · 미결/진행 정리 · 결정 로그)
# 2) 마크업 준비용 읽기 전용 추출 → .antigravity/reports/WORKFLOW_MARKUP_BASE.md
import re
import sys
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path.cwd()
PLAN = ROOT / ".antigravity" / "WORKFLOW_REDESIGN_PLAN.md"
CLEAN = ROOT / "prototype_clean"
WF = CLEAN / "00_WORKFLOW_GUIDE_baseline.html"
REF = CLEAN / "ADMN-SETT-002_baseline.html"
OUT = ROOT / ".antigravity" / "reports" / "WORKFLOW_MARKUP_BASE.md"

# ---------- 1. 플랜 갱신 ----------
NEW_MIGYEOL = """## 미결
- 없음 · 마크업 착수 가능
- 범위 밖 후속 과제: README 화면 인벤토리 정본 대조 갱신(CONF-010·LOGIN-002/003 누락, BRD-002/006 표기), SNB screenCode·정답지 메뉴명 정리

"""

STAGE03_AUDIT = """하위 블록(상시 · 월마감 주기와 무관): 변경·열람 기록 확인 — 정산 감사 로그 CONF-010 — 변경 전·후 비교
조건 칩: 민감정보 마스킹 해제 시 사유 입력 팝업(USER-007) · 일정 시간 후 자동 재마스킹
예외(감사): 보존기한 경과 시 개인정보만 파기, 금액 기록은 보존

"""

NEW_MIHWAKJEONG = """### 미확정
- 디렉터리 섹션: 마크업 단계에서 실제 파일 목록 + SNB 메뉴명 기준으로 바로 작성

"""

LOGS = """- 2026-10-21 · 정답지는 시스템 콘텐츠 유형이 아니라 운영자가 무료 콘텐츠 제목에 쓰는 명칭. 업무플로우 페이지에 별도 노드·칩 없음, 디렉터리는 BRD-005 SNB 메뉴명 칩 1개
- 2026-10-21 · 구 Set 2(오프라인 계약·도서·패키지) 정산 STAGE 01 흡수 확정. 운영 플로우는 회원·수강 / 출고·환불 / 문의·환급 3개
- 2026-10-21 · STAGE 04(상시 보안·감사) 폐지, STAGE 03 하위 '상시' 블록으로 이동. 정산 플로우 3단계
"""


def update_plan():
    if not PLAN.exists():
        return ["플랜 파일 없음"]
    t = PLAN.read_text(encoding="utf-8")
    errs = []

    def sub(pattern, repl, label, flags=re.S):
        nonlocal t
        t2, n = re.subn(pattern, repl, t, count=1, flags=flags)
        if n == 0:
            errs.append(f"매칭 실패: {label}")
        t = t2

    sub(r"정산 플로우\(STAGE 01~04\)", "정산 플로우(STAGE 01~03)", "확정결정 섹션 수")
    sub(r"## 미결\n.*?(?=## 진행 단계)", NEW_MIGYEOL, "미결 섹션")
    sub(r"1\. \[ \] 정본 추출", "1. [x] 정본 추출", "진행 1")
    sub(r"2\. \[ \] 노드 문구표", "2. [x] 노드 문구표", "진행 2")
    sub(r"3\. \[ \] white 확인", "3. [x] white 확인 (구조 확정 · 문구는 마크업 화면에서 최종 확인)", "진행 3")
    sub(r"초안 v1 · 2026-10-21 · white 확인 대기",
        "초안 v1.1 · 2026-10-21 · 구조 확정(Set 2 → STAGE 01 흡수, STAGE 04 → STAGE 03 하위)", "문구표 머리")
    sub(r"- 월 정산: 계약·상품 설정 → 사전 검증 → 정산·집행 → 보안·감사",
        "- 월 정산: 계약·상품 설정 → 사전 검증 → 정산·집행·감사", "첫 화면 칩")
    sub(r"#### STAGE 03 · 정산 실행·마감·집행\n", "#### STAGE 03 · 정산 실행·마감·집행·감사\n", "STAGE 03 제목")
    sub(r"#### STAGE 04 · 상시 보안·감사\n.*?(?=### 미확정)", STAGE03_AUDIT, "STAGE 04 블록")
    sub(r"### 미확정\n.*?(?=## 결정 로그)", NEW_MIHWAKJEONG, "미확정 블록")

    if errs:
        return errs
    t = t.rstrip() + "\n" + LOGS
    PLAN.write_text(t, encoding="utf-8")
    return []


# ---------- 2. 마크업 기초 추출 ----------
def strip_css_comments(s):
    return re.sub(r"/\*.*?\*/", "", s, flags=re.S)


def css_summary(css):
    css = strip_css_comments(css)
    vars_ = re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", css)
    classes = sorted(set(re.findall(r"\.([A-Za-z_][\w-]*)", "".join(re.findall(r"([^{}]+)\{", css)))))
    return vars_, classes


class Skeleton(HTMLParser):
    VOID = {"meta", "link", "br", "img", "input", "hr", "source"}

    def __init__(self, maxdepth):
        super().__init__()
        self.d, self.max, self.lines, self.on = 0, maxdepth, [], False

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.on = True
        if self.on and self.d <= self.max and tag not in ("script", "style"):
            a = dict(attrs)
            s = tag
            if a.get("id"):
                s += "#" + a["id"]
            if a.get("class"):
                s += "." + ".".join(a["class"].split())
            if a.get("onclick"):
                s += f"  [onclick={a['onclick'][:50]}]"
            if a.get("href"):
                s += f"  [href={a['href'][:50]}]"
            self.lines.append("  " * self.d + s)
        if tag not in self.VOID:
            self.d += 1

    def handle_endtag(self, tag):
        if tag not in self.VOID:
            self.d = max(0, self.d - 1)


def skeleton(html, depth, cap):
    p = Skeleton(depth)
    p.feed(html)
    out, prev, n = [], None, 0
    for ln in p.lines + [None]:
        if ln == prev:
            n += 1
            continue
        if prev is not None:
            out.append(prev + (f"  ×{n}" if n > 1 else ""))
        prev, n = ln, 1
    if len(out) > cap:
        out = out[:cap] + [f"... ({len(out) - cap}줄 생략)"]
    return out


def extract():
    R = ["# 업무플로우 마크업 기초 추출", "", "> update_plan_v1_1_and_extract_markup_base.py 자동 생성 · 읽기 전용", ""]

    css_files = sorted(CLEAN.rglob("common-v84.css"))
    R += ["## 1. common-v84.css", "", f"경로: {', '.join(str(c.relative_to(ROOT)) for c in css_files) or '미발견'}", ""]
    if css_files:
        v, c = css_summary(css_files[0].read_text(encoding="utf-8", errors="replace"))
        R += ["### CSS 변수", ""] + [f"- `{k}: {val.strip()[:60]}`" for k, val in v] + [""]
        R += [f"### 클래스 ({len(c)}개)", "", ", ".join(c), ""]

    wf = WF.read_text(encoding="utf-8", errors="replace")
    head = re.search(r"<head.*?</head>", wf, re.S)
    head = head.group(0) if head else ""
    R += ["## 2. 현재 페이지 <head>", ""]
    R += ["### 외부 에셋"] + [f"- {m}" for m in re.findall(r"<(?:link|script)[^>]+(?:href|src)=\"[^\"]+\"[^>]*>", head)] + [""]
    inline_css = "".join(re.findall(r"<style[^>]*>(.*?)</style>", wf, re.S))
    v2, c2 = css_summary(inline_css)
    R += [f"### 인라인 스타일 클래스 ({len(c2)}개)", "", ", ".join(c2), ""]
    R += [f"### 인라인 스타일 변수 ({len(v2)}개)", "", ", ".join(k for k, _ in v2), ""]

    R += ["## 3. 현재 페이지 body 뼈대 (depth 6)", "", "```"] + skeleton(wf, 6, 160) + ["```", ""]

    if REF.exists():
        ref = REF.read_text(encoding="utf-8", errors="replace")
        rhead = re.search(r"<head.*?</head>", ref, re.S)
        R += ["## 4. 참고 화면 ADMN-SETT-002 <head> 에셋", ""]
        R += [f"- {m}" for m in re.findall(r"<(?:link|script)[^>]+(?:href|src)=\"[^\"]+\"[^>]*>", rhead.group(0) if rhead else "")] + [""]
        R += ["## 5. 참고 화면 ADMN-SETT-002 body 뼈대 (depth 5)", "", "```"] + skeleton(ref, 5, 90) + ["```", ""]

    R += ["## 6. 현재 페이지 인라인 스크립트", ""]
    scripts = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", wf, re.S)
    for i, s in enumerate(scripts, 1):
        s = s.strip()
        R += [f"### script {i} ({len(s):,}자)", "```js", s[:2500] + ("\n... (생략)" if len(s) > 2500 else ""), "```", ""]
    if not scripts:
        R.append("(없음)")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(R), encoding="utf-8")
    size = len(OUT.read_text(encoding="utf-8"))
    print(f"[OK] {OUT.relative_to(ROOT)} ({size:,}자){'  [WARN] 30,000자 초과' if size > 30000 else ''}")


def main():
    if not WF.exists():
        print("[ERROR] 업무플로우 파일 없음")
        sys.exit(1)
    errs = update_plan()
    if errs:
        print("[ABORT-PLAN] 플랜 파일 미변경:")
        for e in errs:
            print("  -", e)
    else:
        print("[OK] 플랜 파일 v1.1 갱신")
    extract()
    if errs:
        sys.exit(2)


if __name__ == "__main__":
    main()
