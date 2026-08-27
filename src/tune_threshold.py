print("RUNNING THRESHOLD TUNING...")

from dataset import load_subject, extract_trials
from detector import detect_events
from evaluation import evaluate_events

FS = 256
# Test thresholds from 500 to 2000 in steps of 100
THRESHOLDS_TO_TEST = range(500, 2001, 100)

def calculate_f1(matched, missed, false_positives):
    true_positives = len(matched)
    false_negatives = len(missed)
    
    if true_positives == 0:
        return 0.0, 0.0, 0.0
        
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)
    
    if precision + recall == 0:
        return precision, recall, 0.0
        
    f1 = 2 * (precision * recall) / (precision + recall)
    return precision, recall, f1

def main():
    eog, control, target_ga = load_subject("S1")
    trials = extract_trials(eog, control, target_ga)
    
    best_f1 = 0
    best_threshold = 0
    results = []
    
    print(f"Tuning across {len(trials)} trials...\n")
    print(f"{'Threshold':<10} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10} | {'FP'}")
    print("-" * 55)

    for threshold in THRESHOLDS_TO_TEST:
        all_matched = []
        all_missed = []
        total_false_positives = 0
        
        for trial in trials:
            # Tuning on the raw horizontal signal to establish a baseline
            events = detect_events(trial["horizontal"], FS, velocity_threshold=threshold)
            matched, missed, false = evaluate_events(events, trial["control"])
            
            all_matched.extend(matched)
            all_missed.extend(missed)
            total_false_positives += len(false)
            
        precision, recall, f1 = calculate_f1(all_matched, all_missed, total_false_positives)
        
        print(f"{threshold:<10} | {precision:.4f}   | {recall:.4f}   | {f1:.4f}   | {total_false_positives}")
        
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold

    print("\n===== TUNING COMPLETE =====")
    print(f"Optimal Threshold: {best_threshold}")
    print(f"Best Overall F1-Score: {best_f1:.4f}")

if __name__ == "__main__":
    main()