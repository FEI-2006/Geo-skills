---
name: geo-legend
description: Decide where a legend or colorbar goes and lay it out so a figure looks clean in print. Use when the user asks where to put the legend, says a legend covers the data, is too big, is repeated in every panel, has too many entries, or wants a map, chart or multi-panel figure to look better organised (matplotlib or similar). Covers inside corners, outside placement, shared legends, direct labels, classified-map legends and colorbars. Not for choosing colours or for general figure styling (use geo-figure).
---

# geo-legend

Place legends so that readers find the key without hunting for it and the data stays visible. A good legend is one the reader barely notices: it sits where nothing else is, uses the same order as the data, and appears once.

## Workflow

1. **Look at what is in the figure.** Count the panels, the series or classes, and the length of the labels. Note what already occupies the corners (scale bar, north arrow, locator inset, panel label) and whether the data are lines, points, bars or a full-coverage raster. If the user shares an image, find the empty regions first.
2. **Choose the pattern** with the decision table below. Read `references/placement-guide.md` for the reasoning, the spacing numbers and the map-specific cases.
3. **Build it with the helpers** in `templates/legend_layout.py`:
   - `place_legend(ax, ...)` for one axes: tries the corners, picks the one that hides the fewest data points, keeps `avoid` boxes free, and moves the legend outside when no corner is empty enough.
   - `collect_handles(axes)` + `legend_outside(fig, handles, labels, side="below")` for one shared legend.
   - `categorical_handles(class_colors, class_names)` for classified and segmentation maps.
   - `direct_labels(ax)` to label lines at their ends.
   - `add_colorbar(fig, ax, mappable, label)` for continuous data.
4. **Check.** Run `check_legends(fig)`. It reports a legend that runs off the figure, covers data, overlaps another legend or the axes, fills more than a quarter of its axes, uses text under 6 pt, has more than 10 entries, repeats a label, or is duplicated in several panels. Fix every issue, then look at the rendered figure once more: the check cannot judge taste.
5. **Report** what was placed where and why, in one or two sentences, and list anything the user should decide (for example: dropping a class, or merging two series).

## Decision table

| Situation | Do this |
|---|---|
| One panel, few entries, an empty corner exists | Inside, in the emptiest corner (`place_legend`) |
| One panel, no empty corner | Outside below the axes, or direct labels for lines |
| 2 or more panels with the same series or classes | One shared legend, below (or on the right for tall figures); delete per-panel legends |
| 2–6 lines that end at different heights | Direct labels at the line ends; skip the legend |
| Classified or segmentation map | Patch legend in a nodata or empty corner with a light frame, or below the map; same class order as the data |
| Continuous raster | Colorbar, not a legend: horizontal below wide maps, vertical on the right of tall ones; label with variable and units |
| More than about 8–10 entries | Merge or group classes, use a colorbar if the variable is ordered, or move the full key to a table |
| Panels differ in series | Per-panel legends only for entries unique to that panel; shared legend for the rest |

## Rules

- **Never cover data.** A legend inside the axes may only sit on empty space or on nodata. A semi-opaque frame (alpha about 0.9, no edge) is acceptable on a full-coverage raster, never on a line or scatter plot.
- **Keep the figure size.** Outside legends must not change the figure width. Reserve space for them (constrained layout or `legend_outside`), instead of saving with `bbox_inches="tight"` and letting the width drift away from the journal column.
- **One legend per idea.** Panels that share series share one legend. Repeating it in every panel wastes space and invites inconsistent order.
- **Same order, same colours.** Order entries as the data appear (top-to-bottom by final value for lines, by class value for maps) and use identical colours and markers in every panel.
- **Frame and text.** No frame for legends outside the axes. Text size equals tick label size or one point smaller, never below 6 pt. Entry labels short and in sentence case, with units only when they differ between entries.
- **Titles earn their place.** Add a legend title when entries are values of a variable (for example `Station`, `Land cover`); skip it when entries are self-explanatory. Left-align it with the entries.
- **Columns.** Horizontal legends below the figure: as many columns as fit in 90% of the width, balanced rows. Vertical legends on the right: one column.
- **Keep clear of map furniture.** Pass the scale bar, north arrow, locator inset and panel label as `avoid` boxes so the legend never collides with them.
- **Use handles that match the data.** Lines get line handles, filled classes get square patches, points get markers of the plotted size. Do not use a line handle for an area.

## Integrity

Moving, resizing or restyling a legend must never change what the figure says. Do not drop, rename or reorder entries to make the layout fit without telling the user, and keep every legend entry that the plotted data need. If the legend cannot fit without removing information, say so and offer the options.
