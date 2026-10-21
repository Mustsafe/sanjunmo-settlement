# -*- coding: utf-8 -*-
"""
publish_workflow_to_prototype.py  (레포 루트에서 실행)
6단계: prototype_clean/00_WORKFLOW_GUIDE_baseline.html → prototype/ 덮어쓰기
- 참조 파일 검사는 <script>/<style> 밖의 실제 태그 속성만 대상
- 누락 참조가 있으면 중단(파일 미변경)
"""
import re, sys, shutil, datetime
from pathlib import Path

ROOT = Path.cwd()
NAME = "00_WORKFLOW_GUIDE_baseline.html"
SRC = ROOT / "prototype_clean" / NAME
DST = ROOT / "prototype" / NAME
PLAN = ROOT / ".antigravity" / "WORKFLOW_REDESIGN_PLAN.md"
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = ROOT / "_archive" / "backup" / f"v5_3b_{TS}" / "prototype" / NAME

for p in [SRC, DST.parent, PLAN]:
    if not p.exists(): print(f"[ERROR] 없음: {p}"); sys.exit(2)

with SRC.open(encoding="utf-8", newline="") as f: html = f.read()

body = re.sub(r'<(script|style)\b[^>]*>.*?</\1\s*>', '', html, flags=re.S | re.I)
refs = set(re.findall(r'<\w+\b[^>]*?\s(?:src|href)="([^"]+)"', body))
missing, checked = [], 0
for r in sorted(refs):
    if re.match(r'(https?:|#|javascript:|data:|mailto:|tel:)', r): continue
    base = r.split("?")[0].split("#")[0]
    if not base: continue
    checked += 1
    if not (DST.parent / base).exists(): missing.append(base)
for r in sorted(set(re.findall(r'<script\b[^>]*\ssrc="([^"]+)"', html))):
    if r.startswith("http"): continue
    checked += 1
    if not (DST.parent / r.split("?")[0]).exists(): missing.append(r)

print(f"[CHECK] 로컬 참조 {checked}건 검사")
if missing:
    print(f"[ABORT] prototype/에 없는 참조: {sorted(set(missing))}. 파일 미변경. 로그를 분석 AI에 반환하세요.")
    sys.exit(2)

if DST.exists():
    BACKUP.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(DST, BACKUP)
    print(f"[BACKUP] {BACKUP}")
shutil.copy2(SRC, DST)
print(f"[DONE] {DST} ← clean본 덮어쓰기")

with PLAN.open(encoding="utf-8", newline="") as f: plan = f.read()
MARK = "- 6단계 실제 완료(v5.3b)"
if MARK not in plan:
    plan = plan.rstrip() + f"\n{MARK}: v5.3 참조 검사 오탐(script 내 문자열 조합을 경로로 인식)으로 보류됐던 덮어쓰기를 script/style 제외 검사로 재실행\n"
    with PLAN.open("w", encoding="utf-8", newline="") as f: f.write(plan)
    print("[PLAN] 결정 로그 추가")
