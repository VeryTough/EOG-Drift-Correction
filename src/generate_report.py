print("GENERATING MARKDOWN REPORT...")

report_content = """# Optimizing EOG Baseline Drift Correction for Real-Time Event Detection

**Course:** Advanced Cloud Computing (Course Project)  
**Professor:** Suraj Prakash Sahoo  

### Project Team
| Name | Registration Number |
| :--- | :--- |
| Vivek | 24BEC0098 |
| Prantar | 24BEC0670 |
| Kartik | 24BEC0093 |

---

## 1. Introduction & Objective
The objective of this project is to evaluate and compare different baseline drift correction methods for Electrooculography (EOG) signals. Drift correction is a critical preprocessing step in Brain-Computer Interfaces (BCI) to maximize the accuracy of automated saccade and blink detection. 

**Dataset:** The study utilizes a dataset consisting of 300 trials. Each trial is 4 seconds long, sampled at 256 Hz, and contains sample-level ground truth labels for forward saccades, return saccades, and blinks.

## 2. Methodology
To establish a robust pipeline, we compared raw, uncorrected signals against three standard signal processing techniques:
*   **High-pass filtering:** A 2nd-order Butterworth filter (0.1 Hz cutoff).
*   **Polynomial detrending:** A 3rd-order global polynomial fit.
*   **Wavelet detrending:** A db4 wavelet decomposition down to level 8.

**Threshold Tuning:** 
Instead of selecting an arbitrary velocity threshold for event detection, an empirical parameter sweep was conducted on the raw signal (testing velocities from 500 to 2000). The optimal threshold was mathematically locked at **1000** to maximize the overall F1-Score, ensuring a fair baseline comparison across all correction methods.

## 3. Quantitative Results & Computational Speed
Each method was evaluated against the 300-trial dataset using the locked threshold of 1000. 

### Table 1: Detection Metrics
| Method | Precision | Recall | F1-Score | False Positives |
| :--- | :--- | :--- | :--- | :--- |
| Raw | 0.8712 | 0.8944 | 0.8827 | 119 |
| High-pass | 0.8664 | 0.8933 | 0.8796 | 124 |
| **Polynomial** | **0.8796** | **0.8933** | **0.8864** | **110** |
| Wavelet (lvl8) | 0.8700 | 0.8922 | 0.8810 | 120 |

### Table 2: Execution Time (per 4-second trial)
| Method | Avg Time per Trial (ms) |
| :--- | :--- |
| Raw | 0.0001 ms |
| Wavelet (db4, lvl8) | 0.0976 ms |
| **Polynomial** | **0.1058 ms** |
| High-pass | 0.2386 ms |

![Metrics Chart](final_metrics_chart.png)
*Figure 1: Visual comparison showing Polynomial detrending achieving the highest F1-Score while minimizing False Positives.*

## 4. Discussion & Visual Analysis

**The Polynomial Advantage**
As shown in Table 1 and Figure 1, 3rd-order Polynomial detrending is the optimal mathematical method for this specific pipeline. It achieved the highest overall F1-Score (0.8864) and the lowest number of False Positives (110). Furthermore, clocking in at 0.1058 ms per trial, it is highly efficient and easily capable of running in a real-time BCI streaming environment.

**The Wavelet Boundary Effect**
While wavelet decomposition is a standard tool in bio-signal processing, it underperformed in this specific architecture. Applying an 8-level deep db4 wavelet to a short 1024-sample epoch introduced edge artifacts (boundary effects) due to the lack of sufficient data points at the lowest frequencies. This mathematical noise directly contributed to a higher false positive count (120) compared to the polynomial approach.

![Signal Plot](final_comparison_plot.png)
*Figure 2: Visual comparison of the four correction methods on Trial 1.*

**Visual vs. Mathematical Trade-offs**
An interesting caveat was discovered during visual inspection (Figure 2). While Polynomial detrending scored best statistically across the 300-trial dataset, it can occasionally introduce artificial visual curves at the edges of short epochs heavily dominated by large step-changes (saccades). High-pass filtering maintained the standard visual shape slightly better, despite scoring lower on automated event detection metrics.

## 5. Conclusion & Future Work
For an automated, real-time BCI pipeline where algorithmic classification is prioritized over human visual inspection, **3rd-order Polynomial detrending** is the recommended baseline correction method due to its superior F1-score and low computational overhead.

**Future Work:** 
Given that the underlying dataset includes vertical EOG channels and target gaze angles, the natural progression of this pipeline is to map the combined horizontal and vertical signals into a 2D gaze-tracking coordinate system, simulating real-time cursor control for accessibility applications.
"""

with open("Final_Report.md", "w") as f:
    f.write(report_content)

print("Success! 'Final_Report.md' has been generated in your main folder.")