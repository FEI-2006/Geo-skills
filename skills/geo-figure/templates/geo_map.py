"""Publication-ready map helpers for remote sensing and GIS figures.

Only needs numpy and matplotlib. Works with arrays read by rasterio, xarray or
GDAL and with GeoDataFrames (geopandas) when those libraries are installed.

Run this file directly to draw an example two-panel figure:
    python geo_map.py
"""
from __future__ import annotations

import math

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch, Rectangle

MM_PER_INCH = 25.4

# Column widths in millimetres (see references/journal-specs.md)
WIDTHS_MM = {
    "elsevier_single": 90, "elsevier_1.5": 140, "elsevier_double": 190,
    "ieee_single": 88.9, "ieee_double": 182,
}


def set_journal_style(font_size: float = 8, font: str = "DejaVu Sans") -> None:
    """Apply consistent, print-sized styling. Use Arial/Helvetica if installed."""
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", font],
        "font.size": font_size,
        "axes.titlesize": font_size,
        "axes.labelsize": font_size,
        "xtick.labelsize": font_size - 1,
        "ytick.labelsize": font_size - 1,
        "legend.fontsize": font_size - 1,
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "pdf.fonttype": 42,  # embed TrueType so text stays editable
        "ps.fonttype": 42,
    })


def fig_size_mm(width_mm: float, aspect: float = 0.75) -> tuple[float, float]:
    """Return (width, height) in inches for a figure `width_mm` wide.

    aspect = height / width.
    """
    w = width_mm / MM_PER_INCH
    return w, w * aspect


def _nice_length(target: float) -> float:
    """Round a length down to 1, 2 or 5 × 10^n."""
    if target <= 0:
        return 0
    exp = math.floor(math.log10(target))
    for m in (5, 2, 1):
        if m * 10 ** exp <= target:
            return m * 10 ** exp
    return 10 ** exp


def add_scale_bar(ax, length: float | None = None, units: str = "km",
                  crs: str = "projected", location: tuple = (0.05, 0.05),
                  segments: int = 2, height_frac: float = 0.012) -> None:
    """Draw a black-and-white scale bar.

    crs="projected": axis coordinates are metres (UTM, Albers, etc.).
    crs="geographic": axis coordinates are degrees; the bar is computed at the
    map's centre latitude (approximate, fine for small areas).
    length: bar length in `units`; chosen automatically when None.
    """
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    unit_m = {"km": 1000.0, "m": 1.0}[units]
    if crs == "projected":
        m_per_x = 1.0
    elif crs == "geographic":
        lat = math.radians((y0 + y1) / 2)
        m_per_x = 111_320 * math.cos(lat)
    else:
        raise ValueError("crs must be 'projected' or 'geographic'")
    map_width_units = (x1 - x0) * m_per_x / unit_m
    if length is None:
        length = _nice_length(map_width_units / 4)
    bar_x = length * unit_m / m_per_x
    bx = x0 + location[0] * (x1 - x0)
    by = y0 + location[1] * (y1 - y0)
    h = height_frac * (y1 - y0)
    seg = bar_x / segments
    for i in range(segments):
        ax.add_patch(Rectangle((bx + i * seg, by), seg, h, facecolor="black" if i % 2 == 0 else "white",
                               edgecolor="black", linewidth=0.5, zorder=10))
    label = f"{length:g} {units}"
    ax.text(bx, by + 1.8 * h, "0", ha="center", va="bottom", fontsize=mpl.rcParams["xtick.labelsize"], zorder=10)
    ax.text(bx + bar_x, by + 1.8 * h, label, ha="center", va="bottom",
            fontsize=mpl.rcParams["xtick.labelsize"], zorder=10)


def add_north_arrow(ax, location: tuple = (0.93, 0.88), size: float = 0.07) -> None:
    """Simple north arrow in axes coordinates (assumes north is up)."""
    x, y = location
    ax.annotate("N", xy=(x, y), xytext=(x, y - size), xycoords="axes fraction",
                ha="center", va="center", fontweight="bold", zorder=10,
                arrowprops=dict(arrowstyle="-|>", lw=0.8, color="black"),
                fontsize=mpl.rcParams["font.size"])


def add_panel_label(ax, label: str, location: tuple = (0.02, 0.98)) -> None:
    """Sub-figure label such as (a), placed top-left on a white box."""
    ax.text(*location, f"({label})", transform=ax.transAxes, ha="left", va="top",
            fontweight="bold", zorder=11,
            bbox=dict(boxstyle="square,pad=0.15", facecolor="white", edgecolor="none", alpha=0.8))


