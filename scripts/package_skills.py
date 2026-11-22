"""Build upload-ready ZIP files for each skill.

Claude expects the skill folder itself at the top level of the ZIP
(<skill-name>/SKILL.md), so each archive is built from the skills/ folder.

    python scripts/package_skills.py          # writes dist/<skill-name>.zip
"""
from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {"__pycache__", ".DS_Store"}


def package(skill_dir: Path, out_dir: Path) -> Path:
    out_dir.mkdir(exist_ok=True)
    zip_path = out_dir / f"{skill_dir.name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(skill_dir.rglob("*")):
            if f.is_file() and not (set(f.parts) & SKIP) and f.suffix != ".pyc":
                zf.write(f, f.relative_to(skill_dir.parent))
    return zip_path


if __name__ == "__main__":
    for d in sorted((ROOT / "skills").iterdir()):
        if (d / "SKILL.md").is_file():
            p = package(d, ROOT / "dist")
            print(f"{p.relative_to(ROOT)}  ({p.stat().st_size / 1024:.0f} KB)")
