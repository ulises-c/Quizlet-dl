# Quizlet-dl

Downloads a Quizlet study set and exports it as JSON and a tab-separated file ready to import into [Anki](https://apps.ankiweb.net).

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
- `<set title>.tsv` — Anki-ready (tab-separated, with headers and a tag matching the set title)

## Importing into Anki

1. Open Anki and select the deck you want to import into
2. Go to **File → Import**
3. Select the `.tsv` file
4. Anki will detect the tab separator and map front/back/tags automatically
5. Click **Import**

The TSV includes `#html:true` so any HTML in Quizlet cards renders correctly in Anki.

## How authentication works

The script reads your Quizlet session cookies directly from your local Firefox profile — no login prompt, no password entry. As long as you're signed into Quizlet in Firefox, it just works.

If you'd prefer to supply credentials instead, copy `.env.example` to `.env` and fill in your username and password. The script will attempt an automated login when no Firefox session is available.

## Limitations

- Requires an active Quizlet session in Firefox on the same machine
- Folders, classes, and premium-only content are not supported
