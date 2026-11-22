"""Checks for the Geo-Skills repository.

Run from the repository root:
    python -m pytest tests        (or)        python tests/test_skills.py
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
TEMPLATES = SKILLS / "geo-figure" / "templates"


def skill_dirs():
    return sorted(p for p in SKILLS.iterdir() if p.is_dir())


def test_every_skill_has_required_files():
    for d in skill_dirs():
        for f in ("SKILL.md", "README.md", "README_CN.md"):
            assert (d / f).is_file(), f"{d.name} is missing {f}"


def test_frontmatter_name_matches_folder_and_has_description():
    for d in skill_dirs():
        text = (d / "SKILL.md").read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        assert m, f"{d.name}: SKILL.md has no frontmatter"
        fm = dict(line.split(":", 1) for line in m.group(1).splitlines() if ":" in line)
        assert fm.get("name", "").strip() == d.name, f"{d.name}: name field must equal folder name"
        desc = fm.get("description", "").strip()
        assert 50 < len(desc) <= 1024, f"{d.name}: description should be 50-1024 characters"


def test_referenced_files_exist():
    for d in skill_dirs():
        text = (d / "SKILL.md").read_text(encoding="utf-8")
        for ref in re.findall(r"`((?:references|templates)/[^`]+)`", text):
            assert (d / ref).exists(), f"{d.name}: SKILL.md mentions missing file {ref}"


def test_skills_listed_in_root_readmes():
    for readme in ("README.md", "README_CN.md"):
        text = (ROOT / readme).read_text(encoding="utf-8")
        for d in skill_dirs():
            assert f"skills/{d.name}" in text, f"{readme} does not list {d.name}"


def _run_template(name: str, tmp: str) -> str:
    env = dict(os.environ, MPLBACKEND="Agg", PYTHONPATH=str(TEMPLATES))
    out = subprocess.run([sys.executable, str(TEMPLATES / name)], cwd=tmp, env=env,
                         capture_output=True, text=True, timeout=300)
    assert out.returncode == 0, out.stderr
    return out.stdout


def test_map_template_runs_and_passes_its_own_check():
    with tempfile.TemporaryDirectory() as tmp:
        stdout = _run_template("geo_map.py", tmp)
        assert "'pass': True" in stdout, stdout
        assert (Path(tmp) / "example_map.pdf").stat().st_size > 10_000


def test_chart_template_runs_and_passes_its_own_check():
    with tempfile.TemporaryDirectory() as tmp:
        stdout = _run_template("geo_chart.py", tmp)
        assert "'pass': True" in stdout, stdout
        assert (Path(tmp) / "example_chart.pdf").stat().st_size > 10_000


def test_check_figure_catches_problems():
    sys.path.insert(0, str(TEMPLATES))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from geo_map import check_figure, fig_size_mm

    fig, ax = plt.subplots(figsize=fig_size_mm(120))
    ax.plot([0, 1], [0, 1])
    ax.text(0.5, 0.5, "tiny", fontsize=4)
    result = check_figure(fig, target_width_mm=90)
    assert not result["pass"]
    joined = " ".join(result["issues"])
    assert "Width" in joined and "below" in joined and "no axis label" in joined
    plt.close(fig)


def test_scatter_statistics_are_correct():
    sys.path.insert(0, str(TEMPLATES))
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from geo_chart import scatter_1to1

    fig, ax = plt.subplots()
    obs = np.array([1.0, 2.0, 3.0, 4.0])
    stats = scatter_1to1(ax, obs, obs + 1.0, units="m")
    assert stats["n"] == 4
    assert abs(stats["rmse"] - 1.0) < 1e-9
    assert abs(stats["r2"] - (1 - 4 / 5)) < 1e-9
    plt.close(fig)


if __name__ == "__main__":
    failures = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except AssertionError as e:
                failures += 1
                print(f"FAIL {name}: {e}")
    sys.exit(1 if failures else 0)
