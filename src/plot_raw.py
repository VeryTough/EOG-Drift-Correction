from pathlib import Path

import matplotlib.pyplot as plt
from scipy.io import loadmat


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "raw" / "DATASET" / "S1"


# Load data
eog = loadmat(DATA_DIR / "EOG.mat")["EOG"]
control = loadmat(DATA_DIR / "ControlSignal.mat")["ControlSignal"].ravel()

horizontal = eog[0]

# Plot first 6000 samples
n_samples = 6000
x = range(n_samples)

fig, ax1 = plt.subplots(figsize=(14, 6))

# EOG
ax1.plot(x, horizontal[:n_samples], label="Horizontal EOG")
ax1.set_xlabel("Sample")
ax1.set_ylabel("EOG amplitude")
ax1.set_title("S1 EOG and Control Signal — First 6000 Samples")

# Control signal
ax2 = ax1.twinx()
ax2.step(
    x,
    control[:n_samples],
    where="post",
    alpha=0.5,
    label="Control Signal"
)
ax2.set_ylabel("Control state")
ax2.set_yticks([1, 2, 3])

plt.tight_layout()
plt.show()