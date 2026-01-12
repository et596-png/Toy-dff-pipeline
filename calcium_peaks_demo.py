# Neuronal Ca2+ Activity — Minimal ΔF/F Pipeline Demo (synthetic data)
# Author: Abdullah Enze Tian (demo project)
#
# Goal: illustrate an end-to-end workflow:
# (1) simulate a calcium-like fluorescence trace
# (2) compute ΔF/F
# (3) detect simple events by thresholding
# (4) export CSVs + a QC plot
#
# NOTE: This is a toy demo on synthetic data (not a biological analysis pipeline).

import numpy as np
import matplotlib.pyplot as plt
import csv

def main():
    # ----------------------------
    # 1) Simulate fluorescence trace
    # ----------------------------
    np.random.seed(0)
    frames = 1000
    baseline_value = 50.0
    noise_sigma = 2.0

    raw_trace = np.random.normal(baseline_value, noise_sigma, frames)

    # Insert 5 clear spikes (0-based indices)
    event_frames = [100, 250, 500, 750, 900]
    event_amplitudes = [52, 58, 51, 42, 47]
    for idx, amp in zip(event_frames, event_amplitudes):
        raw_trace[idx] += amp

    # ----------------------------
    # 2) Compute ΔF/F
    # ----------------------------
    # Baseline F0: mean of first 100 frames
    F0 = float(np.mean(raw_trace[:100]))
    dff = (raw_trace - F0) / F0

    # ----------------------------
    # 3) Peak detection (simple threshold)
    # ----------------------------
    threshold = float(np.mean(dff) + 1.5 * np.std(dff))
    peak_indices = np.where(dff > threshold)[0]  # all frames over threshold (toy)

    # ----------------------------
    # 4) Save outputs (CSVs + plot)
    # ----------------------------
    # raw_trace_dfF.csv
    with open("raw_trace_dfF.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Frame", "Raw", "DeltaF/F"])
        for i, (raw_val, dff_val) in enumerate(zip(raw_trace, dff), start=1):
            writer.writerow([i, f"{raw_val:.2f}", f"{dff_val:.3f}"])

    # events.csv
    with open("events.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Frame", "Value"])
        for idx in peak_indices:
            writer.writerow([idx + 1, f"{dff[idx]:.3f}"])

    # QC plot
    plt.figure(figsize=(10, 4))
    plt.plot(dff, label="ΔF/F")
    plt.scatter(peak_indices, dff[peak_indices], label="Detected events", s=18)
    plt.axhline(y=0, linestyle="--", linewidth=0.8)
    plt.xlabel("Frame")
    plt.ylabel("ΔF/F")
    plt.title("Simulated Ca²⁺ Trace with Detected Peaks (Toy Demo)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("trace_qc.png", dpi=200)
    plt.close()

    print("Done.")
    print(f"F0 = {F0:.3f}")
    print(f"Threshold (ΔF/F) = {threshold:.4f}")
    print(f"Detected frames (1-based): {[int(i)+1 for i in peak_indices[:10]]} ... (total {len(peak_indices)})")
    print("Generated files: raw_trace_dfF.csv, events.csv, trace_qc.png")

if __name__ == "__main__":
    main()
