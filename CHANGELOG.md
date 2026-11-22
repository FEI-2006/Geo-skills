# Changelog

## 0.2.0 — 2026-11-22

### geo-figure
- Added `check_figure()`: flags a width that does not match the journal column, text below 6 pt, and axes or colorbars without labels.
- Added `plot_vector()` for GeoDataFrames (geopandas optional).
- Added `references/captions.md` with caption structure and templates.
- Workflow now includes an automatic check step and a caption step; added common requests.

### geo-polishing
- Added `references/examples.md` with worked abstract, methods and results examples.
- Added four modes (light edit, standard polish, translate, shorten), a fixed output format and a self-check step.

### Repository
- Renamed the project title to Geo-Skills.
- Added tests (`tests/`), a GitHub Actions workflow, upload-ready ZIPs in `dist/` with `scripts/package_skills.py`, `CONTRIBUTING.md` and a skill template.
- Corrected the Claude install instructions.

## 0.1.0 — 2026-11-22

- First release with geo-figure (Beta) and geo-polishing (Draft).
