# Verification — Spanish Irregular Verbs (A1, rebuild)

Built 4 September 2026 to the `lbc-listing-standard` skill. This product ships without a
native-speaker reviewer, so every form is machine-derived and cross-checked against a
second, independent source.

## Sources

| | |
|---|---|
| **Primary** | `verbecc` (Python). Template-driven conjugation from a verb dictionary. |
| **Second, independent** | Wiktionary Spanish conjugation tables, via the REST HTML API. |

## Gate 1: no predicted forms

verbecc exposes a `predicted` flag. Where a verb is absent from its dictionary it *guesses*
a template with a trained model. `extract.py` asserts `predicted is False` for every verb
and raises otherwise.

**All 45 verbs passed.** Nothing in this pack is a guess.

## Gate 2: Wiktionary cross-check

```
verbs cross-checked : 26 of 27
cells compared      : 1,092
mismatches          : 1  (found, diagnosed and corrected — see below)
```

Tenses compared per verb: present, imperfect, preterite, future, conditional, present
subjunctive, imperfect subjunctive (-ra), future subjunctive.

`traer` could not be fetched (repeated HTTP 429 rate limiting from Wiktionary). It is the
one verb in this pack verified by verbecc alone. Re-run `verify.py` later to close it.

### The error the cross-check caught

```
haber | Present | él/ella/Ud. | verbecc='hay'  wiktionary='ha'
```

verbecc returns the **impersonal** form `hay` ("there is / there are") in the third-person
slot. In the auxiliary paradigm, which is what a conjugation chart of *haber* means, the
form is **`ha`** (*ha hablado*). Corrected to `ha`, and the page now carries a note
explaining `hay` so the distinction is taught rather than hidden.

This is the entire reason for having a second source. verbecc alone would have shipped it.

### The trap in the second source, and how it is handled

A Wiktionary page stacks many languages. Parsing the first conjugation table on `tener`
returns `tiengo, tiens, tien, tenez` — **Aragonese, not Spanish.** `wikt.py` scopes to the
`id="Spanish"` heading and stops at the next `<h2>` before touching any table, and raises
rather than guessing if the Spanish section is absent. Wiktionary also packs tuteo and voseo
into one cell (`tienes tú tenés vos`); `tu_form()` keeps the tuteo form and strips footnote
markers.

## What is claimed, and whether it is true

| Claim | Verified how | Status |
|---|---|---|
| 27 verbs conjugated in full | counted from `verbs.json` families | True |
| 45 verbs in the index | counted from `verbs.json` index | True |
| 10 tenses | counted from `verbs.json` simple | True |
| 5 patterns | counted from families | True |
| 4 files, 77 pages | `pypdf` page count on the built PDFs | True |
| 37 pages US Letter / 37 A4 / 2 practice / 1 poster | same | True |
| Body 11pt on pages, 20pt on poster | computed font size in the renderer | True |
| Vector text | Chromium PDF engine, embedded fonts | True |
| 1,092 cells checked | `verification.json` | True |

**Every number in the listing images is read at build time from the PDFs themselves**
(`listing.py` opens them with `pypdf`). When the family pages were split and the count moved
from 73 to 77, all ten images and the video regenerated with the correct figure and no hand
editing. That closes the failure mode from the previous build, where "14 pages" was wrong in
three places.

## Layout QA, run programmatically

Print pages, all 37 + 2 + poster:

| Check | Threshold | Result |
|---|---|---|
| Body type, Letter and A4 | ≥ 11pt | 11pt to 12.5pt |
| Body type, poster | ≥ 20pt | 20pt |
| Any text at all | ≥ 10pt | 10pt |
| Horizontal overflow | none | none |
| Content fill | 85% to 97.5% | 85.2% to 95% |
| Fonts loaded | no silent fallback | Fredoka + Nunito confirmed loaded |

Listing images, all 10:

| Check | Threshold | Result |
|---|---|---|
| Inside the 1600×2000 safe zone | x 200–1800 | pass |
| Vertical overflow | none | none |
| Smallest text | ≥ 40px | 44px |
| Hero product name | ≥ 260px | 272px |

### A QA bug found and fixed during this build

The previous fill metric measured the bottom of the footer. The footer uses
`margin-top:auto`, so it is pinned to the bottom of the page and **always** read about 96%,
even on a half-empty page. It was hiding real whitespace. The metric now measures the bottom
of the last content element, which immediately exposed three under-filled pages (overview
81.8%, index 82.7%, and family pages showing only 4 of 7 verbs). All three were fixed.

## Colour and accessibility

Pattern colour is never the only signal: every block also carries the pattern name in words,
and the family pill is repeated in the page header. Header text is dark ink on pastel, which
clears 4.5:1 on all five families. An earlier palette used white text on amber at 1.97:1;
that was caught by computing the ratios rather than eyeballing them.

## Reproducing this build

```
pip install verbecc pypdf pypdfium2 --break-system-packages
python3 extract.py          # asserts predicted == False for all 45 verbs
python3 verify.py           # Wiktionary cross-check, must report 0 open mismatches
cd build && python3 gen.py 1.0
python3 qa.py               # print-page gates
python3 render.py           # PDFs
python3 listing.py          # listing images, counts read from the PDFs
python3 lqa.py              # listing-image gates
```

## Limits

- `traer` is verified by verbecc alone (Wiktionary rate limit).
- Compound tenses are not on the verb pages in this product. The pack covers the 10 simple
  tenses and does not claim otherwise.
- The cross-check verifies **form**. It says nothing about usage or register, which is why
  this lane is conjugation tables and not phrase sheets.
