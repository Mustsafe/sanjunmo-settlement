#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[Skill 3] 화면 간 데이터 대조기 (읽기 전용 QA 도구 — HTML을 수정하지 않음)

목적
  같은 권리자 · 계약 · 도서가 화면마다 다른 이름 · 번호로 적혀 있지 않은지 대조한다.
  샘플 데이터라도 화면 사이에서 어긋나면 검수자가 흐름을 따라갈 수 없다.

검사 (마크업 + 스크립트 문자열 전체, 태그 제거 후)
  [1] 권리자 RH-NNNN       → 붙어 있는 이름("정종대 (RH-0025)", "RH-0025 (정종대)")이 둘 이상이면 오류
  [2] 계약 CON-YYYY-NNN     → 같은 줄 가까이(60자)에 함께 적힌 권리자 RH 코드가 둘 이상이면 오류
  [2b] 스크립트 데이터       → 한 객체 안의 권리자 코드 키(holderId · rightsHolderId · payeeId 등)와
                              이름 키(holderName · rightsHolderName 등)를 짝지어, 같은 RH 코드에 다른 이름이 붙으면 오류.
                              계약 코드 키(id · contractId)와 권리자 코드 키를 짝지어, 같은 계약이 다른 권리자를 가리키면 오류
  [3] 도서 SKU PROD-BK-NNNN → 옛 형식(BOOK-NNNN · BK-YYYY-NNN · TMP-BK-*)이 남아 있으면 오류
                              임시코드는 BK-REQ-YYYY-NNNN만 허용(자릿수가 다르면 오류)
                              같은 도서명이 서로 다른 SKU로 적혀 있으면 오류
                              같은 SKU에 붙은 도서명이 여럿이면 참고(약칭일 수 있음)
                              스크립트 객체 안의 SKU 키(sku · productId · id)와 이름 키(title · productName · name)도 짝짓는다
  [4] 이름 → 코드 역방향    → 같은 권리자 이름이 서로 다른 RH 코드로 적혀 있으면 오류
  [5] 수취인 코드           → 2계층 수취인도 권리자 원장의 RH 코드를 쓴다. 옛 수취인 코드(PY-NNNN)가 남아 있으면 오류

사용법:
  python scripts/qa/skill_cross_data_check.py                  # prototype_clean 기준(두 폴더는 데이터가 같음)
  python scripts/qa/skill_cross_data_check.py prototype
  python scripts/qa/skill_cross_data_check.py --strict         # 오류 1건 이상이면 exit 1
