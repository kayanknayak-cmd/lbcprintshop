# Verification — Spanish Verb Conjugation Chart (A1)

Built 4 September 2026. This file records how the content was produced and checked, since
the product ships without native-speaker review.

## Source of truth

**verbecc** (Python), a template-driven conjugator that derives forms from a verb
dictionary plus conjugation templates. Installed and run in the cloud workspace on
4 Sep 2026. Supported languages: ca, es, fr, it, pt, ro.

## Gate 1: no predicted forms

verbecc exposes a `predicted` flag. When a verb is in its dictionary the forms come from a
template; when it is not, the library predicts a template with a trained model. Observed:

```
hablar      predicted=False   template=cort:ar
comer       predicted=False   template=deb:er
vivir       predicted=False   template=viv:ir
flurbizar   predicted=True    template=ca:zar     (nonsense verb, correctly flagged)
```

`extract.py` asserts `predicted is False` for every verb and raises otherwise. All three
model verbs on this chart passed.

## Gate 2: independent second derivation

`verify.py` contains a second, separately written conjugator built from the published
regular-ending tables for -ar, -er and -ir, the `haber` paradigm for compound tenses, and
the standard command-formation rules (tú = third person singular present indicative,
Ud./nosotros/Uds. = present subjunctive, vosotros = infinitive minus r plus d, negatives =
present subjunctive). It shares no code and no data with verbecc.

Every cell on the chart was compared between the two derivations.

```
cells checked : 354
mismatches    : 0
```

Raw result: `_source_data/verification.json`.

Two independent derivations agreeing on all 354 cells is the substitute for a native
reviewer. It is a strong check on **form**. It says nothing about usage, register or
naturalness, which is why this product is a conjugation table and not a phrase sheet.

## What is claimed on the listing, and whether it is true

| Claim | Status |
|---|---|
| "All 18 tenses" | True. 8 indicative, 2 conditional, 6 subjunctive, 2 imperative. The imperfect subjunctive and past perfect subjunctive each count once and are shown in both -ra and -se forms, which is standard practice. 20 blocks are printed. |
| "Three model verbs" | True. hablar, comer, vivir. |
| "All six persons" | True. yo, tú, él/ella/Ud., nosotros, vosotros, ellos/Uds. Imperative shows its five, which is all it has. |
| "11 pages" | True, after correction. 1 poster + 4 US Letter + 4 A4 + 2 practice = 11. |
| "Vector text" | True. Rendered via Chromium's PDF engine with embedded fonts, not rasterised. |
| "354 cells, 0 mismatches" | True, and reproducible by running `_source_data/verify.py`. |

### Error found and fixed during QA

The first draft claimed **14 pages**. The real count is **11**: 1 poster + 4 US Letter +
4 A4 + 2 practice grids. The wrong figure appeared in three places, all now corrected:
the listing description, listing image `02_full_set.png`, and image `10_files.png`.
Re-rendered and re-checked 4 Sep 2026.

Worth noting for the rest of the lane: page count is the easiest number on a listing to
get wrong, and it is one a buyer can check. Recount it from the built PDFs, never from
the plan, on every product.

## Type-size and layout QA

`lrender.py` checks every listing image programmatically and refuses to pass one that
breaks the spec. Result for all 10 images:

- All content inside the 1600x2000 centre safe zone (x from 200 to 1800)
- No vertical overflow beyond the 2000px canvas
- Smallest rendered text: **34px** on a 2000px canvas, against a floor of 28px
- Product name on the hero: 300px, against a floor of 200px

Print files were checked separately for horizontal overflow and page fill:

| File | Page fill | Overflow |
|---|---|---|
| 18x24 poster | 98.7% | none |
| Letter verb page | 97.3% | none |
| Letter reference page | 93.4% | none |
| A4 verb page | 92.1% | none |
| A4 reference page | 96.4% | none |

## Reproducing this build

```
pip install verbecc --break-system-packages
python3 _source_data/extract.py     # writes conjugations.json, asserts predicted=False
python3 _source_data/verify.py      # independent diff, must print 0 mismatches
python3 _source_data/gen.py 1.075 1.075 1.24
python3 _source_data/listing.py
```

## Limits

- verbecc's Spanish dictionary is the single upstream source for the forms; the independent
  derivation checks the regular paradigms only. Irregular verbs, which product A4 will
  cover, cannot be checked this way and need a different second source (Wiktionary
  conjugation tables were the plan).
- The chart covers regular verbs. It does not claim to cover irregulars, and the listing
  copy does not imply it does.
