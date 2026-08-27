from pathlib import Path

import numpy as np
from scipy.io import loadmat


FS = 256

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "raw" / "DATASET"


def load_subject(subject_id):
    """Load all data for one subject."""

    subject_dir = DATA_DIR / subject_id

    eog = loadmat(subject_dir / "EOG.mat")["EOG"]
    control = loadmat(
        subject_dir / "ControlSignal.mat"
    )["ControlSignal"].ravel()
    target_ga = loadmat(
        subject_dir / "TargetGA.mat"
    )["TargetGA"]

    return eog, control, target_ga


def extract_trials(eog, control, target_ga):
    """Split continuous recording into individual trials."""

    horizontal = eog[0]
    vertical = eog[1]

    # Actual target rows are every second row.
    targets = target_ga[::2]

    # A new trial starts at 3 -> 1.
    trial_starts = [0]

    for i in range(1, len(control)):
        if control[i - 1] == 3 and control[i] == 1:
            trial_starts.append(i)

    trials = []

    for trial_number, start in enumerate(trial_starts):

        if trial_number < len(trial_starts) - 1:
            end = trial_starts[trial_number + 1]
        else:
            end = len(control)

        trials.append({
            "trial_number": trial_number + 1,
            "start_sample": start,
            "end_sample": end,
            "horizontal": horizontal[start:end],
            "vertical": vertical[start:end],
            "control": control[start:end],
            "target_horizontal": targets[trial_number, 0],
            "target_vertical": targets[trial_number, 1],
        })

    return trials