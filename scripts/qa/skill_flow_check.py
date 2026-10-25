#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[Skill 6] 메뉴·흐름 정합 검사기 (읽기 전용 QA 도구 — HTML을 수정하지 않음, 정적 분석만)

검사
  [1] SNB 정합   (a) 두 폴더 SNB_GROUPS 동일  (b) 화면 브레드크럼 그룹명 = SNB 그룹 title
                 (c) README 4절 인벤토리 표의 그룹·파일 = SNB                          → 오류
  [2] 링크 그래프 화면 본문의 (ADMN-)XXX-000_baseline.html 참조로 out/in 계산.
                 나가는 링크 0 · 들어오는 링크 0(SNB로만 도달) 화면 목록               → 참고
  [3] 업무 플로우 가이드(00_WORKFLOW_GUIDE) 노드  (a) 코드 ↔ href 파일 일치 → 오류
                 (b) 노드 화면 이름 ≠ SNB label(괄호 부가설명 제외) → 참고
                 (c) 가이드 어디에도 없는 SNB 메뉴 → 참고
  [4] 샘플 표시 이름 일관성  기준: common-master.js 권리자 시드(RH-NNNN, name).
                 RH 코드 근처 이름이 원장과 다르면 오류, 부가설명만 다르면 참고
                 (계약 CT-* · 도서 SKU 이름 일관성은 skill_cross_data_check.py가 다룸 → 생략)

사용법:
  python scripts/qa/skill_flow_check.py                    # 양쪽(prototype, prototype_clean)
  python scripts/qa/skill_flow_check.py prototype_clean    # 한쪽만
  python scripts/qa/skill_flow_check.py --strict           # 오류 1건 이상이면 exit 1
