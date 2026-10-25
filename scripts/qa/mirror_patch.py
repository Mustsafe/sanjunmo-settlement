#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
한쪽 폴더 수정을 다른 폴더에 옮기는 도구 (--dry-run 으로 먼저 확인 권장)

동작
  git diff HEAD -U0 -- <from 파일> 의 각 hunk 를 <to> 의 동명 파일에 적용한다. 줄 번호는 쓰지 않는다.
  - 삭제 줄이 있는 hunk: 삭제 줄 블록을 원문 그대로(줄 끝 무시) 찾아 정확히 1건일 때만 추가 줄로 교체.
  - 추가만 있는 hunk(삽입): 변경 전 파일의 앞뒤 줄(1~4줄)을 기준점으로 삼아, 기준점이 1건으로 정해질 때만 삽입.
  - 0건 · 2건 이상이면 그 hunk 는 건너뛰고 보고한다. (clean 은 문구를 바꾸므로 문구가 다른 줄은 건너뛰어진다)
  - 줄 끝(CRLF/LF)은 대상 파일 것을 유지한다. 적용 전 _archive/backup/mirror_<시각>/<to>/ 에 백업한다.

사용법:
  python scripts/qa/mirror_patch.py --from prototype_clean --to prototype [파일...] [--dry-run]
  파일 생략 시 git diff HEAD 로 --from 폴더의 변경 파일 전부. 파일은 이름만 써도 된다.
  --base <폴더>  : HEAD 대신 변경 전 사본 폴더와 비교 (커밋되지 않은 임시 폴더 시험용)
