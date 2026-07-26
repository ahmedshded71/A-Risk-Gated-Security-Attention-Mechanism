# 🛡️ RGSA-Transformer
### A Risk-Gated Security Attention Mechanism for Rare Threat Detection in Industrial IoT Intrusion Detection

[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![TensorFlow 2.15](https://img.shields.io/badge/TensorFlow-2.15-orange.svg)](https://www.tensorflow.org/)
[![Keras 3.0](https://img.shields.io/badge/Keras-3.0-red.svg)](https://keras.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Journal](https://img.shields.io/badge/Journal-Network%20(MDPI)-purple.svg)](https://www.mdpi.com/journal/network)
[![Status](https://img.shields.io/badge/Status-Peer%20Review%20Ready-brightgreen.svg)]()
[![Domain](https://img.shields.io/badge/Domain-IIoT%20%26%20Neuro--Symbolic%20AI-blueviolet.svg)]()

---

## 👥 Authors & Affiliations

| Author | Affiliation | ORCID |
| :--- | :--- | :--- |
| **Shaimaa Ahmed Elsaid** <sup>1,*</sup> | Department of Computer Engineering, College of Computer Engineering and Sciences, Prince Sattam bin Abdulaziz University, Al-Kharj 16278, Saudi Arabia | — |
| **Eslam Mahmoud Fouda** <sup>2</sup> | Electronics and Communications Department, Air Defense College, Egyptian Military Academy, Egypt | — |
| **Ahmed M. Saad** <sup>3</sup> | Computers and Control Systems Department, Air Defense College, Egyptian Military Academy, Egypt | — |

<sup>*</sup> **Corresponding author:** sh.ahmed@psau.edu.sa

---

## 📖 Abstract

Current intrusion detection systems primarily focus on learning recurring data traffic patterns, leading to the overlooking of rare and highly dangerous threats. To address this significant gap, we propose the **Risk-Gated Security Attention (RGSA)** mechanism — the first of its kind in the field. Systematic algorithmic improvements have been introduced to enhance the capability to detect sporadic and covert attacks:

1. **Threat Semantics Translation**: The framework translates threat semantics from **CVE/CVSS databases** into formal encodings, processed by the neural attention mechanism as structured language units.
2. **Dynamic Risk Prioritization**: The most serious threat attributes are prioritized by a dynamically trainable **risk gateway**, even if statistically rare, while guiding model training with a **risk-weighted loss** to minimize real-world security impacts rather than solely category frequency.
3. **Forensic Integrity Preservation**: The use of synthetic oversampling techniques (SMOTE, GANs) has been **completely excluded for attack classes**. For purely attack datasets, a limited number of low-volume benign synthetic samples were added to implement the mandatory two-stage processing path.

Extensive testing on **CIC-IDS2017**, **CIC-IDS2018**, and **CIC-IoT2023** demonstrates that RGSA elevates detection capabilities to a higher and more sophisticated level, resulting in an extremely low **False Negative Rate (FNR ≤ 0.28%)** for critical threats, a very high level of classification accuracy for critical attack categories (**F1 = 0.9957 – 1.0000**), and strong cross-domain generalization (**weighted F1 ≥ 0.9985**).

**Keywords:** Intrusion Detection System (IDS); Risk-Gated Security Attention (RGSA); Neuro-Symbolic AI; Attention Mechanism; Risk-Aware Deep Learning; CVE/CVSS; Security Data Integrity; Class Imbalance; Network Security.

---

## 🏆 Key Results (Empirical Validation)

The following metrics are extracted directly from the experimental evaluation in the paper (Tables 5, 6, and 7), demonstrating RGSA's superiority in detecting rare, high-impact threats while exceeding **NIST SP 800-115** operational standards.

### Binary Detection Performance (Stage 1 — Table 5)

| Dataset | Accuracy (%) | Recall (%) | Precision (%) | F1-Score | FNR (%) ↓ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **CIC-IDS2017** (Enterprise) | 98.70 | 99.72 | 98.10 | 0.9892 | **0.28** |
| **CIC-IDS2018** (Modern Enterprise) | 99.97 | 99.96 | 99.98 | 0.9997 | **0.04** |
| **CIC-IoT2023** (Industrial IoT) | 99.95 | 99.98 | 99.96 | 0.9998 | **0.03** |

### Multiclass Classification Performance (Stage 2 — Table 6)

| Dataset | Attack Types | Accuracy (%) | Macro-F1 | Weighted-F1 | Critical F1 | Critical Recall (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **CIC-IDS2017** | 8 | 99.94 | 0.9966 | 0.9994 | 0.9957 | 99.39 |
| **CIC-IDS2018** | 4 | 99.99 | 1.0000 | 0.9999 | 1.0000 | 100.00 |
| **CIC-IoT2023** | 6 | 99.85 | 0.9889 | 0.9985 | 0.9969 | 99.59 |

### Critical Attack Detection — Forensic Fidelity (Table 7)

| Dataset | Attack Type | CVE/Reference | Severity | Recall (%) | Precision (%) | F1-Score | Support |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| CIC-IDS2017 | **Heartbleed** | CVE-2014-0160 | 🔴 CRITICAL | 100.00 | 100.00 | **1.0000** | 103 |
| CIC-IDS2017 | **Infiltration** | N/A | 🔴 CRITICAL | 96.48 | 100.00 | **0.9821** | 341 |
| CIC-IDS2017 | **Botnet** | N/A | 🟠 HIGH | 99.85 | 99.70 | **0.9978** | 2,024 |
| CIC-IDS2018 | **WebAttack_SQLi** | N/A | 🟠 HIGH | 100.00 | 100.00 | **1.0000** | 866 |
| CIC-IDS2018 | **Botnet** | N/A | 🔴 CRITICAL | 100.00 | 100.00 | **1.0000** | 113,939 |
| CIC-IoT2023 | **Mirai** | N/A | 🔴 CRITICAL | 99.59 | 99.80 | **0.9969** | 210,730 |

> 💡 **Why this matters:** Traditional attention-based IDS models typically exhibit 40%–70% error rates on rare attacks like Heartbleed or Infiltration. RGSA's risk-gated mechanism successfully reverses this paradox, achieving near-perfect recall on statistically rare but highly critical threats without compromising overall accuracy or relying on synthetic data artifacts.

---

## 🌟 Core Contributions

This research is the **first to modify and use the architecture of a Risk-Gated Security Attention (RGSA) Transformer** to design an efficient IDS for IIoT networks. The main modifications include:

### 1. 🧠 Security-Aware Tokenization
Raw traffic is broken into properly grouped segments, each associated with a specific **MITRE ATT&CK tactic**, so that token relationships constituting domain-specific forensics are not lost during the standard process of unordered tokens.

### 2. ⚡ Risk-Gated Attention Mechanism
Attention is modulated dynamically by a **learnable risk estimator**, which forces the model to focus on rare and high-impact threats even when the class imbalance is severe. The mechanism computes:
- Query-Key bilinear fusion: $W_{int}([Q_{exp}, K_{exp}])$
- Token-level risk estimation: $\text{Sigmoid}(W_{risk} \cdot \text{Token})$
- Gated attention: $\alpha_{ij} = \text{interaction\_gate}_{ij} \times \text{risk\_score}_{i}$

### 3. ⚖️ Authenticity-Preserving Class Balancing
A hierarchical tier-aware balancing strategy uses **exact duplication of real attack samples**. By completely avoiding synthetic oversampling (SMOTE/GANs) for attack classes, the forensic integrity of network flows is preserved. Only a minimal benign injection is performed on purely malicious datasets to enable pipeline functionality.

### 4. 🎯 Adaptive Single/Two-Stage Pipeline
The framework automatically determines the suitable detection pipeline based on the label distribution in the training dataset:
- **Two-Stage Mode** (when benign traffic exists): Binary detector → Multiclass classifier
- **Single-Stage Mode** (when 100% attacks): Direct multiclass classification

### 5. 🔥 Tier-Aware Focal Loss
A risk-weighted focal loss ($\gamma = 3.0$) combined with hierarchical class weighting optimizes detection based on **security severity** rather than statistical frequency:

$$FL(p_t) = -\alpha_{y} \cdot (1 - p_t)^{\gamma} \cdot \log(p_t)$$

Where $\alpha_y$ is derived from NIST SP 800-115 security tiers:
- 🔴 **Critical Tier**: weight = 50.0 (Heartbleed, Infiltration, Botnet, Mirai, WebAttack_SQLi)
- 🟡 **Moderate Tier**: weight = 2.0 (DoS_Slow, DoS_GoldenEye, BruteForce_SSH, DDoS_TCP)
- 🟢 **Common Tier**: weight = 1.0 (DoS_Hulk, PortScan, DDoS_UDP, DDoS_HTTP, Reconnaissance)
- ⚪ **Benign**: weight = 0.7

---

## 📊 Dataset Characteristics (Table 2)

| Feature | CIC-IDS2017 | CIC-IDS2018 | CIC-IoT2023 |
| :--- | :---: | :---: | :---: |
| **Total Samples (Original)** | 2,830,743 | 4,580,217 | 1,245,873 |
| **Benign Traffic Ratio** | 85.2% | 78.6% | 0.0% (100% attacks) |
| **Attack Classes** | 14 | 17 | 7 |
| **Critical Attacks** | Heartbleed, Infiltration | Botnet, WebAttack_SQLi | Mirai, DDoS_TCP |
| **Numerical Features** | 78 | 83 | 68 |
| **Traffic Type** | NetFlow (Enterprise) | NetFlow (Enterprise) | IoT Device Flows |
| **Security Standard** | NIST SP 800-94 | NIST SP 800-115 | IEEE 802.15.4 |

---

## ⚙️ Experimental Setup (Table 3)

| Component/Parameter | Specification |
| :--- | :--- |
| **Execution Platform** | Kaggle (Python 3.10, TensorFlow 2.15, Keras 3.0) |
| **Hardware Acceleration** | NVIDIA Tesla T4 GPU (16GB VRAM) |
| **Feature Normalization** | MinMaxScaler (range [0, 1]) |
| **Data Splitting** | 80% training / 20% testing with stratified sampling |
| **Security Tokenizer** | 5 security tokens × 32 dimensions per token |
| **Attention Mechanism** | Risk-Gated Security Attention (RGSA) |
| **Loss Function** | Sparse Categorical Focal Loss ($\gamma = 3.0$) |
| **Class Weighting** | Hierarchical: Critical=50.0, Moderate=2.0, Common=1.0, Benign=0.7 |
| **Optimizer** | Adam (initial LR = 1e-3, ReduceLROnPlateau patience=5) |
| **Regularization** | Dropout (0.3–0.4), BatchNorm, LayerNorm |
| **Training Protocol** | Max 35 epochs with EarlyStopping (patience=8) |
| **Operational Modes** | Adaptive: Two-stage (benign present) / Single-stage (100% attacks) |
| **Total Parameters** | **284,317** (fully trainable) |
| **Training Duration** | 27–35 epochs (EarlyStopping dependent) |

---

## 📉 Ablation Study: Basic vs. Advanced RGSA (Table 8)

The ablation study reveals that the advanced RGSA model (with risk-controlled pruning and NIST-compliant dynamic balancing) achieves the optimal balance between sensitivity and accuracy:

| Dataset | Task | Model Variant | Accuracy (%) | Recall (%) | F1-Score | FNR (%) ↓ |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| CIC-IDS2017 | Binary | Basic RGSA | 98.13 | 98.20 | 0.9748 | 0.60 |
| | | **Advanced RGSA** | **98.70** | **99.72** | **0.9892** | **0.28** |
| | Multiclass | Basic RGSA | 98.62 | 98.85 | 0.9801 | 0.45 |
| | | **Advanced RGSA** | **99.94** | **99.39** | **0.9957** | **0.61** |
| CIC-IDS2018 | Binary | Basic RGSA | 98.65 | 98.72 | 0.9848 | 0.38 |
| | | **Advanced RGSA** | **99.97** | **99.96** | **0.9997** | **0.04** |
| | Multiclass | Basic RGSA | 98.88 | 98.95 | 0.9902 | 0.15 |
| | | **Advanced RGSA** | **99.99** | **100.00** | **1.0000** | **0.00** |
| CIC-IoT2023 | Binary | Basic RGSA | 99.22 | 98.85 | 0.9872 | 0.35 |
| | | **Advanced RGSA** | **99.95** | **99.98** | **0.9998** | **0.03** |
| | Multiclass | Basic RGSA | 98.55 | 98.20 | 0.9847 | 0.80 |
| | | **Advanced RGSA** | **99.85** | **99.59** | **0.9969** | **0.41** |

---

## 📁 Project Structure

```
A-Risk-Gated-Security-Attention-Mechanism/
│
├── main.py                              # Entry point
├── pyproject.toml                       # Dependencies (uv)
├── README.md                            # This file
├── LICENSE                              # MIT License
├── .gitignore
├── .python-version                      # Python 3.10
├── uv.lock                              # Locked dependencies
│
├── Dockerfile                           # CPU Docker image
├── Dockerfile.gpu                       # GPU Docker image (CUDA)
├── docker-compose.yml                   # CPU orchestration
├── docker-compose.gpu.yml               # GPU orchestration
├── .dockerignore
│
├── scripts/
│   ├── entrypoint.sh                    # Container startup
│   └── run.sh                           # Quick CLI runner
│
├── src/
│   └── rgsa/
│       ├── __init__.py
│       ├── config.py                    # Constants, paths, mappings, tiers
│       ├── data/
│       │   ├── loader.py                # Dataset discovery & preprocessing
│       │   └── balancing.py             # Hierarchical balancing + BENIGN injection
│       ├── models/
│       │   ├── architecture.py          # SecurityTokenizer, RGSA Attention
│       │   └── losses.py                # sparse_focal_loss (γ=3.0)
│       ├── training/
│       │   ├── pipeline.py              # Two-stage pipeline orchestration
│       │   └── weights.py               # Hierarchical class weights
│       ├── evaluation/
│       │   ├── metrics.py               # Specificity, inference timing (P50-P99)
│       │   └── visualization.py         # CM (raw counts), ROC/AUC, curves
│       └── utils/
│           └── reporting.py             # JSON/TXT/CSV report generation
│
├── data/                                # Place CSV datasets here
│   └── .gitkeep
│
└── outputs/                             # Generated artifacts
    └── .gitkeep
```

---

## 🚀 Installation & Requirements

### Option 1: Modern & Fast (Recommended — using `uv`)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/RGSA-Transformer-IDS.git
cd RGSA-Transformer-IDS

# 2. Install uv (if not installed)
# Linux/macOS:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows PowerShell:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 3. Initialize and install dependencies instantly
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
pip install numpy==1.26.4 pandas==2.2.1 matplotlib==3.8.3 seaborn==0.13.2 scikit-learn==1.4.1 tensorflow==2.15.0
```

### Option 3: Docker (Recommended for Reproducibility)

```bash
# Build the image (from repository root)
docker build -t rgsa-transformer:5.6.2-cpu .

# Run the container mounting local data and outputs
docker run --rm -it \
  -v $(pwd)/data:/app/data:ro \
  -v $(pwd)/outputs:/app/outputs \
  rgsa-transformer:5.6.2-cpu

# Or use docker-compose
docker compose up --build

# For GPU support (requires NVIDIA drivers + NVIDIA Container Toolkit)
docker compose -f docker-compose.gpu.yml up --build
```

---

## 💻 Usage

### 1. Place Datasets

Put your CSV files in the `./data/` directory:

```bash
cp /path/to/combine.csv data/           # CIC-IDS2017
cp /path/to/merged_dataset.csv data/    # CIC-IDS2018
cp /path/to/cic_iot2023.csv data/       # CIC-IoT2023
```

### 2. Run the Pipeline

```bash
# Execute the modular pipeline
uv run python main.py

# Or execute the original Jupyter Notebook
jupyter notebook eslam-fouda-ahmed-saad-code.ipynb
```

The pipeline will automatically:

1. Discover and load the datasets with unified attack label mapping.
2. Apply hierarchical security-tier balancing (injecting synthetic BENIGN **only** if the dataset is 100% attacks).
3. Train the Binary Detector (Stage 1) and measure per-sample inference latency.
4. Train the Multiclass Classifier (Stage 2) with Sparse Focal Loss and hierarchical class weights.
5. Generate integrated evaluation metrics, confusion matrices (with raw counts), and comprehensive methodology reports.

---

## 📈 Generated Outputs

Upon execution, the framework generates a comprehensive suite of artifacts in the `./outputs/` directory:

### Visualizations (300 DPI)
- `confusion_matrix_raw_binary_detector_*.png` — Binary stage with actual counts
- `confusion_matrix_raw_multiclass_classifier_*.png` — Multiclass stage with actual counts
- `roc_auc_binary_*.png` — Binary ROC/AUC curve
- `roc_auc_multiclass_*.png` — Multiclass One-vs-Rest ROC/AUC curves
- `training_curves_binary_detector_*.png` — Accuracy and loss curves
- `training_curves_multiclass_classifier_*.png` — Accuracy and loss curves

### Models
- `best_binary_*.keras` — Best binary detector weights
- `best_multiclass_*.keras` — Best multiclass classifier weights

### Reports
- `methodology_*.json` — Balancing strategy, duplication factors, and tier stats
- `methodology_report_*_v5.6.2.txt` — Full Q1 journal-ready methodology breakdown
- `rgsa_results_*_v5.6.2.csv` — Detailed metrics per dataset
- `rgsa_multi_dataset_comparison_v5.6.2.csv` — Cross-dataset comparison
- `inference_time_summary_v5.6.2.txt` — Real-time deployment readiness assessment

---

## 🎓 Publication Readiness

This codebase is explicitly structured to meet the rigorous reproducibility and evaluation standards of **Q1 Cybersecurity & AI Journals** (e.g., IEEE TIFS, TDSC, IEEE IoT Journal, MDPI Network):

- ✅ **Mandatory two-stage pipeline** (eliminates single-stage evaluation bias).
- ✅ **Forensic data integrity** (explicit rejection of SMOTE/GANs for attack classes).
- ✅ **Transparent sample count tracking** (detailed breakdowns in all reports).
- ✅ **Real-time deployment feasibility** proven via P99 latency and throughput metrics.
- ✅ **Security-tier-aligned evaluation** (NIST SP 800-115 impact metrics, not just macro-accuracy).
- ✅ **Per-sample inference time metrics** (avg, P50, P90, P95, P99).
- ✅ **6 Confusion matrices with RAW COUNTS** (actual numbers, not just percentages).
- ✅ **Ablation study** demonstrating the effectiveness of RGSA enhancements.
- ✅ **Cross-dataset comparative analysis** against state-of-the-art models.

---

## 🔬 Reproducibility

All experiments were conducted on the **Kaggle platform** with the following configuration:

- **Python**: 3.10
- **TensorFlow**: 2.15
- **Keras**: 3.0
- **Hardware**: NVIDIA Tesla T4 GPU (16GB VRAM)
- **Random Seeds**: `np.random.seed(42)`, `tf.random.set_seed(42)`
- **Data Split**: 80% training / 20% testing with stratified sampling
- **Total Parameters**: 284,317 (fully trainable)
- **Training Duration**: 27–35 epochs (EarlyStopping dependent)

The complete execution log and all generated artifacts are available in the [Kaggle notebook](https://www.kaggle.com/code/eslamfouda/eslam-fouda-ahmed-saad-code).

---

## 🔮 Future Work

The following research directions will be pursued:

1. **Direct Threat Intelligence Integration**: Exploiting **CISA KEV** (Known Exploited Vulnerabilities) catalog to adapt to zero-day vulnerabilities in real-time.
2. **Adversarial Robustness**: Conducting adversarial attack research to evaluate and strengthen the model against sophisticated evasion techniques.
3. **Real-Time SDN Deployment**: Implementing the model in real-time **Software-Defined Networking (SDN)** environments with hardware acceleration (FPGA/TPU).
4. **Privacy-Preserving Federated Learning**: Transitioning to federated learning while maintaining the risk management mechanism to ensure collaborative, privacy-preserving defense across enterprise boundaries.

---

## ⚠️ Limitations

- The method relies on carefully designed mappings from **CVE/CVSS databases**, which may require updates as new vulnerabilities emerge.
- Testing with reference datasets may limit the generalization of results to new, unseen attack classifications.
- The current implementation focuses on offline batch processing; real-time streaming deployment requires additional optimization.

---

## 📜 Citation

If you use this code, framework, or methodology in your research, please cite our work:

### BibTeX

```bibtex
@article{elsaid2026rgsa,
  title={A Risk-Gated Security Attention Mechanism for Rare Threat Detection in Industrial IoT Intrusion Detection},
  author={Elsaid, Shaimaa Ahmed and Fouda, Eslam Mahmoud and Saad, Ahmed M.},
  journal={Network},
  volume={6},
  number={x},
  pages={X--X},
  year={2026},
  publisher={MDPI},
  doi={10.3390/network60x0000},
  note={Code available at: https://github.com/yourusername/RGSA-Transformer-IDS}
}
```

### APA

> Elsaid, S. A., Fouda, E. M., & Saad, A. M. (2026). A Risk-Gated Security Attention Mechanism for Rare Threat Detection in Industrial IoT Intrusion Detection. *Network, 6*(x), X–X. https://doi.org/10.3390/network60x0000

### IEEE

> S. A. Elsaid, E. M. Fouda, and A. M. Saad, "A Risk-Gated Security Attention Mechanism for Rare Threat Detection in Industrial IoT Intrusion Detection," *Network*, vol. 6, no. x, pp. X–X, 2026, doi: 10.3390/network60x0000.

### MLA

> Elsaid, Shaimaa Ahmed, Eslam Mahmoud Fouda, and Ahmed M. Saad. "A Risk-Gated Security Attention Mechanism for Rare Threat Detection in Industrial IoT Intrusion Detection." *Network* 6.x (2026): X–X.

---

## 🙏 Acknowledgments

This study is supported via funding from **Prince Sattam bin Abdulaziz University**, project number **(PSAU/2025/01/33925)**.

### Dataset Acknowledgments

- **CIC-IDS2017 / CIC-IDS2018**: Canadian Institute for Cybersecurity, University of New Brunswick
- **CIC-IoT2023**: Canadian Institute for Cybersecurity
- **Kaggle Platform**: For computational resources and dataset hosting

### Standards & Frameworks

- **NIST SP 800-115**: Technical Guide to Information Security Testing and Assessment
- **NIST SP 800-94**: Guide to Intrusion Detection and Prevention Systems (IDPS)
- **MITRE ATT&CK**: Globally-accessible knowledge base of adversary tactics and techniques
- **IEEE 802.15.4**: Standard for Low-Rate Wireless Personal Area Networks (LR-WPANs)

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

**Copyright (c) 2026 Shaimaa Ahmed Elsaid, Eslam Mahmoud Fouda, Ahmed M. Saad**

---

## 📬 Contact

For academic collaborations, enterprise deployment inquiries, or technical questions:

- **Corresponding Author**: Shaimaa Ahmed Elsaid — sh.ahmed@psau.edu.sa
- **GitHub Issues**: Please open an issue on this repository for code-related questions.

---

<div align="center">

**⭐ If you find this work useful, please consider starring the repository and citing our paper! ⭐**

*Advancing Industrial IoT Security through Neuro-Symbolic AI*

</div>