리포트: scripts/qa/reports/CROSS_DATA_CHECK_REPORT.md
"""
import argparse
import datetime
import html
import os
import re
import sys
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REPORT = os.path.join(ROOT, "scripts", "qa", "reports", "CROSS_DATA_CHECK_REPORT.md")

NAME = r"([가-힣]{2,4})(?:\s*(?:강사|대표|저자|작가))?"
RH = r"RH-\d{4}"
CON = r"CON-\d{4}-\d{3}"
CT = r"(?:CT|CON)-\d{4}-[0-9A-Z]{3,4}"
RH_KEY = r"(?:rightsHolderId|primaryHolderId|holderId|payeeId|partnerId|rights_holder_id)"
NAME_KEY = r"(?:rightsHolderName|primaryHolderName|holderName|payeeName|partnerName|holder_name)"
CT_KEY = r"(?:id|contractId|contract_id)"


def lead_name(s):
    """이름 값의 첫 한글 낱말(2자 이상) — '고(故) 박위생 → …' → 박위생, '(주)산준교육 에이전시' → 산준교육"""
    if "*" in s:                               # 비식별(가명) 표시는 대조하지 않는다
        return None
    for w in re.findall(r"[가-힣]{2,}", s):
        if w not in NOT_NAME:
            return w[:4]
    return None


def objects(raw):
    """스크립트 객체 리터럴 조각 — 중괄호 안쪽(중첩 없는 가장 안쪽 객체)"""
    return re.findall(r"\{[^{}]{0,2000}\}", raw)
BK = r"PROD-BK-\d{4}"
BK_OLD = r"\bBOOK-(?:\d{4}|X{4}|AUTO)\b|(?<![A-Z-])BK-\d{4}-\d+|TMP-BK-[0-9A-Z*]+"
BK_REQ = r"BK-REQ-\d{4}-\d+"
TITLE_CH = r"[^()<>'\"\n|·:\[\]{}]"
NOT_NAME = {"강사", "대표", "저자", "본인", "정산", "계약", "권리", "수취", "위탁", "전속", "인세", "도서", "산업", "소방", "선택", "현재", "공동", "단독", "해지", "대상", "주권", "외부", "권리자", "정상", "사단법인", "재단법인", "주식회사"}


def plain(text):
    text = re.sub(r"/\*.*?\*/|<!--.*?-->", " ", text, flags=re.S)   # 주석은 화면 데이터가 아니다
    text = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(text)


def norm_title(t):
    t = re.sub(r"\s+", " ", t).strip(" -–—.,…")
    t = re.sub(r"^\d{4}\s*", "", t)          # 연도 접두 제거
    return t


def scan(folder):
    base = os.path.join(ROOT, folder)
    files = sorted(f for f in os.listdir(base) if f.endswith(".html"))
    rh_names = defaultdict(lambda: defaultdict(set))     # RH → 이름 → 파일
    name_rh = defaultdict(lambda: defaultdict(set))      # 이름 → RH → 파일
    con_rh = defaultdict(lambda: defaultdict(set))       # CON → RH → 파일
    bk_titles = defaultdict(lambda: defaultdict(set))    # BK → 도서명 → 파일
    title_bk = defaultdict(lambda: defaultdict(set))     # 도서명 → BK → 파일
    bk_files = defaultdict(set)
    bk_old = defaultdict(set)                            # 옛 도서 코드 형식 → 파일
    py_old = defaultdict(set)                            # 옛 수취인 코드 → 파일
    obj_rh_names = defaultdict(lambda: defaultdict(set))  # 스크립트 객체: RH → 이름 → 파일
    obj_ct_rh = defaultdict(lambda: defaultdict(set))     # 스크립트 객체: 계약 → RH → 파일
    for f in files:
        raw = open(os.path.join(base, f), encoding="utf-8").read()
        for o in objects(raw):
            sku = re.search(r"""\b(?:sku|productId|id)\s*:\s*["'](""" + BK + r""")["']""", o)
            ttl = re.search(r"""\b(?:title|productName|name)\s*:\s*["']([^"']{4,80})["']""", o)
            if sku and ttl and re.search(r"[가-힣]", ttl.group(1)):
                title = norm_title(ttl.group(1))
                bk_titles[sku.group(1)][title].add(f)
                title_bk[title][sku.group(1)].add(f)
            rid = re.search(RH_KEY + r"""\s*:\s*["'](""" + RH + r""")["']""", o)
            if not rid:
                continue
            nm = re.search(NAME_KEY + r"""\s*:\s*["']([^"']{1,80})["']""", o)
            if nm and lead_name(nm.group(1)):
                obj_rh_names[rid.group(1)][lead_name(nm.group(1))].add(f)
            ct = re.search(CT_KEY + r"""\s*:\s*["'](""" + CT + r""")["']""", o)
            if ct:
                obj_ct_rh[ct.group(1)][rid.group(1)].add(f)
        t = plain(raw)
        for m in re.finditer(NAME + r"\s*\(\s*(" + RH + r")", t):
            if m.group(1) not in NOT_NAME:
                rh_names[m.group(2)][m.group(1)].add(f)
        for m in re.finditer(r"(" + RH + r")\s*\(\s*" + NAME + r"\s*[)·/,]", t):
            if m.group(2) not in NOT_NAME:
                rh_names[m.group(1)][m.group(2)].add(f)
        for code, names in rh_names.items():
            for n, fs in names.items():
                if f in fs:
                    name_rh[n][code].add(f)
        for m in re.finditer(CON, t):
            win = t[max(0, m.start() - 60): m.end() + 60]
            for r in set(re.findall(RH, win)):
                con_rh[m.group(0)][r].add(f)
        for m in re.finditer(BK, t):
            bk_files[m.group(0)].add(f)
        for m in re.finditer(BK_OLD, raw):
            bk_old[m.group(0)].add(f)
        for m in re.finditer(r"\bPY-\d{4}(?:-S\d)?", raw):
            py_old[m.group(0)].add(f)
        for m in re.finditer(BK_REQ, raw):
            if len(m.group(0).rsplit("-", 1)[1]) != 4:
                bk_old[m.group(0)].add(f)
        pats = [
            (r"(" + TITLE_CH + r"{4,40}?)\s*\(\s*(?:ISBN [\d-]+\s*·\s*SKU:\s*)?(" + BK + r")\s*\)", 1, 2),
            (r"(" + BK + r")\s*\(\s*(" + TITLE_CH + r"{4,40}?)\s*[)…]", 2, 1),
            (r"""(?:sku|productId)\s*:\s*["'](""" + BK + r""")["']\s*,\s*(?:title|productName)\s*:\s*["']([^"']{4,60})["']""", 2, 1),
        ]
        for pat, ti, ci in pats:
            for m in re.finditer(pat, t):
                title = norm_title(m.group(ti))
                if len(title) >= 4 and re.search(r"[가-힣]", title):
                    bk_titles[m.group(ci)][title].add(f)
                    title_bk[title][m.group(ci)].add(f)
    return files, rh_names, name_rh, con_rh, bk_titles, title_bk, bk_files, bk_old, py_old, obj_rh_names, obj_ct_rh