def format_lonlat_ticks(ax, n: int = 4) -> None:
    """Label ticks as degrees N/S/E/W for maps in geographic coordinates."""
    from matplotlib.ticker import FuncFormatter, MaxNLocator

    def lon(v, _):
        return f"{abs(v):g}°{'E' if v >= 0 else 'W'}"

    def lat(v, _):
        return f"{abs(v):g}°{'N' if v >= 0 else 'S'}"

    ax.xaxis.set_major_locator(MaxNLocator(n))
    ax.yaxis.set_major_locator(MaxNLocator(n))
    ax.xaxis.set_major_formatter(FuncFormatter(lon))
    ax.yaxis.set_major_formatter(FuncFormatter(lat))


def plot_continuous_raster(ax, array, extent, cmap="viridis", vmin=None, vmax=None,
                           nodata=None, label="", cbar=True, orientation="vertical"):
    """Continuous raster (NDVI, temperature, PM2.5...). nodata becomes transparent.

    extent: (left, right, bottom, top) in map coordinates, e.g. rasterio
    `plotting_extent(src)` or (xmin, xmax, ymin, ymax).
    """
    data = np.ma.masked_invalid(np.asarray(array, dtype=float))
    if nodata is not None:
        data = np.ma.masked_equal(data, nodata)
    cm = plt.get_cmap(cmap).copy()
    cm.set_bad(alpha=0)
    im = ax.imshow(data, extent=extent, cmap=cm, vmin=vmin, vmax=vmax,
                   interpolation="nearest", origin="upper")
    if cbar:
        cb = plt.colorbar(im, ax=ax, orientation=orientation, fraction=0.046, pad=0.03)
        cb.set_label(label)
        cb.outline.set_linewidth(0.5)
    ax.set_aspect("equal")
    return im


def plot_categorical_raster(ax, array, extent, class_colors: dict, class_names: dict,
                            nodata=None, legend_loc="lower right", ncol=1):
    """Classified / segmentation raster with a legend.

    class_colors: {class_value: "#rrggbb"}; class_names: {class_value: "Name"}.
    Uses nearest-neighbour display so class edges stay sharp.
    """
    values = sorted(class_colors)
    data = np.ma.masked_invalid(np.asarray(array, dtype=float))
    if nodata is not None:
        data = np.ma.masked_equal(data, nodata)
    cm = ListedColormap([class_colors[v] for v in values])
    cm.set_bad(alpha=0)
    bounds = [v - 0.5 for v in values] + [values[-1] + 0.5]
    im = ax.imshow(data, extent=extent, cmap=cm, norm=BoundaryNorm(bounds, cm.N),
                   interpolation="nearest", origin="upper")
    handles = [Patch(facecolor=class_colors[v], edgecolor="black", linewidth=0.3, label=class_names[v])
               for v in values]
    ax.legend(handles=handles, loc=legend_loc, ncol=ncol, frameon=True, framealpha=0.9,
              edgecolor="none", handlelength=1.0, handleheight=1.0)
    ax.set_aspect("equal")
    return im


def add_locator_inset(ax, region_extent, study_extent, background=None,
                      bounds=(0.68, 0.62, 0.3, 0.34)):
    """Small inset showing where the study area lies in a larger region.

    region_extent / study_extent: (xmin, xmax, ymin, ymax) in the same CRS.
    background: optional callable f(inset_ax) that draws outlines, e.g.
        lambda a: countries_gdf.boundary.plot(ax=a, lw=0.3, color="grey")
    """
    ins = ax.inset_axes(bounds)
    if background is not None:
        background(ins)
    xmin, xmax, ymin, ymax = study_extent
    ins.add_patch(Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                            facecolor="none", edgecolor="red", linewidth=1.0))
    ins.set_xlim(region_extent[0], region_extent[1])
    ins.set_ylim(region_extent[2], region_extent[3])
    ins.set_xticks([])
    ins.set_yticks([])
    ins.set_facecolor("white")
    for s in ins.spines.values():
        s.set_linewidth(0.5)
    return ins


def plot_vector(ax, gdf, column=None, categorical=False, cmap="viridis", label="",
                color="none", edgecolor="black", linewidth=0.4, legend=True, **kwargs):
    """Draw a GeoDataFrame (requires geopandas) with journal styling.

    column=None draws outlines only (e.g., study-area boundary, roads).
    column="name" colours features by that attribute; set categorical=True for classes.
    The GeoDataFrame must already be in the CRS you want to show; this helper
    never reprojects silently.
    """
    if column is None:
        gdf.plot(ax=ax, color=color, edgecolor=edgecolor, linewidth=linewidth, **kwargs)
        return ax
    legend_kwds = {"frameon": False} if categorical else {"label": label, "shrink": 0.8}
    gdf.plot(ax=ax, column=column, categorical=categorical, cmap=cmap, edgecolor=edgecolor,
             linewidth=linewidth, legend=legend, legend_kwds=legend_kwds, **kwargs)
    ax.set_aspect("equal")
    return ax


