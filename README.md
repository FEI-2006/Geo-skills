# geo-skills

[中文](README_CN.md)

Reusable AI agent skills for remote sensing, GIS and geography research: publication-ready figures and journal-style English for geoscience papers.

Each skill is a folder with a `SKILL.md` (the instructions an agent follows) plus references and templates. They work with Claude, Codex and other agents that read `SKILL.md` files.

## Skills

| Skill | Status | What it does |
|---|---|---|
| [geo-figure](skills/geo-figure) | Beta | Maps and charts sized and styled for Elsevier, IEEE, Taylor & Francis and MDPI journals, with Python templates |
| [geo-polishing](skills/geo-polishing) | Draft | Polishes or translates manuscript text into clear geoscience English, with a Chinese–English terminology glossary |

Status labels: **Draft** = rules written, not yet tested on real cases; **Beta** = tested on examples; **Stable** = used on real academic work.

![Example map from geo-figure](skills/geo-figure/examples/example_map.png)

## Design principles

1. **Never change the science.** Skills do not invent data, results or citations, and flag problems instead of silently fixing them.
2. **Follow the journal.** Sizes, resolutions and style rules come from publisher guidelines, cited in the references.
3. **Output first.** Each skill ends with something usable: a figure file, polished text, a checklist.
4. **Self-contained.** Each skill folder works on its own.

## Install

**Claude (app or claude.ai):** zip a skill folder (for example `skills/geo-figure`) and upload it under Settings → Capabilities → Skills.

**Claude Code:** copy the folders into your skills directory:

```bash
git clone https://github.com/FEI-2006/geo-skills.git
cp -r geo-skills/skills/* ~/.claude/skills/
```

**Other agents (Codex, etc.):** copy the whole skill folder into the agent's skills or prompts directory. Keep the `references/` and `templates/` subfolders.

## Roadmap

- geo-reviewer: simulated peer review against RSE / TGRS / IJGIS criteria
- geo-gvi: standardized street-view green view index workflow
- geo-data-statement: data availability and code availability statements

## Contributing

Issues and pull requests are welcome. A new skill needs a `SKILL.md`, an English and a Chinese README, and a row in the table above.

## License

[MIT](LICENSE) © 2026 Xiaoyan Fei
