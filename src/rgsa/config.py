"""Configuration constants, paths, and security tier definitions."""
import os

# ------------------ Dataset Path Discovery ------------------
DATASET_PATHS = {
    'CIC-IoT2023': [
        './data/cic_iot2023.csv',
        './CIC-IoT2023/cic_iot2023.csv',
        '../input/cic-iot2023/cic_iot2023.csv',
    ],
    'CIC-IDS2018': [
        './data/merged_dataset.csv',
        './CIC-IDS2018/merged_dataset.csv',
        '../input/cic-ids2018/merged_dataset.csv',
    ],
    'CIC-IDS2017': [
        './data/combine.csv',
        './CIC-IDS2017/combine.csv',
        '../input/cicids2017-full-dataset/combine.csv',
    ],
}

DATASET_KEYWORDS = {
    'CIC-IDS2017': ['cicids2017', 'cic-ids2017', 'combine.csv'],
    'CIC-IDS2018': ['cicids2018', 'cic-ids2018', 'merged_dataset.csv'],
    'CIC-IoT2023': ['ciciot2023', 'cic-iot2023', 'cic_iot2023.csv'],
}

# ------------------ Unified Attack Mapping ------------------
UNIFIED_ATTACK_MAPPING = {
    'BENIGN': 'BENIGN', 'NORMAL': 'BENIGN', '0': 'BENIGN', '0.0': 'BENIGN',
    'DOS_HULK': 'DoS_Hulk', 'D0S_HULK': 'DoS_Hulk', 'DOS HULK': 'DoS_Hulk',
    'DOS_SLOW': 'DoS_Slow', 'D0S_SLOW': 'DoS_Slow', 'SLOWLORIS': 'DoS_Slow',
    'DOS_GOLDENEYE': 'DoS_GoldenEye', 'GOLDENEYE': 'DoS_GoldenEye',
    'DOS_OTHER': 'DoS_Other', 'D0S_OTHER': 'DoS_Other',
    'PORTSCAN': 'PortScan', 'PORT SCAN': 'PortScan',
    'BOTNET': 'Botnet', 'BOT': 'Botnet',
    'HEARTBLEED': 'Heartbleed', 'INFILTRATION': 'Infiltration',
    'DDOS_HOIC': 'DDoS_HOIC', 'HOIC': 'DDoS_HOIC',
    'DDOS_LOIC_HTTP': 'DDoS_LOIC_HTTP', 'LOIC_HTTP': 'DDoS_LOIC_HTTP',
    'DDOS_LOIC_UDP': 'DDoS_LOIC_UDP', 'LOIC_UDP': 'DDoS_LOIC_UDP',
    'BRUTE_FORCE_XSS': 'WebAttack_XSS', 'XSS': 'WebAttack_XSS',
    'BRUTE_FORCE_SQL_INJECTION': 'WebAttack_SQLi', 'SQL_INJECTION': 'WebAttack_SQLi',
    'BRUTE_FORCE_FTP': 'BruteForce_FTP', 'FTP-PATATOR': 'BruteForce_FTP',
    'BRUTE_FORCE_SSH': 'BruteForce_SSH', 'SSH-PATATOR': 'BruteForce_SSH',
    'WEB_ATTACK': 'WebAttack_Other',
    'DDOS_TCP': 'DDoS_TCP', 'TCP': 'DDoS_TCP',
    'DDOS_UDP': 'DDoS_UDP', 'UDP': 'DDoS_UDP',
    'DDOS_HTTP': 'DDoS_HTTP', 'HTTP': 'DDoS_HTTP',
    'MIRAI': 'Mirai', 'MIRAI_BOTNET': 'Mirai',
    'RECONNAISSANCE': 'Reconnaissance', 'RECON': 'Reconnaissance',
    'OSSCAN': 'OS_Scan',
}

# ------------------ Security Tiers (NIST-aligned) ------------------
SECURITY_TIERS = {
    'critical': {
        'HEARTBLEED': {'cve': 'CVE-2014-0160', 'severity': 'CRITICAL'},
        'INFILTRATION': {'cve': 'N/A', 'severity': 'CRITICAL'},
        'BOTNET': {'cve': 'N/A', 'severity': 'HIGH'},
        'MIRAI': {'cve': 'N/A', 'severity': 'CRITICAL'},
        'WEBATTACK_SQLI': {'cve': 'N/A', 'severity': 'HIGH'},
    },
    'moderate': {
        'DOS_SLOW': {'cve': 'N/A', 'severity': 'HIGH'},
        'DOS_GOLDENEYE': {'cve': 'N/A', 'severity': 'MEDIUM'},
        'BRUTEFORCE_SSH': {'cve': 'N/A', 'severity': 'MEDIUM'},
        'DDOS_TCP': {'cve': 'N/A', 'severity': 'MEDIUM'},
    },
    'common': {
        'DOS_HULK': {'cve': 'N/A', 'severity': 'LOW'},
        'DOS_OTHER': {'cve': 'N/A', 'severity': 'LOW'},
        'PORTSCAN': {'cve': 'N/A', 'severity': 'LOW'},
        'DDOS_UDP': {'cve': 'N/A', 'severity': 'LOW'},
        'DDOS_HTTP': {'cve': 'N/A', 'severity': 'LOW'},
        'RECONNAISSANCE': {'cve': 'N/A', 'severity': 'LOW'},
    },
}

# ------------------ Hyperparameters ------------------
HYPERPARAMS = {
    'token_dim': 32,
    'batch_size': 256,
    'epochs': 25,
    'learning_rate': 0.001,
    'test_size': 0.2,
    'val_split': 0.15,
    'target_benign_ratio': 0.40,
    'focal_gamma': 3.0,
}

# ------------------ Output Directories ------------------
OUTPUT_DIR = './outputs'
os.makedirs(OUTPUT_DIR, exist_ok=True)