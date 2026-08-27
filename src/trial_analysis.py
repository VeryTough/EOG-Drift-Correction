from pathlib import Path

import numpy as np
from scipy.io import loadmat


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "raw" / "DATASET" / "S1"


# Load control signal
control = loadmat(
    DATA_DIR / "ControlSignal.mat"
)["ControlSignal"].ravel()


# Find transitions
transition_indices = np.where(np.diff(control) != 0)[0] + 1

transition_counts = {
    "1 -> 2": 0,
    "2 -> 3": 0,
    "3 -> 1": 0,
    "other": 0,
}


for index in transition_indices:
    old_state = int(control[index - 1])
    new_state = int(control[index])

    transition = f"{old_state} -> {new_state}"

    if transition in transition_counts:
        transition_counts[transition] += 1
    else:
        transition_counts["other"] += 1


print("Transition counts:")
for transition, count in transition_counts.items():
    print(f"  {transition}: {count}")


print("\nTotal transitions:", len(transition_indices))


# Show final transitions
print("\nLast 10 transitions:")

for index in transition_indices[-10:]:
    old_state = int(control[index - 1])
    new_state = int(control[index])

    print(
        f"Sample {index:6d} | "
        f"Time {index / 256:8.3f} s | "
        f"{old_state} -> {new_state}"
    )