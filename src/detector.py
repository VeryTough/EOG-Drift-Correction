import numpy as np
from scipy.ndimage import gaussian_filter1d


def detect_events(
    signal,
    fs,
    velocity_threshold,
    smoothing_sigma=2,
    min_duration_ms=20
):
    """
    Detect rapid eye movements using velocity thresholding.

    Parameters
    ----------
    signal : array
        EOG signal.
    fs : float
        Sampling frequency.
    velocity_threshold : float
        Absolute velocity threshold.
    smoothing_sigma : float
        Gaussian smoothing parameter.
    min_duration_ms : float
        Minimum duration of a detected event.

    Returns
    -------
    events : list of tuples
        Each tuple contains (start_sample, end_sample).
    """

    # Smooth the signal
    smoothed = gaussian_filter1d(
        signal.astype(float),
        sigma=smoothing_sigma
    )

    # Estimate velocity
    velocity = np.gradient(
        smoothed
    ) * fs

    # Threshold velocity
    above_threshold = (
        np.abs(velocity) > velocity_threshold
    )

    # Find start/end of threshold regions
    changes = np.diff(
        above_threshold.astype(int)
    )

    starts = np.where(changes == 1)[0] + 1
    ends = np.where(changes == -1)[0] + 1

    # Handle events touching the boundaries
    if above_threshold[0]:
        starts = np.insert(starts, 0, 0)

    if above_threshold[-1]:
        ends = np.append(
            ends,
            len(signal)
        )

    # Convert minimum duration to samples
    min_duration = int(
        min_duration_ms / 1000 * fs
    )

    events = []

    for start, end in zip(starts, ends):

        if end - start >= min_duration:
            events.append(
                (start, end)
            )

    return events