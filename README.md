# Quizlet-dl

Downloads a Quizlet study set and exports it as JSON and a tab-separated file ready to import into [Anki](https://apps.ankiweb.net).

## Requirements

- [uv](https://docs.astral.sh/uv/getting-started/installation/) — handles Python and dependencies automatically
- [Firefox](https://www.mozilla.org/en-US/firefox/new/) — must be installed and you must be logged into Quizlet in it

```bash
uv run quizlet-dl.py --help  # installs deps on first run
playwright install firefox
```

## Usage

```bash
uv run quizlet-dl.py <url>
```

Example:

```bash
uv run quizlet-dl.py "https://quizlet.com/123456789/my-set/"
```

Output files are saved in the same directory as the script:
- `<set title>.json`
- `<set title>.tsv` — Anki-ready (see below)

## Importing into Anki

1. Open Anki
2. Go to **File → Import**
3. Select the `.tsv` file
4. Click **Import** — no configuration needed

The TSV includes [Anki file headers](https://docs.ankiweb.net/importing/text-files.html) (requires Anki 2.1.54+) that pre-configure the import automatically:

| Header | Value | Effect |
|--------|-------|--------|
| `#separator:tab` | tab | Tab-delimited columns |
| `#html:true` | true | Renders HTML in card fields |
| `#deck` | Set title | Creates or routes to a matching deck |
| `#notetype:Basic` | Basic | Uses Anki's built-in Basic note type (Front / Back) |
| `#columns` | Front, Back, Tags | Maps columns to fields |
| `#tags column:3` | 3 | Applies the third column as tags |

Each card is tagged with the sanitized set title (spaces replaced with underscores) for easy filtering in the browser.

## How authentication works

The script reads your Quizlet session cookies directly from your local Firefox profile — no login prompt, no password entry. As long as you're signed into Quizlet in Firefox, it just works.

If you'd prefer to supply credentials instead, copy `.env.example` to `.env` and fill in your username and password. The script will attempt an automated login when no Firefox session is available.

## Limitations

- **macOS only** — the Firefox profile path uses the macOS-specific `~/Library/Application Support/Firefox/Profiles/` location
- **Text-only cards** — cards containing images, diagrams, or audio are silently dropped (only `.TermText` elements are scraped)
- **Requires an active Quizlet login in Firefox** — no cookies means no access to private or member-only sets
- **Automated login is unreliable** — Cloudflare bot detection blocks it; the `.env` credential fallback rarely succeeds
- **Direct study set URLs only** — folders, classes, and premium-only content are not supported
- **One tag per card** — all cards get the sanitized set title as their only tag; no per-card topic tags
- **Anki Basic note type only** — exports front/back pairs; cloze deletions and custom note types are not supported
