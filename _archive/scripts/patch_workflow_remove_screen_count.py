# patch_workflow_remove_screen_count.py
# 00_WORKFLOW_GUIDE_baseline.html 화면 수 표기 제거 (prototype/ + prototype_clean/ 동시)
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
TARGETS = [
    ROOT / "prototype" / "00_WORKFLOW_GUIDE_baseline.html",
    ROOT / "prototype_clean" / "00_WORKFLOW_GUIDE_baseline.html",
]

# (설명, 패턴, 치환값)
RULES = [
    ("hero 배지·설명문: 백오피스 N개 화면", re.compile(r"백오피스\s+\d+개\s+화면"), "백오피스 화면"),
    ("여정 맵 제목: 전체 N개 화면의", re.compile(r"전체\s+\d+개\s+화면의\s+"), ""),
    ("도메인 디렉터리 배지: 전체 N개 프로토타입 100% 연결", re.compile(r"전체\s+\d+개\s+프로토타입\s+100%\s+연결"), "전체 프로토타입 연결"),
]

# 화면 수 잔존 여부 확인용 (도메인 수 '11개 전 도메인'은 대상 아님)
RESIDUAL = re.compile(r"\d+개\s*(?:화면|프로토타입)")


def main():
    missing = [str(p) for p in TARGETS if not p.exists()]
    if missing:
        print("[ERROR] 대상 파일 없음:", *missing, sep="\n  ")
        sys.exit(1)

    plans = []
    errors = []
    for path in TARGETS:
        with open(path, "r", encoding="utf-8", newline="") as f:
            src = f.read()
        out = src
        counts = []
        for desc, pat, repl in RULES:
            out, n = pat.subn(repl, out)
            counts.append((desc, n))
            if n == 0:
                errors.append(f"{path.relative_to(ROOT)} :: 매칭 0건 → {desc}")
        plans.append((path, src, out, counts))

    # 하나라도 매칭 실패하면 아무 파일도 쓰지 않고 종료
    if errors:
        print("[ABORT] 매칭 실패로 패치 중단 (파일 미변경). 아래 로그를 분석 AI에 반환하세요.")
        for e in errors:
            print("  -", e)
        sys.exit(2)

    for path, src, out, counts in plans:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(out)
        print(f"[OK] {path.relative_to(ROOT)}")
        for desc, n in counts:
            print(f"     {n}건 · {desc}")
        left = RESIDUAL.findall(out)
        if left:
            print(f"     [WARN] 잔존 화면 수 표기 {len(left)}건: {left}")
        else:
            print("     잔존 화면 수 표기 0건")


if __name__ == "__main__":
    main()
