#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
DOCS_DIR = ROOT / "docs"
TARGET_PROTO_DIRS = [ROOT / "prototype", ROOT / "prototype_clean"]

def sync_all_markdown():
    changed = []
    all_mds = [ROOT / "README.md"] + sorted(DOCS_DIR.rglob("*.md"))

    for md in all_mds:
        if not md.exists():
            continue
        txt = md.read_text(encoding="utf-8")
        orig = txt

        # 1. 도서정가제 0% 고정 -> 최대 10% 기본할인 허용 (정가 취소선 + 할인가 노출)
        txt = re.sub(r"도서정가제\s*할인\s*0%\s*고정", "도서정가제 기본할인 최대 10% 허용(추가 쿠폰·포인트 0% 고정)", txt)
        txt = re.sub(r"도서정가제\s*0%\s*할인\s*고정", "도서정가제 기본할인 최대 10% 허용(추가 쿠폰·포인트 0% 고정)", txt)
        txt = re.sub(r"도서정가제\s*0%\s*고정", "도서정가제 기본할인 최대 10% 이내(추가 혜택 차단)", txt)
        txt = re.sub(r"할인\s*0%\s*고정", "기본할인 최대 10%(쿠폰·포인트 0% 고정)", txt)
        txt = re.sub(r"정가\s*100%\s*고정", "정가 대비 최대 10% 기본할인 허용(추가 쿠폰·포인트 차단)", txt)

        # 2. 인세 및 정산 모수: 정가 기준 -> 실결제액(할인 판매가) 기준, 위탁은 계약원장 선택
        txt = txt.replace("교재 인세 10%(정가 기준)", "교재 인세 10%(실결제액 기준)")
        txt = txt.replace("인세율(정가 기준)", "인세율(실결제액 기준)")
        txt = txt.replace("정가 기준 인세", "실결제액(할인 판매가) 기준 인세")
        txt = txt.replace(
            "당월 확정 판매 부수 × 기준가",
            "당월 확정 판매 실결제액 합계(할인 후 실판매가 기준, 위탁도서는 계약원장 선택 기준가 적용)"
        )
        txt = re.sub(
            r"도서\s*정가\s*기준으로\s*산정",
            "도서 실결제액(최대 10% 기본할인 적용 후 실판매가) 기준으로 산정(단, 위탁도서는 계약원장에서 실결제액/정가 기준 선택)",
            txt
        )

        # 3. 01권 제6장 / 03권 데이터 사전 / 통합 상세 설계서 보강용 명시적 정책 블록 주입
        if "01_비즈니스정책_계약_도서_이월_기획서.md" in md.name and "consignment_base_price_type" not in txt:
            target_anchor = "## **제6장."
            policy_callout = (
                "> **[도서 가격할인(최대 10%) 및 정산·무료배송 기준가 확정 정책]**\n"
                "> 1. **도서 기본 할인 허용(0~10%):** 교재 등록(`ADMN-PROD-004`) 및 도서 공급원장(`ADMN-BOOK-001`)에서 도서 정가(`list_price`) 대비 **최대 10%까지 기본 할인율(`book_discount_rate`, 0~10%)**을 설정할 수 있으며, 프론트에는 정가(취소선)와 할인가(실판매가 `sale_price`)를 함께 노출합니다. 단, 추가 쿠폰 적용·포인트 사용·포인트 적립은 0%로 상시 하드락합니다.\n"
                "> 2. **인세·개발지원금·패키지 안분·무료배송(30,000원↑) 판정 모수:** 자사발행 도서 인세(`Pipeline 2.1`), 자사저작권 도서 개발지원금 모수(`Pipeline 5.1`), 복합 패키지 교재 분리 금액, 무료배송(30,000원 이상) 판정은 모두 **할인 후 실결제액(`sale_price`)**을 기준으로 산정합니다.\n"
                "> 3. **위탁도서(`CONSIGNMENT`) 계약별 정산 기준가 선택:** 위탁도서(`Pipeline 2.2`)는 출판사별 계약 조건에 따라 권리자 계약 원장(`ADMN-INST-001`) 및 도서 공급원장(`ADMN-BOOK-001`)에서 정산 기준가(`consignment_base_price_type`)를 **`실결제액(할인 판매가) 기준 [기본값]`** 또는 **`도서 정가 기준`** 중 선택하여 적용합니다.\n\n"
            )
            if target_anchor in txt:
                txt = txt.replace(target_anchor, policy_callout + target_anchor, 1)

        if "03_백오피스화면_외부연동_및_데이터사전.md" in md.name and "consignment_base_price_type" not in txt:
            dict_anchor = "| 가격 결정 주체 | price\\_owner |"
            new_row = (
                "| 위탁 정산 기준가 구분 | consignment\\_base\\_price\\_type | 위탁도서 정산 모수 기준 (실결제액 기준: PAID\\_AMOUNT [기본값] / 도서 정가 기준: LIST\\_PRICE, 계약원장 선택) |\n"
                "| 도서 기본 할인율 | book\\_discount\\_rate | 도서 정가 대비 기본 할인율 (0~10% 정수, 도서정가제 상한 10% 하드락) |\n"
            )
            if dict_anchor in txt:
                txt = txt.replace(dict_anchor, new_row + dict_anchor, 1)

        if "산준모닷컴 구축 통합 상세 설계서.md" in md.name and "최대 10% 기본 할인" not in txt:
            txt = txt.replace(
                "법적 도서정가제 준수를 위해 교재 가격 상당 분에 대한 혜택 적용 차단 정책 사전 노출.",
                "도서정가제 범위 내 도서 기본 할인(최대 10%, 정가 취소선 + 할인가 노출)만 적용되며, 추가 쿠폰·포인트 사용 및 적립(0%)은 차단됨을 사전 노출. 무료배송(30,000원↑) 및 정산은 할인 후 실결제액 기준 적용."
            )

        if txt != orig:
            md.write_text(txt, encoding="utf-8")
            changed.append(str(md.relative_to(ROOT)))

    return changed

