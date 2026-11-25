"""Legend and colorbar layout helpers for publication figures (matplotlib).

Self-contained: needs only numpy and matplotlib. Run directly for two example figures:
    python legend_layout.py

Main entry points
    place_legend()      one legend for one axes, in the emptiest corner or outside
    legend_outside()    one shared legend for the whole figure, below / above / right / left
    collect_handles()   merge and de-duplicate handles from several panels
    categorical_handles()  patches for classified maps (class_colors, class_names)
    direct_labels()     label lines at their right-hand end instead of using a legend
    add_colorbar()      colorbar that keeps the map's size and aligns with it
    check_legends()     report legends that cover data, overlap, run off the figure, etc.
"""
from __future__ import annotations

import math

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker  # noqa: F401  (used by the examples)
import numpy as np
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Patch
from matplotlib.transforms import Bbox

MM_PER_INCH = 25.4

# Preference order when several corners are equally empty
_CORNERS = ["upper right", "upper left", "lower right", "lower left",
            "upper center", "lower center", "center right", "center left"]


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------
def _fontsize(fontsize) -> float:
    """Resolve a size such as 7, 'small' or None (rcParams legend.fontsize) to points."""
    if fontsize is None:
        fontsize = mpl.rcParams["legend.fontsize"]
    return FontProperties(size=fontsize).get_size_in_points()


def _renderer(fig):
    fig.canvas.draw()
    return fig.canvas.get_renderer()


def _frac_bbox(fig, bbox_display: Bbox) -> Bbox:
    return bbox_display.transformed(fig.transFigure.inverted())


def _is_constrained(fig) -> bool:
    eng = fig.get_layout_engine()
    return eng is not None and type(eng).__name__ == "ConstrainedLayoutEngine"


def _left_title(leg):
    """Left-align the legend title with its entries (matplotlib centres it by default)."""
    try:
        leg._legend_box.align = "left"
    except AttributeError:  # private attribute; harmless if matplotlib changes it
        pass
    return leg


def collect_handles(axes):
    """Merge legend entries from several axes, keeping the first handle for each label.

    Entries whose label starts with an underscore are skipped (matplotlib convention).
    Returns (handles, labels). Remove the per-axes legends first with remove_axes_legends().
    """
    seen: dict = {}
    for ax in np.atleast_1d(axes).ravel():
        handles, labels = ax.get_legend_handles_labels()
        for h, lab in zip(handles, labels):
            if lab and not lab.startswith("_") and lab not in seen:
                seen[lab] = h
    return list(seen.values()), list(seen.keys())


def remove_axes_legends(axes) -> None:
    for ax in np.atleast_1d(axes).ravel():
        leg = ax.get_legend()
        if leg is not None:
            leg.remove()


def categorical_handles(class_colors: dict, class_names: dict):
    """Square colour patches for a classified or segmentation map, ordered by class value."""
    values = sorted(class_colors)
    handles = [Patch(facecolor=class_colors[v], edgecolor="black", linewidth=0.3) for v in values]
    return handles, [class_names[v] for v in values]


def auto_ncol(labels, avail_in: float, fontsize: float = 7, handle_in: float = 0.35,
              gap_in: float = 0.25) -> int:
    """Largest number of columns whose total width fits in `avail_in` inches.

    Width is estimated from label length (about 0.55 em per character), which is
    accurate enough to choose between 1, 2, 3... columns.
    """
    labels = [str(lab) for lab in labels]
    n = len(labels)
    if n == 0:
        return 1
    char_w = 0.55 * fontsize / 72.0
    widths = [len(lab) * char_w + handle_in + gap_in for lab in labels]
    for ncol in range(n, 0, -1):
        rows = math.ceil(n / ncol)
        cols = [widths[i * rows:(i + 1) * rows] for i in range(ncol)]
        if sum(max(c) for c in cols if c) <= avail_in:
            return math.ceil(n / rows)  # drop columns that would be empty
    return 1


