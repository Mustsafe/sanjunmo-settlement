# PAREN_FIX_SRC 리포트

## 1. prototype_clean/common-snb.js 에서 TEXT_REPLACEMENTS, REGEX_CLEANERS, EXTRA_MAP 적용 함수 및 호출 줄

### 1-1. TEXT_REPLACEMENTS 및 REGEX_CLEANERS 적용 함수: `transformText`

**함수 전체 원문 (prototype_clean/common-snb.js L371~L384):**
```javascript
371:   function transformText(str) {
372:     if (!str || typeof str !== "string" || !str.trim()) return str;
373:     let out = str;
374:     for (let i = 0; i < TEXT_REPLACEMENTS.length; i++) {
375:       const target = TEXT_REPLACEMENTS[i][0];
376:       if (out.indexOf(target) !== -1) {
377:         out = out.split(target).join(TEXT_REPLACEMENTS[i][1]);
378:       }
379:     }
380:     for (let j = 0; j < REGEX_CLEANERS.length; j++) {
381:       out = out.replace(REGEX_CLEANERS[j], "");
382:     }
383:     return out;
384:   }
```

**`transformText` 를 호출하는 줄:**
- prototype_clean/common-snb.js:401: `const cleaned = transformText(orig);`
- prototype_clean/common-snb.js:407: `const ct = transformText(document.title);`

**참조: DOM 순회 및 호출 함수 `walkAndClean` 및 실행 등록부 (L386~L430):**
```javascript
386:   function walkAndClean(root) {
387:     if (!root) return;
388:     const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false);
389:     const textNodes = [];
390:     let node;
391:     while ((node = walker.nextNode())) {
392:       const p = node.parentNode;
393:       if (!p) continue;
394:       const tag = p.tagName;
395:       // 코드/스타일/입력창 내부 텍스트는 절대 건드리지 않음
396:       if (tag === "SCRIPT" || tag === "STYLE" || tag === "TEXTAREA" || tag === "CODE" && p.classList.contains("raw-keep")) continue;
397:       textNodes.push(node);
398:     }
399:     for (let i = 0; i < textNodes.length; i++) {
400:       const orig = textNodes[i].nodeValue;
401:       const cleaned = transformText(orig);
402:       if (cleaned !== orig) {
403:         textNodes[i].nodeValue = cleaned;
404:       }
405:     }
406:     if (document.title) {
407:       const ct = transformText(document.title);
408:       if (ct !== document.title) document.title = ct;
409:     }
410:   }

412:   function startSafeCleaner() {
413:     walkAndClean(document.body);
414:     let pending = false;
415:     const obs = new MutationObserver(function () {
416:       if (pending) return;
417:       pending = true;
418:       requestAnimationFrame(function () {
419:         pending = false;
420:         walkAndClean(document.body);
421:       });
422:     });
423:     obs.observe(document.body, { childList: true, subtree: true });
424:   }
425: 
426:   if (document.readyState === "loading") {
427:     document.addEventListener("DOMContentLoaded", startSafeCleaner);
428:   } else {
429:     startSafeCleaner();
430:   }
```

---

### 1-2. EXTRA_MAP 적용 함수: `cleanString`

**함수 전체 원문 (prototype_clean/common-snb.js L629~L637):**
```javascript
629:   function cleanString(str) {
630:     if (!str || typeof str !== 'string') return str;
631:     let out = str;
632:     for (const [k, v] of Object.entries(EXTRA_MAP)) {
633:       if (out.includes(k)) out = out.split(k).join(v);
634:     }
635:     out = out.replace(MARKER_RE, '').replace(CIRCLED_RE, '').replace(TRACK_RE, '');
636:     return out;
637:   }
```

**`cleanString` 을 호출하는 줄:**
- prototype_clean/common-snb.js:646: `const cleaned = cleanString(node.nodeValue);`
- prototype_clean/common-snb.js:654: `const cleaned = cleanString(val);`

