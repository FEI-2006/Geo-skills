# Legend placement guide

Practical numbers and reasoning behind `SKILL.md`. Sizes assume a figure drawn at final print width (for example 90 mm or 190 mm), as in `geo-figure`.

## 1. Pick the location

Work down this list and stop at the first option that works.

1. **Direct labels** (lines only). Put each series name at the right-hand end of its line. The reader never looks back and forth. Works for 2–6 series whose end values are at least about 5% of the axis range apart; `direct_labels()` spreads close labels apart automatically. Not suitable when lines cross at the right edge or when series differ by marker rather than line.
2. **Inside, in an empty corner.** Good for one panel with up to about 5 short entries. The legend should cover no data and should not touch the axes spines (border pad about 0.4 em). Preferred corners, in order: upper right, upper left, lower right, lower left. For cumulative or rising curves the lower right is usually empty; for decaying curves the upper right.
3. **Outside below the axes.** Best default for multi-panel figures and for many or long entries. Horizontal, as many columns as fit, no frame. Keeps the plotting area unobstructed and reads naturally after the x-axis.
4. **Outside on the right.** Use for tall figures, for long labels, or when the legend has a title and several entries. One column, no frame. Costs width, so check the figure still fits the journal column.
5. **Outside above.** Rarely; for a single-row legend directly under a figure title in a poster or slide.

## 2. Maps

- **Classified or segmentation map.** The map fills the axes, so nothing is empty. Use the nodata corner if the raster has one; otherwise place the legend in the least important corner with a frame (alpha about 0.9, no edge line), or below the map. Do not put it where the scale bar, north arrow, locator inset or panel label sit.
- **Shared classes across panels** (image, reference, prediction): one legend below all panels. Remove per-panel legends.
- **Continuous data.** Use a colorbar, not a legend. Horizontal below the map for wide maps and for several panels in a row; vertical on the right for tall maps. Shrink to about 70% of the map's length so the bar does not dominate. Label with the variable and units; put tick labels outside the bar.
- **Two variables on one map** (for example boundaries plus classes): put the class legend and the line/point legend in one column, separated by a blank entry or a short subtitle, instead of two boxes that compete for corners.
- **Basemap credit** is not a legend entry. Put it in the caption or in small text at the lower edge of the map.

## 3. Multi-panel figures

- A shared legend sits centred below all panels, or on the right if the panels are arranged in a column.
- If panels show different series, give each panel only its own entries and keep identical series in the same colour in every panel.
- If one panel needs space for a legend that the others do not, prefer the shared legend over resizing a single panel. Equal panel sizes matter more than a slightly tighter fit.
- Panel labels such as (a) stay in the upper-left corner; keep legends out of that corner.

## 4. Sizing and spacing

| Element | Value |
|---|---|
| Legend text | tick label size or 1 pt smaller; at least 6 pt |
| Gap between axes (including tick and axis labels) and an outside legend | 2–3 mm |
| Border pad inside the axes | about 0.4 em from the spines |
| Handle length | 1.5–2 em for lines; square patches for classes |
| Space between columns | about 1.5 em |
| Largest legend inside an axes | no more than 25% of the axes area |
| Entries in one legend | up to about 8 comfortable; 10 is the limit before it needs restructuring |

## 5. When there are too many entries

- Merge rare classes into "Other" and say so in the caption.
- Group entries (for example by land-cover family) with short subtitles, or split into two legends in different places.
- For ordered or numeric variables switch to a colorbar.
- For many lines highlight the few that matter and draw the rest in light grey with one entry, "Other sites (n = 40)".
- Move a full key that cannot be shortened into a table or the supplement.

## 6. Common mistakes

- Legend inside the axes covering the last data points, which are often the most important.
- The same legend repeated in every panel.
- A frame with a drop shadow, or a bold edge around a legend that is already clear.
- Entry order that differs from the order of the lines or the classes on the map.
- Line handles for filled areas, or tiny markers that cannot be matched to the data.
- A legend that pushes the figure beyond the journal column after `bbox_inches="tight"`.
- A legend whose text is smaller than the axis labels or under 6 pt.
- A legend colliding with the scale bar, north arrow or inset map.

## 7. Matplotlib notes

- With constrained layout, `fig.legend(..., loc="outside lower center")` (also `outside upper center`, `outside center right`, `outside center left`) reserves space automatically. `legend_outside()` uses this when constrained layout is on and shrinks the subplot area itself otherwise.
- `loc="best"` ignores images, patches and your scale bar; use `place_legend()` when those are present.
- `ax.legend(..., bbox_to_anchor=(...))` outside the axes does not reserve space, and saving with `bbox_inches="tight"` then changes the figure size. Prefer the helpers.
- Draw once (`fig.canvas.draw()`) before measuring legend boxes; the helpers do this for you.
