from pathlib import Path
import numpy as np
from scipy.io import loadmat


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "raw" / "DATASET" / "S1"

eog = loadmat(DATA_DIR / "EOG.mat")["EOG"]
control = loadmat(DATA_DIR / "ControlSignal.mat")["ControlSignal"].ravel()
targets = loadmat(DATA_DIR / "TargetGA.mat")["TargetGA"]


print("Control state durations:")
states, counts = np.unique(control, return_counts=True)

for state, count in zip(states, counts):
    print(f"  State {state}: {count} samples")


print("\nFirst occurrence of each state:")

for state in states:
    indices = np.where(control == state)[0]
    print(f"  State {state}: sample {indices[0]}")


print("\nTargetGA first 20 rows:")
print(targets[:20])