**참조: DOM 순회 함수 `runEnhancedClean` 및 실행 등록부 (L639~L670):**
```javascript
639:   function runEnhancedClean(root) {
640:     if (!root) return;
641:     const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false);
642:     let node;
643:     while ((node = walker.nextNode())) {
644:       const parentTag = node.parentNode && node.parentNode.tagName;
645:       if (parentTag === 'SCRIPT' || parentTag === 'STYLE') continue;
646:       const cleaned = cleanString(node.nodeValue);
647:       if (cleaned !== node.nodeValue) node.nodeValue = cleaned;
648:     }
649:     if (root.querySelectorAll) {
650:       root.querySelectorAll('[placeholder],[title],[data-tooltip]').forEach(el => {
651:         ['placeholder', 'title', 'data-tooltip'].forEach(attr => {
652:           const val = el.getAttribute(attr);
653:           if (val) {
654:             const cleaned = cleanString(val);
655:             if (cleaned !== val) el.setAttribute(attr, cleaned);
656:           }
657:         });
658:       });
659:     }
660:   }

662:   document.addEventListener('DOMContentLoaded', () => {
663:     runEnhancedClean(document.body);
664:     let timer = null;
665:     const observer = new MutationObserver(() => {
666:       if (timer) clearTimeout(timer);
667:       timer = setTimeout(() => runEnhancedClean(document.body), 80);
668:     });
669:     observer.observe(document.body, { childList: true, subtree: true });
670:   });
```


---

## 2. prototype_clean/common-snb.js 의 REGEX_CLEANERS 배열 전체 원문 (L351~L369)

```javascript
351:   const REGEX_CLEANERS = [
352:     // [ADMN-...] 또는 [Term-...] 또는 [테이블 A~G] 또는 [8.3절...] 대괄호 태그 제거
353:     /\[\s*(?:ADMN-[A-Z]+-\d+[^\]]*|Term-[A-Z]+|테이블\s*[A-G]|(?:제?\d+장|\d+(?:\.\d+)?절|부록)[^\]]*)\]\s*/g,
354:     // (ADMN-...), (SETT-001), (001-P1), (S1), (P2) 등 화면코드 괄호 제거
355:     /\s*\(\s*(?:ADMN-|USER-)?(?:SETT|INST|BOOK|PROD|ORD|RFD|USER|PROM|BRD|CONF|DASH|STAT|CRS|MY|FREE|LECT)-\d+(?:-[A-Z0-9]+)?[^)]*\)/g,
356:     /\s*\(\s*(?:\d{3}-[SP]\d+|[SP]\d+)\s*\)/g,
357:     // (6.5절 · 8.3절), (제15장 15.2절), (Case 7), (부록 D-15) 등 기획서 장/절/케이스 괄호 제거
358:     /\s*\(\s*(?:합의서\s*)?(?:제?\d+장\s*)?\d+(?:\.\d+)?절[^)]*\)/g,
359:     /\s*·\s*\d+(?:\.\d+)?절/g,
360:     /\s*\(\s*(?:Case\s*\d+[^)]*|부록\s*[A-Z][^)]*|QA\s*D-\d+[^)]*)\)/gi,
361:     // (member_status), (goods_stock_log), (own_copyright_yn) 등 영문 snake_case DB 컬럼 괄호 제거
362:     /\s*\(\s*[a-z]+_[a-z0-9_]+(?:\s*=\s*[^)]+)?\s*\)/g,
363:     // Table: xxx 배지 텍스트 제거
364:     /^\s*Table:\s*[a-z0-9_]+\s*$/i,
365:     // 잔여 화면코드 접두사 및 기술 코드 제거
366:     /\b(?:ADMN|USER)-[A-Z]+-\d+(?:-[A-Z0-9]+)?\b/g,
367:     /\bROLE_[A-Z0-9_]+\b/g,
368:     /\b[a-z]+_(?:yn|type|status|mode|limit|flag|scope)\b/g
369:   ];
```

---

## 3. PAREN_DUP_SCAN.md 의 "## prototype —" 제목부터 파일 끝까지 원문

## prototype — 6건

