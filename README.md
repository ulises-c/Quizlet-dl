# Quizlet-dl

Downloads a Quizlet study set and exports it as JSON and TSV (tab-separated, Anki-compatible).

## Requirements

- Python 3.8+
- [Firefox](https://www.mozilla.org/en-US/firefox/new/) — must be installed and you must be logged into Quizlet in it
- Playwright + playwright-stealth

```bash
pip install playwright playwright-stealth
playwright install firefox
```

## Usage

```bash
python quizlet-dl.py <url>
```

Example:

```bash
python quizlet-dl.py "https://quizlet.com/123456789/my-set/"
```

Output files are saved in the same directory as the script:
- `<set title>.json`
- `<set title>.txt` (tab-separated, term → definition)

## How authentication works

The script reads your Quizlet session cookies directly from your local Firefox profile — no login prompt, no password entry. As long as you're signed into Quizlet in Firefox, it just works.

If you'd prefer to supply credentials instead, copy `.env.example` to `.env` and fill in your username and password. The script will attempt an automated login when no Firefox session is available.

## Limitations

- Requires an active Quizlet session in Firefox on the same machine
- Folders, classes, and premium-only content are not supported
