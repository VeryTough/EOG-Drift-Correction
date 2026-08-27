print("RUNNING WAVELET EXPERIMENT")

from collections import Counter

from dataset import load_subject, extract_trials
from detector import detect_events
from evaluation import evaluate_events
from drift_correction import wavelet_detrend


FS = 256
THRESHOLD = 1000


def main():

    eog, control, target_ga = load_subject("S1")

    trials = extract_trials(
        eog,
        control,
        target_ga
    )

    matched_count = Counter()
    missed_count = Counter()
    false_positives = 0

    print("Trials:", len(trials))

    for trial_number, trial in enumerate(trials, start=1):

        signal = wavelet_detrend(
            trial["horizontal"],
            wavelet="db4",
            level=8
        )

        events = detect_events(
            signal,
            FS,
            velocity_threshold=THRESHOLD
        )

        matched, missed, false = evaluate_events(
            events,
            trial["control"]
        )

        for event in matched:
            matched_count[event["type"]] += 1

        for event in missed:
            missed_count[event["type"]] += 1

        false_positives += len(false)

        # Progress every 25 trials
        if trial_number % 25 == 0:
            print(
                f"Processed {trial_number}/"
                f"{len(trials)} trials..."
            )

    print("\n===== WAVELET EOG RESULTS =====")

    for event_type in [
        "forward_saccade",
        "return_saccade",
        "blink"
    ]:

        detected = matched_count[event_type]
        missed = missed_count[event_type]

        total = detected + missed

        accuracy = (
            detected / total * 100
            if total > 0
            else 0
        )

        print(
            f"{event_type}: "
            f"{detected}/{total} "
            f"({accuracy:.2f}%)"
        )

    print(
        "\nFalse positives:",
        false_positives
    )


if __name__ == "__main__":
    main()