#!/usr/bin/env python3
import json, os, re, shutil, sqlite3, sys, tempfile
from datetime import date
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

FF_PROFILE = os.path.expanduser(
    "~/Library/Application Support/Firefox/Profiles/ihhi4t5l.default-release"
)
SAMESITE_MAP = {0: "None", 1: "Lax", 2: "Strict"}


def _firefox_quizlet_cookies():
    src = os.path.join(FF_PROFILE, "cookies.sqlite")
    with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as tmp:
        shutil.copy2(src, tmp.name)
        tmp_path = tmp.name
    try:
        conn = sqlite3.connect(tmp_path)
        rows = conn.execute(
            "SELECT host, name, value, path, expiry, isSecure, isHttpOnly, sameSite "
            "FROM moz_cookies WHERE host LIKE '%quizlet%'"
        ).fetchall()
        conn.close()
    finally:
        os.unlink(tmp_path)

    cookies = []
    for host, name, value, path, expiry, secure, http_only, same_site in rows:
        c = {
            "name": name,
            "value": value,
            "domain": host,
            "path": path,
            "secure": bool(secure),
            "httpOnly": bool(http_only),
            "sameSite": SAMESITE_MAP.get(same_site, "None"),
        }
        c["expires"] = int(expiry / 1000) if expiry and expiry > 0 else -1
        cookies.append(c)
    return cookies


def scrape(url):
    cookies = _firefox_quizlet_cookies()
    print(f"Loaded {len(cookies)} Quizlet cookies from Firefox profile.")

    with sync_playwright() as p:
        print("Opening browser...")
        browser = p.firefox.launch(headless=False)
        context = browser.new_context()
        context.add_cookies(cookies)

        page = context.new_page()
        Stealth().use_sync(page)

        page.goto(url, timeout=30000)
        page.wait_for_load_state("domcontentloaded", timeout=30000)
        page.wait_for_timeout(2000)
        title = page.title().split("|")[0].strip()
        print(f"Loaded: {title}")

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
        print("ERROR: no card text found.")
        return

    cards = [(all_texts[i], all_texts[i + 1]) for i in range(0, len(all_texts) - 1, 2)]
    print(f"Extracted {len(cards)} cards")

    for ch in r'/\:?"<>|':
        title = title.replace(ch, "")
    title = title.strip() or "quizlet_set"

    tag = title.replace(" ", "_")

    m = re.search(r"quizlet\.com/(\d+)/([^/?#]+)", url)
    uid  = m.group(1) if m else "unknown"
    slug = m.group(2) if m else tag
    stem = f"{uid}_{slug}_{date.today().isoformat()}"

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports")
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, stem + ".json")
    tsv_path  = os.path.join(out_dir, stem + ".tsv")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"title": title, "cards": [{t: d} for t, d in cards]}, f, indent=2, ensure_ascii=False)

    with open(tsv_path, "w", encoding="utf-8") as f:
        f.write("#separator:tab\n")
        f.write("#html:true\n")
        f.write(f"#deck:{title}\n")
        f.write("#notetype:Basic\n")
        f.write("#columns:Front\tBack\tTags\n")
        f.write("#tags column:3\n")
        for term, defn in cards:
            f.write(f"{term}\t{defn}\t{tag}\n")

    print(f"  JSON → {json_path}")
    print(f"  TSV  → {tsv_path} (Anki-ready)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python quizlet-dl.py <url>", file=sys.stderr)
        sys.exit(1)
    scrape(sys.argv[1])
