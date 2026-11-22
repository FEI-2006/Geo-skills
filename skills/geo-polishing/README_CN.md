# geo-polishing

[English](README.md)

**状态：Draft**（规则已写好，尚未在完整论文上验证）

把遥感、GIS 和地理学论文的中文或初稿英文，润色、重组或翻译成符合地学期刊风格的清晰英文，同时**不改动**作者的数字、结论和引用。

## 输出内容

1. 润色后的文本，可以直接粘贴
2. 修改对照表：原文 → 修改后 → 原因
3. 给作者的问题：文中含糊、缺少依据或前后不一致的地方

## 示例

**输入**

> 随着城市化的快速发展，城市绿地在改善空气质量方面发挥着越来越重要的作用。本文以芝加哥为研究区，利用谷歌街景影像计算绿视率，结果表明绿视率和PM2.5浓度呈显著负相关（r=-0.42）。

**输出**

> Urban green space can help improve air quality. Using Chicago as the study area, we calculated the green view index (GVI) from Google Street View (GSV) imagery. GVI was negatively correlated with PM₂.₅ concentration (r = −0.42, p [value needed]).

同时会附上修改对照表，并提出问题：p 值和样本量是多少？"显著"是否经过统计检验？这句话是否需要引用前人关于绿地与 PM₂.₅ 的研究？

## 文件说明

```
geo-polishing/
├── SKILL.md                     # AI 执行时遵循的规则和流程
├── references/style-rules.md    # 各章节写作惯例与用词建议
└── references/glossary.md       # 遥感与 GIS 中英术语对照表
```

## 关于 AI 使用声明

很多期刊要求作者声明是否使用 AI 进行语言润色。本技能用于提升表达清晰度，不会帮忙隐藏 AI 的使用，也不会替作者编写研究结果。