"""
import argparse
import datetime
import os
import re
import shutil
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HUNK_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")


def git(*args):
    r = subprocess.run(["git", "-c", "core.quotepath=off", *args], cwd=ROOT, capture_output=True)
    return r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace")


def split_keep(text):
    """줄 끝을 보존한 줄 리스트."""
    return re.findall(r"[^\n]*\n|[^\n]+$", text)


def strip_eol(s):
    return s.rstrip("\r\n")


def parse_hunks(diff):
    """[(old_start, [삭제줄], [추가줄])]"""
    hunks, cur = [], None
    for raw in diff.split("\n"):
        line = raw.rstrip("\r")
        m = HUNK_RE.match(line)
        if m:
            cur = [int(m.group(1)), int(m.group(2)) if m.group(2) is not None else 1, [], []]
            hunks.append(cur)
        elif cur is not None:
            if line.startswith("-") and not line.startswith("---"):
                cur[2].append(line[1:])
            elif line.startswith("+") and not line.startswith("+++"):
                cur[3].append(line[1:])
    return [(h[0], h[1], h[2], h[3]) for h in hunks]


def find_block(lines_n, block):
    """정규화 줄 리스트에서 block 이 연속 일치하는 시작 위치들."""
    n = len(block)
    if n == 0:
        return []
    return [i for i in range(len(lines_n) - n + 1) if lines_n[i:i + n] == block]


def eol_at(lines, idx, default="\r\n"):
    for k in (idx, idx - 1, idx + 1):
        if 0 <= k < len(lines):
            m = re.search(r"\r?\n$", lines[k])
            if m:
                return m.group(0)
    return default


def apply_file(base_lines, hunks, target_lines):
    """hunk 들을 target_lines 에 적용. (새 줄 리스트, 적용 수, 건너뜀 [(앞부분, 이유)])"""
    lines = list(target_lines)
    applied, skipped = 0, []
    for old_start, old_cnt, dels, adds in hunks:
        head = (dels[0] if dels else (adds[0] if adds else "")).strip()[:90]
        norm = [strip_eol(l) for l in lines]
        if dels:
            pos = find_block(norm, dels)
            if len(pos) != 1:
                skipped.append((head, f"삭제 줄 블록 {len(pos)}건 일치"))
                continue
            i = pos[0]
            eol = eol_at(lines, i)
            lines[i:i + len(dels)] = [a + eol for a in adds]
            applied += 1
        else:
            # 삽입: 변경 전 파일에서 old_start(앞 줄 번호) 기준 앞뒤 k줄을 기준점으로
            base_n = [strip_eol(l) for l in base_lines]
            done = False
            for k in range(1, 5):
                lo, hi = old_start - k, old_start + k
                if lo < 0 or hi > len(base_n):
                    # 파일 끝/처음에 가까우면 가능한 범위만
                    lo, hi = max(lo, 0), min(hi, len(base_n))
                anchor = base_n[lo:hi]
                if not anchor:
                    break
                pos = find_block(norm, anchor)
                if len(pos) == 1:
                    ins_at = pos[0] + (old_start - lo)
                    eol = eol_at(lines, ins_at - 1)
                    if ins_at > 0 and not re.search(r"\n$", lines[ins_at - 1]):
                        lines[ins_at - 1] += eol
                    lines[ins_at:ins_at] = [a + eol for a in adds]
                    applied += 1
                    done = True
                    break
                if len(pos) == 0:
                    skipped.append((head, "삽입 기준 줄이 대상에 없음"))
                    done = True
                    break
            if not done:
                skipped.append((head, "삽입 기준 줄이 여러 곳에 일치"))
    return lines, applied, skipped


def main():
    ap = argparse.ArgumentParser(description="한쪽 폴더 수정을 다른 폴더에 옮기기")
    ap.add_argument("--from", dest="src", required=True)
    ap.add_argument("--to", dest="dst", required=True)
    ap.add_argument("--base", help="HEAD 대신 변경 전 사본 폴더 (시험용)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("files", nargs="*")
    args = ap.parse_args()
    src = args.src.replace("\\", "/").rstrip("/")
    dst = args.dst.replace("\\", "/").rstrip("/")

    if args.files:
        names = [os.path.basename(f.replace("\\", "/")) for f in args.files]
    elif args.base:
        names = sorted(f for f in os.listdir(os.path.join(ROOT, src))
                       if os.path.isfile(os.path.join(ROOT, args.base, f)) and
                       open(os.path.join(ROOT, src, f), "rb").read() != open(os.path.join(ROOT, args.base, f), "rb").read())
    else:
        _, out, _ = git("diff", "HEAD", "--name-only", "--", src)
        names = [os.path.basename(l.strip()) for l in out.splitlines() if l.strip().startswith(src + "/")]

    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bdir = os.path.join(ROOT, "_archive", "backup", "mirror_" + stamp, os.path.basename(dst))
    tot_a = tot_s = nfiles = 0
    skipped_all = []
    for name in names:
        sp, dp = os.path.join(ROOT, src, name), os.path.join(ROOT, dst, name)
        if not os.path.isfile(sp):
            skipped_all.append((name, "(파일 전체)", "from 폴더에 파일 없음"))
            continue
        if not os.path.isfile(dp):
            skipped_all.append((name, "(파일 전체)", "to 폴더에 동명 파일 없음"))
            continue
        if args.base:
            _, diff, _ = git("diff", "--no-index", "-U0", "--no-color", "--", os.path.join(args.base, name), os.path.join(src, name))
            with open(os.path.join(ROOT, args.base, name), encoding="utf-8", newline="") as f:
                base_lines = split_keep(f.read())
        else:
            _, diff, _ = git("diff", "HEAD", "-U0", "--no-color", "--", f"{src}/{name}")
            _, old, _ = git("show", f"HEAD:{src}/{name}")
            base_lines = split_keep(old)
        hunks = parse_hunks(diff)
        if not hunks:
            continue
        with open(dp, encoding="utf-8", newline="") as f:
            target = split_keep(f.read())
        new, a, sk = apply_file(base_lines, hunks, target)
        nfiles += 1
        tot_a += a
        tot_s += len(sk)
        skipped_all += [(name, h, why) for h, why in sk]
        if a and not args.dry_run:
            os.makedirs(bdir, exist_ok=True)
            shutil.copy2(dp, os.path.join(bdir, name))
            with open(dp, "w", encoding="utf-8", newline="") as f:
                f.write("".join(new))
    tag = " (dry-run)" if args.dry_run else ""
    print(f"[mirror] 파일 {nfiles} · hunk 적용 {tot_a} / 건너뜀 {tot_s}{tag}")
    for name, h, why in skipped_all:
        print(f"  - 건너뜀 {name}: {h} ({why})")
    if tot_a and not args.dry_run:
        print(f"  백업: {os.path.relpath(bdir, ROOT)}")


if __name__ == "__main__":
    main()
