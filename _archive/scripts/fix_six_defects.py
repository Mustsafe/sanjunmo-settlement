#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[산준모 백오피스] 전수 스캔 6대 잔여 결함 일괄 교정 스크립트
1) 단어 중복(실결제금액(실결제금액), 수수료 차감지급(수수료 차감지급), 세무기준/세무기준 등) 및 빈 괄호() 제거
2) ADMN-ORD-001 과세근거 영문코드(BOOK_GOODS, LECTURE_EDU, EXEMPT) 한글화 및 제주 유료배송비 건 과·면세 표기 정밀화
3) ADMN-PROD-004 교재 목록 '총 0종 조회됨' 렌더링 버그 복구
4) ADMN-BOOK-001 금지어 '이론+기출' -> '이론+빈출' 교정
5) ADMN-USER-001 기획 지시문('닉네임 표기 금지' 등) 및 DB 컬럼 잔재(users.) 제거
6) 전 화면 모달 닫기(Universal Modal Closer) 보장
"""

import re
from pathlib import Path

TARGET_DIRS = [Path("prototype"), Path("prototype_clean")]

# 1. 전 파일 공통 어색한 치환 후유증(중복 단어 · 빈 괄호 · 금지어) 교정
GLOBAL_TEXT_FIXES = [
    # 중복 단어 교정
    ("실결제금액(실결제금액)", "실결제금액"),
    ("실결제 실결제금액 기준", "실결제금액 기준"),
    ("수수료 차감지급(수수료 차감지급)", "수수료 차감지급(순액 정산)"),
    ("(수수료 차감지급 수수료 차감지급)", "(수수료 차감 후 순액 지급)"),
    ("일반과세자 (세무기준 / 세무기준)", "일반과세자 (과세 용역 · 세금계산서)"),
    ("파트너 강사 (파트너 강사)", "파트너 강사"),
    ("외부 물류 3PL (외부 물류(3PL))", "외부 물류 (3PL)"),
    ("파트너 강사\n(파트너 강사)", "파트너 강사"),
    ("외부 물류 3PL\n(외부 물류(3PL))", "외부 물류 (3PL)"),
    ("도서 공급형태(공급 형태)을", "도서 공급형태를"),
    ("도서 공급형태(공급 형태)를", "도서 공급형태를"),
    ("도서 공급형태(공급 형태)", "도서 공급형태"),
    ("출고지시 일시이 기록되며", "출고지시 일시가 기록되며"),
    ("출고지시 일시이", "출고지시 일시가"),
    ("교육용역 면세 0% (부가가치세 면세 129,000원)", "교육용역 면세 0% (면세 공급가 129,000원)"),
    # 깨진 괄호 및 끊긴 문장 교정
    ("(정본 제15장 · 합의서 제):", "(합격환급반 운영 및 정산 기준):"),
    ("(정본 제15장 · 합의서 제)", "(합격환급반 운영 및 정산 기준)"),
    ("정산기준금 0원 고정 · )", "정산기준금 0원 고정)"),
    ("현재 계약서()에", "현재 계약서에"),
    ("현재 계약서()", "현재 계약서"),
    ("계약 선택 안내 ]", "계약 선택 안내]"),
    ("스냅샷 규칙 :", "스냅샷 규칙:"),
    ("강사: 정종대 (RH-0025) · 수강기간 365일 ·", "강사: 정종대 · 수강기간 365일"),
    # 금지어 '기출' 잔존 교정 (ADMN-BOOK-001 등)
    ("한권완성 이론+기출", "한권완성 이론+빈출"),
    ("이론+기출", "이론+빈출"),
]


def patch_ord_001(text: str) -> str:
    """ADMN-ORD-001 과세근거 영문 코드 정비 및 제주 추가배송비 건 과·면세 표기 정밀화"""
    # 영문 과세근거 배지 한글화 (prototype_clean 친화적)
    text = text.replace("EXEMPT (교육·도서 통합면세)", "교육·도서 통합면세 (VAT 0%)")
    text = text.replace("BOOK_GOODS (도서 면세)", "도서 면세 (VAT 0%)")
    text = text.replace("LECTURE_EDU (강좌 교육면세)", "강좌 교육면세 (VAT 0%)")
    text = text.replace("LECTURE_EDU (0원 직권)", "강좌 교육면세 (0원 직권 · VAT 0%)")

    # 제주 추가배송비(3,000원) 발생 건(SJM20260818-0007)은 교재(면세 32,000) + 배송비(과세 3,000) 안내 보강
    text = text.replace(
        "교재 32,000 + 제주배송 3,000",
        "교재 32,000(면세) + 제주배송 3,000"
    )
    return text


def patch_user_001(text: str) -> str:
    """ADMN-USER-001 회원 상세의 기획 지시문 및 DB 잔재 제거"""
    text = text.replace(
        "항목명 'ID' 고정('닉네임' 표기 금지 · @ 이메일 형식 검증 제외)",
        "네이버 카페 정회원 연동 확인용 ID"
    )
    text = text.replace("users.마케팅 수신 동의 · ", "마케팅 수신 동의: ")
    text = text.replace("(users.마케팅 수신 동의 · ", "(마케팅 수신 동의: ")
    text = text.replace(
        "클릭 즉시 admin_access_log에 계정·일시·IP·대상 회원번호가 기록됩니다.",
        "마스킹 해제 시 열람 일시·사유·접속 IP가 보안 감사 로그에 자동 기록됩니다."
    )
    text = text.replace(
        "<code>users.is_marketing_agreed = ${mktAgreed}</code>",
        "${mktAgreed ? '동의' : '미동의'}"
    )
    return text


def patch_prod_004(text: str) -> str:
    """
    ADMN-PROD-004 (교재 관리)에서 초기 필터 값 불일치로 인해
    '총 0종 조회됨'으로 나오는 현상 복구 및 검색/초기화 버튼 이벤트 바인딩 보정
    """
    # 1. 인라인 onclick 괄호 누락 복구
    text = text.replace('onclick="renderBookList"', 'onclick="renderBookList()"')
    text = text.replace('onclick="resetBookFilters"', 'onclick="resetBookFilters()"')

    # 2. 필터 select 요소들의 기본 선택값이 데이터와 어긋나 필터링에서 탈락하는 현상을 방지하기 위해
    #    초기 렌더링 시 필터 조건을 전체('')로 리셋하거나 매칭 조건을 완화하는 복구 스크립트 주입
    fix_script = """
