print("RUNNING FINAL COMPARISON...")

from dataset import load_subject, extract_trials
from detector import detect_events
from evaluation import evaluate_events

# Import all your correction methods
from drift_correction import highpass_filter, polynomial_detrend, wavelet_detrend

FS = 256
OPTIMAL_THRESHOLD = 1000

def calculate_metrics(matched, missed, false_positives):
    tp = len(matched)
    fn = len(missed)
    fp = false_positives
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return precision, recall, f1

def main():
    eog, control, target_ga = load_subject("S1")
    trials = extract_trials(eog, control, target_ga)
    
    # Define the pipeline for each method
    methods = {
        "Raw": lambda sig: sig,
        "High-pass": lambda sig: highpass_filter(sig, FS),
        "Polynomial": lambda sig: polynomial_detrend(sig, order=3),
        "Wavelet (db4, lvl8)": lambda sig: wavelet_detrend(sig, wavelet="db4", level=8)
    }
    
    print(f"\nEvaluating {len(trials)} trials with locked Threshold = {OPTIMAL_THRESHOLD}")
    print("-" * 75)
    print(f"{'Method':<20} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10} | {'FP':<5}")
    print("-" * 75)
    
    for name, process_signal in methods.items():
        all_matched = []
        all_missed = []
        total_fp = 0
        
        for trial in trials:
            # 1. Apply the specific correction method
            processed_sig = process_signal(trial["horizontal"])
            
            # 2. Detect events using the locked optimal threshold
            events = detect_events(processed_sig, FS, velocity_threshold=OPTIMAL_THRESHOLD)
            
            # 3. Evaluate against ground truth
            matched, missed, false = evaluate_events(events, trial["control"])
            
            all_matched.extend(matched)
            all_missed.extend(missed)
            total_fp += len(false)
            
        precision, recall, f1 = calculate_metrics(all_matched, all_missed, total_fp)
        
        print(f"{name:<20} | {precision:.4f}     | {recall:.4f}     | {f1:.4f}     | {total_fp:<5}")

if __name__ == "__main__":
    main()