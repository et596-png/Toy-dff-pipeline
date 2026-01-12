# Neuronal Ca²⁺ Activity — Minimal ΔF/F Pipeline Demo (Toy)

**Goal:** show a beginner-level, reproducible workflow for a calcium-like fluorescence trace:
1) simulate data, 2) compute ΔF/F, 3) detect simple events, 4) export CSVs + a QC plot.

> This is a tiny toy demo on **synthetic** data (not a real biological analysis pipeline).

## What it generates
- `raw_trace_dfF.csv` — columns: `Frame`, `Raw`, `DeltaF/F` (1–1000)
- `events.csv` — detected frames (toy rule: `ΔF/F > mean + 1.5×std`)
- `trace_qc.png` — ΔF/F trace with detected-event markers
- `analysis_notebook_en.ipynb` — the same workflow in a notebook format

## Methods (toy)
- **Simulation:** baseline ~50 (Gaussian noise σ=2), plus 5 injected peaks at frames ~100, 250, 500, 750, 900.
- **Baseline:** `F0 = mean(first 100 frames)`.
- **Normalization:** `ΔF/F = (F - F0) / F0`.
- **Detection:** threshold = `mean(ΔF/F) + 1.5×std(ΔF/F)` (no merging/refractory; kept minimal intentionally).

## Run (Python)
```bash
pip install numpy matplotlib
python calcium_peaks_demo.py
```

## Limitations / next steps
- Thresholding is minimal; it can flag multiple adjacent frames as events.
- Next steps: peak merging/refractory window, prominence/duration filters, baseline drift handling, and alignment to behavioral timestamps.
