import numpy as np


EVENT_TYPES = {
    1: "forward_saccade",
    2: "return_saccade",
    3: "blink",
}


def ground_truth_events(control):
    """
    Convert ControlSignal states into ground-truth event windows.

    1 = forward saccade
    2 = return saccade
    3 = blink
    """

    events = []

    for state, name in EVENT_TYPES.items():

        indices = np.where(control == state)[0]

        if len(indices) == 0:
            continue

        start = indices[0]
        end = indices[-1] + 1

        events.append({
            "type": name,
            "start": start,
            "end": end,
        })

    return events


def evaluate_events(detected_events, control, fs):
    """
    Evaluate detected events against ControlSignal windows.

    A detection is considered a hit if it overlaps the
    corresponding ground-truth window.
    """

    ground_truth = ground_truth_events(control)

    matched = []
    false_positives = []

    used_ground_truth = set()

    for detected_start, detected_end in detected_events:

        # Find overlapping ground-truth events
        candidates = []

        for i, gt in enumerate(ground_truth):

            if i in used_ground_truth:
                continue

            overlap_start = max(
                detected_start,
                gt["start"]
            )

            overlap_end = min(
                detected_end,
                gt["end"]
            )

            if overlap_start < overlap_end:
                candidates.append((i, gt))

        if not candidates:

            false_positives.append({
                "start": detected_start,
                "end": detected_end,
            })

            continue

        # Use the first matching ground-truth event
        gt_index, gt = candidates[0]

        used_ground_truth.add(gt_index)

        latency = (
            detected_start - gt["start"]
        ) / fs

        matched.append({
            "type": gt["type"],
            "detected_start": detected_start,
            "detected_end": detected_end,
            "ground_truth_start": gt["start"],
            "ground_truth_end": gt["end"],
            "latency_seconds": latency,
        })

    missed = [
        gt
        for i, gt in enumerate(ground_truth)
        if i not in used_ground_truth
    ]

    return {
        "ground_truth": ground_truth,
        "matched": matched,
        "false_positives": false_positives,
        "missed": missed,
    }