#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
ARCHIVE_DOCS = ROOT / "_archive" / "docs"
ARCHIVE_DOCS.mkdir(parents=True, exist_ok=True)

# 1. 파일 이동
# (a) BACKOFFICE_ALIGNMENT_MASTER_PLAN.md -> _archive/docs/
f_backoffice = DOCS / "BACKOFFICE_ALIGNMENT_MASTER_PLAN.md"
if f_backoffice.exists():
    shutil.move(str(f_backoffice), str(ARCHIVE_DOCS / f_backoffice.name))
    print(f"[OK] 아카이브 이동: {f_backoffice.name} -> _archive/docs/")

# (b) SET1_TO_4_ALIGNMENT_PLAN.md -> _archive/docs/
f_set14 = DOCS / "SET1_TO_4_ALIGNMENT_PLAN.md"
if f_set14.exists():
    shutil.move(str(f_set14), str(ARCHIVE_DOCS / f_set14.name))
    print(f"[OK] 아카이브 이동: {f_set14.name} -> _archive/docs/")

# (c) 산준모닷컴 구축 통합 상세 설계서.md (구 원본) -> _archive/docs/산준모닷컴 구축 통합 상세 설계서_v3.2_구원본.md
f_old_orig = DOCS / "산준모닷컴 구축 통합 상세 설계서.md"
f_v4_copy = DOCS / "산준모닷컴 구축 통합 상세 설계서_v4.0_통합본.md"

if f_old_orig.exists() and f_v4_copy.exists():
    dest_old = ARCHIVE_DOCS / "산준모닷컴 구축 통합 상세 설계서_v3.2_구원본.md"
    shutil.move(str(f_old_orig), str(dest_old))
    print(f"[OK] 구 원본 아카이브 이동: {f_old_orig.name} -> {dest_old.name}")

    # (d) 산준모닷컴 구축 통합 상세 설계서_v4.0_통합본.md -> 산준모닷컴 구축 통합 상세 설계서.md (정식 대표 명칭으로 교체)
    shutil.move(str(f_v4_copy), str(f_old_orig))
    print(f"[OK] v4.0 통합본을 대표 정본으로 확정: {f_old_orig.name}")

    # 헤더 내 SET1_TO_4_ALIGNMENT_PLAN 경로를 _archive/docs/로 갱신
    txt = f_old_orig.read_text(encoding="utf-8")
    txt = txt.replace("docs/SET1_TO_4_ALIGNMENT_PLAN.md", "_archive/docs/SET1_TO_4_ALIGNMENT_PLAN.md")
    f_old_orig.write_text(txt, encoding="utf-8")
    print("[OK] 대표 정본 내 플랜 참조 경로 최신화 완료")

# 2. README.md 라우팅 테이블 갱신
readme = ROOT / "README.md"
if readme.exists():
    r = readme.read_text(encoding="utf-8")
    orig_r = r

    # 기존 두 줄 및 하단 중복 한 줄 치환
    target_block = """| **Set 1~4 통합설계서 & 프로토타입 플랜** | `docs/SET1_TO_4_ALIGNMENT_PLAN.md` · `docs/산준모닷컴 구축 통합 상세 설계서_v4.0_통합본.md` | **Set 1~4 기준 통합 상세 설계서 재구조화(사본) 및 프로토타입 전수 정합성 체크리스트·상태값 관리 (최우선 참조)** |
| **백오피스 정합성 검토 플랜** | `docs/BACKOFFICE_ALIGNMENT_MASTER_PLAN.md` | **전수 비즈니스 정합성 검토 12단계(Phase 1-A ~ 5-C) 진행 상태 및 체크리스트 (세션 핸드오프 시 최우선 열람)** |"""

    new_block = """| B2C 통합 상세 설계서 | `docs/산준모닷컴 구축 통합 상세 설계서.md` | **B2C 프론트/백오피스 전 세트(Set 1~4) 3장 단일 체제 통합 상세 설계서 (v4.0 완결 정본 · [표 5.1-A] PG/3PL/환불/정산 포함)** |
| 정합성 검토 완료 아카이브 | `_archive/docs/SET1_TO_4_ALIGNMENT_PLAN.md` · `_archive/docs/BACKOFFICE_ALIGNMENT_MASTER_PLAN.md` | Set 1~4 통폐합 플랜 및 백오피스 정합성 12단계 전수 검토 완료 히스토리 아카이브 |"""

    if target_block in r:
        r = r.replace(target_block, new_block)
        # 하단 중복 줄 제거
        dup_line = "| B2C 통합 상세 설계서 | docs/산준모닷컴 구축 통합 상세 설계서.md | B2C 프론트/백오피스 전 세트(회원·강좌·교재·장바구니·3PL 배송·환불·CS·알림톡) 및 [표 5.1-A] PG·결제수단 마스터 기준표 |\n"
        r = r.replace(dup_line, "")
        readme.write_text(r, encoding="utf-8")
        print("[OK] README.md 라우팅 테이블 갱신 완료")

# 3. sync_to_gdrive.ps1 내 obsoleteDocs에 v4.0_통합본 추가
sync_script = ROOT / "sync_to_gdrive.ps1"
if sync_script.exists():
    s = sync_script.read_text(encoding="utf-8")
    if "산준모닷컴 구축 통합 상세 설계서_v4.0_통합본.md" not in s:
        s = s.replace(
            '"04_QA_정산케이스스펙_및_회귀테스트_법령근거_v4.0.0.md"',
            '"04_QA_정산케이스스펙_및_회귀테스트_법령근거_v4.0.0.md",\r\n    "산준모닷컴 구축 통합 상세 설계서_v4.0_통합본.md",\r\n    "SET1_TO_4_ALIGNMENT_PLAN.md",\r\n    "BACKOFFICE_ALIGNMENT_MASTER_PLAN.md"'
        )
        sync_script.write_text(s, encoding="utf-8")
        print("[OK] sync_to_gdrive.ps1 구글 드라이브 정리 목록 최신화 완료")

print("[DONE] docs 아카이빙 및 파일명 재구조화 완료!")