def check_figure(fig, target_width_mm: float, min_font_pt: float = 6.0,
                 tolerance_mm: float = 3.0) -> dict:
    """Check a finished figure against the journal width and minimum text size.

    Returns a dict with 'pass' (bool) and 'issues' (list of strings). Font sizes
    are checked as drawn, so call this after the figure is complete and sized
    with fig_size_mm(). Also flags axes and colorbars without labels.
    """
    issues = []
    w_mm = fig.get_figwidth() * MM_PER_INCH
    if abs(w_mm - target_width_mm) > tolerance_mm:
        issues.append(f"Width is {w_mm:.0f} mm; target column is {target_width_mm:.0f} mm.")
    small = sorted({round(t.get_fontsize(), 1) for t in fig.findobj(mpl.text.Text)
                    if t.get_text().strip() and t.get_visible() and t.get_fontsize() < min_font_pt})
    if small:
        issues.append(f"Text below {min_font_pt} pt at print size: {small} pt.")
    for i, ax in enumerate(fig.axes):
        if ax.get_label() == "<colorbar>":
            lab = ax.get_ylabel() or ax.get_xlabel()
            if not lab:
                issues.append(f"Colorbar on axes {i} has no label (add the variable and units).")
            continue
        if not ax.axison or not ax.get_visible():
            continue
        has_ticks = bool(ax.get_xticks().size or ax.get_yticks().size)
        if has_ticks and not (ax.get_xlabel() or ax.get_ylabel()) and ax.get_position().width > 0.15:
            issues.append(f"Axes {i} has tick labels but no axis label.")
    return {"pass": not issues, "width_mm": round(float(w_mm), 1), "issues": issues}


def save_figure(fig, path_stem: str, dpi: int = 600, formats=("pdf", "png")) -> list[str]:
    """Save vector PDF (text editable) and a raster copy at `dpi`."""
    out = []
    for fmt in formats:
        p = f"{path_stem}.{fmt}"
        fig.savefig(p, dpi=dpi)
        out.append(p)
    return out


# ---------------------------------------------------------------------------
# Example: synthetic data in UTM metres, double-column Elsevier figure
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    set_journal_style(8)
    rng = np.random.default_rng(42)
    ny, nx = 300, 400
    x0, y0, res = 410_000.0, 5_140_000.0, 30.0  # 30 m pixels, UTM zone 32N
    extent = (x0, x0 + nx * res, y0, y0 + ny * res)

    yy, xx = np.mgrid[0:ny, 0:nx]
    ndvi = 0.25 + 0.45 * np.exp(-(((xx - 260) / 120) ** 2 + ((yy - 140) / 90) ** 2))
    ndvi += 0.05 * rng.standard_normal((ny, nx))
    ndvi = np.clip(ndvi, -0.2, 0.95)
    ndvi[:25, :60] = -9999  # nodata corner

    classes = np.digitize(ndvi, [0.2, 0.45])  # 0 built-up, 1 low veg, 2 trees
    classes = np.where(ndvi == -9999, 255, classes)

    fig, (a, b) = plt.subplots(1, 2, figsize=fig_size_mm(WIDTHS_MM["elsevier_double"], 0.42),
                               constrained_layout=True)
    plot_continuous_raster(a, ndvi, extent, cmap="viridis", vmin=-0.2, vmax=0.9,
                           nodata=-9999, label="NDVI (–)")
    plot_categorical_raster(b, classes, extent, nodata=255,
                            class_colors={0: "#bdbdbd", 1: "#c2e699", 2: "#238443"},
                            class_names={0: "Built-up", 1: "Low vegetation", 2: "Trees"})
    for ax, lab in ((a, "a"), (b, "b")):
        ax.ticklabel_format(style="plain", useOffset=False)
        ax.set_xlabel("Easting (m)")
        ax.set_ylabel("Northing (m)")
        add_scale_bar(ax, crs="projected", units="km")
        add_north_arrow(ax)
        add_panel_label(ax, lab)
    b.set_ylabel("")
    add_locator_inset(a, (300_000, 700_000, 4_950_000, 5_350_000),
                      (extent[0], extent[1], extent[2], extent[3]), bounds=(0.62, 0.04, 0.3, 0.3))
    print(check_figure(fig, WIDTHS_MM["elsevier_double"]))
    print(save_figure(fig, "example_map", dpi=500))
