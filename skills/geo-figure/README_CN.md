# geo-figure

[English](README.md)

**状态：Beta**（已用模拟数据测试，尚未用于真实投稿）

用 Python 为遥感、GIS 和地理学论文制作达到投稿标准的地图和图表。它会按期刊栏宽设定图片尺寸，统一配色、单位和标注规范，最后逐项检查并列出需要修改的地方。

## 能做什么

- 研究区地图：比例尺、指北针、经纬度坐标和位置示意小图
- 连续栅格图（NDVI、温度、PM2.5 等），无效值自动透明
- 分类图和语义分割结果图：类别边界清晰，附图例
- 时间序列图：使用真实日期，缺测时段断开不连线
- 预测值与观测值散点图：1:1 线，并自动计算 n、R² 和 RMSE
- 精度指标分组柱状图（OA、F1、mIoU）
- Elsevier、IEEE、Taylor & Francis、MDPI 期刊的图片宽度与分辨率要求
- 自动检查（`check_figure`）：图片宽度、最小字号，以及坐标轴或色带是否缺少标注
- 地图、分割结果和精度图的图注（caption）模板

## 文件说明

```
geo-figure/
├── SKILL.md                     # AI 执行时遵循的规则和流程
├── references/journal-specs.md  # 各出版社的栏宽与 dpi 要求
├── references/captions.md       # 图注写法与模板
├── templates/geo_map.py         # 地图工具函数（只需 numpy + matplotlib）
├── templates/geo_chart.py       # 图表工具函数（numpy + pandas + matplotlib）
└── examples/                    # 两个模板生成的示例图
```

## 示例

运行 `python templates/geo_map.py` 和 `python templates/geo_chart.py` 会生成 `examples/` 里的示例图（使用模拟数据）。

## 环境要求

Python 3.9 以上，需要 numpy、pandas 和 matplotlib。rasterio、xarray、geopandas 为可选，工具函数可以直接使用它们读出的数组和范围。
