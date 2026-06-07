# Attribution

This project is a fork of [Quizlet-dl](https://github.com/OxxoCodes/Quizlet-dl) by [OxxoCodes](https://github.com/OxxoCodes), used under the MIT License.

The codebase has been substantially rewritten. The original used a plain `requests.get()` with a spoofed Windows Chrome User-Agent and `BeautifulSoup` to parse static HTML — matching card elements via regex CSS class selectors (`SetPage-setDetailsTerms`, `SetPageTerm-wordText`, `SetPageTerm-definitionText`). It required no authentication and targeted unauthenticated public sets only, outputting JSON to a user-specified directory.

This fork replaces that approach entirely:

| | Original | This fork |
|---|---|---|
| HTTP | `requests` + spoofed User-Agent | Playwright (real Firefox) + `playwright-stealth` |
| Auth | None — public sets only | Firefox session cookies read directly from SQLite |
| Page loading | Single GET of static HTML | Scroll loop to trigger lazy-loaded card rendering |
| Selectors | Regex class matching (`SetPage-*`) | `.TermText` on fully rendered DOM |
| Output | JSON only | JSON + Anki-ready TSV with import headers |
| Dependencies | pip (`requests`, `beautifulsoup4`) | `uv` inline script metadata |
| Platform | Windows | macOS |