| 파일 | 앞말 | 괄호 안 | 주변 텍스트 |
|---|---|---|---|
| ADMN-INST-001_baseline.html | [v4.0.0 대표 사례] 자사저작권 도서 | 자사 저작권 보유 | [v4.0.0 대표 사례] 자사저작권 도서(자사 저작권 보유) 매출연동 지원금 15% + 선급금  |
| ADMN-INST-001_baseline.html | 위탁 도서 판매대금 정산 | 위탁도서 정산 | 위탁 도서 판매대금 정산(위탁도서 정산) |
| ADMN-PROD-004_baseline.html | ADMN-BOOK-001 · 정식 SKU | BOOK-XXXX | ADMN-BOOK-001 · 정식 SKU(BOOK-XXXX)를 부여하고 출판사 공급률·제조원가· |
| ADMN-SETT-006_baseline.html | 강사가 환급분 20만원을 정상 부담하며 플랫폼 보전금 | 120만원 | 정상 적용 강사가 환급분 20만원을 정상 부담하며 플랫폼 보전금(120만원) 왜곡 없음 |
| ADMN-SETT-009_baseline.html | 자사 발행 도서 인세 및 자사저작권 | 도서 인세 | 자사 발행 도서 인세 및 자사저작권 (도서 인세) |
| ADMN-SETT-009_baseline.html | 일반 상품 판매매출 | 일반상품 매출 | 일반 상품 판매매출 (일반상품 매출) |

---

## 4. PAREN_DUP_SCAN.md 의 prototype_clean 표에서 ADMN-SETT-008 행부터 표 끝까지 원문