# ---------------------------------------------------------------------------
# legends outside the axes (shared legends)
# ---------------------------------------------------------------------------
def _reserve_space(fig, leg, side: str, gap_mm: float = 2.0, rounds: int = 3) -> None:
    """Shift the subplot area so axes, tick labels and axis labels clear the legend."""
    gap = gap_mm / MM_PER_INCH
    for _ in range(rounds):
        r = _renderer(fig)
        lb = _frac_bbox(fig, leg.get_window_extent(r))
        boxes = [a.get_tightbbox(r) for a in fig.axes if a.get_visible()]
        tb = _frac_bbox(fig, Bbox.union(boxes))
        sp = fig.subplotpars
        gx, gy = gap / fig.get_figwidth(), gap / fig.get_figheight()
        if side == "below":
            need = lb.y1 + gy - tb.y0
            if need > 1e-4:
                fig.subplots_adjust(bottom=sp.bottom + need)
        elif side == "above":
            need = tb.y1 - (lb.y0 - gy)
            if need > 1e-4:
                fig.subplots_adjust(top=sp.top - need)
        elif side == "right":
            need = tb.x1 - (lb.x0 - gx)
            if need > 1e-4:
                fig.subplots_adjust(right=sp.right - need)
        elif side == "left":
            need = lb.x1 + gx - tb.x0
            if need > 1e-4:
                fig.subplots_adjust(left=sp.left + need)
        else:
            raise ValueError(f"unknown side {side!r}")


def legend_outside(fig, handles, labels, side: str = "below", ncol: int | None = None,
                   title: str | None = None, fontsize=None, frameon: bool = False, **kwargs):
    """One legend for the whole figure, placed outside the panels without changing figure size.

    side: 'below' (default for 2+ panels), 'above', 'right' or 'left'.
    Works with constrained layout (uses matplotlib's 'outside' locations) and with
    manual layout (shrinks the subplot area just enough). Below/above legends use as
    many columns as fit in the figure width; right/left legends use one column.
    """
    fs = _fontsize(fontsize)
    if ncol is None:
        ncol = auto_ncol(labels, 0.92 * fig.get_figwidth(), fs) if side in ("below", "above") else 1
    if _is_constrained(fig):
        loc = {"below": "outside lower center", "above": "outside upper center",
               "right": "outside center right", "left": "outside center left"}[side]
        return _left_title(fig.legend(handles, labels, loc=loc, ncol=ncol, title=title,
                                      frameon=frameon, fontsize=fs, title_fontsize=fs, **kwargs))
    loc, anchor = {"below": ("lower center", (0.5, 0.0)), "above": ("upper center", (0.5, 1.0)),
                   "right": ("center right", (1.0, 0.5)), "left": ("center left", (0.0, 0.5))}[side]
    leg = _left_title(fig.legend(handles, labels, loc=loc, bbox_to_anchor=anchor, ncol=ncol, title=title,
                                 frameon=frameon, fontsize=fs, title_fontsize=fs, borderaxespad=0.2,
                                 **kwargs))
    _reserve_space(fig, leg, side)
    return leg


# ---------------------------------------------------------------------------
# legends inside one axes (auto placement)
# ---------------------------------------------------------------------------
def _data_points_display(ax, max_images_pts: int = 3000, include_images: bool = True) -> np.ndarray:
    """Sample of the places in `ax` that hold data, as an (N, 2) array in display pixels."""
    pts = []
    for line in ax.lines:
        xy = np.asarray(line.get_xydata(), dtype=float)
        xy = xy[np.isfinite(xy).all(axis=1)]
        if len(xy):
            if len(xy) > 2000:
                xy = xy[np.linspace(0, len(xy) - 1, 2000).astype(int)]
            pts.append(line.get_transform().transform(xy))
    for coll in ax.collections:
        off = np.asarray(coll.get_offsets(), dtype=float)
        if off.size:
            off = off[np.isfinite(off).all(axis=1)]
            pts.append(coll.get_offset_transform().transform(off))
        else:
            for path in coll.get_paths()[:300]:
                if len(path.vertices):
                    pts.append(coll.get_transform().transform(path.vertices))
    for patch in ax.patches:
        bb = patch.get_window_extent()
        gx, gy = np.meshgrid(np.linspace(bb.x0, bb.x1, 5), np.linspace(bb.y0, bb.y1, 5))
        pts.append(np.column_stack([gx.ravel(), gy.ravel()]))
    if include_images:
        for img in ax.images:
            arr = np.ma.masked_invalid(np.ma.asarray(img.get_array(), dtype=float))
            if arr.ndim != 2:
                continue
            l, r, b, t = img.get_extent()
            ny, nx = arr.shape
            step = max(1, int(math.sqrt(arr.size / max_images_pts)))
            ii, jj = np.mgrid[0:ny:step, 0:nx:step]
            ok = ~np.ma.getmaskarray(arr[ii, jj])
            xs = l + (jj[ok] + 0.5) / nx * (r - l)
            ys = t - (ii[ok] + 0.5) / ny * (t - b)  # origin='upper'
            if len(xs):
                pts.append(ax.transData.transform(np.column_stack([xs, ys])))
    return np.vstack(pts) if pts else np.empty((0, 2))


