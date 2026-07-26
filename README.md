# 🛡️ RGSA-Transformer v5.6.2
### Risk-Gated Security Attention Mechanism for Rare Threat Detection in Industrial IoT Intrusion Detection

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/Framework-TensorFlow/Keras-orange.svg)](https://www.tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Q1%20Journal%20Ready-brightgreen.svg)]()
[![Domain](https://img.shields.io/badge/Domain-Industrial%20IoT%20%26%20Neuro--Symbolic%20AI-purple.svg)]()

---

## 📖 Abstract & Overview
Current Intrusion Detection Systems (IDS) primarily focus on learning recurring data traffic patterns, leading to the overlooking of rare, highly dangerous, and covert threats (e.g., Heartbleed, advanced persistent threats). 

This repository presents the complete, executable implementation of **RGSA-Transformer v5.6.2**, a novel **Neuro-Symbolic AI** framework. It introduces a **Risk-Gated Security Attention (RGSA)** mechanism deployed within a **Mandatory Two-Stage Pipeline**. Unlike traditional models that rely on statistical accuracy, RGSA translates threat semantics from **CVE/CVSS databases** into formal encodings, dynamically prioritizing the most serious threat attributes via a trainable risk gateway. 

Crucially, to preserve **Security Data Integrity** and forensic fidelity, this framework **completely excludes synthetic oversampling (SMOTE/GANs) for attack classes**. Instead, it employs an intelligent, NIST SP 800-115-aligned hierarchical duplication strategy. (Synthetic BENIGN samples are injected *only* in pure-attack datasets like CIC-IoT2023 to enable the mandatory two-stage pipeline).

---

## 🏆 Key Results (Empirical Validation)
Extensive testing across enterprise and IoT environments demonstrates that RGSA elevates detection capabilities to a sophisticated, impact-sensitive level. It **exceeds NIST SP 800-115 operational standards** (Binary FNR < 1.0%) while maintaining **forensic data integrity** (zero SMOTE/GANs used for attack classes).

| Dataset | Binary FNR ↓ | Critical Threat Performance (Multiclass) | Overall Weighted F1 ↑ |
| :--- | :---: | :--- | :---: |
| **CIC-IDS2017**<br>*(Enterprise)* | **0.28%** | • Heartbleed: **F1 = 1.0000** (100% Recall)<br>• Infiltration: **F1 = 0.9821** (96.48% Recall) | **0.9994** |
| **CIC-IDS2018**<br>*(Modern Enterprise)* | **0.04%** | • WebAttack_SQLi: **F1 = 1.0000** (100% Recall)<br>• Botnet: **F1 = 1.0000** (100% Recall) | **0.9999** |
| **CIC-IoT2023**<br>*(Industrial IoT)* | **0.03%** | • Mirai Botnet: **F1 = 0.9969** (99.59% Recall)<br>• Reconnaissance: **F1 = 0.9994** (99.95% Recall) | **0.9984** |

> 💡 **Why this matters:** Traditional attention-based IDS models typically exhibit 40%–70% error rates on rare attacks like Heartbleed or Infiltration. RGSA’s risk-gated mechanism successfully reverses this paradox, achieving near-perfect recall on statistically rare but highly critical threats without compromising overall accuracy.

## 🌟 Core Contributions & Features
- 🧠 **Neuro-Symbolic Risk-Gated Attention**: A custom Transformer layer that computes Query-Key bilinear fusion and modulates attention weights via a learned `risk_gate` (Sigmoid), suppressing low-risk noise and amplifying critical threat signatures.
- ⚙️ **Mandatory Two-Stage Pipeline**: 
  1. **Binary Detector**: Rapidly filters Benign vs. Attack traffic to minimize False Negatives (FNR).
  2. **Multiclass Classifier**: Identifies specific attack types using **Sparse Focal Loss** ($\gamma=3.0$) to handle extreme class imbalance.
- ⚖️ **Forensically Sound Hierarchical Balancing**: Implements NIST-aligned exact duplication based on security tiers (🔴 Critical, 🟡 Moderate, 🟢 Common). **Zero SMOTE/GANs** are used for attacks, preserving real-world flow characteristics.
- ⏱️ **Real-Time Deployment Profiling**: Measures precise per-sample inference latency (P50, P90, P95, P99) and throughput (samples/sec), proving viability for high-traffic IIoT edge environments (< 1 ms/sample).
- 📊 **Publication-Ready Visualizations**: Generates 300 DPI confusion matrices featuring **RAW COUNTS** (actual sample numbers) alongside percentages, ROC/AUC curves, and training dynamics.
- 📑 **Automated Methodology Reporting**: Outputs comprehensive JSON, TXT, and CSV reports detailing sample breakdowns, tier statistics, and performance metrics for full reproducibility.

---

## 🏗️ Architecture & Methodology Details
1. **Security Tokenization Layer**: Decomposes high-dimensional flow representations (78/83/68 features) into 5 semantically meaningful security tokens (32-dim each), aligned with MITRE ATT&CK tactical categories (temporal, payload, protocol, metadata).
2. **RGSA Mechanism**: 
   - Computes $Q, K, V$ projections.
   - Calculates interaction scores: $W_{int}([Q_{exp}, K_{exp}])$.
   - Applies token-level risk estimation: $\text{Sigmoid}(W_{risk} \cdot \text{Token})$.
   - Final attended representation preserves gradient flow via residual connections and Layer Normalization.
3. **Tier-Aware Focal Loss**: Dynamically allocates higher gradient weights to critical-tier attacks (e.g., Heartbleed weight = 50.0) while downplaying easy, common examples (e.g., PortScan weight = 1.0).

---

## 📂 Supported Datasets
The framework includes flexible path discovery and unified label mapping for:
- **CIC-IDS2017**: Enterprise Network Traffic (NetFlow, 78 features)
- **CIC-IDS2018**: Modern Enterprise & DDoS Traffic (NetFlow, 83 features)
- **CIC-IoT2023**: Internet of Things Device Flows (68 features, 100% attack traffic)

---

## 🚀 Installation & Requirements

### Option 1: Modern & Fast (Recommended using `uv`)
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/RGSA-Transformer-IDS.git
cd RGSA-Transformer-IDS

# 2. Initialize and install dependencies instantly with uv
uv sync
```

### Option 2: Traditional `pip`
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/RGSA-Transformer-IDS.git
cd RGSA-Transformer-IDS

# 2. Create virtual environment and install
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt  # numpy, pandas, matplotlib, seaborn, scikit-learn, tensorflow
```

---

### Option 3: Docker (Recommended for reproducible environments)

Build the Docker image and run the container which includes all dependencies and a ready-to-run entrypoint.

```bash
# Build the image (from repository root)
docker build -t rgsa-transformer:latest .

# Run the container mounting local data and outputs (adjust paths as needed)
docker run --rm -it \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/outputs:/app/outputs \
  -p 8888:8888 \
  rgsa-transformer:latest \
  bash -c "uv run python main.py"
```

Notes:
- Use the provided Dockerfile (create one if missing) to pin Python/TensorFlow versions for reproducibility.
- For GPU support, build an image from an official CUDA/TensorFlow base and run with --gpus all.

Docker files included in this repository:

- Dockerfile            — CPU image (used by docker-compose)
- Dockerfile.gpu        — GPU image (CUDA/TensorFlow base)
- docker-compose.yml    — Compose service for CPU
- docker-compose.gpu.yml— Compose service for GPU

Quick helpers:

- scripts/run.sh        — build/run helpers (build, build-gpu, run, gpu, shell, logs, stop, clean, test)
- scripts/entrypoint.sh — container entrypoint (environment and dataset checks)

Examples:

Start using docker-compose (CPU):
```bash
./scripts/run.sh run
```

Start with GPU (requires NVIDIA drivers and nvidia-docker):
```bash
./scripts/run.sh gpu
```


## 💻 Usage

Ensure your datasets (`.csv`) are placed in the `./data/` directory (or update the `DATASET_PATHS` dictionary in `src/rgsa/config.py`).

```bash
# Execute the modular pipeline
uv run python main.py

# Or execute the original Jupyter Notebook
jupyter notebook eslam-fouda-ahmed-saad-code.ipynb
```

**The pipeline will automatically:**
1. Discover and load the datasets with unified attack label mapping.
2. Apply hierarchical security-tier balancing (injecting synthetic BENIGN *only* if the dataset is 100% attacks).
3. Train the Binary Detector (Stage 1) and measure per-sample inference latency.
4. Train the Multiclass Classifier (Stage 2) with Sparse Focal Loss and hierarchical class weights.
5. Generate integrated evaluation metrics, confusion matrices (with raw counts), and comprehensive methodology reports.

---

## 📈 Generated Outputs
Upon execution, the framework generates a comprehensive suite of artifacts in the `./outputs/` directory:
- **Visualizations**: `confusion_matrix_raw_*.png` (300 DPI, actual counts + %), `roc_auc_*.png`, `training_curves_*.png`.
- **Models**: `best_binary_*.keras`, `best_multiclass_*.keras`.
- **Reports**: 
  - `methodology_*.json` (Balancing strategy, duplication factors, and tier stats)
  - `methodology_report_*_v5.6.2.txt` (Full Q1 journal-ready methodology breakdown)
  - `rgsa_results_*_v5.6.2.csv` (Detailed metrics per dataset)
  - `inference_time_summary_v5.6.2.txt` (Real-time deployment readiness assessment)

---

## 🎓 Publication Readiness
This codebase is explicitly structured to meet the rigorous reproducibility and evaluation standards of **Q1 Cybersecurity & AI Journals (e.g., IEEE TIFS, TDSC, IEEE IoT Journal)**:
- ✅ **Mandatory two-stage pipeline** (eliminates single-stage evaluation bias).
- ✅ **Forensic data integrity** (explicit rejection of SMOTE/GANs for attack classes).
- ✅ **Transparent sample count tracking** (detailed breakdowns in all reports).
- ✅ **Real-time deployment feasibility** proven via P99 latency and throughput metrics.
- ✅ **Security-tier-aligned evaluation** (NIST SP 800-115 impact metrics, not just macro-accuracy).

---
## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 

*For academic collaborations or enterprise deployment inquiries, please contact the authors.*