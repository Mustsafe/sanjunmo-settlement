# scripts/qa/scan_paren_dup.py — 읽기 전용. 레포 루트에서 실행.
# A) 렌더링된 화면에서 "앞말 (같은 말)" 괄호 중복 탐지 (prototype, prototype_clean)
# B) prototype_clean HTML 원문의 "(ADMN-코드)" 자리 전수 목록 (런타임에 화면명으로 바뀌는 곳)
import re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path.cwd()
FOLDERS = ["prototype_clean", "prototype"]
REP = ROOT / ".antigravity" / "reports"
REP.mkdir(parents=True, exist_ok=True)
OUT_A = REP / "PAREN_DUP_SCAN.md"
OUT_B = REP / "PAREN_DUP_STATIC.md"

JS = r"""() => {
  const out = new Set();
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
  let n;
  while ((n = w.nextNode())) {
    if (n.closest('script,style')) continue;
    const own = [...n.childNodes].some(c => c.nodeType === 3 && c.textContent.includes('('));
    if (!own) continue;
    const t = n.textContent.replace(/\s+/g, ' ').trim();
    if (t && t.length <= 400) out.add(t);
  }
  return [...out];
}"""

PAREN = re.compile(r"\(([^()]{1,40})\)")

def norm(s):
    return re.sub(r"[\s·・/\-–—_,.:()\[\]<>]", "", s).lower()

def bigr(s):
    return {s[i:i + 2] for i in range(len(s) - 1)}

def is_dup(outer, inner):
    o, i = norm(outer), norm(inner)
    if len(i) < 2 or not o or not re.search(r"[가-힣A-Za-z]{2}", inner):
        return False
    if i in o:
        return True
    bi = bigr(i)
    return bool(bi) and len(bi & bigr(o)) / len(bi) >= 0.6

def outer_of(text, start):
    seg = text[:start]
    cut = max(seg.rfind(ch) for ch in ")•:|—")
    return seg[cut + 1:][-30:].strip()

rows, total = {f: [] for f in FOLDERS}, 0
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    for f in FOLDERS:
        for h in sorted((ROOT / f).glob("*.html")):
            try:
                pg.goto(h.resolve().as_uri())
                pg.wait_for_timeout(800)
                texts = pg.evaluate(JS)
            except Exception as e:
                rows[f].append((h.name, f"[로드 실패] {e}", "", ""))
                continue
            seen = set()
            for t in texts:
                for m in PAREN.finditer(t):
                    o, i = outer_of(t, m.start()), m.group(1).strip()
                    key = (o, i)
                    if key in seen or not is_dup(o, i):
                        continue
                    seen.add(key)
                    s = max(0, m.start() - 60)
                    rows[f].append((h.name, t[s:m.end() + 20], o, i))
    b.close()

lines = ["# PAREN_DUP_SCAN — 렌더링 결과 괄호 중복 (자동 탐지, 원문)", ""]
for f in FOLDERS:
    lines += [f"## {f} — {len(rows[f])}건", "", "| 파일 | 앞말 | 괄호 안 | 주변 텍스트 |", "|---|---|---|---|"]
    for name, ctx, o, i in rows[f]:
        c = ctx.replace("|", "\\|")
        lines.append(f"| {name} | {o.replace('|', '/')} | {i.replace('|', '/')} | {c} |")
    lines.append("")
    total += len(rows[f])
OUT_A.write_text("\n".join(lines), encoding="utf-8")

CODE = re.compile(r"\((?:<code>)?ADMN-[A-Z0-9]+(?:-[A-Z0-9]+)*(?:/[0-9]{3})?(?:</code>)?\)")
static = []
for h in sorted((ROOT / "prototype_clean").glob("*.html")):
    in_block = False
    for ln, l in enumerate(h.read_text(encoding="utf-8").split("\n"), 1):
        if re.search(r"<(script|style)\b", l): in_block = True
        if not in_block:
            for m in CODE.finditer(l):
                s = max(0, m.start() - 70)
                static.append(f"- {h.name}:{ln}: {l[s:m.end() + 10].strip()}")
        if re.search(r"</(script|style)>", l): in_block = False
OUT_B.write_text("\n".join(["# PAREN_DUP_STATIC — prototype_clean 원문의 (ADMN-코드) 자리 (script/style 제외)",
                            "", f"총 {len(static)}건", ""] + static), encoding="utf-8")

for f in FOLDERS:
    print(f"[A] {f}: {len(rows[f])}건")
print(f"[B] prototype_clean (ADMN-코드) 자리: {len(static)}건")
for o in (OUT_A, OUT_B):
    n = len(o.read_text(encoding="utf-8"))
    print(f"[SIZE] {o.name}: {n}자" + ("  [WARN] 30,000자 초과" if n > 30000 else ""))
