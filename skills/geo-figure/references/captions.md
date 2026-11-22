# Writing figure captions

A caption should let a reader understand the figure without the main text.

## Structure

1. **Title sentence** (what is shown, where, when): "Green view index (GVI) across Chicago street segments in summer 2024."
2. **Panels**: "(a) Mean GVI per census tract; (b) standard deviation across 20 bootstrap samples."
3. **Encoding**: what colours, symbols, lines and bands mean, if not in the legend. Say what error bars or bands show: "Shaded bands show the 95% confidence interval."
4. **Data and processing**: sources and any display-only processing. "Background: Sentinel-2 true-colour composite (10 m), 2–98% linear stretch. Coordinates: UTM zone 32N (EPSG:32632)."
5. **Statistics** where relevant: n, test, p.

## Templates

**Study-area map**
> Location of the study area. (a) [Region] with the study area outlined in red; (b) [study area] showing [features]. Basemap: [source, licence]. Coordinate system: [CRS, EPSG code].

**Classification or segmentation result**
> [Method] results for [area, date]. (a) Input [sensor] image ([bands] composite); (b) reference labels; (c) prediction from [method]. Classes: [list]. White areas are no-data.

**Accuracy comparison**
> Accuracy of [methods] on the [dataset] test set (n = [number] images/pixels). OA, overall accuracy; F1, F1 score; mIoU, mean intersection over union.

**Predicted vs observed**
> Predicted versus observed [variable] for [n] [samples] in the [test set / cross-validation]. The dashed line is the 1:1 line.

## Checks

- Abbreviations used in the figure are defined in the caption.
- Units appear in the figure (axes, colorbar) or the caption.
- Image and data credits follow the provider's licence wording.
- Panel letters in the caption match those in the figure.
