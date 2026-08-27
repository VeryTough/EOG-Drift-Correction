print("GENERATING PLOT...")

import matplotlib.pyplot as plt
import warnings
from dataset import load_subject, extract_trials
from drift_correction import highpass_filter, polynomial_detrend, wavelet_detrend

warnings.filterwarnings("ignore")
FS = 256

def main():
    eog, control, target_ga = load_subject("S1")
    trials = extract_trials(eog, control, target_ga)
    
    # Grab the very first trial for visualization
    trial = trials[0]
    sig = trial["horizontal"]
    
    # Apply corrections
    sig_hp = highpass_filter(sig, FS)
    sig_poly = polynomial_detrend(sig, order=3)
    sig_wav = wavelet_detrend(sig, wavelet="db4", level=8)
    
    # Create the plot
    fig, axs = plt.subplots(4, 1, figsize=(10, 8), sharex=True)
    fig.suptitle("EOG Drift Correction Methods (Trial 1)", fontsize=14, fontweight='bold')
    
    axs[0].plot(sig, color='gray')
    axs[0].set_title("1. Raw Signal")
    
    axs[1].plot(sig_hp, color='blue')
    axs[1].set_title("2. High-pass Filter")
    
    axs[2].plot(sig_poly, color='green')
    axs[2].set_title("3. Polynomial Detrending (Best Overall)")
    
    axs[3].plot(sig_wav, color='red')
    axs[3].set_title("4. Wavelet Detrending (db4, lvl8)")
    
    plt.tight_layout()
    plt.savefig("final_comparison_plot.png")
    print("Success! Saved as 'final_comparison_plot.png' in your main folder.")
    plt.show()

if __name__ == "__main__":
    main()