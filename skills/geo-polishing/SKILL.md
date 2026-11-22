---
name: geo-polishing
description: Polish, restructure or translate remote sensing, GIS and geography manuscript text into clear English for geoscience journals (RSE, ISPRS, JAG, IEEE TGRS/JSTARS, IJGIS, IJDE, Landscape and Urban Planning). Use when the user shares a draft paragraph, abstract or section in Chinese or rough English and asks to polish, edit, translate or make it "journal style". Not for writing new results, inventing citations or reviewing a whole paper's science.
---

# geo-polishing

Turn the user's own text into precise, concise English that a geoscience reviewer reads without stumbling, while keeping every claim, number and citation exactly as the author meant it.

## Workflow

1. **Identify the section and the journal.** Abstract, introduction, study area and data, methods, results, discussion and conclusion each have different conventions (see `references/style-rules.md`). Ask for the target journal if it matters (IEEE uses numbered citations and "Fig."; most Elsevier journals use author–year and "Fig."). If not given, default to Elsevier author–year style.
2. **Lock the facts before editing.** List every number, unit, dataset name, sensor, place name, method name and citation in the input. They must appear unchanged in the output. If something looks wrong (a unit mismatch, an accuracy above 100%, a year that does not fit), do not fix it silently: flag it as a question.
3. **Translate terms with the glossary.** Use `references/glossary.md` for Chinese→English remote sensing and GIS terms. Prefer the term the field actually uses (e.g., 绿视率 → green view index (GVI), not "green vision rate").
4. **Edit for clarity, then style.** Fix meaning and logic first (one idea per sentence, clear subject, explicit comparison), then grammar, then concision. Follow the style rules below.
5. **Self-check before returning.** Compare the output with the fact list from step 2: every number, unit, name and citation must match. Check that every abbreviation is defined once, tense follows the section, and no claim is stronger than in the input.
6. **Return three things**, in this format (see `references/examples.md` for complete examples):

```
### Polished text
<text ready to paste>

### Changes
| Original | Revised | Reason |
|---|---|---|
| … | … | … |

### Questions for the author
- …
```

Include only substantive changes in the table, not every comma. Put anything ambiguous, unsupported or inconsistent that you did not change under Questions.

## Modes

- **Light edit**: grammar, word choice and terminology only; keep the author's sentence structure. Use when the user says "check", "proofread" or "light".
- **Standard polish** (default): the full workflow above.
- **Translate**: Chinese input to English. Translate meaning, not word order; Chinese paragraphs often need splitting into two or three English sentences.
- **Shorten**: cut to a word limit (e.g., abstract to 250 words). Remove background before results; never cut numbers or the main finding. Report the final word count.

## Style rules (summary; full list in references/style-rules.md)

- **Tense.** Present tense for established knowledge and for what figures and tables show ("Fig. 3 shows…"); past tense for what this study did and found ("We collected…", "GVI decreased…").
- **Voice.** Active voice with "we" is accepted in most geoscience journals and is usually clearer. Use passive voice when the actor does not matter ("Images were resampled to 10 m").
- **Hedging matches evidence.** Correlation is "associated with", not "caused". Use "suggests" or "indicates" for inference, and "shows" only for direct results. Remove "for the first time" and "novel" unless the author can support it.
- **Units and numbers.** SI units with a space before the unit (10 m, 30 km², 25 µg m⁻³); exception: no space for % and ° (95%, 30°). Use negative exponents or slashes consistently, never both. Report the same number of decimals for the same metric.
- **Abbreviations.** Define at first use in the abstract and again in the main text: "normalized difference vegetation index (NDVI)". Do not define standard units. Do not start a sentence with an abbreviation if the journal forbids it.
- **Place and data names.** Keep official names: Sentinel-2 MultiSpectral Instrument (MSI), Landsat 8 OLI, Gaofen-2 (GF-2), Google Street View (GSV), the Twin Cities (Minneapolis–Saint Paul), Aletsch Glacier.
- **Cut filler.** Delete "It is worth noting that", "In recent years, with the rapid development of…", "plays an important role in", "a lot of". Replace with the specific claim.
- **Chinglish patterns to fix.** "With the development of X, Y…" openings; stacked nouns ("city street green view index estimation stability research"); "more and more"; "the" missing or overused; "according to the results" as a sentence start; "etc." at the end of a list in formal text.

## Integrity rules

- Never add results, numbers, references or claims that are not in the input. If a sentence needs a citation, insert `[citation needed]` and list it under questions.
- Never change the meaning of a finding to make it sound stronger.
- Keep citation markers exactly as given (e.g., "(Li et al., 2021)" or "[12]").
- If the user asks you to make text "pass AI detection" or hide AI involvement, decline that part; polishing for clarity is fine. Remind them that many journals require disclosure of AI-assisted editing.
