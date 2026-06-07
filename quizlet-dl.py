#!/usr/bin/env python3
import json, os, sys
from playwright.sync_api import sync_playwright


def scrape(url):
    with sync_playwright() as p:
        print("Opening browser (do not close the window)...")
        browser = p.chromium.launch(channel="chrome", headless=False)
        page = browser.new_page()

        page.goto(url, timeout=30000)
        page.wait_for_function(
            "() => document.title && !document.title.includes('Just a moment')",
            timeout=20000,
        )
        page.wait_for_timeout(2000)
        title = page.title().split("|")[0].strip()
        print(f"Loaded: {title}")

        # Scroll to trigger lazy loading of all terms
        prev = 0
        for _ in range(40):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(400)
            count = page.evaluate("document.querySelectorAll('.TermText').length")
            if count == prev:
                break
            prev = count

        all_texts = page.evaluate(
            "() => Array.from(document.querySelectorAll('.TermText')).map(el => el.textContent.trim())"
        )
        browser.close()

    if len(all_texts) < 2:
        print("ERROR: no card text found in the page.")
        return

    # Elements alternate: term, definition, term, definition, ...
    cards = [(all_texts[i], all_texts[i + 1]) for i in range(0, len(all_texts) - 1, 2)]
    print(f"Extracted {len(cards)} cards")

    for ch in r'/\:?"<>|':
        title = title.replace(ch, "")
    title = title.strip() or "quizlet_set"

    out_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(out_dir, title + ".json")
    txt_path  = os.path.join(out_dir, title + ".txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"title": title, "cards": [{t: d} for t, d in cards]}, f, indent=2, ensure_ascii=False)

    with open(txt_path, "w", encoding="utf-8") as f:
        for term, defn in cards:
            f.write(f"{term}\t{defn}\n")

    print(f"  JSON → {json_path}")
    print(f"  TSV  → {txt_path}")


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://quizlet.com/1016681673/emgt-330-flash-cards/"
    scrape(url)
