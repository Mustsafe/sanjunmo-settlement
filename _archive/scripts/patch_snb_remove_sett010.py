# patch_snb_remove_sett010.py
# 1) common-snb.js 에서 SETT-010 메뉴 항목 제거 (prototype/ + prototype_clean/)
# 2) WORKFLOW_REDESIGN_PLAN.md 에 결정 기록
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
SNB_FILES = [p for p in (ROOT / "prototype" / "common-snb.js",
                         ROOT / "prototype_clean" / "common-snb.js") if p.exists()]
PLAN = ROOT / ".antigravity" / "WORKFLOW_REDESIGN_PLAN.md"
LINE_RE = re.compile(r'^[ \t]*\{[^\n]*code:\s*"SETT-010"[^\n]*\},?[ \t]*\r?\n', re.M)

DECISIONS = """
## 결정 로그
- 2026-10-21 · SETT-010 은 독립 화면 아님. 화면설계서 단계의 내부 정산 조회 번호였고 정본은 SETT-009. 원천세·지급명세서 산출물은 SETT-009 신고 자료 뷰(?view=tax-report) 기능 → SNB 항목 제거
- 2026-10-21 · SNB 메뉴명은 정본 화면명의 축약으로 보고 유지. 업무플로우 페이지 카드도 SNB 메뉴명 사용
- 2026-10-21 · 1:1 문의 분기 허브 = BRD-002, 정답지 = BRD-006 (통합 설계서 Set 4 [A] 기준). README 인벤토리 표기 불일치는 별도 정리
- 2026-10-21 · patch_all_snb_v3.html 은 화면 아님 → 디렉터리 제외
"""


def main():
    if not SNB_FILES:
        print("[ERROR] common-snb.js 를 찾지 못함")
        sys.exit(1)

    plans, errors = [], []
    for p in SNB_FILES:
        with open(p, "r", encoding="utf-8", newline="") as f:
            src = f.read()
        out, n = LINE_RE.subn("", src)
        if n != 1:
            errors.append(f"{p.relative_to(ROOT)} :: SETT-010 매칭 {n}건 (1건이어야 함)")
        plans.append((p, out, n))

    if errors:
        print("[ABORT] 파일 미변경. 로그를 분석 AI에 반환하세요.")
        for e in errors:
            print("  -", e)
        sys.exit(2)

    for p, out, n in plans:
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(out)
        left = "SETT-010" in out
        print(f"[OK] {p.relative_to(ROOT)} · 제거 {n}건 · 잔존 {'있음 [WARN]' if left else '0건'}")

    if PLAN.exists():
        txt = PLAN.read_text(encoding="utf-8")
        if "## 결정 로그" not in txt:
            PLAN.write_text(txt.rstrip() + "\n" + DECISIONS, encoding="utf-8")
            print(f"[OK] 플랜 파일 결정 로그 추가")
        else:
            print("[SKIP] 결정 로그 섹션 이미 있음 — 수동 확인")
    else:
        print("[WARN] 플랜 파일 없음")


if __name__ == "__main__":
    main()
