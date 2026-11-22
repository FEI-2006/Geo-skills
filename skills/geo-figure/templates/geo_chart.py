"""Publication-ready chart helpers for geoscience papers.

Needs numpy, pandas and matplotlib. Run directly for an example figure:
    python geo_chart.py
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from geo_map import WIDTHS_MM, add_panel_label, check_figure, fig_size_mm, save_figure, set_journal_style

# Colour-blind-safe qualitative palette (Okabe & Ito, 2008)
OKABE_ITO = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7", "#56B4E9", "#F0E442", "#000000"]


def time_series(ax, series: dict[str, pd.Series], ylabel: str, band: dict | None = None,
                band_label: str = "", max_gap: str | None = None):
    """Line plot with real dates. Gaps longer than `max_gap` (e.g. "20D") are left blank.

    series: {name: pd.Series indexed by datetime}.
    band: optional {name: (lower, upper)} Series pairs for uncertainty shading;
    say in the caption what the band is (SD, 95% CI...).
    """
    for i, (name, s) in enumerate(series.items()):
        s = s.sort_index()
        if max_gap is not None:
            idx = pd.DatetimeIndex(s.index)
            diff = idx[1:] - idx[:-1]
            big = np.asarray(diff > pd.Timedelta(max_gap))
            if big.any():
                # put one NaN in the middle of each long gap so the line breaks there
                mids = pd.DatetimeIndex(idx[:-1][big] + diff[big] / 2).as_unit(idx.unit)
                s = pd.concat([s, pd.Series(np.nan, index=mids)]).sort_index()
        c = OKABE_ITO[i % len(OKABE_ITO)]
        ax.plot(s.index, s.values, color=c, lw=1.0, label=name)
        if band and name in band:
            lo, hi = band[name]
            ax.fill_between(lo.index, lo.values, hi.values, color=c, alpha=0.2, lw=0,
                            label=band_label or None)
    import matplotlib.dates as mdates
    loc = mdates.AutoDateLocator(minticks=3, maxticks=6)
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", color="0.9", lw=0.5)
    ax.legend(frameon=False, loc="best")


def scatter_1to1(ax, observed, predicted, units: str, label_obs="Observed", label_pred="Predicted"):
    """Predicted vs observed with a 1:1 line and n, R², RMSE (computed, not typed)."""
    o = np.asarray(observed, dtype=float)
    p = np.asarray(predicted, dtype=float)
    ok = np.isfinite(o) & np.isfinite(p)
    o, p = o[ok], p[ok]
    n = o.size
    rmse = float(np.sqrt(np.mean((p - o) ** 2)))
    r2 = float(1 - np.sum((o - p) ** 2) / np.sum((o - o.mean()) ** 2))
    lo, hi = min(o.min(), p.min()), max(o.max(), p.max())
    pad = 0.05 * (hi - lo)
    ax.scatter(o, p, s=6, color=OKABE_ITO[0], alpha=0.6, linewidths=0)
    ax.plot([lo - pad, hi + pad], [lo - pad, hi + pad], color="black", lw=0.7, ls="--", label="1:1 line")
    ax.set_xlim(lo - pad, hi + pad)
    ax.set_ylim(lo - pad, hi + pad)
    ax.set_aspect("equal")
    ax.set_xlabel(f"{label_obs} ({units})")
    ax.set_ylabel(f"{label_pred} ({units})")
    ax.text(0.97, 0.04, f"n = {n}\nR² = {r2:.2f}\nRMSE = {rmse:.2f} {units}",
            transform=ax.transAxes, va="bottom", ha="right")
    return {"n": n, "r2": r2, "rmse": rmse}


def grouped_bars(ax, table: pd.DataFrame, ylabel: str = "Score (%)", ylim=(0, 100), fmt="{:.1f}",
                 show_values: bool = False):
    """Grouped bars for accuracy metrics. Rows = methods, columns = metrics (OA, F1, IoU...)."""
    n_methods, n_metrics = table.shape
    width = 0.8 / n_methods
    x = np.arange(n_metrics)
    for i, (method, row) in enumerate(table.iterrows()):
        bars = ax.bar(x + (i - (n_methods - 1) / 2) * width, row.values, width,
                      color=OKABE_ITO[i % len(OKABE_ITO)], label=method, edgecolor="none")
        if show_values:  # exact numbers belong in a table; use only for few bars
            for bar, v in zip(bars, row.values):
                ax.text(bar.get_x() + bar.get_width() / 2, v + 0.8, fmt.format(v),
                        ha="center", va="bottom", fontsize=5.5, rotation=90)
    ax.set_xticks(x, table.columns)
    ax.set_ylim(*ylim)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", color="0.9", lw=0.5)
    ax.set_axisbelow(True)
    ax.legend(frameon=True, framealpha=0.9, edgecolor="none", loc="lower right")


if __name__ == "__main__":
    set_journal_style(8)
    rng = np.random.default_rng(7)

    days = pd.date_range("2025-01-01", "2025-12-31", freq="D")
    days = days[(days < "2025-06-10") | (days > "2025-07-05")]  # a monitoring gap
    seasonal = 12 + 6 * np.cos(2 * np.pi * (days.dayofyear - 15) / 365)
    pm_under = pd.Series(seasonal * 1.6 + rng.normal(0, 1.5, len(days)), index=days)
    pm_above = pd.Series(seasonal + rng.normal(0, 1.2, len(days)), index=days)

    obs = rng.gamma(4, 3, 300)
    pred = obs + rng.normal(0, 2, 300)

    acc = pd.DataFrame({"OA": [91.2, 93.5, 95.1], "F1": [84.0, 87.9, 90.4], "mIoU": [72.3, 77.8, 81.6]},
                       index=["DeepLabV3+", "SegFormer", "Ours"])

    fig = plt.figure(figsize=fig_size_mm(WIDTHS_MM["elsevier_double"], 0.36), constrained_layout=True)
    gs = fig.add_gridspec(1, 3, width_ratios=[1.6, 1, 1.1])
    a, b, c = (fig.add_subplot(gs[0, i]) for i in range(3))
    time_series(a, {"Underground": pm_under, "Aboveground": pm_above},
                ylabel="PM$_{2.5}$ (µg m$^{-3}$)", max_gap="10D")
    a.set_xlabel("Date")
    stats = scatter_1to1(b, obs, pred, units="µg m$^{-3}$")
    grouped_bars(c, acc, ylim=(50, 100))
    for ax, lab in zip((a, b, c), "abc"):
        add_panel_label(ax, lab)
    print(stats)
    print(check_figure(fig, WIDTHS_MM["elsevier_double"]))
    print(save_figure(fig, "example_chart", dpi=500))