def _overlap_frac(box: Bbox, other: Bbox) -> float:
    w = min(box.x1, other.x1) - max(box.x0, other.x0)
    h = min(box.y1, other.y1) - max(box.y0, other.y0)
    if w <= 0 or h <= 0:
        return 0.0
    return (w * h) / max(box.width * box.height, 1e-9)


def place_legend(ax, handles=None, labels=None, loc: str = "auto", avoid=(), title: str | None = None,
                 ncol: int = 1, fontsize=None, on_overflow: str = "outside",
                 max_cover: float = 0.01, framealpha: float = 0.9, include_images: bool = True,
                 **kwargs):
    """Put the legend of one axes where it hides the least data.

    loc        'auto' tries the corners and edges and picks the one covering the fewest data
               points (lines, scatter points, bars and valid raster cells); or pass a
               matplotlib location such as 'upper left' to force it.
    avoid      boxes in axes fractions, (x0, y0, x1, y1), that must stay free: scale bar,
               north arrow, locator inset, panel label.
    on_overflow  what to do when every position covers more than `max_cover` of the data:
               'outside' (below the figure; default) or 'inside' (use the best corner anyway,
               with a semi-opaque frame; right for full-coverage rasters).
    Returns (legend, where) with where like 'inside:upper left' or 'outside:below'.
    """
    if handles is None or labels is None:
        handles, labels = ax.get_legend_handles_labels()
        keep = [(h, lab) for h, lab in zip(handles, labels) if lab and not lab.startswith("_")]
        handles, labels = [h for h, _ in keep], [lab for _, lab in keep]
    fs = _fontsize(fontsize)
    common = dict(ncol=ncol, title=title, fontsize=fs, title_fontsize=fs, frameon=True,
                  framealpha=framealpha, edgecolor="none", borderaxespad=0.4, **kwargs)
    if loc != "auto":
        return _left_title(ax.legend(handles, labels, loc=loc, **common)), f"inside:{loc}"

    fig = ax.figure
    r = _renderer(fig)
    pts = _data_points_display(ax, include_images=include_images)
    ax_box = ax.get_window_extent(r)
    avoid_boxes = [Bbox([[ax_box.x0 + a[0] * ax_box.width, ax_box.y0 + a[1] * ax_box.height],
                         [ax_box.x0 + a[2] * ax_box.width, ax_box.y0 + a[3] * ax_box.height]])
                   for a in avoid]
    scored = []
    for rank, cand in enumerate(_CORNERS):
        leg = ax.legend(handles, labels, loc=cand, **common)
        bb = leg.get_window_extent(r)
        leg.remove()
        n_in = int(((pts[:, 0] >= bb.x0) & (pts[:, 0] <= bb.x1) &
                    (pts[:, 1] >= bb.y0) & (pts[:, 1] <= bb.y1)).sum()) if len(pts) else 0
        blocked = sum(_overlap_frac(bb, a) for a in avoid_boxes)
        too_big = bb.width > ax_box.width or bb.height > ax_box.height
        scored.append((blocked > 0.02, too_big, n_in, rank, cand))
    scored.sort()
    blocked, too_big, n_in, _, best = scored[0]
    cover = n_in / max(len(pts), 1)
    if (blocked or too_big or cover > max_cover) and on_overflow == "outside":
        leg = legend_outside(fig, handles, labels, side="below", title=title, fontsize=fs)
        return leg, "outside:below"
    return _left_title(ax.legend(handles, labels, loc=best, **common)), f"inside:{best}"


# ---------------------------------------------------------------------------
# direct labels and colorbars
# ---------------------------------------------------------------------------
def direct_labels(ax, fontsize=None, pad_pt: float = 3.0, min_gap: float | None = None) -> list:
    """Label each line at its right-hand end instead of using a legend.

    Labels are spread apart vertically so they never overlap, and coloured like their line.
    Leave room on the right (constrained layout does this automatically). Best for 2-6
    lines that do not cross at the right edge; use a legend for more series or for markers.
    """
    fs = _fontsize(fontsize)
    r = _renderer(ax.figure)
    inv = ax.transAxes.inverted()
    items = []
    for line in ax.lines:
        lab = line.get_label()
        xy = np.asarray(line.get_xydata(), dtype=float)
        ok = np.isfinite(xy).all(axis=1)
        if not lab or lab.startswith("_") or not ok.any():
            continue
        last = xy[ok][-1]
        y_frac = inv.transform(line.get_transform().transform(last))[1]
        items.append([float(np.clip(y_frac, 0.0, 1.0)), lab, line.get_color()])
    items.sort(key=lambda t: t[0])
    gap = min_gap if min_gap is not None else 1.4 * fs / 72.0 / (ax.get_window_extent(r).height / ax.figure.dpi)
    for i in range(1, len(items)):  # push up, then pull back down from the top
        items[i][0] = max(items[i][0], items[i - 1][0] + gap)
    if items and items[-1][0] > 1.0:
        items[-1][0] = 1.0
        for i in range(len(items) - 2, -1, -1):
            items[i][0] = min(items[i][0], items[i + 1][0] - gap)
    texts = []
    for y, lab, color in items:
        texts.append(ax.annotate(lab, xy=(1.0, y), xycoords="axes fraction", xytext=(pad_pt, 0),
                                 textcoords="offset points", va="center", ha="left", color=color,
                                 fontsize=fs, annotation_clip=False))
    return texts


