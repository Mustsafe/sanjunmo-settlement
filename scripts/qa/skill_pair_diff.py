#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[Skill 7] 두 폴더 기능 차이 검사기 (읽기 전용 QA 도구 — HTML을 수정하지 않음)

목적
  prototype 과 prototype_clean 은 같은 기능이어야 한다. clean 은 기획 문구를 빼거나 바꾸므로
  문자열 · HTML 텍스트 · 주석 · 공백 차이는 무시하고, '로직'이 달라진 곳만 잡는다.

검사
  [1] 인라인 <script> 와 공통 .js: 주석 제거 · 문자열/템플릿 리터럴을 S 로 치환 · 공백 정규화 후 줄 단위 비교
      (함수 목록 · 식별자 · 조건식 차이가 여기서 잡힌다)
  [2] 함수 정의 이름 집합 차이, 식별자 집합 차이(요약)
  [3] HTML 구조: id 목록 · onclick 함수명 · input/select/textarea id 차이
  참고(의도된 차이): common-snb.js 의 clean 전용 문구 치환 블록, 기획 설명 클래스
      (info-callout · policy-banner · policy-note · rule-banner)가 붙은 요소의 id 차이

사용법:
  python scripts/qa/skill_pair_diff.py                 # prototype ↔ prototype_clean
  python scripts/qa/skill_pair_diff.py --strict        # 로직/구조 차이가 있으면 exit 1
  python scripts/qa/skill_pair_diff.py A폴더 B폴더     # 다른 쌍 (시험용)
