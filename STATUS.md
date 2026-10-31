# What was built

**Calmer Bills — The Ring-Binder of Discount-Call Scripts**: a warm,
plain-English manual for the five money-conversations most people avoid
(internet, phone, insurance, card-interest, and medical-bill discount
calls), shipped as Markdown source in `docs/` plus a build script that
renders a static HTML site into `site/`.

Contents:

- Five one-page call scripts: internet provider, phone carrier, insurance
  claim, card-interest rate, medical bill (`docs/scripts/`).
- [Walk-away math](docs/walk-away-math.md) — the budget/target/walk-away
  worksheet to complete before dialing.
- [The promise tracker](docs/promise-tracker.md) — template + phrases that
  turn verbal promises into written ones.
- [Saying no kindly](docs/saying-no.md) — five ready-to-read declines.
- [The escalation ladder](docs/escalation-ladder.md) — six polite rungs.
- [Glossary](docs/glossary.md) — plain-English definitions.
- Build tooling: `build.py` (Python 3 + `markdown` package), self-tests in
  `tests/test_build.py`.

Education only, never legal/financial/medical advice — the disclaimer is
baked into every built page (banner + footer). Local-first: the site is
static files, works offline, no network calls, no accounts, no tracking.

Credit: Asdale Dynamics, LLC (MIT licensed — `LICENSE` has the exact line
`Copyright (c) 2026 Asdale Dynamics, LLC`).

## How to run it

```sh
python3 build.py          # builds site/ (output: ~12 HTML pages)
python3 tests/test_build.py   # runs the 11 self-tests
```

Then open `site/index.html` in any browser. Nothing else is required; no
install step, no server needed (any static file opener works).

## Verification results

- `python3 build.py` — OK: builds 12 pages, deterministic output.
- `python3 tests/test_build.py` — all 11 tests pass:
  - every sidebar page builds; no missing/extra pages
  - build is byte-for-byte deterministic across runs
  - one `<h1>` per page; disclaimer banner on every page
  - every internal link resolves (no dead links, no raw `.md` links)
  - LICENSE contains the exact required copyright line
  - README credits Asdale Dynamics, LLC
  - docs contain no emails, phone numbers, or SSNs (placeholder-only)

## Known gaps

- The two sibling guides (`credit-and-debt-calm-guide`,
  `medical-bills-comfort-guide`) are referenced by name only — they live in
  their own repositories.
- The HTML uses minimal inline styling; no search, no JS, no print-PDF
  export (browser print works; pages have a print stylesheet).
- The `markdown` Python package must be installed (`pip install markdown`);
  no requirements file is pinned since it's the only dependency.