def add_colorbar(fig, ax, mappable, label: str, location: str = "bottom", shrink: float = 0.7,
                 extend: str = "neither", ticks=None):
    """Colorbar that stays out of the map and lines up with it.

    location 'bottom' (horizontal, usually best for wide maps and for several panels) or
    'right' (vertical, best for tall maps). `label` should hold the variable and units.
    """
    cb = fig.colorbar(mappable, ax=ax, location=location, shrink=shrink, extend=extend,
                      ticks=ticks, pad=0.03, fraction=0.05 if location == "bottom" else 0.045,
                      aspect=30 if location == "bottom" else 22)
    cb.set_label(label)
    cb.outline.set_linewidth(0.5)
    return cb


# ---------------------------------------------------------------------------
# automatic check
# ---------------------------------------------------------------------------
def check_legends(fig, max_entries: int = 10, min_font_pt: float = 6.0, max_cover: float = 0.02,
                  max_area_frac: float = 0.25, include_images: bool = False) -> dict:
    """Check every legend in a finished figure. Returns {'pass': bool, 'issues': [...]}.

    Flags: legend off the figure, over another legend or over axes content, covering more
    than `max_cover` of the data, taking more than `max_area_frac` of its axes, text below
    `min_font_pt`, more than `max_entries` entries, repeated labels, and identical legends
    in several panels (use one shared legend). Raster cells are ignored unless
    include_images=True because legends on full-coverage rasters are expected to sit on them.
    """
    issues = []
    r = _renderer(fig)
    entries = []  # (name, legend, owner axes or None)
    for i, leg in enumerate(fig.legends):
        entries.append((f"Figure legend {i}", leg, None))
    for i, ax in enumerate(fig.axes):
        if ax.get_legend() is not None:
            entries.append((f"Legend on axes {i}", ax.get_legend(), ax))

    for name, leg, ax in entries:
        bb = leg.get_window_extent(r)
        if bb.x0 < fig.bbox.x0 - 1 or bb.y0 < fig.bbox.y0 - 1 or bb.x1 > fig.bbox.x1 + 1 or bb.y1 > fig.bbox.y1 + 1:
            issues.append(f"{name} runs off the figure edge.")
        texts = leg.get_texts()
        if len(texts) > max_entries:
            issues.append(f"{name} has {len(texts)} entries (more than {max_entries}); merge or group "
                          f"classes, use a colorbar for continuous data, or label the data directly.")
        labs = [t.get_text() for t in texts]
        if len(set(labs)) < len(labs):
            issues.append(f"{name} repeats a label.")
        small = [t.get_fontsize() for t in texts if t.get_fontsize() < min_font_pt]
        if small:
            issues.append(f"{name} text is {min(small):.1f} pt (minimum {min_font_pt} pt).")
        if ax is not None:
            ab = ax.get_window_extent(r)
            if bb.width * bb.height > max_area_frac * ab.width * ab.height:
                issues.append(f"{name} fills more than {max_area_frac:.0%} of its axes; move it outside.")
            pts = _data_points_display(ax, include_images=include_images)
            if len(pts):
                n_in = ((pts[:, 0] >= bb.x0) & (pts[:, 0] <= bb.x1) &
                        (pts[:, 1] >= bb.y0) & (pts[:, 1] <= bb.y1)).sum()
                if n_in / len(pts) > max_cover:
                    issues.append(f"{name} covers {n_in / len(pts):.0%} of the data in its axes; "
                                  f"move it to an empty corner or outside (place_legend does this).")
        else:
            for j, a in enumerate(fig.axes):
                if a.get_visible() and _overlap_frac(bb, a.get_tightbbox(r)) > 0.0:
                    issues.append(f"{name} overlaps axes {j} or its labels.")

    for i in range(len(entries)):
        for j in range(i + 1, len(entries)):
            if _overlap_frac(entries[i][1].get_window_extent(r), entries[j][1].get_window_extent(r)) > 0:
                issues.append(f"{entries[i][0]} overlaps {entries[j][0].lower()}.")

    per_axes = [tuple(t.get_text() for t in a.get_legend().get_texts())
                for a in fig.axes if a.get_legend() is not None]
    if len(per_axes) > 1 and len(set(per_axes)) < len(per_axes):
        issues.append("Several panels have identical legends; keep one shared legend (legend_outside).")
    return {"pass": not issues, "n_legends": len(entries), "issues": issues}


