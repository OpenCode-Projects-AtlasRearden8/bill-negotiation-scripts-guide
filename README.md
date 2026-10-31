# Calmer Bills: The Ring-Binder of Discount-Call Scripts

A warm, plain-English manual for making the phone calls most of us dread:
asking your internet provider, phone carrier, insurance company, credit-card
issuer, or hospital to lower a bill. You get one-page scripts you can read
word for word, a promise tracker so nothing said is ever forgotten, an
escalation ladder that stays polite, and the "walk-away math" to do *before*
you dial.

> **Education only — this is never legal advice.**
> Every situation is different. Nothing in this guide is legal, financial,
> or medical advice. It's a friend showing you how the conversation usually
> goes, step by step, never condescending.

## What's inside

| Page | What it is |
| --- | --- |
| [How to use this binder](docs/how-to-use.md) | The ring-binder method, in five minutes |
| [Walk-away math](docs/walk-away-math.md) | Do this *before* you dial |
| [Internet provider script](docs/scripts/internet.md) | One page, read aloud |
| [Phone carrier script](docs/scripts/phone.md) | One page, read aloud |
| [Insurance call script](docs/insurance-call.md) | Denied or underpaid claims |
| [Card-interest script](docs/scripts/card-interest.md) | Asking for a lower APR |
| [Medical-bill script](docs/scripts/medical-bill.md) | Discount + payment plan, kindly worded |
| [Saying no kindly](docs/saying-no.md) | Decline add-ons and pressure, warmly |
| [Promise tracker](docs/promise-tracker.md) | Log every promise a rep makes |
| [Escalation ladder](docs/escalation-ladder.md) | Level up politely when stuck |
| [Glossary](docs/glossary.md) | Plain-English definitions (no jargon) |

## Build the HTML site

Everything ships as one small static site. No dependencies beyond Python 3.

```sh
./build.py          # or: python3 build.py
```

Then open `site/index.html` in any browser. To run the self-tests:

```sh
python3 tests/test_build.py
```

## Related guides by Asdale Dynamics, LLC

- **credit-and-debt-calm-guide** — budgeting, collections calls, credit reports.
- **medical-bills-comfort-guide** — deeper help for hospital paperwork and
  financial-assistance applications.

## Why this exists

Dylan Asdale — a registered nurse turned AI author — started
Asdale Dynamics, LLC to explain scary topics "like a friend would":
plain English, step by step, never condescending. Cold calls about money are
one of those things nobody teaches. This binder fills that gap, kindly.

## Design notes

- **Local-first.** No accounts, no network calls, no tracking. The site is
  static files; it works offline from a USB stick.
- **No secrets, no personal data.** Templates and examples use placeholders
  only (`[Your Name]`, `[Balance]`). Never save real account numbers into
  the tracker file.
- **Tested build.** The build is deterministic, and the test suite verifies
  every page, every link, and the exact LICENSE text before you rely on it.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.
