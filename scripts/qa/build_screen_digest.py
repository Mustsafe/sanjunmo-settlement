#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
화면 요약본 생성기 (읽기 전용 QA 도구 — HTML을 수정하지 않음)

목적
  대형 HTML(수백~3,800줄)을 통째로 읽지 않고도 구조를 파악하도록, 화면별 요약본을 만든다.
  각 항목에 원본 줄 번호(L123)를 붙여 필요한 줄만 열어 볼 수 있다.

요약 내용
  제목 · 브레드크럼 그룹 / 탭 · 서브뷰 버튼 / 모달(백드롭 id · 제목) / 버튼(라벨 → onclick 함수)
  폼 필드(라벨 · id · type · 기본값 · option) / 표 머리(th) / 상태값 문자열 집계
  스크립트 샘플 코드(RH- CT- PROD-BK- SUP- PKG- CRS- MS- 등) / localStorage 키 / 함수 정의(이름 · 줄)

사용법:
  python scripts/qa/build_screen_digest.py                  # prototype_clean
  python scripts/qa/build_screen_digest.py prototype
출력: scripts/qa/reports/digest/<파일명>.md + INDEX.md (clean 외 폴더는 digest_<폴더>/ 로 분리)
"""
import argparse
import os
import re
import sys
from collections import Counter, OrderedDict
from html.parser import HTMLParser

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REPORTS = os.path.join(ROOT, "scripts", "qa", "reports")

CODE_RE = re.compile(r"\b(?:RH|CT|CON|PROD-BK|PROD-CR|PROD-PK|SUP|PKG|CRS|MS|PY|BK-REQ|ORD|RFD|USR|INST|BRD|VEND)-[0-9A-Z][0-9A-Z-]*\b")
LS_RE = re.compile(r"""(?:getItem|setItem|removeItem)\(\s*['"`]([^'"`]+)['"`]""")
LS_CONST_RE = re.compile(r"""(?:const|let|var)\s+([A-Z_][A-Z0-9_]*(?:KEY|STORE|STORAGE)[A-Z0-9_]*)\s*=\s*['"`]([^'"`]+)['"`]""")
FN_RES = [
    re.compile(r"\bfunction\s+([A-Za-z_$][\w$]*)\s*\("),
    re.compile(r"\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(?:function\b|\([^)]*\)\s*=>|[A-Za-z_$][\w$]*\s*=>)"),
    re.compile(r"\bwindow\.([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(?:function\b|\([^)]*\)\s*=>)"),
]
STATE_WORDS = re.compile(r"(중|완료|대기|예정|종료|정지|중지|불가|가능|승인|반려|보류|취소|품절|임시|확정|지급|환불|진행|해지|만료|활성|사용|정상|오류|경고|대상|제외|거절|요청|접수|처리)$")
FN_CALL = re.compile(r"([A-Za-z_$][\w$.]*)\s*\(")
SKIP_FN_PREFIX = ("forceCloseModal",)


def t_is_choice(f):
    return f["type"] in ("radio", "checkbox")


def norm(s):
    return re.sub(r"\s+", " ", s or "").strip()


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # (tag, attrs, line, textbuf)
        self.group = self.code = self.title = ""
        self.title_line = 0
        self.tabs = []
        self.modals = []
        self.cur_modal = None
        self.buttons = OrderedDict()
        self.fields = []
        self.cur_table = None
        self.tables = []
        self.states = Counter()
        self.state_line = {}
        self.scripts = []
        self.last_label = ""
        self.cur_select = None
        self.in_script = None
        self.in_style = False

    def line(self):
        return self.getpos()[0]

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        ln = self.line()
        if tag == "script":
            self.in_script = [ln, []]
            return
        if tag == "style":
            self.in_style = True
            return
        if tag in ("br", "img", "hr", "link", "meta"):
            return
        if tag == "input":
            t = a.get("type", "text")
            if t not in ("hidden", "button", "submit"):
                fld = {"tag": tag, "id": a.get("id", ""), "type": t, "value": a.get("value", ""),
                       "label": "" if t in ("radio", "checkbox") else self.last_label, "line": ln, "opts": []}
                self.fields.append(fld)
                for item in self.stack:
                    if item[0] == "label":
                        item[1].setdefault("_f", []).append(fld)
            return
        if tag == "table":
            self.cur_table = {"line": ln, "ths": [], "id": a.get("id", "")}
            self.tables.append(self.cur_table)
        if any("modal-backdrop" in c for c in cls):
            self.cur_modal = {"id": a.get("id", ""), "line": ln, "title": ""}
            self.modals.append(self.cur_modal)
        if tag in ("select", "textarea"):
            self.cur_select = {"tag": tag, "id": a.get("id", ""), "type": tag, "value": a.get("value", ""),
                               "label": self.last_label, "line": ln, "opts": []}
            self.fields.append(self.cur_select)
        self.stack.append((tag, a, ln, []))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_data(self, data):
        if self.in_script is not None:
            self.in_script[1].append(data)
            return
        if self.in_style:
            return
        for item in self.stack:
            item[3].append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.in_script is not None:
            self.scripts.append((self.in_script[0], "".join(self.in_script[1])))
            self.in_script = None
            return
        if tag == "style":
            self.in_style = False
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                break
        else:
            return
        while len(self.stack) > i:
            t, a, ln, buf = self.stack.pop()
            self.finish(t, a, ln, norm("".join(buf)))

    def finish(self, tag, a, ln, text):
        cls = (a.get("class") or "").split()
        clss = " ".join(cls)
        if tag == "h1" and "crumb-title" in cls:
            self.title, self.title_line = text, ln
        if "crumb-group" in cls:
            self.group = text
        if "crumb-code" in cls:
            self.code = text
        if tag == "th" and self.cur_table is not None and text:
            self.cur_table["ths"].append(text)
        if tag == "table":
            self.cur_table = None
        if tag == "label" and text:
            self.last_label = text[:30]
            for fld in a.get("_f", []):
                if t_is_choice(fld):
                    fld["label"] = text[:30]
        if tag == "option" and self.cur_select is not None:
            self.cur_select["opts"].append(text)
            if text and len(text) <= 10 and STATE_WORDS.search(text):
                self.count_state(text, ln)
        if tag in ("select", "textarea") and self.cur_select is not None and self.cur_select["tag"] == tag:
            if tag == "textarea":
                self.cur_select["value"] = text[:30]
            self.cur_select = None
        if self.cur_modal is not None and not self.cur_modal["title"] and text and ("modal-title" in clss or tag in ("h2", "h3")):
            self.cur_modal["title"] = text[:70]
        if tag == "button":
            is_tab = ("tab" in clss or "subview" in clss or a.get("role") == "tab")
            oc = a.get("onclick") or ""
            m = FN_CALL.search(oc)
            fn = m.group(1) if m else ""
            label = text or a.get("title") or a.get("aria-label") or ""
            if is_tab:
                self.tabs.append((label[:40], fn or a.get("data-tab") or a.get("data-view") or "", ln))
            elif label or fn:
                key = (label[:30], fn)
                if key not in self.buttons:
                    self.buttons[key] = [ln, 1]
                else:
                    self.buttons[key][1] += 1
        if (any(k in clss for k in ("badge", "chip", "status", "-tag", "pill")) and tag in ("span", "div", "td", "b", "em")
                and text and len(text) <= 12 and re.search(r"[가-힣]", text) and STATE_WORDS.search(text)):
            self.count_state(text, ln)

    def count_state(self, text, ln):
        self.states[text] += 1
        self.state_line.setdefault(text, ln)


def analyze_scripts(scripts):
    codes, ls, fns = OrderedDict(), OrderedDict(), []
    for start, text in scripts:
        def ln(pos, start=start, text=text):
            return start + text.count("\n", 0, pos)
        for m in CODE_RE.finditer(text):
            c = m.group(0).rstrip("-")
            codes.setdefault(c, ln(m.start()))
        for m in LS_RE.finditer(text):
            ls.setdefault(m.group(1), ln(m.start()))
        for m in LS_CONST_RE.finditer(text):
            ls.setdefault(m.group(2), ln(m.start()))
        seen = set()
        for rx in FN_RES:
            for m in rx.finditer(text):
                n = m.group(1)
                if n in seen or n.startswith(SKIP_FN_PREFIX):
                    continue
                seen.add(n)
                fns.append((n, ln(m.start())))
    fns.sort(key=lambda x: x[1])
    return codes, ls, fns


def compress_codes(codes):
    """접두어별로 묶어 '첫 코드 … 마지막 코드 외 n건' 형식으로 줄인다."""
    groups = OrderedDict()
    for c, l in codes.items():
        groups.setdefault(re.sub(r"-\d.*$", "", c), []).append((c, l))
    out = []
    for pre, items in groups.items():
        if len(items) <= 3:
            out.append(", ".join(f"{c}(L{l})" for c, l in items))
        else:
            out.append(f"{items[0][0]}(L{items[0][1]}) … {items[-1][0]} 외 {len(items) - 2}건")
    return out


def digest(path, name):
    with open(path, encoding="utf-8", newline="") as f:
        src = f.read()
    nlines = src.count("\n") + 1
    p = P()
    p.feed(src)
    p.close()
    codes, ls, fns = analyze_scripts(p.scripts)
    L = [f"# {name}",
         f"- {p.code or '-'} · {p.title or '(제목 없음)'} (L{p.title_line}) · 그룹: {p.group or '-'} · 원본 {nlines}줄"]
    if p.tabs:
        L.append("\n## 탭 · 서브뷰")
        L.append(" / ".join(f"{t}→{fn}(L{ln})" if fn else f"{t}(L{ln})" for t, fn, ln in p.tabs))
    if p.modals:
        L.append("\n## 모달")
        for m in p.modals:
            L.append(f"- {m['id'] or '(id 없음)'} L{m['line']} · {m['title'] or '-'}")
    if p.buttons:
        L.append("\n## 버튼 (라벨 → onclick)")
        items = [f"{lab or '(아이콘)'}→{fn or '-'}(L{v[0]}{'x' + str(v[1]) if v[1] > 1 else ''})" for (lab, fn), v in p.buttons.items()]
        L.append(" · ".join(items[:50]) + (f" … 외 {len(items) - 50}건" if len(items) > 50 else ""))
    if p.fields:
        L.append("\n## 폼 필드 (라벨 · id · type · 기본값 · option)")
        for f in p.fields[:60]:
            s = f"- L{f['line']} {f['label'] or '-'} · {f['id'] or '-'} · {f['type']}"
            if f["value"]:
                s += f" · ={f['value'][:20]}"
            if f["opts"]:
                o = f["opts"]
                s += " · [" + "|".join(x[:12] for x in o[:6]) + (f"…+{len(o) - 6}" if len(o) > 6 else "") + "]"
            L.append(s)
        if len(p.fields) > 60:
            L.append(f"- … 외 {len(p.fields) - 60}건")
    ths = [t for t in p.tables if t["ths"]]
    if ths:
        L.append("\n## 표 머리 (th)")
        for t in ths[:20]:
            L.append(f"- L{t['line']}{' #' + t['id'] if t['id'] else ''}: " + " | ".join(x[:14] for x in t["ths"][:14]) + (f"…+{len(t['ths']) - 14}" if len(t["ths"]) > 14 else ""))
        if len(ths) > 20:
            L.append(f"- … 외 {len(ths) - 20}개 표")
    if p.states:
        L.append("\n## 상태값 (배지 · 옵션)")
        L.append(" · ".join(f"{k}x{v}(L{p.state_line[k]})" for k, v in p.states.most_common(25)))
    if codes:
        L.append("\n## 스크립트 샘플 코드")
        L.append(" / ".join(compress_codes(codes)))
    if ls:
        L.append("\n## localStorage 키")
        L.append(" · ".join(f"{k}(L{l})" for k, l in ls.items()))
    if fns:
        L.append(f"\n## 함수 정의 ({len(fns)})")
        L.append(" · ".join(f"{n}:{l}" for n, l in fns[:120]) + (f" … 외 {len(fns) - 120}건" if len(fns) > 120 else ""))
    return "\n".join(L) + "\n", p, nlines, len(src.encode("utf-8"))


def main():
    ap = argparse.ArgumentParser(description="화면 요약본 생성")
    ap.add_argument("folder", nargs="?", default="prototype_clean")
    args = ap.parse_args()
    folder = os.path.join(ROOT, args.folder)
    out = os.path.join(REPORTS, "digest" if args.folder == "prototype_clean" else "digest_" + args.folder)
    os.makedirs(out, exist_ok=True)
    files = sorted(f for f in os.listdir(folder) if f.endswith(".html"))
    idx = [f"# 화면 요약 INDEX ({args.folder})", "", "| 코드 | 제목 | 탭 | 모달 | 줄 | 요약/원본 |", "| :-- | :-- | --: | --: | --: | --: |"]
    tot_s = tot_o = 0
    ratios = []
    for fn in files:
        text, p, nl, ob = digest(os.path.join(folder, fn), fn)
        with open(os.path.join(out, fn[:-5] + ".md"), "w", encoding="utf-8", newline="") as f:
            f.write(text)
        sb = len(text.encode("utf-8"))
        tot_s += sb
        tot_o += ob
        r = sb / ob * 100
        ratios.append((r, fn))
        code = p.code or fn.split("_baseline")[0]
        idx.append(f"| [{code}]({fn[:-5]}.md) | {(p.title or '-')[:50]} | {len(p.tabs)} | {len(p.modals)} | {nl} | {r:.1f}% |")
    with open(os.path.join(out, "INDEX.md"), "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(idx) + "\n")
    ratios.sort(reverse=True)
    print(f"[digest] {args.folder}: {len(files)}개 생성 · 총 {tot_s / tot_o * 100:.1f}% (최대 {ratios[0][0]:.1f}% {ratios[0][1]}) → {os.path.relpath(out, ROOT)}")


if __name__ == "__main__":
    main()
