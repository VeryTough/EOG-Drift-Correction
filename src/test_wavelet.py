import matplotlib.pyplot as plt
import numpy as np

from dataset import load_subject, extract_trials
from drift_correction import wavelet_detrend


FS = 256


# Load S1
eog, control, target_ga = load_subject("S1")

# Extract trials
trials = extract_trials(
    eog,
    control,
    target_ga
)

# First trial
trial = trials[0]

raw = trial["horizontal"]

# Wavelet correction
wavelet = wavelet_detrend(
    raw,
    wavelet="db4",
    level=5
)

# Time axis
time = np.arange(len(raw)) / FS


# Plot
plt.figure(figsize=(14, 6))

plt.plot(
    time,
    raw,
    label="Raw"
)

plt.plot(
    time,
    wavelet,
    label="Wavelet corrected"
)

plt.xlabel("Time (seconds)")
plt.ylabel("EOG amplitude")

plt.title(
    "Wavelet Drift Correction — S1 Trial 1"
)

plt.legend()

plt.tight_layout()
plt.show()


# Basic statistics
print("Raw signal:")
print("  Min:", np.min(raw))
print("  Max:", np.max(raw))
print("  Standard deviation:", np.std(raw))

print("\nWavelet corrected:")
print("  Min:", np.min(wavelet))
print("  Max:", np.max(wavelet))
print("  Standard deviation:", np.std(wavelet))

print(
    "\nLength check:",
    len(raw),
    len(wavelet)
)