리포트: scripts/qa/reports/FLOW_CHECK_REPORT.md
"""
import argparse
import datetime
import html as htmllib
import os
import re
import sys
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REPORT = os.path.join(ROOT, "scripts", "qa", "reports", "FLOW_CHECK_REPORT.md")
FOLDERS = ["prototype", "prototype_clean"]
GUIDE = "00_WORKFLOW_GUIDE_baseline.html"
REF = re.compile(r"((?:ADMN-[A-Z]+-\d{3}|00_WORKFLOW_GUIDE)_baseline\.html)")


def rd(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read()


def lineno(text, pos):
    return text.count("\n", 0, pos) + 1


def strip_tags(s):
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def blank_comments(text):
    """HTML/블록 주석을 같은 길이의 공백(줄바꿈 유지)으로 바꾼다. 줄 주석(//)은 줄 단위로 비운다."""
    def sp(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    text = re.sub(r"<!--.*?-->", sp, text, flags=re.S)
    text = re.sub(r"/\*.*?\*/", sp, text, flags=re.S)
    text = re.sub(r"(?m)^[ \t]*//.*$", sp, text)
    return text


# ---------------------------------------------------------------- SNB
def parse_snb(folder):
    p = os.path.join(ROOT, folder, "common-snb.js")
    t = rd(p)
    m = re.search(r"const SNB_GROUPS\s*=\s*\[", t)
    if not m:
        return None
    i = m.end() - 1
    depth, j = 0, i
    while j < len(t):
        c = t[j]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                break
        j += 1
    body = t[i:j + 1]
    groups = []
    for g in re.finditer(r'title:\s*"([^"]*)"\s*,\s*items:\s*\[(.*?)\]\s*\}', body, flags=re.S):
        items = []
        for it in re.finditer(r"\{([^{}]*)\}", g.group(2)):
            d = dict(re.findall(r'(\w+):\s*"([^"]*)"', it.group(1)))
            if "code" in d:
                items.append(d)
        groups.append({"title": g.group(1), "items": items})
    return groups


def href_file(h):
    return h.split("?")[0].split("#")[0]


def snb_file_groups(groups):
    fg = defaultdict(set)
    for g in groups:
        for it in g["items"]:
            fg[href_file(it["href"])].add(g["title"])
    return fg


def crumb_group(text):
    """브레드크럼의 그룹명. crumb-group 요소 우선, 없으면 crumb-sub의 '그룹 > …' 앞부분."""
    m = re.search(r'<(span|div)[^>]*class="[^"]*\bcrumb-group\b[^"]*"[^>]*>(.*?)</\1>', text, flags=re.S)
    if m and "crumb-code" not in m.group(2):
        return strip_tags(m.group(2)), lineno(text, m.start()), "crumb-group"
    for m in re.finditer(r'<span[^>]*class="[^"]*\bcrumb-sub\b[^"]*"[^>]*>(.*?)</span>', text, flags=re.S):
        s = strip_tags(m.group(1))
        if s:
            return s.split(" > ")[0].strip(), lineno(text, m.start()), "crumb-sub"
    return None, 0, ""


def check_snb(folder, groups, errors, notes):
    fg = snb_file_groups(groups)
    base = os.path.join(ROOT, folder)
    for f in sorted(fg):
        p = os.path.join(base, f)
        if not os.path.exists(p):
            errors.append(("1b SNB 대상 파일 없음", f, f"`{folder}/common-snb.js` href 파일이 폴더에 없음"))
            continue
        name, ln, kind = crumb_group(rd(p))
        if name is None:
            notes.append(("1b 브레드크럼 없음", f, "crumb-group/crumb-sub 없음(비교 생략)"))
        elif name not in fg[f]:
            errors.append(("1b 브레드크럼 그룹 불일치", f"{folder}/{f}:{ln}",
                           f"화면 `{name}` ({kind}) ≠ SNB `{' / '.join(sorted(fg[f]))}`"))
    # SNB에 없는 화면 파일
    for f in sorted(os.listdir(base)):
        if f.endswith("_baseline.html") and f not in fg:
            notes.append(("1b SNB에 없는 화면 파일", f, "SNB 메뉴에서 직접 열리지 않음(링크로만 도달)"))


def expand_range(a, b):
    ma, mb = re.match(r"(.*?)(\d+)$", a), re.match(r"(.*?)(\d+)$", b)
    if ma and mb and ma.group(1) == mb.group(1):
        w = len(ma.group(2))
        return [f"{ma.group(1)}{n:0{w}d}" for n in range(int(ma.group(2)), int(mb.group(2)) + 1)]
    return [a, b]


def parse_readme():
    t = rd(os.path.join(ROOT, "README.md"))
    m = re.search(r"^\| SNB 그룹 \|.*$", t, flags=re.M)
    if not m:
        return None
    rows, cur = [], None
    for ln, line in enumerate(t[m.end():].splitlines(), start=lineno(t, m.end()) + 1):
        if not line.startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or all(set(c) <= set(":- ") for c in cells):
            continue
        g = re.match(r"\*\*(.+?)\*\*\s*(?:\((\d+)\))?", cells[0])
        if g:
            cur = [g.group(1), g.group(2), ln, []]
            rows.append(cur)
        files = []
        c1 = cells[1]
        for a, b in re.findall(r"`([^`]+)`\s*~\s*`([^`]+)`", c1):
            files += expand_range(a, b)
        c1 = re.sub(r"`([^`]+)`\s*~\s*`([^`]+)`", "", c1)
        files += re.findall(r"`([^`]+)`", c1)
        if cur is not None:
            cur[3] += [(f if f.endswith(".html") else f + "_baseline.html", ln) for f in files]
    return rows


def check_readme(groups, errors, notes):
    rows = parse_readme()
    if rows is None:
        errors.append(("1c README 표 없음", "README.md", "`| SNB 그룹 |` 표를 찾지 못함"))
        return
    snb = {g["title"]: g for g in groups}
    seen = set()
    for title, n, ln, files in rows:
        seen.add(title)
        if title not in snb:
            errors.append(("1c README 그룹이 SNB에 없음", f"README.md:{ln}", title))
            continue
        sf = {href_file(it["href"]) for it in snb[title]["items"]}
        rf = {f for f, _ in files}
        for f in sorted(rf - sf):
            errors.append(("1c README 파일이 해당 SNB 그룹에 없음", f"README.md:{dict(files)[f]}", f"{title} · {f}"))
        for f in sorted(sf - rf):
            errors.append(("1c SNB 파일이 README 그룹에 없음", f"README.md:{ln}", f"{title} · {f}"))
        if n and int(n) != len(snb[title]["items"]):
            notes.append(("1c README 건수 ≠ SNB 메뉴 수", f"README.md:{ln}",
                          f"{title}: README ({n}) · SNB 메뉴 {len(snb[title]['items'])}(화면 수 vs 메뉴 수 정의 차이일 수 있음)"))
    for t in snb:
        if t not in seen:
            errors.append(("1c SNB 그룹이 README에 없음", "README.md", t))


# ---------------------------------------------------------------- 링크
def check_links(folder, groups, notes):
    base = os.path.join(ROOT, folder)
    screens = sorted(f for f in os.listdir(base) if f.endswith("_baseline.html"))
    out, inn = defaultdict(set), defaultdict(set)
    for f in screens:
        t = blank_comments(rd(os.path.join(base, f)))
        for r in set(REF.findall(t)):
            if r != f and r in screens:
                out[f].add(r)
                inn[r].add(f)
    snbf = snb_file_groups(groups)
    no_out = [f for f in screens if not out[f]]
    no_in = [f for f in screens if not inn[f]]
    no_in_ng = [f for f in screens if not (inn[f] - {GUIDE})]
    return screens, out, inn, no_out, no_in, no_in_ng, snbf


# ---------------------------------------------------------------- 가이드
def base_label(s):
    s = re.sub(r"\s*[\(（][^)）]*[\)）]", "", s)
    return re.sub(r"\s+", "", s)


def check_guide(folder, groups, errors, notes):
    p = os.path.join(ROOT, folder, GUIDE)
    if not os.path.exists(p):
        errors.append(("3 가이드 파일 없음", f"{folder}/{GUIDE}", ""))
        return 0, 0
    t = rd(p)
    items = {it["code"]: it for g in groups for it in g["items"]}
    by_href = {it["href"]: it for it in items.values()}
    seen_codes, seen_href = set(), set()
    nodes = 0
    for m in re.finditer(r'<a\b[^>]*class="[^"]*\bwf-node\b[^"]*"[^>]*href="([^"]*)"[^>]*>(.*?)</a>', t, flags=re.S):
        nodes += 1
        href, inner = m.group(1), m.group(2)
        ln = lineno(t, m.start())
        sm = re.search(r'<span[^>]*class="[^"]*wf-node-scr[^"]*"[^>]*>(.*?)</span>\s*(?:<span|</a|$)', inner, flags=re.S)
        scr_html = sm.group(1) if sm else inner
        cm = re.search(r'<code[^>]*class="[^"]*wf-code[^"]*"[^>]*>(.*?)</code>', scr_html, flags=re.S)
        code = strip_tags(cm.group(1)) if cm else None
        name = strip_tags(re.sub(r"<code.*?</code>", "", scr_html, flags=re.S))
        seen_href.add(href)
        if code is None:
            if href.startswith("#"):
                continue
            notes.append(("3a 노드에 코드 없음", f"{folder}/{GUIDE}:{ln}", f"{name} → {href}"))
            continue
        seen_codes.add(code)
        it = items.get(code)
        if it is None:
            exp = "ADMN-" + re.sub(r"-S\d+$", "", code) + "_baseline.html"
            if href_file(href) != exp:
                errors.append(("3a 코드 ↔ href 파일 불일치", f"{folder}/{GUIDE}:{ln}",
                               f"`{code}`(SNB에 없는 코드) → `{href}` (기대 `{exp}`)"))
            else:
                notes.append(("3a SNB에 없는 코드(파일은 일치)", f"{folder}/{GUIDE}:{ln}", f"`{code}` → `{href}`"))
            continue
        if href_file(it["href"]) != href_file(href):
            errors.append(("3a 코드 ↔ href 파일 불일치", f"{folder}/{GUIDE}:{ln}",
                           f"`{code}` → 노드 `{href}` · SNB `{it['href']}`"))
        if name and norm(base_label(name)) != norm(base_label(it["label"])):
            notes.append(("3b 노드 이름 ≠ SNB label", f"{folder}/{GUIDE}:{ln}",
                          f"`{code}` 노드 `{name}` · SNB `{it['label']}`"))
    # 3c: 가이드 어디에도 없는 SNB 메뉴(노드 코드 또는 아무 링크의 href로 등장하면 등장한 것으로 본다)
    anyhref = set(re.findall(r'href="([^"]*_baseline\.html[^"]*)"', t))
    for g in groups:
        for it in g["items"]:
            if it["code"] in seen_codes or it["href"] in seen_href or it["href"] in anyhref:
                continue
            notes.append(("3c 가이드에 없는 SNB 메뉴", f"{folder}/{GUIDE}", f"[{g['title']}] `{it['code']}` {it['label']}"))
    return nodes, len(seen_codes)


# ---------------------------------------------------------------- 표기 이름
TITLE_WORDS = r"(?:강사|저자|작가|대표|기여자|위탁사|선생님|님)"


def core(s):
    """비교용 핵심 이름: 괄호·고(故)·직함·법인 표기·공백 제거."""
    s = re.sub(r"[\(（][^)）]*[\)）]", " ", s)
    s = s.replace("고 ", "").replace("故", "")
    s = re.sub(r"[·,/].*$", "", s)
    s = re.sub(TITLE_WORDS, " ", s)
    s = re.sub(r"주식회사|\(주\)|사단법인|유한회사", " ", s)
    return re.sub(r"[^가-힣A-Za-z0-9]", "", s)


def norm(s):
    return re.sub(r"[^가-힣A-Za-z0-9]", "", s)


def load_ledger(folder):
    p = os.path.join(ROOT, folder, "common-master.js")
    if not os.path.exists(p):
        p = os.path.join(ROOT, "prototype_clean", "common-master.js")
    t = rd(p)
    led = {}
    for m in re.finditer(r'\{\s*id:\s*"(RH-\d{4})"\s*,\s*name:\s*"([^"]*)"', t):
        led.setdefault(m.group(1), m.group(2))
    return led


OBJ_ID = r"(?:rightsHolderId|primaryHolderId|holderId|payeeId|partnerId|rights_holder_id)"
OBJ_NAME = r"(?:rightsHolderName|primaryHolderName|holderName|payeeName|partnerName|holder_name)"
GENERIC = {"저자", "강사", "작가", "대표", "기여자", "프리랜서", "외주", "계약", "본인", "권리자", "상태", "정상", "단독",
           "적용", "사업자", "개인", "법인", "위탁", "출판사", "위탁사", "일시", "삽화", "자문", "상속", "승계"}


def name_ok(cand_text, led_name):
    """cand_text 안의 한글 낱말 꼬리(최대 3낱말) 중 하나가 원장 핵심 이름과 포함 관계면 일치."""
    lc = core(led_name)
    words = re.findall(r"[가-힣A-Za-z0-9]+", cand_text)
    for k in range(1, min(3, len(words)) + 1):
        c = core(" ".join(words[-k:])) or norm(" ".join(words[-k:]))
        if c and (c in lc or lc in c):
            return True
    return False


def extra_info(raw, rh, led=""):
    """화면 표기에서 이름 뒤 부가설명(괄호 안, RH 코드 제외)을 뽑는다."""
    ex = []
    for pm in re.finditer(r"[\(（]([^)）]*)[\)）]", raw):
        s = re.sub(r"RH-\d{4}", "", pm.group(1))
        s = re.sub(r"^[\s·,/]+|[\s·,/]+$", "", s)
        if s:
            ex.append(s)
    s = " ".join(ex)
    for w in {led, core(led), led.split("(")[0].strip()} - {""}:
        s = s.replace(w, " ")
    s = re.sub(TITLE_WORDS + r"[:：]?", " ", s)
    return re.sub(r"[\s·,/:：]+", " ", s).strip()


def check_names(folder, ledger, errors, notes, rows_out):
    base = os.path.join(ROOT, folder)
    for f in sorted(os.listdir(base)):
        if not (f.endswith(".html") or f.endswith(".js")):
            continue
        raw = rd(os.path.join(base, f))
        t = blank_comments(raw)
        hits = []   # (rh, 화면 표기, pos)
        # A: 이름 (… RH-NNNN …) — 이름은 괄호 안 RH 코드 앞의 낱말(예: "저자 (김안전 · RH-0019)", "(강사: 정종대 RH-0025)")
        for m in re.finditer(r"[\(（]([^()）\n]*?)(RH-\d{4})[^()）\n]*[\)）]", t):
            before = re.sub(r"^.*[:：]", "", m.group(1))
            parts = [x for x in re.split(r"[·,/]", before) if x.strip()]
            before = parts[-1] if parts else ""
            toks = [w for w in re.findall(r"[가-힣]+", before) if w not in GENERIC]
            if toks and 2 <= len(toks[-1]) <= 4:
                hits.append((m.group(2), m.group(0), m.start(), toks[-1], m.group(1)))
        # B: RH-NNNN (이름) — 괄호 안이 2~4자 낱말 하나일 때만 이름으로 본다("RH-0077 (박자녀)")
        for m in re.finditer(r"(RH-\d{4})\s*[\(（]([^()）\n]+)[\)）]", t):
            lead = re.split(r"[·,/]", m.group(2))[0].strip()
            if re.fullmatch(r"[가-힣]{2,4}", lead):
                hits.append((m.group(1), m.group(0), m.start(), lead, m.group(2)))
        # D: 한 객체 리터럴 안의 id 키와 name 키
        for m in re.finditer(r"\{[^{}]*\}", t):
            ob = m.group(0)
            im = re.search(OBJ_ID + r"""\s*:\s*["'](RH-\d{4})["']""", ob)
            nm = re.search(OBJ_NAME + r"""\s*:\s*["']([^"']*)["']""", ob)
            if im and nm and re.search(r"[가-힣]", nm.group(1)) and "*" not in nm.group(1):
                hits.append((im.group(1), nm.group(0), m.start() + nm.start(), re.split(r"[\(（]", nm.group(1).replace("(故)", "故"))[0].strip(), nm.group(1)))
        for rh, shown, pos, namepart, inner in hits:
            led = ledger.get(rh)
            if led is None or "*" in namepart:
                continue
            ln = lineno(t, pos)
            if not name_ok(namepart, led):
                errors.append(("4 표기 이름 불일치", f"{folder}/{f}:{ln}", f"`{rh}` 원장 `{led}` · 화면 `{shown.strip()}`"))
                rows_out.append((rh, led, shown.strip(), f"{folder}/{f}:{ln}", "오류"))
                continue
            ex = extra_info(shown, rh, led)
            if ex and norm(ex) not in norm(led):
                notes.append(("4 부가설명 차이", f"{folder}/{f}:{ln}", f"`{rh}` 원장 `{led}` · 화면 `{shown.strip()}`"))
                rows_out.append((rh, led, shown.strip(), f"{folder}/{f}:{ln}", "참고"))


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folders", nargs="*", help="기본: prototype prototype_clean")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    folders = args.folders or FOLDERS

    snbs = {f: parse_snb(f) for f in folders}
    result = {}
    all_errors = 0
    L = ["# FLOW CHECK REPORT — SNB · 링크 · 업무 플로우 가이드 · 샘플 표기 정합", "",
         f"- 생성: {datetime.datetime.now():%Y-%m-%d %H:%M}",
         f"- 대상: {', '.join(f'`{f}`' for f in folders)}", ""]
    errors_x, notes_x = [], []
    if len(folders) == 2:
        a, b = snbs[folders[0]], snbs[folders[1]]
        if a != b:
            errors_x.append(("1a 두 폴더 SNB_GROUPS 다름", "common-snb.js", "그룹 · 메뉴 정의가 일치하지 않음"))
            ta = {(g["title"], it["code"]): it for g in a for it in g["items"]}
            tb = {(g["title"], it["code"]): it for g in b for it in g["items"]}
            for k in sorted(set(ta) | set(tb)):
                if ta.get(k) != tb.get(k):
                    errors_x.append(("1a 차이", f"{k[0]} · {k[1]}", f"{folders[0]}: {ta.get(k)} / {folders[1]}: {tb.get(k)}"))
    summaries = []
    sections = []
    for fo in folders:
        groups = snbs[fo]
        errors = list(errors_x) if fo == folders[0] else []
        notes = []
        if groups is None:
            errors.append(("1 SNB_GROUPS 파싱 실패", f"{fo}/common-snb.js", ""))
            sections.append((fo, errors, notes, [], None))
            continue
        check_snb(fo, groups, errors, notes)
        if fo == "prototype_clean" or len(folders) == 1 or fo == folders[-1]:
            check_readme(groups, errors, notes)
        snb_err = len(errors)
        screens, out, inn, no_out, no_in, no_in_ng, snbf = check_links(fo, groups, notes)
        link_notes = [("2 나가는 링크 0", f, "본문에서 다른 화면으로 가는 링크 없음") for f in no_out]
        link_notes += [("2 들어오는 링크 0(SNB로만 도달)", f, "다른 화면 본문에서 참조하지 않음") for f in no_in]
        link_notes += [("2 들어오는 링크 0(가이드 제외)", f, "가이드에서만 연결됨") for f in no_in_ng if f not in no_in]
        notes += link_notes
        g_err0 = len(errors)
        nodes, ncodes = check_guide(fo, groups, errors, notes)
        guide_err = len(errors) - g_err0
        guide_note = sum(1 for n in notes if n[0].startswith("3"))
        ledger = load_ledger(fo)
        n_err0 = len(errors)
        name_rows = []
        check_names(fo, ledger, errors, notes, name_rows)
        name_err = len(errors) - n_err0
        name_note = sum(1 for n in notes if n[0].startswith("4"))
        link_note = len(link_notes)
        all_errors += len(errors)
        summaries.append((fo, snb_err, link_note, guide_err, guide_note, name_err, name_note))
        sections.append((fo, errors, notes, name_rows,
                         dict(screens=len(screens), nodes=nodes, ncodes=ncodes, ledger=len(ledger),
                              groups=len(groups), menus=sum(len(g["items"]) for g in groups), out=out, inn=inn)))

    tot = [sum(s[i] for s in summaries) for i in range(1, 7)]
    label = "양쪽" if len(folders) == 2 else folders[0]
    line = (f"[Skill 6] {label}: SNB 오류 {tot[0]} · 링크 참고 {tot[1]} · 가이드 오류 {tot[2]}/참고 {tot[3]} · "
            f"표기 오류 {tot[4]}/참고 {tot[5]} → {os.path.relpath(REPORT, ROOT)}")
    L += [f"- 요약: {line}", "", "| 폴더 | SNB 오류 | 링크 참고 | 가이드 오류 | 가이드 참고 | 표기 오류 | 표기 참고 |", "| :--- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for s in summaries:
        L.append("| " + " | ".join(str(x) for x in s) + " |")
    L.append("")
    for fo, errors, notes, name_rows, st in sections:
        L += [f"# `{fo}`", ""]
        if st:
            L += [f"- SNB 그룹 {st['groups']} · 메뉴 {st['menus']} · 화면 파일 {st['screens']} · 가이드 노드 {st['nodes']}(코드 {st['ncodes']}종) · 원장 권리자 {st['ledger']}", ""]
        for title, rows in (("오류", errors), ("참고", [n for n in notes if not n[0].startswith("2 ") and not n[0].startswith("4 ")])):
            L += [f"## {title} ({len(rows)}건)", ""]
            if rows:
                L += ["| 유형 | 위치 | 내용 |", "| :--- | :--- | :--- |"]
                L += [f"| {k} | `{c}` | {v} |" for k, c, v in rows]
            else:
                L.append("없음")
            L.append("")
        if st:
            lk = [n for n in notes if n[0].startswith("2 ")]
            L += [f"## 링크 그래프 참고 ({len(lk)}건)", "", "| 유형 | 화면 | 내용 |", "| :--- | :--- | :--- |"]
            L += [f"| {k} | `{c}` | {v} |" for k, c, v in lk] or ["| 없음 | | |"]
            L += ["", "### 화면별 링크 수", "", "| 화면 | out | in |", "| :--- | ---: | ---: |"]
            for f in sorted(st["out"].keys() | st["inn"].keys()):
                L.append(f"| `{f}` | {len(st['out'][f])} | {len(st['inn'][f])} |")
            L.append("")
        L += [f"## 샘플 표기 불일치 ({len(name_rows)}건)", ""]
        if name_rows:
            L += ["| 코드 | 원장 이름 | 화면 표기 | 파일:줄 | 구분 |", "| :--- | :--- | :--- | :--- | :--- |"]
            L += [f"| `{a}` | {b} | {c.replace('|', '/')} | `{d}` | {e} |" for a, b, c, d, e in sorted(name_rows, key=lambda r: (r[4] != "오류", r[0], r[3]))]
        else:
            L.append("없음")
        L.append("")
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(L) + "\n")
    print(line)
    if args.strict and all_errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
