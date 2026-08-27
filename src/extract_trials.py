from dataset import load_subject, extract_trials


eog, control, target_ga = load_subject("S1")

trials = extract_trials(
    eog,
    control,
    target_ga
)

print("Number of trials:", len(trials))

trial = trials[0]

print("\nFirst trial:")
print("Trial:", trial["trial_number"])
print("Samples:", len(trial["horizontal"]))
print("Target:",
      trial["target_horizontal"],
      trial["target_vertical"])