# Attribution

This project is a fork of [Quizlet-dl](https://github.com/OxxoCodes/Quizlet-dl) by [OxxoCodes](https://github.com/OxxoCodes), used under the MIT License.

The original project has been substantially rewritten. Key changes made in this fork:

- Replaced credential-based login with Firefox cookie extraction
- Switched to Playwright + playwright-stealth for scraping
- Added Anki-ready TSV export with file headers
- Migrated to uv for dependency management
- Added per-set subfolder exports with URL-derived filenames
