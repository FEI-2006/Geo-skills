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
LEGEND_TEMPLATES = SKILLS / "geo-legend" / "templates"


def skill_dirs():
    return sorted(p for p in SKILLS.iterdir() if p.is_dir())


def test_every_skill_has_required_files():
    for d in skill_dirs():
        for f in ("SKILL.md", "README.md"):  # README_CN.md is optional
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


def _legend_mod():
    sys.path.insert(0, str(LEGEND_TEMPLATES))
    import matplotlib
    matplotlib.use("Agg")
    import legend_layout
    return legend_layout


def test_legend_template_runs_and_passes_its_own_check():
    with tempfile.TemporaryDirectory() as tmp:
        env = dict(os.environ, MPLBACKEND="Agg")
        out = subprocess.run([sys.executable, str(LEGEND_TEMPLATES / "legend_layout.py")], cwd=tmp,
                             env=env, capture_output=True, text=True, timeout=300)
        assert out.returncode == 0, out.stderr
        assert out.stdout.count("'pass': True") == 2, out.stdout
        for name in ("example_legend_single.png", "example_legend_shared.png"):
            assert (Path(tmp) / name).stat().st_size > 10_000


def test_auto_ncol_uses_more_columns_when_there_is_room():
    ll = _legend_mod()
    labels = ["Forest", "Cropland", "Urban", "Water", "Bare soil"]
    assert ll.auto_ncol(labels, 7.0) == 5
    assert ll.auto_ncol(labels, 2.0) < 5
    assert ll.auto_ncol(labels, 0.5) == 1


def test_place_legend_avoids_data_corners():
    ll = _legend_mod()
    import matplotlib.pyplot as plt
    import numpy as np
    rng = np.random.default_rng(0)
    fig, ax = plt.subplots(figsize=(4, 3))
    # data fill the upper right and lower left; the upper left and lower right are empty
    ax.scatter(8 + rng.random(50), 8 + rng.random(50), label="A", s=6)
    ax.scatter(1 + rng.random(50), 1 + rng.random(50), label="B", s=6)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    leg, where = ll.place_legend(ax)
    assert where in ("inside:upper left", "inside:lower right"), where
    assert ll.check_legends(fig)["pass"]
    plt.close(fig)


def test_place_legend_goes_outside_when_no_space():
    ll = _legend_mod()
    import matplotlib.pyplot as plt
    import numpy as np
    fig, ax = plt.subplots(figsize=(4, 3), constrained_layout=True)
    x = np.linspace(0, 10, 400)
    for k in range(4):
        ax.plot(x, 5 + 4 * np.sin(x + k) * np.cos(3 * x), label=f"Series {k}")
        ax.scatter(np.random.default_rng(k).random(300) * 10, np.random.default_rng(k + 9).random(300) * 10, s=2)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    leg, where = ll.place_legend(ax)
    assert where == "outside:below", where
    assert ll.check_legends(fig)["pass"]
    plt.close(fig)


def test_shared_legend_keeps_figure_size_in_both_layout_modes():
    ll = _legend_mod()
    import matplotlib.pyplot as plt
    for constrained in (True, False):
        fig, axs = plt.subplots(1, 3, figsize=(7.5, 2.4), constrained_layout=constrained)
        for k, ax in enumerate(axs):
            for name in ("U-Net", "SegFormer", "Random forest"):
                ax.plot([0, 1, 2], [0, 1 + k, 2], label=name)
            ax.set_xlabel("Epoch")
            ax.set_ylabel("mIoU (-)")
            ax.legend()
        ll.remove_axes_legends(axs)
        handles, labels = ll.collect_handles(axs)
        assert labels == ["U-Net", "SegFormer", "Random forest"]  # de-duplicated
        ll.legend_outside(fig, handles, labels, side="below")
        assert abs(fig.get_figwidth() - 7.5) < 1e-9 and abs(fig.get_figheight() - 2.4) < 1e-9
        result = ll.check_legends(fig)
        assert result["pass"], (constrained, result)
        plt.close(fig)


def test_check_legends_catches_problems():
    ll = _legend_mod()
    import matplotlib.pyplot as plt
    import numpy as np
    fig, axs = plt.subplots(1, 2, figsize=(6, 3))
    x = np.linspace(0, 1, 50)
    for ax in axs:
        for k in range(12):
            ax.plot(x, x * 0.1 * k, label=f"Class {k}")
        ax.legend(loc="center", fontsize=4)
    result = ll.check_legends(fig)
    assert not result["pass"]
    joined = " ".join(result["issues"])
    assert "entries" in joined and "covers" in joined and "identical legends" in joined and "pt" in joined
    plt.close(fig)


def test_direct_labels_do_not_overlap():
    ll = _legend_mod()
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(4, 3), constrained_layout=True)
    for name, y in (("A", 1.00), ("B", 1.01), ("C", 1.02)):  # nearly identical end values
        ax.plot([0, 1], [0, y], label=name)
    texts = ll.direct_labels(ax)
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    boxes = sorted((t.get_window_extent(r) for t in texts), key=lambda b: b.y0)
    for lower, upper in zip(boxes, boxes[1:]):
        assert upper.y0 >= lower.y1 - 0.5
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
