# Contributing to Geo-Skills

Thanks for helping. New skills and improvements to existing ones are both welcome.

## Adding a skill

1. Copy `template/SKILL.md` into `skills/geo-<name>/SKILL.md`. The folder name must equal the `name` field.
2. Write the `description` so an agent can tell when to use the skill: name the tasks and the words a user would say, and what the skill is not for (50–1024 characters).
3. Put long material (specs, glossaries, examples) in `references/` and code in `templates/`. Refer to them from `SKILL.md` with their relative paths.
4. Add `README.md` (English) and `README_CN.md` (Chinese) with a status label, what it does, an example and the file list.
5. Add a row to the skills table in both root READMEs.
6. Run the checks and rebuild the ZIPs:

```bash
python -m pytest -q tests
python scripts/package_skills.py
```

## Status labels

- **Draft**: rules written, not yet tested on real cases
- **Beta**: tested on examples (include them in the skill folder)
- **Stable**: used on real academic work; say what in the pull request

## Ground rules for every skill

- Never invent data, results or citations, and never strengthen the author's claims.
- Flag problems for the user instead of fixing them silently.
- Cite the source for any journal requirement or standard you encode.
- Keep each skill self-contained.
