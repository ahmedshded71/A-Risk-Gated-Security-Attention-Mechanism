# RGSA-Transformer v5.6.2
### Risk-Gated Security Attention Mechanism for Real-Time Intrusion Detection Systems (IDS)

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/Framework-TensorFlow/Keras-orange.svg)](https://www.tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Q1%20Journal%20Ready-brightgreen.svg)]()

---

## 📖 Overview
This repository presents the complete, executable implementation of **RGSA-Transformer v5.6.2**, a state-of-the-art deep learning framework for Network Intrusion Detection. It introduces a novel **Risk-Gated Security Attention (RGSA)** mechanism deployed within a **Mandatory Two-Stage Pipeline**. 

Designed for real-time, high-throughput environments, this framework evaluates network traffic across enterprise (CIC-IDS2017/2018) and IoT (CIC-IoT2023) datasets, providing rigorous latency profiling, hierarchical security-based class balancing, and publication-ready evaluation metrics.

## 🌟 Key Features
- 🧠 **Risk-Gated Security Attention (RGSA)**: A custom Transformer layer that dynamically modulates attention weights using a learned risk-gating mechanism, focusing computational power on high-risk network flow segments.
- ⚙️ **Mandatory Two-Stage Pipeline**:
  - **Stage 1 (Binary Detector)**: Rapidly filters Benign vs. Attack traffic to minimize false negatives (FNR).
  - **Stage 2 (Multiclass Classifier)**: Identifies specific attack types using Sparse Focal Loss to handle extreme class imbalance.
- ⚖️ **Hierarchical Security Balancing**: Implements NIST-aligned oversampling strategies based on security tiers (🔴 Critical, 🟡 Moderate, 🟢 Common) and CVE severities. Automatically injects synthetic BENIGN samples if missing (e.g., CIC-IoT2023).
- ⏱️ **Real-Time Deployment Profiling**: Measures precise per-sample inference latency (P50, P90, P95, P99) and throughput (samples/sec) to guarantee real-time IDS viability.
- 📊 **Publication-Ready Visualizations**: Generates 300 DPI confusion matrices featuring **RAW COUNTS** (actual sample numbers) alongside percentages, ROC/AUC curves, and training dynamics.
- 📑 **Automated Methodology Reporting**: Outputs comprehensive JSON, TXT, and CSV reports detailing sample breakdowns, tier statistics, and performance metrics for full reproducibility.

## 🏗️ Architecture Details
1. **Security Tokenizer**: Maps raw network flow features into semantic security tokens.
2. **RGSA Layer**: Computes Query-Key interactions and applies a `risk_gate` (Sigmoid) to suppress low-risk noise and amplify critical threat signatures.
3. **Hierarchical Class Weighting**: Assigns loss weights dynamically based on the real-world impact of the attack (e.g., Heartbleed/Botnet receive higher weights than PortScan).
4. **Sparse Focal Loss**: Custom loss function for the multiclass stage to force the model to focus on hard-to-classify, minority attack vectors.

## 📂 Supported Datasets
The framework includes flexible path discovery and unified label mapping for:
- **CIC-IDS2017** (Enterprise Network Traffic)
- **CIC-IDS2018** (Modern Enterprise & DDoS Traffic)
- **CIC-IoT2023** (Internet of Things Network Traffic)

## 🚀 Installation & Requirements
```bash
# Clone the repository
git clone https://github.com/yourusername/RGSA-Transformer-IDS.git
cd RGSA-Transformer-IDS

# Install dependencies
pip install numpy pandas matplotlib seaborn scikit-learn tensorflow
```

## 💻 Usage
Ensure your datasets are placed in the expected directories (or update the `DATASET_PATHS` dictionary in the script). Run the main execution block:

```bash
# Execute via Python script
python eslam-fouda-ahmed-saad-code.py

# Or execute the Jupyter Notebook
jupyter notebook eslam-fouda-ahmed-saad-code.ipynb
```

The script will automatically:
1. Discover and load the datasets.
2. Apply hierarchical balancing and synthetic BENIGN injection (if needed).
3. Train the Binary Detector (Stage 1).
4. Measure inference latency and throughput.
5. Train the Multiclass Classifier (Stage 2).
6. Generate integrated evaluation metrics and save all visualizations/reports.

## 📈 Generated Outputs
Upon execution, the framework generates a comprehensive suite of artifacts:
- **Visualizations**: `confusion_matrix_raw_*.png` (with actual counts), `roc_auc_*.png`, `training_curves_*.png`.
- **Models**: `best_binary_*.keras`, `best_multiclass_*.keras`.
- **Reports**: 
  - `methodology_*.json` (Balancing strategy & tier stats)
  - `methodology_report_*_v5.6.2.txt` (Full Q1 journal-ready methodology breakdown)
  - `rgsa_results_*_v5.6.2.csv` (Detailed metrics per dataset)
  - `inference_time_summary_v5.6.2.txt` (Real-time deployment readiness assessment)

## 🎓 Publication Readiness
This codebase is structured to meet the rigorous standards of **Q1 Cybersecurity & AI Journals (e.g., IEEE TIFS, TDSC)**. 
- ✅ Mandatory two-stage pipeline (eliminates single-stage bias).
- ✅ Transparent sample count tracking & reproducibility.
- ✅ Real-time deployment feasibility proven via P99 latency metrics.
- ✅ Security-tier-aligned evaluation (beyond standard accuracy).

## 📜 Citation
If you use this code or framework in your research, please cite:
```bibtex
@misc{RGSA-Transformer-v5.6.2,
  author = {Eslam Fouda, Ahmed Saad},
  title = {RGSA-Transformer: Risk-Gated Security Attention Mechanism for Real-Time IDS},
  year = {2026},
  version = {5.6.2},
  publisher = {GitHub},
  url = {https://github.com/yourusername/RGSA-Transformer-IDS}
}
```

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.