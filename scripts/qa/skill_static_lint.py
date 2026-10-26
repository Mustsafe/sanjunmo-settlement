#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[Skill 1] 정적 문법 검사기 (읽기 전용 QA 도구 — HTML을 수정하지 않음)

목적
  프로토타입 HTML을 브라우저로 열지 않고 다음을 전수 검사한다.
  [1] 인라인 <script> 문법 오류 — Node.js vm.Script로 파싱만 한다(실행하지 않음)
  [2] 깨진 로컬 링크 — href/src/location.href/goNav()가 가리키는 파일이 폴더에 없음
  [3] 중복 ID — <script> 밖 정적 마크업에서 같은 id가 두 번 이상
  [4] 빈 <tbody> — 정적 행이 없고 그 id를 채우는 스크립트 참조도 없음
  [5] 공통 에셋 규격 — README 3.2: link#v4-common-css, script#v4-common-snb 누락(경고)

의존성: Python 3.8+ 표준 라이브러리, Node.js(문법 검사용, 없으면 [1]만 건너뜀)
사용법:
  python scripts/qa/skill_static_lint.py                       # prototype, prototype_clean 둘 다
  python scripts/qa/skill_static_lint.py prototype_clean
  python scripts/qa/skill_static_lint.py --strict              # 오류([1]~[4]) 1건 이상이면 exit 1
리포트: scripts/qa/reports/STATIC_LINT_REPORT.md
"""
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from html.parser import HTMLParser

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# 공통 에셋 규격 [5]에서 script#v4-common-snb 누락 경고를 내지 않는 화면: 운영자 SNB 없이 단독으로 쓰는 파트너 화면
# (common-snb.js가 body 맨 앞에 운영자 SNB를 무조건 넣기 때문에 일부러 로드하지 않음)
NO_SNB_SCREENS = {"ADMN-PTNR-001_baseline.html"}
REPORT = os.path.join(ROOT, "scripts", "qa", "reports", "STATIC_LINT_REPORT.md")

# 여러 블록을 한 번에 넘겨 파싱만 한다 — 임시 파일을 만들지 않는다
NODE_CHECKER = r"""
const vm = require('vm');
let s = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', d => s += d).on('end', () => {
  const out = JSON.parse(s).map(b => {
    try { new vm.Script(b.code, { filename: b.name }); return null; }
    catch (e) {
      const m = /:(\d+)/.exec((e.stack || '').split('\n')[0]);
      return { name: b.name, line: m ? Number(m[1]) : null, msg: e.message };
    }
  }).filter(Boolean);
  process.stdout.write(JSON.stringify(out));
});
"""


class Collector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_script = False
        self.script_attrs = {}
        self.scripts = []          # (start_line, code)
        self.ids = []              # (id, line)
        self.links = []            # (attr, value, line)
        self.tbodies = []          # [id, line, row_count]
        self.open_tbody = None
        self.assets = set()
        self._buf = []
        self._start = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        line = self.getpos()[0]
        if tag == "script":
            self.in_script = True
            self.script_attrs = a
            self._buf = []
            self._start = line
            if a.get("id") == "v4-common-snb":
                self.assets.add("snb")
        if self.in_script and tag != "script":
            return
        if a.get("id"):
            self.ids.append((a["id"], line))
        if tag == "link" and a.get("id") == "v4-common-css":
            self.assets.add("css")
        for attr in ("href", "src"):
            if a.get(attr):
                self.links.append((attr, a[attr], line))
        if tag == "tbody":
            self.open_tbody = [a.get("id", ""), line, 0]
        if tag == "tr" and self.open_tbody is not None:
            self.open_tbody[2] += 1

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag == "script":
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == "script" and self.in_script:
            self.in_script = False
            if not self.script_attrs.get("src"):
                self.scripts.append((self._start, "".join(self._buf)))
        elif tag == "tbody" and self.open_tbody is not None:
            self.tbodies.append(self.open_tbody)
            self.open_tbody = None

    def handle_data(self, data):
        if self.in_script:
            self._buf.append(data)


LOCAL_LINK = re.compile(r"""(?:location\.href\s*=\s*|goNav\(\s*|href\s*[:=]\s*)["']([^"'${}]+?\.(?:html|js|css))(?:[?#][^"']*)?["']""")


def local_target(value):
    v = value.strip()
    if not v or v.startswith(("#", "http:", "https:", "mailto:", "tel:", "javascript:", "data:", "//")) or "${" in v:
        return None
    v = re.split(r"[?#]", v)[0]
    return v or None


