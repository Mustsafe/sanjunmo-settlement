# patch_v5_6_paren_strip.py — 레포 루트에서 실행
# prototype_clean/common-snb.js: 치환 전에 "(코드뿐인 괄호)"를 괄호째 제거하는 단계 추가
import re, sys, shutil, subprocess, datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path.cwd()
SNB = ROOT / "prototype_clean" / "common-snb.js"
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = ROOT / "_archive" / "backup" / f"v5_6_{TS}" / "prototype_clean" / "common-snb.js"
PLAN = ROOT / ".antigravity" / "WORKFLOW_REDESIGN_PLAN.md"

def abort(msg):
    print(f"[ABORT] {msg}\n파일 미변경. 이 출력 전문을 분석 AI에 그대로 전달하세요.")
    sys.exit(2)

if not SNB.exists():
    abort(f"파일 없음: {SNB}")
with open(SNB, encoding="utf-8", newline="") as f:
    t = f.read()
if "__wfStripCodeParens" in t:
    abort("이미 적용됨 (__wfStripCodeParens 존재)")
EOL = "\r\n" if "\r\n" in t else "\n"

PRELUDE = r"""/* v5.6 코드뿐인 괄호 제거 — 치환표 적용 전에 실행 (clean 전용) */
(function () {
  if (window.__wfStripCodeParens) return;
  var ADMN = /^(?:ADMN-)?[A-Z]{2,5}-\d{3}(?:-[A-Z0-9]+)?(?:\/\d{3})?$/;
  var USNAKE = /^[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+$/;
  var LSNAKE = /^[a-z][a-z0-9]*(?:_[a-z0-9]+)+$/;
  var CODEKEY = /^[A-Z0-9_\-\/]+$/;
  var cache = new WeakMap();
  function keySet(src) {
    if (!src || typeof src !== "object") return null;
    if (cache.has(src)) return cache.get(src);
    var arr = Array.isArray(src)
      ? src.map(function (r) { return Array.isArray(r) ? r[0] : r; })
      : Object.keys(src);
    var s = new Set(arr.filter(function (k) {
      return typeof k === "string" && k.length >= 4 && /[A-Z]/.test(k) && CODEKEY.test(k);
    }));
    cache.set(src, s);
    return s;
  }
  function isCode(inner, src) {
    var parts = inner.replace(/[`'"]/g, "").split(/\s*[·,]\s*|\s+\/\s+/);
    var ks = keySet(src);
    return parts.length > 0 && parts.every(function (p) {
      p = p.trim();
      return !!p && (ADMN.test(p) || USNAKE.test(p) || LSNAKE.test(p) || (ks && ks.has(p)));
    });
  }
  var PAREN = /\s*\(\s*([^()]{2,80}?)\s*\)/g;
  var LEAD = /[가-힣A-Za-z0-9%)\]]\s*$/;
  window.__wfStripCodeParens = function (str, src) {
    if (!str || typeof str !== "string" || str.indexOf("(") === -1) return str;
    return str.replace(PAREN, function (m, inner, off, whole) {
      if (!LEAD.test(whole.slice(0, off))) return m;
      return isCode(inner, src) ? "" : m;
    });
  };
  window.__wfStripCodeElParens = function (root, src) {
    if (!root || !root.querySelectorAll) return;
    var els = root.querySelectorAll("code");
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      if (el.classList.contains("raw-keep") || el.children.length) continue;
      var prev = el.previousSibling, next = el.nextSibling;
      if (!prev || !next || prev.nodeType !== 3 || next.nodeType !== 3) continue;
      if (!/\(\s*$/.test(prev.nodeValue) || !/^\s*\)/.test(next.nodeValue)) continue;
      var before = prev.nodeValue.replace(/\s*\(\s*$/, "");
      if (!LEAD.test(before)) continue;
      if (!isCode(el.textContent.trim(), src)) continue;
      prev.nodeValue = before;
      next.nodeValue = next.nodeValue.replace(/^\s*\)/, "");
      el.parentNode.removeChild(el);
    }
  };
})();
""".replace("\n", EOL)

HOOKS = [
    ("transformText",
     r"(function transformText\(str\) \{[ \t]*\r?\n[ \t]*if \(!str[^\n]*\n([ \t]*)let out = str;)",
     "out = window.__wfStripCodeParens(out, TEXT_REPLACEMENTS);"),
    ("cleanString",
     r"(function cleanString\(str\) \{[ \t]*\r?\n[ \t]*if \(!str[^\n]*\n([ \t]*)let out = str;)",
     "out = window.__wfStripCodeParens(out, EXTRA_MAP);"),
    ("walkAndClean",
     r"(function walkAndClean\(root\) \{[ \t]*\r?\n([ \t]*)if \(!root\) return;)",
     "window.__wfStripCodeElParens(root, TEXT_REPLACEMENTS);"),
    ("runEnhancedClean",
     r"(function runEnhancedClean\(root\) \{[ \t]*\r?\n([ \t]*)if \(!root\) return;)",
     "window.__wfStripCodeElParens(root, EXTRA_MAP);"),
]

for label, pat, line in HOOKS:
    ms = list(re.finditer(pat, t))
    if len(ms) != 1:
        abort(f"{label} 삽입 지점 {len(ms)}건 (1건이어야 함)")
    m = ms[0]
    t = t[:m.end()] + EOL + m.group(2) + line + t[m.end():]

t = PRELUDE + EOL + t

BACKUP.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(SNB, BACKUP)
with open(SNB, "w", encoding="utf-8", newline="") as f:
    f.write(t)

node = shutil.which("node")
if node:
    r = subprocess.run([node, "--check", str(SNB)], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        shutil.copy2(BACKUP, SNB)
        abort("node --check 문법 오류 → 원본 복원함\n" + (r.stderr or r.stdout))
    syntax = "node --check 통과"
else:
    syntax = "[WARN] node 없음 — 문법 검사는 E2E로 대체"

if PLAN.exists():
    note = EOL.join([
        "", "### v5.6 괄호 중복 1차 — 런타임 치환 순서 보정 (2026-10-21)",
        "- 원인: transformText가 TEXT_REPLACEMENTS(코드→이름)를 REGEX_CLEANERS(코드 괄호 제거)보다 먼저 적용, cleanString(EXTRA_MAP)은 괄호 제거 없음 → '앞말(같은 말)' 중복.",
        "- 조치: 두 함수 치환 전에 '코드뿐인 괄호'(화면코드·snake_case·치환표 영문 키)를 괄호째 제거. <code> 감싼 형태 포함. prototype_clean/common-snb.js 한 파일.",
        "- 잔여(HTML 원문 중복·코드+설명 혼합 괄호)는 재스캔 결과로 2차 처리.", "",
    ])
    with open(PLAN, "a", encoding="utf-8", newline="") as fp:
        fp.write(note)

print(f"[OK] prototype_clean/common-snb.js 수정 · 백업 {BACKUP.relative_to(ROOT)}")
print(f"  - 프렐류드 추가, 훅 4곳 삽입: " + ", ".join(h[0] for h in HOOKS))
print(f"  - {syntax}")
