# geo-polishing

[中文](README_CN.md)

**Status: Draft** (rules written; not yet validated on a full manuscript)

Polishes, restructures or translates remote sensing, GIS and geography manuscript text into clear English for geoscience journals, without changing the author's numbers, claims or citations.

## What you get back

1. The polished text, ready to paste
2. A change table: original → revised → reason
3. Questions for the author about anything ambiguous, unsupported or inconsistent

Four modes: **light edit** (grammar and terms only), **standard polish** (default), **translate** (Chinese to English) and **shorten** (cut to a word limit without losing numbers or the main finding).

## Example

**Input**

> 随着城市化的快速发展，城市绿地在改善空气质量方面发挥着越来越重要的作用。本文以芝加哥为研究区，利用谷歌街景影像计算绿视率，结果表明绿视率和PM2.5浓度呈显著负相关（r=-0.42）。

**Output**

> Urban green space can help improve air quality. Using Chicago as the study area, we calculated the green view index (GVI) from Google Street View (GSV) imagery. GVI was negatively correlated with PM₂.₅ concentration (r = −0.42, p [value needed]).

| Original | Revised | Reason |
|---|---|---|
| 随着城市化的快速发展…发挥着越来越重要的作用 | Urban green space can help improve air quality. | Removes a generic opening; keeps the claim |
| 绿视率 | green view index (GVI) | Standard term, abbreviation defined at first use |
| 显著负相关 | negatively correlated … p [value needed] | "Significant" needs the test result |

Questions: What is the p value and sample size? Is "significant" from a statistical test? Should this sentence cite earlier work on green space and PM₂.₅?

## Files

```
geo-polishing/
├── SKILL.md                     # instructions the AI agent follows
├── references/style-rules.md    # section-by-section conventions and word choice
├── references/glossary.md       # Chinese → English remote sensing and GIS terms
└── references/examples.md       # worked examples: abstract, methods, results
```

## Note on AI disclosure

Many journals ask authors to disclose AI-assisted language editing. This skill improves clarity; it does not hide AI involvement or write results.
