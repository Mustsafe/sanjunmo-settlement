# PAREN_FIX_SRC_03 리포트

## 1. prototype_clean/ADMN-BOOK-001_baseline.html 에서 "사후 변경" 이 들어간 줄 (앞뒤 1줄 포함)

**prototype_clean/ADMN-BOOK-001_baseline.html:851**
```html
850:             <div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:8px; padding:11px 14px; margin-bottom:14px; font-size:12px; color:#1e3a8a;">
851:               💡 <strong>[정산 기준 정가 변경 이력 관리 원칙]</strong> 도서 정가가 개정판 등으로 인상·변경되더라도 과거 주문의 환불/반품(4단계 <code>DEDUCT</code>) 시에는 <strong>원거래 주문 시점의 정가 스냅샷(<code>effective_from ~ effective_to</code>)</strong>을 역참조하여 인세 및 위탁 대금을 정확히 차감합니다. 또한 출고 이력이 1건이라도 발생한 도서는 <code>book_supply_type</code>(공급 형태)을 사후 변경할 수 없습니다.
852:             </div>
```

---

## 2. prototype_clean/ADMN-ORD-001_baseline.html 에서 "인세" 가 들어간 줄 (앞뒤 1줄 포함)

**prototype_clean/ADMN-ORD-001_baseline.html:1128**
```html
1127:                         <b>정종대 (RH-0025) 명품 산업안전기사 필기 수험서</b><br>
1128:                         <span style="font-size:11.5px;color:var(--text-muted);">ISBN <code>979-11-8921-01 · SKU: BK-2026-101</code> · 스냅샷: <code>ROYALTY_BOOK(인세도서)</code></span>
1129:                       </td>
```
**prototype_clean/ADMN-ORD-001_baseline.html:1132**
```html
1131:                         <span class="badge b-teal">면세 0% (부가세법 제26조제1항제8호)</span><br>
1132:                         <span style="font-size:11px;color:var(--text-muted);">도서 인세 도서 인세 (+1권)</span>
1133:                       </td>
```

---

## 3. prototype_clean/common-snb.js 에서 "book_supply_type", "인세도서", "인세 도서" 가 들어간 줄

#### 단어: "book_supply_type"
- prototype_clean/common-snb.js:603: `"book_supply_type": "도서 공급형태",`
- prototype_clean/common-snb.js:604: `"book_supply_type_snapshot": "도서 공급형태 스냅샷",`

#### 단어: "인세도서"
0건

#### 단어: "인세 도서"
- prototype_clean/common-snb.js:524: `"ROYALTY_BOOK": "인세 도서",`


---

## 4. prototype_clean/*.html 전체에서 "인세도서" 가 들어간 줄

- prototype_clean/ADMN-BOOK-001_baseline.html:700: `<span class="step-num">Step 1. 권리자 계약 원장 (인세도서 가채번)</span>`
- prototype_clean/ADMN-BOOK-001_baseline.html:1039: `<span class="badge badge-sale">인세도서 표준</span>`
- prototype_clean/ADMN-ORD-001_baseline.html:1128: `<span style="font-size:11.5px;color:var(--text-muted);">ISBN <code>979-11-8921-01 · SKU: BK-2026-101</code> · 스냅샷: <code>ROYALTY_BOOK(인세도서)</code></span>`
- prototype_clean/ADMN-PROD-004_baseline.html:738: `<span class="step-num">Step 1. 권리자 계약 원장 (인세도서 가채번)</span>`
- prototype_clean/ADMN-PROD-004_baseline.html:814: `<option value="INST_TEMP">[경로 1] 계약원장 가채번 출발 (인세도서)</option>`
- prototype_clean/ADMN-PROD-004_baseline.html:1026: `<span class="badge badge-sale">강사 인세도서 권장</span>`