def lint_folder(folder, node):
    base = os.path.join(ROOT, folder)
    files = sorted(f for f in os.listdir(base) if f.endswith(".html"))
    existing = set(os.listdir(base))
    results = {}
    blocks = []
    for f in files:
        text = open(os.path.join(base, f), encoding="utf-8").read()
        c = Collector()
        c.feed(text)
        r = {"syntax": [], "links": [], "dup": [], "tbody": [], "assets": []}
        # [2] 링크: 마크업 속성 + 스크립트 안 location.href/goNav/href 문자열
        seen = set()
        cands = [(a, v, ln) for a, v, ln in c.links]
        for start, code in c.scripts:
            for m in LOCAL_LINK.finditer(code):
                cands.append(("script", m.group(1), start + code[:m.start()].count("\n")))
        for attr, value, line in cands:
            t = local_target(value)
            if not t or t in seen:
                continue
            seen.add(t)
            if not os.path.exists(os.path.normpath(os.path.join(base, t))):
                r["links"].append(f"{line}행 {attr}=`{value}`")
        # [3] 중복 ID
        cnt = Counter(i for i, _ in c.ids)
        for i, n in cnt.items():
            if n > 1:
                lines = [str(ln) for x, ln in c.ids if x == i]
                r["dup"].append(f"`{i}` ×{n} ({', '.join(lines)}행)")
        # [4] 빈 tbody
        all_js = "\n".join(code for _, code in c.scripts)
        for tid, line, rows in c.tbodies:
            if rows:
                continue
            if tid and (re.search(r"""['"`]#?%s['"`]""" % re.escape(tid), all_js)):
                continue
            r["tbody"].append(f"{line}행 tbody{'#' + tid if tid else ''} — 정적 행 없음, 채우는 스크립트 참조 없음")
        # [5] 공통 에셋
        if "css" not in c.assets:
            r["assets"].append("link#v4-common-css 없음")
        if "snb" not in c.assets and f not in NO_SNB_SCREENS:
            r["assets"].append("script#v4-common-snb 없음")
        results[f] = r
        for start, code in c.scripts:
            if code.strip():
                blocks.append({"name": f"{f}@{start}", "code": code})
    # [1] 문법
    if node:
        proc = subprocess.run([node, "-e", NODE_CHECKER], input=json.dumps(blocks), capture_output=True, text=True, encoding="utf-8")
        for e in json.loads(proc.stdout or "[]"):
            f, start = e["name"].rsplit("@", 1)
            line = int(start) + (e["line"] or 1) - 1
            results[f]["syntax"].append(f"{line}행 부근: {e['msg']}")
    # common-snb.js의 SNB 링크
    snb = os.path.join(base, "common-snb.js")
    snb_broken = []
    if os.path.exists(snb):
        for m in re.finditer(r"""href:\s*["']([^"']+)["']""", open(snb, encoding="utf-8").read()):
            t = local_target(m.group(1))
            if t and not os.path.exists(os.path.join(base, t)):
                snb_broken.append(m.group(1))
    return files, results, snb_broken


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folders", nargs="*", default=["prototype", "prototype_clean"])
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    node = shutil.which("node")
    L = ["# STATIC LINT REPORT — 정적 문법 · 링크 · 중복 ID · 빈 tbody 검사", "",
         f"- 생성: {datetime.datetime.now():%Y-%m-%d %H:%M}",
         f"- 문법 검사: {'Node.js ' + subprocess.run([node, '--version'], capture_output=True, text=True).stdout.strip() if node else '건너뜀(Node.js 없음)'}", ""]
    errors = 0
    for folder in args.folders:
        files, results, snb_broken = lint_folder(folder, node)
        tot = {k: sum(len(r[k]) for r in results.values()) for k in ("syntax", "links", "dup", "tbody", "assets")}
        errors += tot["syntax"] + tot["links"] + tot["dup"] + tot["tbody"] + len(snb_broken)
        print(f"[{folder}] 파일 {len(files)}개 | 문법 {tot['syntax']} · 깨진 링크 {tot['links']} · 중복 ID {tot['dup']} · 빈 tbody {tot['tbody']} · 에셋 경고 {tot['assets']} · SNB 깨진 링크 {len(snb_broken)}")
        L += [f"## {folder} ({len(files)}개 파일)", "",
              "| 검사 | 건수 |", "| :--- | ---: |",
              f"| [1] 스크립트 문법 오류 | {tot['syntax']} |", f"| [2] 깨진 로컬 링크 | {tot['links']} |",
              f"| [3] 중복 ID | {tot['dup']} |", f"| [4] 빈 tbody(채우는 스크립트 없음) | {tot['tbody']} |",
              f"| [5] 공통 에셋 규격 경고 | {tot['assets']} |", f"| SNB(common-snb.js) 깨진 링크 | {len(snb_broken)} |", ""]
        if snb_broken:
            L += ["**SNB 깨진 링크:** " + ", ".join(f"`{x}`" for x in snb_broken), ""]
        for f in files:
            r = results[f]
            items = [(k, v) for k in ("syntax", "links", "dup", "tbody", "assets") for v in r[k]]
            if not items:
                continue
            L.append(f"### `{f}`")
            label = {"syntax": "문법", "links": "링크", "dup": "중복 ID", "tbody": "빈 tbody", "assets": "에셋"}
            L += [f"- [{label[k]}] {v}" for k, v in items]
            L.append("")
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    open(REPORT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"[Skill 1] 리포트 저장: {os.path.relpath(REPORT, ROOT)} (오류 {errors}건)")
    if args.strict and errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
