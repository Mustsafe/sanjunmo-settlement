#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
update_book_discount_policy.py
- 도서정가제 내 도서 기본 할인율 허용: 0% 고정 -> 최대 10% 한도 (정가 취소선 + 할인가 노출)
- 쿠폰 사용 불가 / 포인트 사용 불가 / 포인트 적립 불가(0%) 하드락 유지
- 인세, 정산(개발지원금·패키지 안분), 무료배송(30,000원 기준) 판정: 모두 '실결제액(할인 후 실판매가)' 기준
- 위탁도서(CONSIGNMENT) 정산 모수: 계약원장(ADMN-INST-001) 및 도서공급원장(ADMN-BOOK-001)에서 [실결제액 기준 vs 정가 기준] 선택 가능하도록 반영
- 대상: docs/ 하위 마크다운 정본 전체 + prototype/ 및 prototype_clean/ 양쪽 동기화
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
DOCS_DIR = ROOT / "docs"
TARGET_PROTO_DIRS = [ROOT / "prototype", ROOT / "prototype_clean"]


def patch_markdown_docs():
    updated_files = []

    # 1. 루트 README.md 패치
    readme_path = ROOT / "README.md"
    if readme_path.exists():
        txt = readme_path.read_text(encoding="utf-8")
        orig = txt
        txt = re.sub(
            r"실물 교재\(BOOK,\s*면세\):\s*산준모 기본 할인 0%,\s*쿠폰·포인트 할인 배분 0원,\s*포인트 적립 0% 하드락\.",
            "실물 교재(BOOK, 면세): 도서정가제 범위 내 상품 기본 할인 최대 10% 허용(정가 취소선 + 할인가 노출), 추가 쿠폰·포인트 사용 0원 및 포인트 적립 0% 하드락. 인세·정산·무료배송(30,000원↑) 판정은 모두 할인 후 실결제액 기준(단, 위탁도서는 계약원장에서 실결제액/정가 기준 선택).",
            txt,
        )
        txt = txt.replace("기본 할인 0%", "기본 할인 최대 10%(쿠폰·포인트 추가할인 0%)")
        if txt != orig:
            readme_path.write_text(txt, encoding="utf-8")
            updated_files.append(str(readme_path.relative_to(ROOT)))

    # 2. docs/ 내 마크다운 문서 일괄 패치
    md_files = list(DOCS_DIR.rglob("*.md"))
    for md in md_files:
        txt = md.read_text(encoding="utf-8")
        orig = txt

        # (A) 도서 할인율 상한 파라미터 및 정책 문구 변경 (02권, 03권 등)
        txt = re.sub(
            r"도서 할인율 상한\(`?book_discount_rate_limit`?\)\s*=\s*\*\*0%\*\*",
            "도서 할인율 상한(`book_discount_rate_limit`) = **10%** (도서정가제 가격할인 한도)",
            txt,
        )
        txt = re.sub(
            r"`book_discount_rate_limit`\s*\|\s*`0`",
            "`book_discount_rate_limit` | `10`",
            txt,
        )
        txt = txt.replace(
            "도서 할인율 상한 및 도서 포인트 적립율 상한 = 0%는 법정 상한(10%/15%)보다 좁게 설정한 내부 정책이며",
            "도서 기본 할인율 상한 = 10%(정가 대비 최대 10% 가격할인 허용) 및 도서 쿠폰·포인트 사용/적립 상한 = 0%는 도서정가제(가격할인 10% 이내)를 준수하기 위한 내부 정책이며",
        )
        txt = txt.replace(
            "교재 실결제액 = 교재 정가",
            "교재 실결제액 = 교재 실판매가(정가 대비 최대 10% 이내 할인가, 쿠폰·포인트 추가할인 0원)",
        )
        txt = txt.replace(
            "교재 실결제액 \\= 교재 정가",
            "교재 실결제액 \\= 교재 실판매가(정가 대비 최대 10% 이내 할인가, 쿠폰·포인트 추가할인 0원)",
        )
        txt = txt.replace(
            "순수 강좌 결제 풀 = 전체 실결제액 − 교재 정가 합계 − 배송비",
            "순수 강좌 결제 풀 = 전체 실결제액 − 교재 실결제액(할인 판매가) 합계 − 배송비",
        )
        txt = txt.replace(
            "순수 강좌 결제 풀 \\= 전체 실결제액 − 교재 정가 합계 − 배송비",
            "순수 강좌 결제 풀 \\= 전체 실결제액 − 교재 실결제액(할인 판매가) 합계 − 배송비",
        )
        txt = txt.replace(
            "교재(면세, 정가 고정)",
            "교재(면세, 최대 10% 기본할인 허용 · 쿠폰/포인트 차단)",
        )
        txt = txt.replace(
            "도서정가제 준수를 위한 당사 정책에 따라 교재 금액에는 할인과 적립이 적용되지 않으며",
            "도서정가제 준수를 위한 당사 정책에 따라 교재 금액에는 상품 기본 할인(최대 10%) 외 추가 쿠폰·포인트 할인과 적립이 적용되지 않으며",
        )

        # (B) 인세 및 위탁 정산 기준가 정책 명시 (01권 제6장, BACKOFFICE_ALIGNMENT_MASTER_PLAN 등)
        txt = txt.replace(
            "정가 기준 인세율",
            "실결제액(할인 판매가) 기준 인세율",
        )
        txt = txt.replace(
            "도서 정가(`list_price`)에 계약 인세율을 곱하여",
            "도서 실결제액(`sale_price`, 최대 10% 기본할인 적용 후 실판매가)에 계약 인세율을 곱하여(단, 위탁도서는 계약원장의 정산기준가 설정에 따라 실결제액 또는 정가 적용)",
        )

        if txt != orig:
            md.write_text(txt, encoding="utf-8")
            updated_files.append(str(md.relative_to(ROOT)))

    return updated_files


