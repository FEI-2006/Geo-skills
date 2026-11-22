# Worked examples

Each example shows the input, the polished output, the change table and the questions for the author. The inputs are invented for illustration.

---

## 1. Abstract (Chinese → English)

**Input**

> 冰裂隙是冰川动力过程的重要指示，但目前对阿尔卑斯山地冰川裂隙的大范围自动提取研究还比较少。本文提出了一种基于深度学习的方法，利用Sentinel-2影像对阿莱奇冰川的冰裂隙进行提取，并分析了2017年到2023年冰裂隙面积的变化。结果表明，该方法的F1值达到0.87，冰裂隙面积增加了12.4%。本研究可以为冰川变化监测提供参考。

**Output**

> Crevasses are key indicators of glacier dynamics, yet few studies have mapped them automatically over large areas of Alpine mountain glaciers. We developed a deep-learning method to extract crevasses from Sentinel-2 imagery of the Aletsch Glacier and analysed changes in crevasse area from 2017 to 2023. The method achieved an F1 score of 0.87, and the total crevasse area increased by 12.4% over the study period. These results show that Sentinel-2 imagery can support repeatable, glacier-wide monitoring of crevasse change.

| Original | Revised | Reason |
|---|---|---|
| 重要指示 | key indicators | Concise; "important indication" is weaker |
| 本文提出了 | We developed | Active voice; "this paper proposes" is wordy |
| F1值达到0.87 | achieved an F1 score of 0.87 | Standard metric phrasing |
| 本研究可以为…提供参考 | These results show that … | Replaces a vague closing with the actual implication |

**Questions for the author**
- Is the 12.4% increase relative to the 2017 area? Please confirm the baseline.
- Which spatial resolution did you use (10 m bands only)? Reviewers will ask, because crevasses narrower than about 10 m are hard to detect.
- Was the F1 score computed at pixel or object level?

---

## 2. Methods (rough English → English)

**Input**

> Firstly, we download the street view images from Google by API, totally 12,000 images. Then the images are segmented by the DeepLabV3+ model which is pretrained on Cityscapes dataset, and the GVI is calculated by the ratio of green pixels and all pixels.

**Output**

> We downloaded 12,000 street view images through the Google Street View Static API. Each image was segmented with a DeepLabV3+ model pretrained on the Cityscapes dataset, and the green view index (GVI) was calculated as the proportion of vegetation pixels to all pixels in an image.

| Original | Revised | Reason |
|---|---|---|
| Firstly, we download | We downloaded | Past tense for methods; "Firstly" is unnecessary |
| from Google by API | through the Google Street View Static API | Name the actual product |
| totally 12,000 images | 12,000 street view images | "Totally" is not used this way in English |
| green pixels | vegetation pixels | Segmentation classes are "vegetation" (and "terrain"), not "green" |
| ratio of … and … | proportion of … to … | Correct construction |

**Questions for the author**
- Which Cityscapes classes count as vegetation (vegetation only, or vegetation + terrain)? State this, because it changes GVI.
- How many images per sampling point, at what headings and spacing, and from which years?
- Please cite DeepLabV3+ (Chen et al., 2018) and the source of the pretrained weights.

---

## 3. Results (Chinese → English)

**Input**

> 从图5可以明显看出，地下车站的PM2.5浓度远远高于地上车站，并且冬季比夏季更高，这说明地下环境导致了更严重的污染。

**Output**

> PM₂.₅ concentrations were higher at underground stations than at aboveground stations in both seasons, and higher in winter than in summer (Fig. 5). [Median or mean values with units needed.] This pattern is consistent with limited ventilation in underground environments, although the present data cannot isolate its cause.

| Original | Revised | Reason |
|---|---|---|
| 从图5可以明显看出 | … (Fig. 5) | Lead with the finding; put the figure reference at the end |
| 远远高于 | higher … [values needed] | "Much higher" needs numbers |
| 说明…导致了 | consistent with … cannot isolate its cause | Observational data support association, not causation |

**Questions for the author**
- What are the median (or mean) concentrations and their spread for each group and season?
- Was the difference tested statistically? If so, give the test and p value.
- Do you have ventilation or train-frequency data that would support the explanation? If not, keep the hedged wording.