# ---------------------------------------------------------------------------
# Examples with synthetic data
# ---------------------------------------------------------------------------
def _demo_single_figure():
    plt.rcParams.update({"font.size": 8, "legend.fontsize": 7, "axes.linewidth": 0.6,
                         "savefig.bbox": "tight", "savefig.pad_inches": 0.02})
    rng = np.random.default_rng(3)
    fig, (a, b, c) = plt.subplots(1, 3, figsize=(190 / MM_PER_INCH, 62 / MM_PER_INCH),
                                  constrained_layout=True)

    t = np.arange(48)
    for name, base in (("Forest", 0.75), ("Cropland", 0.5), ("Urban", 0.22)):
        a.plot(t, base + 0.12 * np.sin(t / 7.5) + 0.01 * rng.standard_normal(48), lw=1.0, label=name)
    a.set_xlabel("Month index")
    a.set_ylabel("NDVI (–)")
    a.set_xlim(0, 47)
    direct_labels(a)
    a.set_title("(a) direct labels", loc="left", fontsize=8)

    for name, (mx, my), col in (("Site A", (2, 2), "#0072B2"), ("Site B", (5, 3), "#E69F00"),
                                ("Site C", (3, 6), "#009E73")):
        b.scatter(mx + rng.standard_normal(40) * 0.6, my + rng.standard_normal(40) * 0.6, s=8, c=col,
                  label=name, linewidths=0)
    b.set_xlabel("Predicted (m)")
    b.set_ylabel("Observed (m)")
    b.set_xlim(-1, 9)
    b.set_ylim(-1, 10)
    place_legend(b, title="Station")
    b.set_title("(b) emptiest corner", loc="left", fontsize=8)

    ny = nx = 120
    yy, xx = np.mgrid[0:ny, 0:nx]
    cls = np.digitize(np.sin(xx / 17) + np.cos(yy / 23), [-0.6, 0.4]).astype(float)
    cls[:50, :75] = np.nan  # nodata block
    cmap = mpl.colors.ListedColormap(["#bdbdbd", "#c2e699", "#238443"])
    c.imshow(cls, cmap=cmap, interpolation="nearest", extent=(0, nx, 0, ny))
    c.set_xlabel("Easting (km)")
    c.set_ylabel("Northing (km)")
    handles, labels = categorical_handles({0: "#bdbdbd", 1: "#c2e699", 2: "#238443"},
                                          {0: "Built-up", 1: "Low vegetation", 2: "Trees"})
    place_legend(c, handles, labels, on_overflow="inside", avoid=[(0.0, 0.0, 0.3, 0.1)])
    c.set_title("(c) free corner on a raster", loc="left", fontsize=8)

    print("single:", check_legends(fig))
    fig.savefig("example_legend_single.png", dpi=300)


def _demo_shared_figure():
    plt.rcParams.update({"font.size": 8, "legend.fontsize": 7, "axes.linewidth": 0.6,
                         "savefig.bbox": "tight", "savefig.pad_inches": 0.02})
    rng = np.random.default_rng(8)
    fig, axs = plt.subplots(1, 3, figsize=(190 / MM_PER_INCH, 58 / MM_PER_INCH), constrained_layout=True)
    models = ["U-Net", "DeepLabV3+", "SegFormer", "Mask2Former", "Random forest"]
    x = np.arange(1, 13)
    for k, ax in enumerate(axs):
        for i, m in enumerate(models):
            ax.plot(x, 0.55 + 0.04 * i + 0.25 * (1 - np.exp(-x / (4 + k))) + 0.01 * rng.standard_normal(12),
                    lw=1.0, label=m)
        ax.set_xlabel("Epoch")
        ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(integer=True))
        ax.set_ylabel("mIoU (–)" if k == 0 else "")
        ax.set_title(f"({'abc'[k]})", loc="left", fontsize=8)
    handles, labels = collect_handles(axs)
    legend_outside(fig, handles, labels, side="below")
    print("shared:", check_legends(fig))
    fig.savefig("example_legend_shared.png", dpi=300)


if __name__ == "__main__":
    mpl.use("Agg")
    _demo_single_figure()
    _demo_shared_figure()