def fmt(d):
    return "; ".join(f"`{k}` ({', '.join(sorted(v))})" for k, v in sorted(d.items()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", nargs="?", default="prototype_clean")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    files, rh_names, name_rh, con_rh, bk_titles, title_bk, bk_files, bk_old, py_old, obj_rh_names, obj_ct_rh = scan(args.folder)

    errors, notes = [], []
    for code, names in sorted(rh_names.items()):
        if len(names) > 1:
            errors.append(("권리자 이름 충돌", code, fmt(names)))
    for n, codes in sorted(name_rh.items()):
        if len(codes) > 1:
            errors.append(("같은 이름 · 다른 권리자 코드", n, fmt(codes)))
    for code, rhs in sorted(con_rh.items()):
        if len(rhs) > 1:
            errors.append(("계약 ↔ 권리자 불일치", code, fmt(rhs)))
    for code, names in sorted(obj_rh_names.items()):
        if len(names) > 1:
            errors.append(("권리자 이름 충돌(스크립트 데이터)", code, fmt(names)))
    obj_name_rh = defaultdict(lambda: defaultdict(set))
    for code, names in obj_rh_names.items():
        for n, fs in names.items():
            obj_name_rh[n][code] |= fs
    for n, codes in sorted(obj_name_rh.items()):
        if len(codes) > 1:
            errors.append(("같은 이름 · 다른 권리자 코드(스크립트 데이터)", n, fmt(codes)))
    for code, rhs in sorted(obj_ct_rh.items()):
        if len(rhs) > 1:
            errors.append(("계약 ↔ 권리자 불일치(스크립트 데이터)", code, fmt(rhs)))
    for c in sorted(bk_old):
        errors.append(("도서 코드 형식 불일치", c, "SKU는 PROD-BK-NNNN, 임시코드는 BK-REQ-YYYY-NNNN — " + ", ".join(sorted(bk_old[c]))))
    for c in sorted(py_old):
        errors.append(("옛 수취인 코드", c, "2계층 수취인도 권리자 원장의 RH 코드를 쓴다 — " + ", ".join(sorted(py_old[c]))))
    for title, codes in sorted(title_bk.items()):
        if len(codes) > 1:
            errors.append(("같은 도서명 · 다른 도서 코드", title, fmt(codes)))
    for code, titles in sorted(bk_titles.items()):
        if len(titles) > 1:
            notes.append(("한 도서 코드 · 여러 도서명(약칭 여부 확인)", code, fmt(titles)))

    L = ["# CROSS DATA CHECK REPORT — 화면 간 권리자 · 계약 · 도서 데이터 대조", "",
         f"- 생성: {datetime.datetime.now():%Y-%m-%d %H:%M}",
         f"- 대상: `{args.folder}` ({len(files)}개 파일)",
         f"- 수집: 권리자 코드 {len(rh_names)} · 계약 코드 {len(con_rh)} · 도서 코드 {len(bk_files)} · 스크립트 객체 권리자 {len(obj_rh_names)} · 계약 {len(obj_ct_rh)}",
         f"- 결과: 오류 {len(errors)}건 · 참고 {len(notes)}건", ""]
    for title, rows in (("오류", errors), ("참고", notes)):
        L += [f"## {title} ({len(rows)}건)", ""]
        if rows:
            L += ["| 유형 | 대상 | 내용 (값 · 파일) |", "| :--- | :--- | :--- |"]
            L += [f"| {k} | `{c}` | {v} |" for k, c, v in rows]
        else:
            L.append("없음")
        L.append("")
    L += ["## 권리자 코드별 이름", "", "| 코드 | 이름 (파일) |", "| :--- | :--- |"]
    L += [f"| `{c}` | {fmt(n)} |" for c, n in sorted(rh_names.items())]
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    open(REPORT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"[Skill 3] {args.folder}: 권리자 {len(rh_names)} · 계약 {len(con_rh)} · 도서 {len(bk_files)} | 오류 {len(errors)} · 참고 {len(notes)} → {os.path.relpath(REPORT, ROOT)}")
    if args.strict and errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
