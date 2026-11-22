---
name: geo-figure
description: Make publication-ready maps and charts for remote sensing, GIS and geography papers in Python (matplotlib). Use when the user asks for a study-area map, a raster/classification/segmentation result map, a time series or comparison chart, or wants an existing figure fixed to meet journal requirements (Elsevier journals such as RSE, ISPRS, JAG; IEEE TGRS/JSTARS/GRSL; Taylor & Francis IJGIS/IJDE).
---

# geo-figure

Produce figures that a geoscience journal will accept without a redraw request, and that a reader can understand without the caption.

## Workflow

1. **Pin down the target before drawing.** Ask (or infer from the manuscript) three things: the journal, the column width the figure will occupy, and the figure type (map, raster result, chart, multi-panel). Look up the width in `references/journal-specs.md`. If the journal is unknown, default to Elsevier single column (90 mm) or double column (190 mm).
2. **Inspect the data before styling it.** Report CRS, extent, pixel size or feature count, value range, nodata value and units. A figure built on the wrong CRS or an unmasked nodata value is wrong no matter how it looks. Do not reproject or resample silently; say what you changed.
3. **Start from a template.** Use `templates/geo_map.py` for maps and raster results and `templates/geo_chart.py` for charts. Set the figure size in millimetres with `fig_size_mm()` so text prints at its real size.
4. **Draw.** Apply the rules below.
5. **Export and check.** Save vector PDF/EPS for line art and charts; save TIFF or PNG at the required dpi for rasters and photos. Then run the checklist at the end of this file and report each item as pass or fix.

## Rules for every figure

- **Size and text.** Draw at final print width. Text 7–9 pt after printing, never below 6 pt. One font family across all panels (Arial/Helvetica or the journal's font).
- **Colour.** Perceptually uniform colormaps for continuous data (viridis, cividis, magma). Diverging colormaps (RdBu, BrBG) only when the data have a meaningful centre such as zero change, and centre them on it. Never use jet or rainbow. Categorical maps: at most about 8 classes, colour-blind-safe palette, and colours that follow convention (water blue, vegetation green, built-up red/grey).
- **Units everywhere.** Every axis and every colorbar has a label with units in parentheses, for example `NDVI (–)`, `PM$_{2.5}$ (µg m$^{-3}$)`, `Crevasse area (km$^2$)`.
- **Panels.** Label sub-figures (a), (b), (c) in the top-left corner, consistent size and position. Share axes and colorbars when panels use the same variable and range; say so in the caption.
- **No chartjunk.** No 3D effects, shadows or background fills. Gridlines light grey and only when they help reading values.

## Extra rules for maps

- **Scale bar** on every map. A north arrow when north is not up or the area is small enough that orientation is not obvious; omit it on global maps.
- **Coordinates.** Show a graticule or tick labels in degrees (e.g., 46.4°N, 8.0°E) or state the projected CRS in the caption (e.g., "UTM zone 32N, EPSG:32632").
- **Study-area maps** need a locator inset showing where the study area sits in the larger region.
- **Rasters.** Mask nodata to transparent, never to zero. Use `interpolation="nearest"` for classified or segmentation maps so class edges are not blurred.
- **Basemaps and imagery.** Credit the source in the figure or caption (e.g., "Imagery © Google", "Sentinel-2, ESA Copernicus"). Respect the licence; Google Street View and basemap tiles have terms of use.

## Extra rules for charts

- Error bars, bands or boxes must say what they show (SD, SE, 95% CI, IQR) in the caption.
- Time axes use real dates, not indices. Mark gaps instead of drawing lines through missing data.
- Scatter plots that compare predictions with observations get a 1:1 line and report n, R² and RMSE with units.
- Accuracy results (OA, kappa, F1, IoU) are clearer as a table or a grouped bar chart than as a radar chart.

## Integrity

Never invent, smooth or alter data to make a figure look better. If an outlier, artefact or missing value is visible, keep it and point it out to the user. Any processing done for display (stretching, clipping percentiles, resampling) must be stated so the user can put it in the caption or methods.

## Final checklist (report pass/fix for each)

1. Width matches the journal column; text ≥ 6 pt at print size.
2. Resolution meets the journal minimum for the figure type (or the file is vector).
3. Every axis and colorbar labelled with units.
4. Colormap suits the data type and is colour-blind safe; no jet or rainbow.
5. Maps: scale bar, coordinates or CRS, north arrow where needed, locator inset for study-area maps.
6. Nodata masked; classified rasters use nearest-neighbour display.
7. Panels labelled (a), (b), … consistently.
8. Data and imagery sources credited.
9. Display-only processing listed for the caption.
