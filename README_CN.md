# Geo-Skills

[![tests](https://github.com/FEI-2006/geo-skills/actions/workflows/tests.yml/badge.svg)](https://github.com/FEI-2006/geo-skills/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Skills: 2](https://img.shields.io/badge/skills-2-green.svg)

[English](README.md)

面向遥感、GIS 和地理学研究的 AI 技能包：帮你做出达到投稿标准的科研图表，并把论文写成符合地学期刊风格的英文。

每个技能是一个文件夹，里面有 `SKILL.md`（AI 执行时遵循的规则）以及参考资料和模板。适用于 Claude、Codex 等能读取 `SKILL.md` 的 AI 工具。

## 技能列表

| 技能 | 状态 | 功能 |
|---|---|---|
| [geo-figure](skills/geo-figure) | Beta | 按 Elsevier、IEEE、Taylor & Francis、MDPI 期刊要求制作地图和图表；附 Python 模板、尺寸与标注自动检查，以及图注模板 |
| [geo-polishing](skills/geo-polishing) | Draft | 把论文润色或翻译成清晰的地学英文，不改动数字和结论；四种模式、完整示例，以及中英术语表 |

状态说明：**Draft** = 规则已写好，尚未用真实案例测试；**Beta** = 已用示例测试；**Stable** = 已用于真实学术工作。

## 设计原则

1. **不改动科学内容。** 不编造数据、结果或引用；发现问题时指出来，而不是悄悄改掉。
2. **以期刊要求为准。** 尺寸、分辨率和写作规范都来自出版社的官方指南，并在参考资料中注明出处。
3. **以产出为先。** 每个技能最后都会给出能直接使用的东西：图片文件、润色后的文本或检查清单。
4. **独立完整。** 每个技能文件夹都可以单独使用。

## 安装方法

**Claude（网页版或桌面应用）**
1. 从 [`dist/`](dist) 下载做好的 ZIP：`geo-figure.zip` 或 `geo-polishing.zip`。
2. 确认"设置 → 功能（Capabilities）"里已开启代码执行与文件创建。
3. 进入"自定义（Customize）→ 技能（Skills）"，点 **+**，选择 **Create skill → Upload a skill**，上传 ZIP。

添加到 Claude 账号的技能，用同一账号登录 Claude Code 时也会自动加载。

**Claude Code（从仓库安装）**

```bash
git clone https://github.com/FEI-2006/geo-skills.git
cp -r geo-skills/skills/* ~/.claude/skills/
```

**其他 AI 工具（Codex 等）：** 把整个技能文件夹复制到该工具的技能或提示词目录，记得保留 `references/` 和 `templates/` 子文件夹。

## 仓库结构

```
skills/            每个技能一个文件夹（SKILL.md、说明文档、参考资料、模板）
dist/              可直接上传的 ZIP，用 scripts/package_skills.py 重新生成
tests/             检查技能结构，并实际运行绘图模板
template/SKILL.md  新技能的起始模板
```

## 开发与测试

```bash
pip install numpy pandas matplotlib pytest
python -m pytest -q tests          # 检查结构并运行两个绘图模板
python scripts/package_skills.py   # 重新生成 dist/*.zip
```

## 后续计划

- geo-reviewer：按 RSE / TGRS / IJGIS 标准模拟审稿
- geo-gvi：标准化的街景绿视率计算流程
- geo-data-statement：数据与代码可用性声明

## 参与贡献

请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)，更新记录见 [CHANGELOG.md](CHANGELOG.md)。

## 许可证

[MIT](LICENSE) © 2026 Xiaoyan Fei