def patch_html_prototypes():
    patched_htmls = []

    for proto_dir in TARGET_PROTO_DIRS:
        if not proto_dir.exists():
            continue

        # 1. ADMN-PROD-004 (교재 관리: 정가 + 할인율 0~10% + 실판매가 구조 반영)
        prod004 = proto_dir / "ADMN-PROD-004_baseline.html"
        if prod004.exists():
            h = prod004.read_text(encoding="utf-8")
            orig = h
            h = h.replace("정가 (=면세 판매가)", "도서 정가 / 할인율(최대 10%) / 실판매가(면세)")
            h = h.replace("도서정가제 0% 할인 고정", "도서정가제 기본할인 최대 10% 허용 (추가 쿠폰·포인트 차단)")
            h = h.replace("할인 0% 고정", "기본할인 0~10% (정가 취소선 노출)")

            # 도서 할인율 10% 한도 검증 스크립트 주입 (없는 경우)
            if "book-discount-limit-guard" not in h and "</body>" in h:
                guard_script = """
<!-- book-discount-limit-guard -->
<script>
(function(){
  document.addEventListener('input', function(e){
    var el = e.target;
    if (!el) return;
    if (el.id === 'f-book-discount-rate' || el.name === 'book_discount_rate') {
      var v = parseFloat(el.value || '0');
      if (v > 10) {
        alert('출판문화산업진흥법(도서정가제) 및 당사 정책에 따라 도서 기본 할인율은 최대 10%까지만 입력할 수 있습니다.');
        el.value = 10;
      } else if (v < 0) {
        el.value = 0;
      }
      var listPriceEl = document.getElementById('f-book-list-price');
      var salePriceEl = document.getElementById('f-book-sale-price');
      if (listPriceEl && salePriceEl) {
        var lp = parseFloat((listPriceEl.value || '0').replace(/,/g, '')) || 0;
        var rate = parseFloat(el.value || '0') || 0;
        var sp = Math.floor(lp * (100 - rate) / 100);
        salePriceEl.value = sp.toLocaleString('ko-KR');
      }
    }
  });
})();
</script>
"""
                h = h.replace("</body>", guard_script + "\n</body>")

            if h != orig:
                prod004.write_text(h, encoding="utf-8")
                patched_htmls.append(str(prod004.relative_to(ROOT)))

        # 2. ADMN-BOOK-001 (도서 공급 원장: 실결제액 인세 기준 + 위탁도서 계약기준가 선택 옵션)
        book001 = proto_dir / "ADMN-BOOK-001_baseline.html"
        if book001.exists():
            h = book001.read_text(encoding="utf-8")
            orig = h
            h = h.replace("현행 정가 (면세)", "정가 / 실판매가(최대 10%↓ · 면세)")
            h = h.replace("정가 (판매가)", "도서 정가 / 할인 후 실판매가(실결제액)")
            h = h.replace("정가 대비", "실결제액 대비 (위탁은 계약기준 선택)")
            h = h.replace(
                "권당 22,800원 (이익률 60.0%) = 정가 38,000원 - 제조원가 11,400원(30%) - 저자인세 3,800원(10%)",
                "권당 20,520원 (실결제액 기준 이익률 60.0%) = 실결제액 34,200원(정가 38,000원·10%↓) - 제조원가 10,260원(30%) - 저자인세 3,420원(실결제액의 10%)"
            )
            h = h.replace(
                "수수료율 <code>30%</code> (<code>VAT_INCLUDED</code>) · 정산 기준 등식 적용",
                "수수료율 <code>30%</code> (<code>VAT_INCLUDED</code>) · 정산모수: 계약원장 선택(<code>실결제액 기준</code> / <code>정가 기준</code>)"
            )
            if h != orig:
                book001.write_text(h, encoding="utf-8")
                patched_htmls.append(str(book001.relative_to(ROOT)))

        # 3. ADMN-INST-001 (권리자 계약 원장: 위탁도서 정산 모수 선택 옵션 명시)
        inst001 = proto_dir / "ADMN-INST-001_baseline.html"
        if inst001.exists():
            h = inst001.read_text(encoding="utf-8")
            orig = h
            h = h.replace("도서 정가 기준 인세", "도서 실결제액(할인 판매가) 기준 인세 (위탁도서는 실결제액/정가 계약별 선택)")
            if h != orig:
                inst001.write_text(h, encoding="utf-8")
                patched_htmls.append(str(inst001.relative_to(ROOT)))

        # 4. ADMN-PROD-005 (패키지 구성: 도서정가제 할인 0% 문구 -> 최대 10% 할인가 적용)
        prod005 = proto_dir / "ADMN-PROD-005_baseline.html"
        if prod005.exists():
            h = prod005.read_text(encoding="utf-8")
            orig = h
            h = h.replace(
                "(C) 포함 교재 결제액 (도서 면세 · 도서정가제 할인 0%)",
                "(C) 포함 교재 실결제액 (도서 면세 · 도서 기본할인 최대 10% 적용 · 추가 쿠폰/포인트 차단)"
            )
            h = h.replace(
                "도서정가제 0% 고정 (환급 대상 제외)",
                "정가 80,000원 → 10% 할인가 72,000원 (쿠폰·포인트 추가할인 제외 / 환급 모수 제외)"
            )
            h = h.replace("정가 (=면세 결제액)", "도서 정가 / 실판매가(최대 10%↓)")
            if h != orig:
                prod005.write_text(h, encoding="utf-8")
                patched_htmls.append(str(prod005.relative_to(ROOT)))

        # 5. ADMN-PROM-001 & ADMN-PROM-002 & ADMN-ORD-001
        for fname in ["ADMN-PROM-001_baseline.html", "ADMN-PROM-002_baseline.html", "ADMN-ORD-001_baseline.html"]:
            fpath = proto_dir / fname
            if fpath.exists():
                h = fpath.read_text(encoding="utf-8")
                orig = h
                h = h.replace(
                    "쿠폰·포인트 할인이 상시 차단(🔒 고정)됩니다.",
                    "상품 기본 할인(최대 10%)만 허용되며, 추가 쿠폰·포인트 사용 및 적립은 상시 차단(🔒 고정)됩니다."
                )
                h = h.replace(
                    "교재 합계 30,000원↑ 무료",
                    "실물 교재·상품 실결제액 합계 30,000원↑ 무료"
                )
                if h != orig:
                    fpath.write_text(h, encoding="utf-8")
                    patched_htmls.append(str(fpath.relative_to(ROOT)))

    return patched_htmls


if __name__ == "__main__":
    md_res = patch_markdown_docs()
    html_res = patch_html_prototypes()
    print(f"[DONE] Markdown updated ({len(md_res)} files):")
    for m in md_res:
        print("  -", m)
    print(f"[DONE] HTML Prototypes updated ({len(html_res)} files):")
    for p in html_res:
        print("  -", p)