def sync_all_prototypes():
    changed = []
    for pdir in TARGET_PROTO_DIRS:
        if not pdir.exists():
            continue

        for html_file in sorted(pdir.glob("*.html")):
            h = html_file.read_text(encoding="utf-8")
            orig = h

            h = h.replace("(도서정가제 할인 0%)", "(최대 10% 기본할인 · 쿠폰/포인트 제외)")
            h = h.replace("도서정가제 할인 0% 고정", "도서 기본할인 최대 10% (쿠폰·포인트 0% 고정)")
            h = h.replace("도서 정가 (할인 0%)", "도서 정가 / 실판매가(최대 10%↓)")
            h = h.replace("원 (면세 · 할인 0%)", "원 (면세 · 최대 10% 기본할인 반영 실결제액)")

            if html_file.name == "ADMN-INST-001_baseline.html":
                h = h.replace(
                    "`CON-2026-001` (인세 10%)",
                    "`CON-2026-001` (인세 10% · 실결제액 기준)"
                )
                h = h.replace(
                    "CON-2026-001 (인세 10%)",
                    "CON-2026-001 (인세 10% · 실결제액 기준)"
                )
                if "consignment-base-price-selector" not in h:
                    marker = "권리자별 상품(강의 · 도서 SKU) 1계층 매핑 현황"
                    inject_ui = (
                        "권리자별 상품(강의 · 도서 SKU) 1계층 매핑 현황 "
                        "<span id=\"consignment-base-price-selector\" style=\"display:inline-flex;align-items:center;gap:8px;margin-left:12px;font-size:12px;font-weight:600;color:#1e40af;background:#eff6ff;border:1px solid #bfdbfe;padding:3px 10px;border-radius:6px;\">"
                        "📚 도서 정산 모수 정책: 자사발행 인세 = <strong>실결제액(최대 10% 할인가) 기준 고정</strong> · "
                        "위탁도서(CONSIGNMENT) 계약 기준가 = "
                        "<label style=\"cursor:pointer;\"><input type=\"radio\" name=\"consign_base_type\" value=\"PAID_AMOUNT\" checked /> 실결제액 기준(기본)</label> "
                        "<label style=\"cursor:pointer;\"><input type=\"radio\" name=\"consign_base_type\" value=\"LIST_PRICE\" /> 도서 정가 기준</label>"
                        "</span>"
                    )
                    h = h.replace(marker, inject_ui, 1)

            if h != orig:
                html_file.write_text(h, encoding="utf-8")
                changed.append(str(html_file.relative_to(ROOT)))

    return changed

if __name__ == "__main__":
    md_updated = sync_all_markdown()
    html_updated = sync_all_prototypes()
    print(f"[DONE] Markdown files updated ({len(md_updated)}):", md_updated)
    print(f"[DONE] HTML prototype files updated ({len(html_updated)}):", html_updated)
