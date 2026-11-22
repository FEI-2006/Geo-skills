# geo-skills

[English](README.md)

面向遥感、GIS 和地理学研究的 AI 技能包：帮你做出达到投稿标准的科研图表，并把论文写成符合地学期刊风格的英文。

每个技能是一个文件夹，里面有 `SKILL.md`（AI 执行时遵循的规则）以及参考资料和模板。适用于 Claude、Codex 等能读取 `SKILL.md` 的 AI 工具。

## 技能列表

| 技能 | 状态 | 功能 |
|---|---|---|
| [geo-figure](skills/geo-figure) | Beta | 按 Elsevier、IEEE、Taylor & Francis、MDPI 期刊要求制作地图和图表，附 Python 模板 |
| [geo-polishing](skills/geo-polishing) | Draft | 把论文润色或翻译成清晰的地学英文，附遥感与 GIS 中英术语表 |

状态说明：**Draft** = 规则已写好，尚未用真实案例测试；**Beta** = 已用示例测试；**Stable** = 已用于真实学术工作。

## 设计原则

1. **不改动科学内容。** 不编造数据、结果或引用；发现问题时指出来，而不是悄悄改掉。
2. **以期刊要求为准。** 尺寸、分辨率和写作规范都来自出版社的官方指南，并在参考资料中注明出处。
3. **以产出为先。** 每个技能最后都会给出能直接使用的东西：图片文件、润色后的文本或检查清单。
4. **独立完整。** 每个技能文件夹都可以单独使用。

## 安装方法

**Claude（桌面应用或 claude.ai）：** 把某个技能文件夹（例如 `skills/geo-figure`）压缩成 zip，在"设置 → 功能 → 技能"中上传。

**Claude Code：** 把文件夹复制到技能目录：

```bash
git clone https://github.com/FEI-2006/geo-skills.git
cp -r geo-skills/skills/* ~/.claude/skills/
```

**其他 AI 工具（Codex 等）：** 把整个技能文件夹复制到该工具的技能或提示词目录，记得保留 `references/` 和 `templates/` 子文件夹。

## 后续计划

- geo-reviewer：按 RSE / TGRS / IJGIS 标准模拟审稿
- geo-gvi：标准化的街景绿视率计算流程
- geo-data-statement：数据与代码可用性声明

## 参与贡献

欢迎提交 Issue 和 Pull Request。新技能需要包含 `SKILL.md`、中英文 README，并在上方表格中加入一行。

## 许可证

[MIT](LICENSE) © 2026 Xiaoyan Fei
