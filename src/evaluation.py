import numpy as np


EVENT_TYPES = {
    1: "forward_saccade",
    2: "return_saccade",
    3: "blink",
}


def ground_truth_events(control):
    events = []

    for state, name in EVENT_TYPES.items():
        indices = np.where(control == state)[0]

        if len(indices) == 0:
            continue

        events.append({
            "type": name,
            "start": indices[0],
            "end": indices[-1] + 1,
        })

    return events


def evaluate_events(detected_events, control):
    ground_truth = ground_truth_events(control)

    matched = []
    false_positives = []
    used = set()

    for detected_start, detected_end in detected_events:

        best_match = None

        for i, gt in enumerate(ground_truth):

            if i in used:
                continue

            overlap_start = max(detected_start, gt["start"])
            overlap_end = min(detected_end, gt["end"])

            if overlap_start < overlap_end:
                best_match = (i, gt)
                break

        if best_match is None:
            false_positives.append(
                (detected_start, detected_end)
            )
        else:
            i, gt = best_match
            used.add(i)

            matched.append({
                "type": gt["type"],
                "start": detected_start,
                "end": detected_end,
            })

    missed = [
        gt for i, gt in enumerate(ground_truth)
        if i not in used
    ]

    return matched, missed, false_positives