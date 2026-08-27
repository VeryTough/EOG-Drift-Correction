print("RUNNING SPEED TEST...")

import time
import warnings
from dataset import load_subject, extract_trials
from drift_correction import highpass_filter, polynomial_detrend, wavelet_detrend

# Ignore the wavelet warning for the speed test to keep output clean
warnings.filterwarnings("ignore")

FS = 256

def main():
    eog, control, target_ga = load_subject("S1")
    trials = extract_trials(eog, control, target_ga)
    
    methods = {
        "Raw": lambda sig: sig,
        "High-pass": lambda sig: highpass_filter(sig, FS),
        "Polynomial": lambda sig: polynomial_detrend(sig, order=3),
        "Wavelet (db4, lvl8)": lambda sig: wavelet_detrend(sig, wavelet="db4", level=8)
    }
    
    print(f"\nTiming {len(trials)} trials (1024 samples each)...")
    print("-" * 45)
    print(f"{'Method':<20} | {'Avg Time per Trial (ms)'}")
    print("-" * 45)
    
    for name, process_signal in methods.items():
        start_time = time.perf_counter()
        
        for trial in trials:
            # We are only measuring the execution time of the drift correction itself
            _ = process_signal(trial["horizontal"])
            
        end_time = time.perf_counter()
        
        # Calculate average time in milliseconds
        avg_time_ms = ((end_time - start_time) / len(trials)) * 1000
        
        print(f"{name:<20} | {avg_time_ms:.4f} ms")

if __name__ == "__main__":
    main()