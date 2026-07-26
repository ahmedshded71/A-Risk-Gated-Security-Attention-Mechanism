"""Dataset discovery, loading, and preprocessing."""
import os
import glob
import numpy as np
import pandas as pd
from rgsa.config import DATASET_PATHS, DATASET_KEYWORDS, UNIFIED_ATTACK_MAPPING


def find_dataset_path(dataset_name: str) -> str:
    """Locate dataset file using predefined paths or keyword search."""
    search_paths = DATASET_PATHS.get(dataset_name, [])
    for path in search_paths:
        if os.path.exists(path):
            return path

    print(f"  ⚠️  Predefined paths not found. Searching for {dataset_name}...")
    keywords = DATASET_KEYWORDS.get(dataset_name, [dataset_name.lower().replace('-', '')])
    search_roots = ['.', './data', './datasets', './input', '../input']

    for root in search_roots:
        if not os.path.exists(root):
            continue
        for dirpath, _, filenames in os.walk(root, topdown=True):
            for filename in filenames:
                if any(kw in filename.lower() for kw in keywords) and filename.endswith('.csv'):
                    full_path = os.path.join(dirpath, filename)
                    print(f"  ✓ Found dataset at: {full_path}")
                    return full_path

    for pattern in [f"*{keywords[0]}*.csv"]:
        matches = glob.glob(pattern, recursive=True)
        if matches:
            return matches[0]

    raise FileNotFoundError(f"Dataset '{dataset_name}' not found.")


def normalize_attack_label(label: str, dataset_name: str) -> str:
    """Map raw dataset labels to unified attack taxonomy."""
    s = str(label).strip().upper()
    if s in UNIFIED_ATTACK_MAPPING:
        return UNIFIED_ATTACK_MAPPING[s]

    if dataset_name == 'CIC-IDS2017':
        if 'DDOS' in s or 'DOS' in s or 'D0S' in s:
            if 'SLOW' in s: return 'DoS_Slow'
            if 'GOLDEN' in s: return 'DoS_GoldenEye'
            if 'HULK' in s: return 'DoS_Hulk'
            return 'DoS_Other'
        if 'PORTSCAN' in s: return 'PortScan'
        if 'BOT' in s: return 'Botnet'
        if 'HEARTBLEED' in s: return 'Heartbleed'
        if 'INFILTRATION' in s: return 'Infiltration'
    elif dataset_name == 'CIC-IDS2018':
        if 'DDOS' in s or 'DOS' in s:
            if 'HOIC' in s: return 'DDoS_HOIC'
            if 'LOIC' in s and 'HTTP' in s: return 'DDoS_LOIC_HTTP'
            if 'LOIC' in s and 'UDP' in s: return 'DDoS_LOIC_UDP'
            return 'DDoS_Other'
        if 'BRUTE' in s or 'PATATOR' in s:
            if 'FTP' in s: return 'BruteForce_FTP'
            if 'SSH' in s: return 'BruteForce_SSH'
            return 'BruteForce_Other'
        if 'WEB' in s or 'XSS' in s or 'SQL' in s:
            if 'XSS' in s: return 'WebAttack_XSS'
            if 'SQL' in s: return 'WebAttack_SQLi'
            return 'WebAttack_Other'
    elif dataset_name == 'CIC-IoT2023':
        if 'DDOS' in s or 'DOS' in s:
            if 'TCP' in s: return 'DDoS_TCP'
            if 'UDP' in s: return 'DDoS_UDP'
            if 'HTTP' in s: return 'DDoS_HTTP'
            return 'DDoS_Other'
        if 'MIRAI' in s: return 'Mirai'
        if 'RECON' in s: return 'Reconnaissance'
        if 'OS' in s and 'SCAN' in s: return 'OS_Scan'

    return 'Other_Attack' if s != 'BENIGN' else 'BENIGN'


def load_and_preprocess(dataset_name: str):
    """Load CSV, clean features, and normalize labels."""
    path = find_dataset_path(dataset_name)
    print(f"\n{'='*90}\n▶️  Loading {dataset_name} from: {path}\n{'='*90}")

    df = pd.read_csv(path, low_memory=False)
    df.columns = df.columns.str.strip()

    label_col = next((col for col in df.columns
                      if 'label' in col.lower() or 'attack' in col.lower() or 'class' in col.lower()), None)
    if label_col is None:
        raise ValueError(f"Label column not found in {dataset_name}")

    df['attack_type'] = df[label_col].apply(lambda x: normalize_attack_label(x, dataset_name))

    identity_keywords = ['flow id', 'source ip', 'destination ip', 'source port',
                         'destination port', 'timestamp', 'time', 'date', 'index', 'id',
                         'flowid', 'flow_id', 'protocol']
    cols_to_drop = [col for col in df.columns
                    if any(kw in col.lower() for kw in identity_keywords) or col == label_col]
    df = df.drop(cols_to_drop, axis=1, errors='ignore')

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if 'attack_type' in numeric_cols:
        numeric_cols.remove('attack_type')
    df = df[numeric_cols + ['attack_type']].replace([np.inf, -np.inf], np.nan).dropna()

    attack_dist = df['attack_type'].value_counts()
    total = len(df)
    benign_count = attack_dist.get('BENIGN', 0)
    print(f"\n✓ {dataset_name} - Original Distribution:")
    print(f"  - Total samples: {total:,}")
    print(f"  - BENIGN: {benign_count:,} ({benign_count/total*100:.2f}%)")
    print(f"  - Attacks: {total - benign_count:,} ({(total-benign_count)/total*100:.2f}%)")
    print(f"  - Attack types: {len(attack_dist) - 1}")

    return df, numeric_cols