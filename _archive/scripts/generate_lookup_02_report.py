# -*- coding: utf-8 -*-
import json
from pathlib import Path

ROOT = Path(".")
REPORT_PATH = ROOT / ".antigravity" / "reports" / "WORKFLOW_LOOKUP_02.md"

def get_lines_matching(file_path: Path, keywords: list):
    if not file_path.exists():
        return None
    res = {kw: [] for kw in keywords}
    for i, line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), 1):
        for kw in keywords:
            if kw in line:
                res[kw].append((i, line))
    return res

# 1 & 2. common-snb.js in clean and prototype
clean_snb = ROOT / "prototype_clean" / "common-snb.js"
proto_snb = ROOT / "prototype" / "common-snb.js"

clean_res = get_lines_matching(clean_snb, ["CONF-006", "USER-007", "정답지"])
proto_res = get_lines_matching(proto_snb, ["CONF-006", "USER-007", "정답지"])

# 3. prototype_clean/*.html for "단계 ·" or "단계·"
matches_step = []
for f in sorted((ROOT / "prototype_clean").glob("*.html")):
    for i, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
        if "단계 ·" in line or "단계·" in line:
            matches_step.append((f.name, i, line))

# 4. ADMN-CONF-005_baseline.html for "정답지"
conf005 = ROOT / "prototype_clean" / "ADMN-CONF-005_baseline.html"
conf005_matches = []
for i, line in enumerate(conf005.read_text(encoding="utf-8").splitlines(), 1):
    if "정답지" in line:
        conf005_matches.append((i, line))

# 5. Load temp_snb_grid.json
with open(".antigravity/reports/temp_snb_grid.json", encoding="utf-8") as f:
    dom_data = json.load(f)

snb_groups = dom_data["snb"]
grid_cards = dom_data["grid"]

# Build Report
doc = []
doc.append("# WORKFLOW_LOOKUP_02 리포트 (읽기 전용 실사 확인)")
doc.append("")
doc.append("> 작성일시: 2026-10-21  ")
doc.append("> 대상: prototype_clean 및 prototype 정본/프로토타입 실사  ")
doc.append("")
doc.append("---")
doc.append("")
doc.append("## 1. prototype_clean/common-snb.js 검색 결과")
doc.append("")
for kw in ["CONF-006", "USER-007", "정답지"]:
    doc.append(f"### 1.{['CONF-006', 'USER-007', '정답지'].index(kw)+1} 키워드: \"{kw}\"")
    items = clean_res[kw]
    if not items:
        doc.append("0건")
    else:
        for ln, text in items:
            doc.append(f"- Line {ln}: `{text}`")
    doc.append("")

doc.append("---")
doc.append("")
doc.append("## 2. prototype/common-snb.js 검색 결과")
doc.append("")
if proto_res is None:
    doc.append("파일 없음")
else:
    for kw in ["CONF-006", "USER-007", "정답지"]:
        doc.append(f"### 2.{['CONF-006', 'USER-007', '정답지'].index(kw)+1} 키워드: \"{kw}\"")
        items = proto_res[kw]
        if not items:
            doc.append("0건")
        else:
            for ln, text in items:
                doc.append(f"- Line {ln}: `{text}`")
        doc.append("")

doc.append("---")
doc.append("")
doc.append("## 3. prototype_clean/*.html 전체 \"단계 ·\" 또는 \"단계·\" 포함 줄")
doc.append("")
if not matches_step:
    doc.append("0건")
else:
    doc.append(f"총 {len(matches_step)}건 검출")
    doc.append("")
    for fn, ln, text in matches_step:
        doc.append(f"- `{fn}` Line {ln}: `{text}`")
doc.append("")

doc.append("---")
doc.append("")
doc.append("## 4. prototype_clean/ADMN-CONF-005_baseline.html 내 \"정답지\" 포함 줄")
doc.append("")
if not conf005_matches:
    doc.append("0건")
else:
    doc.append(f"총 {len(conf005_matches)}건 검출")
    doc.append("")
    for ln, text in conf005_matches:
        doc.append(f"- Line {ln}: `{text}`")
doc.append("")

doc.append("---")
doc.append("")
doc.append("## 5. Playwright 00_WORKFLOW_GUIDE 렌더링 실사 결과")
doc.append("")
doc.append("### 5-1. 좌측 SNB: 그룹 제목별 메뉴 항목 [텍스트 | href]")
doc.append("")
for g in snb_groups:
    doc.append(f"#### SNB 그룹: {g['title']} (총 {len(g['items'])}개 항목)")
    for it in g["items"]:
        doc.append(f"- [{it['text']} | {it['href']}]")
    doc.append("")

doc.append("### 5-2. #wf-dir-grid: 카드 h4별 링크 [텍스트 | href]")
doc.append("")
for c in grid_cards:
    doc.append(f"#### 디렉터리 카드: {c['title']} (총 {len(c['items'])}개 항목)")
    for it in c["items"]:
        doc.append(f"- [{it['text']} | {it['href']}]")
    doc.append("")

doc.append("### 5-3. 그룹별 개수 비교표 및 SNB 전용 항목")
doc.append("")
doc.append("| 그룹명 | SNB 개수 | 디렉터리(#wf-dir-grid) 개수 | 차이 |")
doc.append("| :--- | :-: | :-: | :-: |")

snb_only_items = []
for i in range(len(snb_groups)):
    sg = snb_groups[i]
    gg = grid_cards[i]
    diff_count = len(sg["items"]) - len(gg["items"])
    doc.append(f"| **{sg['title']}** | {len(sg['items'])} | {len(gg['items'])} | {diff_count:+d} |")
    
    grid_hrefs = {x["href"] for x in gg["items"]}
    for it in sg["items"]:
        if it["href"] not in grid_hrefs:
            snb_only_items.append((sg["title"], it["text"], it["href"]))

doc.append("")
doc.append("#### SNB에만 있는 항목 목록 (디렉터리 제외 항목)")
doc.append("")
if not snb_only_items:
    doc.append("0건")
else:
    for gname, text, href in snb_only_items:
        doc.append(f"- **소속 그룹:** {gname} / **항목:** `[{text} | {href}]` (사유: 가이드 페이지 자체 링크 필터링)")
doc.append("")

REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
REPORT_PATH.write_text("\n".join(doc), encoding="utf-8")
print(f"[OK] Report generated at {REPORT_PATH}")