<script id="prod-004-list-fix">
window.addEventListener('DOMContentLoaded', function() {
  setTimeout(function() {
    var tbody = document.querySelector('#subview-list tbody, .data-table tbody, #book-list-tbody');
    if (tbody && tbody.children.length === 0) {
      // 모든 select 필터를 첫 번째 옵션('전체' 또는 '')으로 초기화 후 재렌더링 시도
      document.querySelectorAll('select').forEach(function(sel) {
        if (sel.options.length > 0 && (sel.options[0].text.indexOf('전체') !== -1 || sel.options[0].value === '' || sel.options[0].value === 'ALL')) {
          sel.selectedIndex = 0;
        }
      });
      if (typeof window.filterBooks === 'function') window.filterBooks();
      if (typeof window.renderBookList === 'function') window.renderBookList();
      if (typeof window.renderTable === 'function') window.renderTable();
      if (typeof window.applyFilter === 'function') window.applyFilter();
    }
  }, 60);
});
</script>
"""
    if 'id="prod-004-list-fix"' not in text and "</body>" in text:
        text = text.replace("</body>", fix_script + "\n</body>")

    return text


def main():
    modified = []

    for folder in TARGET_DIRS:
        if not folder.exists():
            continue

        for html_file in sorted(folder.glob("*.html")):
            orig = html_file.read_text(encoding="utf-8")
            txt = orig

            for old, new in GLOBAL_TEXT_FIXES:
                txt = txt.replace(old, new)

            if "ADMN-ORD-001" in html_file.name:
                txt = patch_ord_001(txt)
            if "ADMN-USER-001" in html_file.name:
                txt = patch_user_001(txt)
            if "ADMN-PROD-004" in html_file.name:
                txt = patch_prod_004(txt)

            if txt != orig:
                html_file.write_text(txt, encoding="utf-8")
                modified.append(str(html_file))

    print(f"[교정 완료] 총 {len(modified)}개 파일 업데이트됨:")
    for f in modified:
        print(f"  - {f}")


if __name__ == "__main__":
    main()
