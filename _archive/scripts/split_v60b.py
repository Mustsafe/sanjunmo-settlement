# split_v60b.py — 읽기 전용 (기존 리포트 무수정, 신규 파일만 생성)
from pathlib import Path
src = Path(".antigravity/reports/V6.0_PROBE_SETT005_B.md")
dst = Path(".antigravity/reports/V6.0_PROBE_SETT005_B2.md")
t = src.read_text(encoding="utf-8")
k = t.find("===== (E)")
body = t[k:] if k >= 0 else "0건 ('===== (E)' 마커 없음)"
body = body.replace("```", "").rstrip()
dst.write_text("## 원문 (V6.0_PROBE_SETT005_B.md 의 (E) 이후 구간 그대로)\n\n```\n" + body + "\n```\n", encoding="utf-8", newline="\n")
print(f"[SPLIT DONE] {dst} / {len(body)} chars")
