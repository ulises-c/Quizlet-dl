# Quizlet-dl

Downloads a Quizlet study set and exports it as JSON and a tab-separated file ready to import into [Anki](https://apps.ankiweb.net).

## Requirements

- Python 3.13.x
- [uv](https://docs.astral.sh/uv/getting-started/installation/) — handles dependencies automatically
- [Firefox](https://www.mozilla.org/en-US/firefox/new/) — must be installed and logged into Quizlet; the script reads session cookies from your Firefox profile

```bash
make install  # installs Python deps and the Playwright-managed Firefox binary
```

## Usage

```bash
make run https://quizlet.com/123456789/my-set/
```

Or with an explicit variable if your shell strips the URL:

```bash
make run URL="https://quizlet.com/123456789/my-set/"
```

Output is saved under `exports/` with a timestamped folder so re-downloads never overwrite:

```
exports/
  123456789_my-set_2026-06-07T14-35-22/
    123456789_my-set_2026-06-07T14-35-22.json
    123456789_my-set_2026-06-07T14-35-22.tsv   ← Anki-ready
```

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

## Limitations

- **macOS only** — the Firefox profile path uses the macOS-specific `~/Library/Application Support/Firefox/Profiles/` location
- **Text-only cards** — cards containing images, diagrams, or audio are silently dropped (only `.TermText` elements are scraped)
- **Requires an active Quizlet login in Firefox** — no cookies means no access to private or member-only sets
- **Direct study set URLs only** — folders, classes, and premium-only content are not supported
- **One tag per card** — all cards get the sanitized set title as their only tag; no per-card topic tags
- **Anki Basic note type only** — exports front/back pairs; cloze deletions and custom note types are not supported

## Attribution

Forked from [OxxoCodes/Quizlet-dl](https://github.com/OxxoCodes/Quizlet-dl). The scraping approach has been substantially rewritten — see [ATTRIBUTION.md](ATTRIBUTION.md) for details.
