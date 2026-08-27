from dataset import load_subject, extract_trials
from detector import detect_events


FS = 256
THRESHOLD = 1000


def main():

    # Load S1
    eog, control, target_ga = load_subject("S1")

    # Split into trials
    trials = extract_trials(
        eog,
        control,
        target_ga
    )

    total_expected = 0
    total_detected = 0
    total_missed = 0
    total_false_positives = 0

    print("Running raw EOG experiment...")
    print("Trials:", len(trials))

    for trial in trials:

        signal = trial["horizontal"]

        events = detect_events(
            signal,
            FS,
            velocity_threshold=THRESHOLD
        )

        # Every trial should contain:
        # 1 forward saccade
        # 1 return saccade
        # 1 blink
        expected = 3

        total_expected += expected

        # For this first baseline,
        # count detected events.
        total_detected += min(
            len(events),
            expected
        )

        if len(events) < expected:
            total_missed += expected - len(events)

        if len(events) > expected:
            total_false_positives += len(events) - expected

    detection_rate = (
        total_detected / total_expected
    ) * 100

    print("\n===== RAW EOG RESULTS =====")

    print(
        "Expected events:",
        total_expected
    )

    print(
        "Detected events:",
        total_detected
    )

    print(
        "Missed events:",
        total_missed
    )

    print(
        "False positives:",
        total_false_positives
    )

    print(
        f"Detection rate: {detection_rate:.2f}%"
    )


if __name__ == "__main__":
    main()