리포트: scripts/qa/reports/PAIR_DIFF_REPORT.md
"""
import argparse
import difflib
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REPORT = os.path.join(ROOT, "scripts", "qa", "reports", "PAIR_DIFF_REPORT.md")

CLEAN_HIDDEN_CLS = ("info-callout", "policy-banner", "policy-note", "rule-banner")
KNOWN_NOTE_JS = {"common-snb.js": "clean 전용 문구 치환 블록(런타임 치환기)이 있어 두 폴더가 다름"}
MAX_PER_FILE = 25


def read(p):
    with open(p, encoding="utf-8", newline="") as f:
        return f.read()


def normalize_js(code, start_line=1):
    """주석 제거 · 문자열/템플릿/정규식 리터럴 → S · 공백 정규화. [(원본줄, 정규화된 줄)] 반환."""
    out, buf, line = [], [], start_line
    i, n = 0, len(code)
    last_sig = ""            # 마지막 의미 있는 문자(정규식 리터럴 판별용)
    line_of_buf = start_line

    def flush(ln):
        t = re.sub(r"\s+", " ", "".join(buf)).strip()
        if t:
            out.append((line_of_buf, t))
        buf.clear()

    while i < n:
        c = code[i]
        if c == "\n":
            flush(line)
            line += 1
            line_of_buf = line
            i += 1
            continue
        if not buf:
            line_of_buf = line
        two = code[i:i + 2]
        if two == "//":
            while i < n and code[i] != "\n":
                i += 1
            continue
        if two == "/*":
            j = code.find("*/", i + 2)
            j = n if j < 0 else j + 2
            line += code.count("\n", i, j)
            i = j
            continue
        if c in "'\"":
            j = i + 1
            while j < n and code[j] != c and code[j] != "\n":
                j += 2 if code[j] == "\\" else 1
            buf.append("S")
            last_sig = "S"
            i = j + 1
            continue
        if c == "`":
            j, depth = i + 1, 0
            while j < n:
                if code[j] == "\\":
                    j += 2
                    continue
                if code[j] == "`" and depth == 0:
                    break
                if code[j:j + 2] == "${":
                    depth += 1
                    j += 2
                    continue
                if code[j] == "}" and depth:
                    depth -= 1
                if code[j] == "\n":
                    line += 1
                j += 1
            buf.append("S")
            last_sig = "S"
            i = j + 1
            continue
        if c == "/" and last_sig in ("", "(", ",", "=", ":", "[", "!", "&", "|", "?", "{", "}", ";", "+", "-", "*", "%", "<", ">", "~", "^") \
                and not buf_ends_ident(buf):
            j = i + 1
            in_cls = False
            while j < n and code[j] != "\n":
                if code[j] == "\\":
                    j += 2
                    continue
                if code[j] == "[":
                    in_cls = True
                elif code[j] == "]":
                    in_cls = False
                elif code[j] == "/" and not in_cls:
                    break
                j += 1
            if j < n and code[j] == "/":
                j += 1
                while j < n and code[j].isalpha():
                    j += 1
                buf.append("R")
                last_sig = "R"
                i = j
                continue
        buf.append(c)
        if not c.isspace():
            last_sig = c
        i += 1
    flush(line)
    return out


def buf_ends_ident(buf):
    s = "".join(buf).rstrip()
    return bool(s) and (s[-1].isalnum() or s[-1] in "_$)]")


def inline_scripts(html):
    """src 없는 <script> 블록들의 (내용, 시작줄)."""
    res = []
    for m in re.finditer(r"<script\b([^>]*)>(.*?)</script>", html, re.S | re.I):
        if re.search(r"\bsrc\s*=", m.group(1)):
            continue
        start = html.count("\n", 0, m.start(2)) + 1
        res.append((m.group(2), start))
    return res


def norm_script_lines(html):
    lines = []
    for code, start in inline_scripts(html):
        lines.extend(normalize_js(code, start))
    return lines


FN_RE = re.compile(r"\bfunction\s+([A-Za-z_$][\w$]*)|\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(?:function\b|\([^)]*\)\s*=>|[A-Za-z_$][\w$]*\s*=>)|\bwindow\.([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(?:function\b|\()")
IDENT_RE = re.compile(r"[A-Za-z_$][\w$]*")
JS_KW = set("var let const function return if else for while do switch case break continue new this typeof in of try catch finally throw null undefined true false S R async await class default delete void instanceof".split())


def fn_names(lines):
    names = set()
    for _, t in lines:
        for m in FN_RE.finditer(t):
            names.add(next(g for g in m.groups() if g))
    return names


def idents(lines):
    s = set()
    for _, t in lines:
        s.update(IDENT_RE.findall(t))
    return s - JS_KW


def diff_lines(a, b):
    """정규화 줄 리스트 비교 → [(a줄들, b줄들)] 차이 묶음."""
    sm = difflib.SequenceMatcher(None, [t for _, t in a], [t for _, t in b], autojunk=False)
    res = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            res.append((a[i1:i2], b[j1:j2]))
    return res


def markup_only(html):
    html = re.sub(r"<script\b[^>]*>.*?</script>", lambda m: "\n" * m.group(0).count("\n"), html, flags=re.S | re.I)
    return re.sub(r"<style\b[^>]*>.*?</style>", lambda m: "\n" * m.group(0).count("\n"), html, flags=re.S | re.I)


def structure(html):
    mk = markup_only(html)
    ids, hidden_ids, onclick, fields = {}, set(), set(), {}
    for m in re.finditer(r"<([a-zA-Z][\w-]*)\b([^>]*)>", mk):
        tag, attrs = m.group(1).lower(), m.group(2)
        ln = mk.count("\n", 0, m.start()) + 1
        mid = re.search(r"\bid\s*=\s*[\"']([^\"']+)[\"']", attrs)
        cls = re.search(r"\bclass\s*=\s*[\"']([^\"']*)[\"']", attrs)
        if mid:
            ids.setdefault(mid.group(1), ln)
            if cls and any(h in cls.group(1).split() for h in CLEAN_HIDDEN_CLS):
                hidden_ids.add(mid.group(1))
            if tag in ("input", "select", "textarea"):
                fields.setdefault(mid.group(1), ln)
        for oc in re.finditer(r"\bonclick\s*=\s*\"([^\"]*)\"|\bonclick\s*=\s*'([^']*)'", attrs):
            for f in re.finditer(r"([A-Za-z_$][\w$.]*)\s*\(", oc.group(1) or oc.group(2)):
                onclick.add(f.group(1))
    return ids, hidden_ids, onclick, fields


def show(lines, cap=3):
    s = " ⏎ ".join(t[:110] for _, t in lines[:cap])
    return s + (f" …(+{len(lines) - cap})" if len(lines) > cap else "")


def fmt_range(lines):
    return f"L{lines[0][0]}" + (f"-{lines[-1][0]}" if lines[-1][0] != lines[0][0] else "") if lines else "-"


def compare_logic(la, lb, na, nb):
    """로직 차이 보고 줄(마크다운) 리스트 + 개수."""
    rep = []
    d = diff_lines(la, lb)
    fa, fb = fn_names(la), fn_names(lb)
    ia, ib = idents(la), idents(lb)
    if fa != fb:
        if fa - fb:
            rep.append(f"- 함수 정의가 {na}에만 있음: {', '.join(sorted(fa - fb))}")
        if fb - fa:
            rep.append(f"- 함수 정의가 {nb}에만 있음: {', '.join(sorted(fb - fa))}")
    if ia != ib:
        if ia - ib:
            rep.append(f"- 식별자가 {na}에만 있음: {', '.join(sorted(ia - ib)[:25])}{' …' if len(ia - ib) > 25 else ''}")
        if ib - ia:
            rep.append(f"- 식별자가 {nb}에만 있음: {', '.join(sorted(ib - ia)[:25])}{' …' if len(ib - ia) > 25 else ''}")
    for k, (x, y) in enumerate(d):
        if k >= MAX_PER_FILE:
            rep.append(f"- … 외 {len(d) - MAX_PER_FILE}개 구간")
            break
        rep.append(f"- {na} {fmt_range(x)} ↔ {nb} {fmt_range(y)}\n  - {na}: `{show(x)}`\n  - {nb}: `{show(y)}`")
    return rep, len(d) + (1 if fa != fb else 0)


def main():
    ap = argparse.ArgumentParser(description="두 폴더 기능 차이 검사")
    ap.add_argument("folders", nargs="*", default=["prototype", "prototype_clean"])
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    if len(args.folders) != 2:
        ap.error("폴더는 2개(또는 생략)")
    A, B = args.folders
    da, db = os.path.join(ROOT, A), os.path.join(ROOT, B)
    A, B = os.path.basename(A.rstrip("/\\")), os.path.basename(B.rstrip("/\\"))
    if A == B:
        A, B = A + '(1)', B + '(2)'
    ha = {f for f in os.listdir(da) if f.endswith(".html")}
    hb = {f for f in os.listdir(db) if f.endswith(".html")}
    ja = {f for f in os.listdir(da) if f.endswith(".js")}
    jb = {f for f in os.listdir(db) if f.endswith(".js")}
    sections, notes = [], []
    logic_pairs = struct_pairs = 0
    pairs = sorted(ha & hb)

    for f in sorted(ha ^ hb):
        sections.append(f"## {f}\n- {A if f in ha else B}에만 존재")
        struct_pairs += 1

    for f in pairs:
        ta, tb = read(os.path.join(da, f)), read(os.path.join(db, f))
        rep_l, nl = compare_logic(norm_script_lines(ta), norm_script_lines(tb), A, B)
        ids_a, hid_a, oc_a, fl_a = structure(ta)
        ids_b, hid_b, oc_b, fl_b = structure(tb)
        rep_s, ns = [], 0
        only_a, only_b = set(ids_a) - set(ids_b), set(ids_b) - set(ids_a)
        note_ids = {i for i in only_a if i in hid_a} | {i for i in only_b if i in hid_b}
        only_a_r, only_b_r = only_a - note_ids, only_b - note_ids
        if only_a_r:
            rep_s.append(f"- id가 {A}에만 있음: " + ", ".join(f"{i}(L{ids_a[i]})" for i in sorted(only_a_r)[:30]))
        if only_b_r:
            rep_s.append(f"- id가 {B}에만 있음: " + ", ".join(f"{i}(L{ids_b[i]})" for i in sorted(only_b_r)[:30]))
        if oc_a != oc_b:
            if oc_a - oc_b:
                rep_s.append(f"- onclick 함수가 {A}에만: {', '.join(sorted(oc_a - oc_b))}")
            if oc_b - oc_a:
                rep_s.append(f"- onclick 함수가 {B}에만: {', '.join(sorted(oc_b - oc_a))}")
        fa_only, fb_only = set(fl_a) - set(fl_b), set(fl_b) - set(fl_a)
        if fa_only:
            rep_s.append(f"- 입력 id가 {A}에만: {', '.join(sorted(fa_only))}")
        if fb_only:
            rep_s.append(f"- 입력 id가 {B}에만: {', '.join(sorted(fb_only))}")
        if note_ids:
            notes.append(f"- {f}: 기획 설명 요소 id 차이(의도) {', '.join(sorted(note_ids)[:8])}")
        ns = 1 if rep_s else 0
        if rep_l or rep_s:
            body = [f"## {f}"]
            if rep_l:
                body.append("### 로직 (스크립트)")
                body += rep_l
            if rep_s:
                body.append("### 구조 (HTML)")
                body += rep_s
            sections.append("\n".join(body))
        logic_pairs += 1 if rep_l else 0
        struct_pairs += ns

    # 공통 js
    for f in sorted(ja | jb):
        if f not in ja or f not in jb:
            sections.append(f"## {f}\n- {A if f in ja else B}에만 존재")
            continue
        rep_l, _ = compare_logic(normalize_js(read(os.path.join(da, f))), normalize_js(read(os.path.join(db, f))), A, B)
        if rep_l:
            if f in KNOWN_NOTE_JS:
                notes.append(f"- {f}: {KNOWN_NOTE_JS[f]} (차이 {len(rep_l)}항목 — 아래 참고)\n" + "\n".join("  " + x.replace("\n", "\n  ") for x in rep_l[:6]))
            else:
                sections.append(f"## {f} (공통 js)\n### 로직 (스크립트)\n" + "\n".join(rep_l))
                logic_pairs += 1

    head = [f"# PAIR_DIFF_REPORT — {A} ↔ {B}", "",
            f"쌍 {len(pairs)} · 로직 차이 {logic_pairs}쌍 · 구조 차이 {struct_pairs}쌍",
            "문자열 리터럴 · 주석 · 공백은 정규화(S)해 무시. 줄 번호는 각 폴더 원본 기준.", ""]
    txt = "\n".join(head) + "\n" + ("\n\n".join(sections) if sections else "차이 없음") + "\n\n## 참고 (의도된 차이)\n" + ("\n".join(notes) if notes else "없음") + "\n"
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w", encoding="utf-8", newline="") as fh:
        fh.write(txt)
    print(f"[Skill 7] 쌍 {len(pairs)} · 로직 차이 {logic_pairs}쌍 · 구조 차이 {struct_pairs}쌍 → {os.path.relpath(REPORT, ROOT)}")
    if args.strict and (logic_pairs or struct_pairs):
        sys.exit(1)


if __name__ == "__main__":
    main()
