import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d

from dataset import load_subject, extract_trials
from detector import detect_events


FS = 256

# Load S1
eog, control, target_ga = load_subject("S1")

trials = extract_trials(
    eog,
    control,
    target_ga
)

trial = trials[0]

signal = trial["horizontal"]
ground_truth = trial["control"]


# Smooth signal
smoothed = gaussian_filter1d(
    signal.astype(float),
    sigma=2
)

# Calculate velocity
velocity = np.gradient(smoothed) * FS

threshold = 1000

# Detect events
events = detect_events(
    signal,
    FS,
    velocity_threshold=threshold
)


# Create time axis
time = np.arange(len(signal)) / FS


# Plot EOG
fig, axes = plt.subplots(
    2,
    1,
    figsize=(14, 8),
    sharex=True
)


axes[0].plot(
    time,
    signal,
    label="Horizontal EOG"
)

axes[0].set_ylabel("EOG amplitude")
axes[0].set_title(
    "S1 Trial 1 — EOG and Ground Truth"
)


# Show ground-truth regions
for state, label in [
    (1, "Forward saccade"),
    (2, "Return saccade"),
    (3, "Blink"),
]:

    mask = ground_truth == state

    axes[0].fill_between(
        time,
        signal.min(),
        signal.max(),
        where=mask,
        alpha=0.12,
        label=label
    )


axes[0].legend()


# Plot velocity
axes[1].plot(
    time,
    velocity,
    label="Velocity"
)

axes[1].axhline(
    threshold,
    linestyle="--",
    label="Threshold"
)

axes[1].axhline(
    -threshold,
    linestyle="--"
)

axes[1].set_xlabel("Time (seconds)")
axes[1].set_ylabel("Velocity")
axes[1].set_title(
    "Velocity-Based Detection"
)

axes[1].legend()


plt.tight_layout()
plt.show()


# Print detections
print("\nDetected events:")

for start, end in events:

    print(
        f"Start: {start} "
        f"({start / FS:.3f} s), "
        f"End: {end} "
        f"({end / FS:.3f} s)"
    )

from evaluation import evaluate_events
results = evaluate_events(
    events,
    trial["control"],
    FS
)

print("\nEvaluation:")

print(
    "Matched:",
    len(results["matched"])
)

print(
    "False positives:",
    len(results["false_positives"])
)

print(
    "Missed:",
    len(results["missed"])
)

for event in results["matched"]:
    print(
        f"{event['type']}: "
        f"timing error = "
        f"{event['timing_error_seconds'] * 1000:.1f} ms"
    )