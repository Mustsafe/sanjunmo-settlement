# -*- coding: utf-8 -*-
import sys, json, asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        url = Path("prototype_clean/00_WORKFLOW_GUIDE_baseline.html").resolve().as_uri()
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(1000)

        # 5-1. SNB: group title -> items [text | href]
        snb_result = await page.evaluate(r"""() => {
            const snb = document.getElementById('v4-master-snb');
            if (!snb) return [];
            const nodes = snb.querySelectorAll('.snb-group-title, a[href]');
            const groups = [];
            let cur = null;
            nodes.forEach(n => {
                if (n.classList.contains('snb-group-title')) {
                    cur = { title: n.textContent.trim(), items: [] };
                    groups.push(cur);
                } else if (cur) {
                    const href = n.getAttribute('href') || '';
                    const text = n.textContent.replace(/\s+/g, ' ').trim();
                    cur.items.push({ text: text, href: href });
                }
            });
            return groups;
        }""")

        # 5-2. #wf-dir-grid: card h4 -> items [text | href]
        grid_result = await page.evaluate(r"""() => {
            const box = document.getElementById('wf-dir-grid');
            if (!box) return [];
            const cards = box.querySelectorAll('.wf-dir-card');
            const result = [];
            cards.forEach(card => {
                const h4 = card.querySelector('h4');
                const title = h4 ? h4.textContent.trim() : '';
                const items = [];
                card.querySelectorAll('a[href]').forEach(a => {
                    const href = a.getAttribute('href') || '';
                    const text = a.textContent.replace(/\s+/g, ' ').trim();
                    items.push({ text: text, href: href });
                });
                result.push({ title: title, items: items });
            });
            return result;
        }""")

        await browser.close()

        with open(".antigravity/reports/temp_snb_grid.json", "w", encoding="utf-8") as f:
            json.dump({"snb": snb_result, "grid": grid_result}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
