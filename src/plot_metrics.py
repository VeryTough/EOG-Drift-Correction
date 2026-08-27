print("GENERATING METRICS CHART...")
import matplotlib.pyplot as plt

def main():
    methods = ['Raw', 'High-pass', 'Polynomial', 'Wavelet (lvl8)']
    f1_scores = [0.8827, 0.8796, 0.8864, 0.8810]
    false_positives = [119, 124, 110, 120]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot F1 Scores as Bars
    bars = ax1.bar(methods, f1_scores, color=['#d3d3d3', '#4C72B0', '#55A868', '#C44E52'], alpha=0.8)
    ax1.set_ylabel('Overall F1-Score', fontweight='bold', fontsize=12)
    ax1.set_ylim(0.87, 0.89) # Zoomed in to highlight the differences

    # Add data labels on top of the bars
    for bar in bars:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.0002, f'{yval:.4f}', ha='center', va='bottom', fontweight='bold')

    # Plot False Positives as a Line on a secondary axis
    ax2 = ax1.twinx()
    ax2.plot(methods, false_positives, color='black', marker='o', linewidth=2, markersize=8, linestyle='dashed')
    ax2.set_ylabel('Total False Positives', fontweight='bold', fontsize=12)
    ax2.set_ylim(105, 130)

    plt.title('Method Comparison: F1-Score vs. False Positives', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('final_metrics_chart.png', dpi=300)
    print("Success! Saved as 'final_metrics_chart.png'")
    plt.show()

if __name__ == "__main__":
    main()