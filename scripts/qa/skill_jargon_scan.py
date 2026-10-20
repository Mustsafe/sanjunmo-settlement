#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[Skill 2] SSOT 금지어 & 기획서 내부 암호 스캐너 (읽기 전용 QA 도구)

목적
  prototype_clean/*.html 화면의 '운영자 가시 텍스트'에 남아 있는
  - 기획서 내부 암호 (C-01~04, H-01~05, D-1~16, P1.1~5.1, Pipeline, 제N장, N.N절, *_flag/*_yn/*_id)
  - SSOT 금지어 (기출, 정오표, Vimeo, 80%, ①~⑭, [마커)
  - 번역 중복어 (예: 실결제금액(실결제금액))
  를 정규식으로 전수 탐지하여 docs/JARGON_SCAN_REPORT.md 로 발행한다.

스캔 범위
  [A] DOM 가시 텍스트 : <script>/<style>/주석 제외 텍스트 노드
                        + 가시 속성(placeholder, title, alt, aria-label, button/submit value)
  [B] JS 동적 렌더링 후보 : <script> 내부 문자열 리터럴 중 한글 포함 문자열 (innerHTML 등으로 화면 노출 가능)

의존성: Python 3.8+ 표준 라이브러리만 사용 (Windows/Linux 공용)
사용법:
  python scripts/qa/skill_jargon_scan.py
  python scripts/qa/skill_jargon_scan.py --target prototype_clean --out docs/JARGON_SCAN_REPORT.md
  python scripts/qa/skill_jargon_scan.py --strict   # [A] 탐지 1건 이상이면 exit 1
"""
import argparse
import datetime
import glob
import os
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# ---------------------------------------------------------------------------
# 탐지 규칙: (카테고리, 규칙ID, 설명, 정규식)
# ---------------------------------------------------------------------------
NB = r"(?<![A-Za-z0-9_\-])"  # 앞쪽 경계 (ADMN-, TX- 등 접두 코드와 구분)
RULES = [
    # --- 기획서 내부 암호 ---
    ("내부암호", "CODE_C", "C-01~04 (정산 케이스 코드)", re.compile(NB + r"C-0[1-4](?!\d)")),
    ("내부암호", "CODE_H", "H-01~05 (하드락 코드)", re.compile(NB + r"H-0[1-5](?!\d)")),
    ("내부암호", "CODE_D", "D-1~16 (회귀테스트 코드)", re.compile(NB + r"D-(?:1[0-6]|0?[1-9])(?![\d.]|\s*일)")),
    ("내부암호", "CODE_P", "P1.1~5.1 (Phase 코드)", re.compile(NB + r"P[1-5]\.\d+(?!\d)")),
    ("내부암호", "PIPELINE", "Pipeline 표기", re.compile(r"Pipeline(?:\s*\d+(?:\.\d+)*)?", re.I)),
    ("내부암호", "CHAPTER", "제N장 (기획서 장 번호)", re.compile(r"제\s*\d+\s*장")),
    ("내부암호", "SECTION", "N.N절 (기획서 절 번호)", re.compile(r"\d+(?:\.\d+)+\s*절")),
    ("내부암호", "SNAKE_FLAG", "*_flag DB 컬럼명", re.compile(r"\b[a-z][a-z0-9_]*_flag\b")),
    ("내부암호", "SNAKE_YN", "*_yn DB 컬럼명", re.compile(r"\b[a-z][a-z0-9_]*_yn\b")),
    ("내부암호", "SNAKE_ID", "*_id DB 컬럼명", re.compile(r"\b[a-z][a-z0-9_]*_id\b")),
    # --- SSOT 금지어 ---
    ("금지어", "BAN_GICHUL", "기출", re.compile(r"기출")),
    ("금지어", "BAN_ERRATA", "정오표", re.compile(r"정오표")),
    ("금지어", "BAN_VIMEO", "Vimeo", re.compile(r"Vimeo", re.I)),
    ("금지어", "BAN_80PCT", "80%", re.compile(r"(?<![\d.])80\s*%")),
    ("금지어", "BAN_CIRCLED", "①~⑭ 원문자 번호", re.compile(r"[\u2460-\u246D]")),
    ("금지어", "BAN_MARKER", "[마커 표기", re.compile(r"\[\s*마커")),
    # --- 번역 중복어 ---
    ("번역중복", "DUP_PAREN", "동일어 괄호 중복 (예: 실결제금액(실결제금액))",
     re.compile(r"([가-힣A-Za-z0-9_]{2,})\s*\(\s*\1\s*\)")),
]

VISIBLE_ATTRS = {"placeholder", "title", "alt", "aria-label"}
SKIP_TAGS = {"script", "style", "noscript", "template"}
JS_STR_RE = re.compile(r"""(`(?:\\.|[^`\\])*`|'(?:\\.|[^'\\\n])*'|"(?:\\.|[^"\\\n])*")""", re.S)
HANGUL_RE = re.compile(r"[가-힣]")


class VisibleTextParser(HTMLParser):
    """DOM 가시 텍스트 + 가시 속성 + script 본문을 (line, text) 단위로 수집."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.visible = []  # (line, source, text)
        self.scripts = []  # (start_line, code)
        self._script_buf = None
        self._script_line = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        line = self.getpos()[0]
        for k, v in attrs:
            if v and k in VISIBLE_ATTRS:
                self.visible.append((line, f"@{k}", v))
        if tag == "input" and a.get("type", "").lower() in ("button", "submit", "reset") and a.get("value"):
            self.visible.append((line, "@value", a["value"]))
        if tag in ("br", "img", "input", "meta", "link", "hr", "col", "source", "wbr"):
            return
        self.stack.append(tag)
        if tag == "script":
            self._script_buf = []
            self._script_line = line

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag == "script" and self._script_buf is not None:
            self.scripts.append((self._script_line, "".join(self._script_buf)))
            self._script_buf = None
        if tag in self.stack:
            while self.stack:
                if self.stack.pop() == tag:
                    break

    def handle_data(self, data):
        if self._script_buf is not None and self.stack and self.stack[-1] == "script":
            self._script_buf.append(data)
            return
        if any(t in SKIP_TAGS for t in self.stack):
            return
        if data.strip():
            self.visible.append((self.getpos()[0], "text", data))


def snippet(text, start, end, width=28):
    s = max(0, start - width)
    e = min(len(text), end + width)
    out = ("…" if s > 0 else "") + text[s:e] + ("…" if e < len(text) else "")
    out = re.sub(r"\s+", " ", out).strip()
    return out.replace("|", "\\|").replace("`", "'")


def scan_text(text):
    for cat, rid, desc, rx in RULES:
        for m in rx.finditer(text):
            yield cat, rid, m.group(0), m.start(), m.end()


def strip_tags(s):
    return re.sub(r"<[^>]+>", " ", s)


def scan_file(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        html = f.read()
    p = VisibleTextParser()
    p.feed(html)
    p.close()

    dom_hits, js_hits = [], []
    for line, src, text in p.visible:
        for cat, rid, match, s, e in scan_text(text):
            ln = line + text.count("\n", 0, s)
            dom_hits.append(dict(line=ln, src=src, cat=cat, rule=rid, match=match.strip(),
                                 ctx=snippet(text, s, e)))
    for sline, code in p.scripts:
        for m in JS_STR_RE.finditer(code):
            lit = m.group(0)[1:-1]
            if not HANGUL_RE.search(lit):
                continue  # 한글 없는 리터럴(셀렉터·키값 등)은 화면 노출 가능성 낮음 → 제외
            visible = strip_tags(lit)
            for cat, rid, match, s, e in scan_text(visible):
                ln = sline + code.count("\n", 0, m.start())
                js_hits.append(dict(line=ln, src="js-string", cat=cat, rule=rid, match=match.strip(),
                                    ctx=snippet(visible, s, e)))
    return dom_hits, js_hits


def build_report(target, files, results):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rule_desc = {r[1]: (r[0], r[2]) for r in RULES}
    tot_dom = sum(len(d) for d, _ in results.values())
    tot_js = sum(len(j) for _, j in results.values())
    clean = [f for f, (d, j) in results.items() if not d and not j]

    L = []
    L.append("# JARGON SCAN REPORT — 기획서 내부 암호 · SSOT 금지어 전수 스캔")
    L.append("")
    L.append(f"- 생성 시각: `{now}`")
    L.append(f"- 실행 스킬: `scripts/qa/skill_jargon_scan.py` (Skill 2, 읽기 전용)")
    L.append(f"- 스캔 대상: `{target}/*.html` — **{len(files)}개 화면**")
    L.append(f"- **[A] DOM 가시 텍스트 탐지: {tot_dom}건** (텍스트 노드 + placeholder/title/alt/aria-label/버튼 value)")
    L.append(f"- **[B] JS 동적 렌더링 후보 탐지: {tot_js}건** (`<script>` 내 한글 포함 문자열 리터럴)")
    L.append(f"- 무결 화면(탐지 0건): {len(clean)}개")
    L.append("")
    L.append("> [A]는 정적 화면에 그대로 노출되는 텍스트이므로 우선 정비 대상이다. "
             "[B]는 innerHTML/모달 렌더링 시 노출될 수 있는 후보로, 분석 AI가 노출 여부를 판단한다.")
    L.append("> 본 스킬은 HTML을 수정하지 않는다. 치환 패치는 분석 AI + 코딩 AI가 작성한다.")
    L.append("")

    # 규칙별 요약
    L.append("## 1. 규칙별 탐지 요약")
    L.append("")
    L.append("| 분류 | 규칙 | 설명 | [A] DOM | [B] JS | 대표 매칭어 |")
    L.append("| :--- | :--- | :--- | ---: | ---: | :--- |")
    cnt_dom, cnt_js, words = Counter(), Counter(), defaultdict(Counter)
    for d, j in results.values():
        for h in d:
            cnt_dom[h["rule"]] += 1
            words[h["rule"]][h["match"]] += 1
        for h in j:
            cnt_js[h["rule"]] += 1
            words[h["rule"]][h["match"]] += 1
    for cat, rid, desc, _ in RULES:
        top = ", ".join(f"`{w}`×{c}" for w, c in words[rid].most_common(6)) or "-"
        L.append(f"| {cat} | {rid} | {desc} | {cnt_dom[rid]} | {cnt_js[rid]} | {top} |")
    L.append("")

    # 화면별 요약
    L.append("## 2. 화면별 탐지 요약")
    L.append("")
    L.append("| 화면 | [A] DOM | [B] JS | 내부암호 | 금지어 | 번역중복 |")
    L.append("| :--- | ---: | ---: | ---: | ---: | ---: |")
    for f in files:
        d, j = results[f]
        c = Counter(h["cat"] for h in d + j)
        L.append(f"| `{f}` | {len(d)} | {len(j)} | {c['내부암호']} | {c['금지어']} | {c['번역중복']} |")
    L.append("")

    # 상세
    for title, idx in (("## 3. [A] DOM 가시 텍스트 상세 (우선 정비 대상)", 0),
                       ("## 4. [B] JS 동적 렌더링 후보 상세", 1)):
        L.append(title)
        L.append("")
        any_hit = False
        for f in files:
            hits = results[f][idx]
            if not hits:
                continue
            any_hit = True
            L.append(f"### `{f}` — {len(hits)}건")
            L.append("")
            L.append("| 라인 | 출처 | 분류 | 규칙 | 매칭 | 문맥 |")
            L.append("| ---: | :--- | :--- | :--- | :--- | :--- |")
            for h in sorted(hits, key=lambda x: x["line"]):
                L.append(f"| {h['line']} | {h['src']} | {h['cat']} | {h['rule']} | `{h['match']}` | {h['ctx']} |")
            L.append("")
        if not any_hit:
            L.append("탐지 0건 ✅")
            L.append("")

    if clean:
        L.append("## 5. 무결 화면 (탐지 0건)")
        L.append("")
        for f in clean:
            L.append(f"- `{f}`")
        L.append("")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description="SSOT 금지어 & 기획서 내부 암호 스캐너")
    ap.add_argument("--target", default="prototype_clean", help="스캔 대상 폴더 (프로젝트 루트 기준)")
    ap.add_argument("--out", default="docs/JARGON_SCAN_REPORT.md", help="리포트 출력 경로")
    ap.add_argument("--strict", action="store_true", help="[A] 탐지 1건 이상이면 exit 1")
    args = ap.parse_args()

    tdir = os.path.join(ROOT, args.target)
    paths = sorted(glob.glob(os.path.join(tdir, "*.html")))
    if not paths:
        print(f"[ERROR] HTML 파일 없음: {tdir}", file=sys.stderr)
        return 2
    files = [os.path.basename(p) for p in paths]
    results = {os.path.basename(p): scan_file(p) for p in paths}

    report = build_report(args.target, files, results)
    out = os.path.join(ROOT, args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(report)

    tot_dom = sum(len(d) for d, _ in results.values())
    tot_js = sum(len(j) for _, j in results.values())
    print(f"[Skill 2] scanned={len(files)} dom_hits={tot_dom} js_hits={tot_js} -> {args.out}")
    return 1 if (args.strict and tot_dom) else 0


if __name__ == "__main__":
    sys.exit(main())