| 파일 | 앞말 | 괄호 안 | 주변 텍스트 |
|---|---|---|---|
| ADMN-SETT-008_baseline.html | 간이과세자-영수증발급 (간이과세자 | 영수증발급 | 원장: 간이과세자-영수증발급 (간이과세자(영수증발급)) |
| ADMN-SETT-008_baseline.html | 간이과세자-세금계산서발급 (간이과세자 | 세금계산서발급 | 응답: 간이과세자-세금계산서발급 (간이과세자(세금계산서발급)) |
| ADMN-SETT-008_baseline.html | 비영리·고유번호 단체 | 비영리·고유번호 단체 | 원장: 비영리·고유번호 단체 (비영리·고유번호 단체) |
| ADMN-SETT-008_baseline.html | 국세청 과세유형 코드 | 과세유형_cd | 국세청 과세유형 코드(과세유형_cd) ↔ 세무 판정 매트릭스 자동 매핑  |
| ADMN-SETT-009_baseline.html | 온라인 강좌 수익배분 | 강좌 수익배분 | 온라인 강좌 수익배분 (강좌 수익배분) |
| ADMN-SETT-009_baseline.html | 자사 발행 도서 인세 및 자사저작권 | 도서 인세 | 자사 발행 도서 인세 및 자사저작권 (도서 인세) |
| ADMN-SETT-009_baseline.html | 위탁 도서 판매대금 정산 | 위탁도서 정산 | 위탁 도서 판매대금 정산 (위탁도서 정산) |
| ADMN-SETT-009_baseline.html | 사입 도서(매입 재판매 도서 | 매입 재판매 | 산식은 호출하지 않으며 외부 지급액 0원으로 자사 마감 집계만 수행합니다. • 사입 도서(매입 재판매 도서 (매입 재판매), Case 11) 및 사은품 도서( |
| ADMN-SETT-009_baseline.html | 매입 재판매 도서 | 매입 재판매 | 매입 재판매 도서 (매입 재판매) |
| ADMN-SETT-009_baseline.html | 일반 상품 판매매출 | 일반상품 매출 | 일반 상품 판매매출 (일반상품 매출) |
| ADMN-SETT-009_baseline.html | 사입 재판매 | 매입 재판매 | 사입 재판매 (매입 재판매) = 일반상품(굿즈) |
| ADMN-SETT-009_baseline.html | 과세표준 IS NOT NULL 및 원천징수 사건 성립 | 원천징수 성립일 IS NOT NULL | 과세표준 IS NOT NULL 및 원천징수 사건 성립(원천징수 성립일 IS NOT NULL) 확정 라인만 집계. 지급 하한 미달 |
| ADMN-SETT-009_baseline.html | , 세후 지급대기 이월 | 세후 이월 | 대여금 방식 선급금 상계(LOAN), 세후 지급대기 이월(세후 이월) 합산, 지급 하한 미달 보류(세전  |
| ADMN-SETT-011_baseline.html | 월별 택배 대리점 운임 · 배송비 대사 목록 | 택배 운임 대사 | 월별 택배 대리점 운임 · 배송비 대사 목록 (택배 운임 대사) |
| ADMN-USER-001_baseline.html | 🚫 블랙리스트 관리 | 블랙리스트 관리 | 🚫 블랙리스트 관리 (블랙리스트 관리) |
| ADMN-USER-001_baseline.html | 선택 회원 그룹·태그 부여 | 그룹·태그 관리 | 선택 회원 그룹·태그 부여 (그룹·태그 관리) |
| ADMN-USER-001_baseline.html | ← 회원 목록으로 | 회원 목록 | ← 회원 목록으로 (회원 목록) |
| ADMN-USER-001_baseline.html | 회원 상세 정보 | 회원 상세 | 회원 상세 정보 (회원 상세) |
| ADMN-USER-001_baseline.html | 수강 · 기기 제어 | 수강·기기 제어 | 수강 · 기기 제어 (수강·기기 제어) → |
| ADMN-USER-001_baseline.html | 블랙리스트 · 정지 등재 | 블랙리스트 관리 | 블랙리스트 · 정지 등재 (블랙리스트 관리) |
| ADMN-USER-001_baseline.html | 수강 기간 · 기기/세션 제어 | 수강·기기 제어 | 수강 기간 · 기기/세션 제어 (수강·기기 제어) → |
| ADMN-USER-001_baseline.html | 보안 감사 로그 전체 보기 | 보안 감사로그/010 | 보안 감사 로그 전체 보기 (보안 감사로그/010) ↗ |
| ADMN-USER-001_baseline.html | ← 회원 목록 | 회원 목록 | ← 회원 목록 (회원 목록) |
| ADMN-USER-001_baseline.html | 블랙리스트 등재 | 블랙리스트 관리 | 블랙리스트 등재 (블랙리스트 관리) |
| ADMN-USER-001_baseline.html | ← 회원 상세로 | 회원 상세 | ← 회원 상세로 (회원 상세) |
| ADMN-USER-001_baseline.html | 🚫 블랙리스트 및 부정사용자 제재 원장 | 블랙리스트 관리 | 🚫 블랙리스트 및 부정사용자 제재 원장 (블랙리스트 관리) |
| ADMN-USER-001_baseline.html | 회원 상태 변경 · 블랙리스트 통제 | 블랙리스트 관리 | 회원 상태 변경 · 블랙리스트 통제 (블랙리스트 관리) |
| ADMN-USER-001_baseline.html | 환불 심사 | 환불 심사 관리 | • 환불 심사(환불 심사 관리) 및 합격환급 심사(합격환급반 정산) |
| ADMN-USER-007_baseline.html | 계층 3 파기 보류 예외 | `파기 보류 예외` | 계층 3 파기 보류 예외 (`파기 보류 예외`) |
| ADMN-USER-007_baseline.html | 정보 열람통제 사유 입력 팝업] 통과 후 정산 감사로그 | 감사 로그 | 및 증빙 사본(Presigned URL) 호출은 [민감정보 열람통제 사유 입력 팝업] 통과 후 정산 감사로그(감사 로그)에 영구 기록됩니다. |
| ADMN-USER-007_baseline.html | 정산 감사로그 | 감사 로그 | 정산 감사로그(감사 로그) |
| ADMN-USER-007_baseline.html | D, IP, 열람 시각, 입력 사유가 시스템 감사 로그 | 정산 감사로그 | 작업자 ID, IP, 열람 시각, 입력 사유가 시스템 감사 로그(정산 감사로그)에 즉시 기록 |
| ADMN-USER-007_baseline.html | 파기 작업 감사 로그 | 정산 감사로그 | • 원천징수영수증 / 세금계산서 승인번호 • 파기 작업 감사 로그 (정산 감사로그) |

---

## 5. prototype_clean HTML 원문 줄 (앞뒤 1줄 포함)

### 5-1. ADMN-SETT-005_baseline.html ("요율 오류")
**prototype_clean/ADMN-SETT-005_baseline.html:553**
```html
552:                 <option value="ALL">전체 조정 사유 구분 (13종)</option>
553:                 <option value="RATE_ERR">요율 오류 (RATE_ERR)</option>
554:                 <option value="SHARE_ERR">지분율 오류 (SHARE_ERR)</option>
```
**prototype_clean/ADMN-SETT-005_baseline.html:731**
```html
730:           <select id="newReasonCode" class="select" onchange="updateNewModalPreview()">
731:             <option value="RATE_ERR">요율 오류 (RATE_ERR)</option>
732:             <option value="SHARE_ERR">지분율 오류 (SHARE_ERR)</option>
```
**prototype_clean/ADMN-SETT-005_baseline.html:821**
```html
820:   const REASON_MAP = {
821:     RATE_ERR: "요율 오류 (RATE_ERR)",
822:     SHARE_ERR: "지분율 오류 (SHARE_ERR)",
```
**prototype_clean/ADMN-SETT-005_baseline.html:847**
```html
846:         reasonCode: "RATE_ERR",
847:         reasonLabel: "요율 오류 (RATE_ERR)",
848:         originMonth: "2026-08",
```

### 5-2. ADMN-CONF-004_baseline.html ("카카오 검수중")
**prototype_clean/ADMN-CONF-004_baseline.html:415**
```html
414:         <div class="kpi-card">
415:           <div class="kpi-label">카카오 검수중 (INSPECT_REQ)</div>
416:           <div class="kpi-val" style="color:var(--primary);" id="kpi-tpl-req">1건</div>
```
**prototype_clean/ADMN-CONF-004_baseline.html:449**
```html
448:               <option value="APPROVED">검수승인 / 발송가능 (APPROVED)</option>
449:               <option value="INSPECT_REQ">카카오 검수중 (INSPECT_REQ)</option>
450:               <option value="REJECTED">검수반려 (REJECTED)</option>
```
**prototype_clean/ADMN-CONF-004_baseline.html:622**
```html
621:               <option value="DRAFT">작성초안 (DRAFT)</option>
622:               <option value="INSPECT_REQ">카카오 검수중 (INSPECT_REQ)</option>
623:               <option value="APPROVED">검수승인 완료 (APPROVED)</option>
```
**prototype_clean/ADMN-CONF-004_baseline.html:818**
```html
817:       APPROVED: '<span class="badge badge-green">✓ 검수승인 (발송가능)</span>',
818:       INSPECT_REQ: '<span class="badge badge-blue">⏳ 카카오 검수중</span>',
819:       REJECTED: '<span class="badge badge-red">✕ 검수반려 (사유확인)</span>',
```

### 5-3. ADMN-ORD-001_baseline.html ("수강권 직권부여")
**prototype_clean/ADMN-ORD-001_baseline.html:1756**
```html
1755:                 <div style="font-size:12px;line-height:1.6;color:var(--text-sub);">
1756:                   • 주문 유형: <b class="mono">DIRECT_GRANT</b> (수강권 직권부여 · 구 ADMN-ORD-003 통합)<br>
1757:                   • 실결제금액: <b style="color:var(--primary);">0원</b> (정가 187,000원 − 직권감면 187,000원)<br>
```

### 5-4. ADMN-SETT-004_baseline.html ("매입 재판매 도서")
**prototype_clean/ADMN-SETT-004_baseline.html:543**
```html
542:           <strong>📌 [정산 기준 · 통합설계서 표 5.1-A 토스페이먼츠 5대 결제수단(신용/체크·계좌이체·가상계좌 DONE·간편결제 5종·휴대폰) 1:1 대사 및 이원화 임계값 통제]</strong>
543:           매입 재판매 도서(<code>매입 재판매 도서 (PURCHASED_RESALE)</code>) 및 사은품(<code>강좌 부속·사은품 (BUNDLED)</code>), 배송비(<code>SHIPPING_FEE</code>)는 정산 엔진 비인입 대상이므로 <strong>정산서 총액과 전사 결제 매출 총액은 구조적으로 일치하지 않습니다.</strong> 본 화면은 오직 <strong>자체 결제 DB(<code>payments / order_items</code>)와 PG사 정산 원장 간의 1:1 대사</strong>만 수행합니다.
544:         </div>
```
