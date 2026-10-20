#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
readme = ROOT / "README.md"
COPY_SPEC = DOCS / "산준모닷컴 구축 통합 상세 설계서_v4.0_통합본.md"

# 1. README.md 라우팅 포인터 반영
if readme.exists():
    r_txt = readme.read_text(encoding="utf-8")
    if "SET1_TO_4_ALIGNMENT_PLAN.md" not in r_txt:
        anchor = "| **백오피스 정합성 검토 플랜** |"
        new_line = "| **Set 1~4 통합설계서 & 프로토타입 플랜** | `docs/SET1_TO_4_ALIGNMENT_PLAN.md` · `docs/산준모닷컴 구축 통합 상세 설계서_v4.0_통합본.md` | **Set 1~4 기준 통합 상세 설계서 재구조화(사본) 및 프로토타입 전수 정합성 체크리스트·상태값 관리 (최우선 참조)** |\n"
        if anchor in r_txt:
            r_txt = r_txt.replace(anchor, new_line + anchor, 1)
            readme.write_text(r_txt, encoding="utf-8")
            print("[OK] README.md 라우팅 포인터 반영 완료")

# 2. 통합 상세 설계서 사본(v4.0_통합본) 최상단에 AI 구조화 편집 절대 규칙 헤더 주입
if COPY_SPEC.exists():
    c_txt = COPY_SPEC.read_text(encoding="utf-8")
    if "[AI 에이전트 문서 편집 및 구조화 절대 규칙 (필독 거버넌스)]" not in c_txt:
        ai_header = """# 산준모 B2C 플랫폼 통합 상세 설계서 (v4.0 통합본)

> **[AI 에이전트 문서 편집 및 구조화 절대 규칙 (필독 거버넌스)]**
> 1. **하단 신규 장(Chapter 4·5 등) 덧붙이기(Append) 절대 금지:**
>    - 본 문서는 `제1장(프로젝트 개요)` ➔ `제2장(공통 알림 메시지 발송 체계)` ➔ `제3장(Set 1 ~ Set 4 수직 릴리즈 통합 상세 설계)`의 **3장 단일 체제**로 통합 운영합니다.
>    - 향후 정책 변경·피드백 반영·보정 사항이 발생하더라도 문서 하단에 별도 장(제4장, 제5장 등)으로 이어 붙이지 말고, 반드시 해당하는 **`3.1 [Set 1] ~ 3.4 [Set 4]` 내부 섹션에 인라인(In-line) 병합**하십시오.
> 2. **Set 1 ~ Set 4 내부 표준 3단 템플릿 준수:**
>    - 각 Set(`3.1` ~ `3.4`)는 반드시 아래 3단 구조를 유지하여 작성·수정합니다:
>      - **`[A] 프론트엔드(USER-*) ↔ 백오피스(ADMN-*) 1:1 페어 매핑표`**
>      - **`[B] 화면별 상세 데이터 필드 및 입출력/모달 제어 명세`**
>      - **`[C] 세트 핵심 비즈니스 정책 및 하드락 가드레일 (정산 5권 SSOT 연동)`**
> 3. **상위 정본(SSOT) 위계 및 마스터 플랜 동기화:**
>    - 정산·세무·계약·도서 공급과 관련된 수식 및 규칙은 `docs/[산준모 정산시스템]_00~04.md`가 1순위 절대 정본입니다.
>    - 본 문서의 각 Set 업데이트 및 프로토타입 검증 진행 상태는 반드시 `docs/SET1_TO_4_ALIGNMENT_PLAN.md`의 체크리스트와 동기화하십시오.

---
"""
        first_line_target = "# 산준모 B2C 플랫폼 통합 상세 설계서 (v3.2.0)"
        if first_line_target in c_txt:
            c_txt = c_txt.replace(first_line_target, ai_header.strip(), 1)
        else:
            c_txt = ai_header + c_txt
        COPY_SPEC.write_text(c_txt, encoding="utf-8")
        print(f"[OK] {COPY_SPEC.name} 상단 AI 구조화 거버넌스 헤더 삽입 완료")
