"""Hierarchical security-based class balancing with BENIGN injection."""
import json
import numpy as np
import pandas as pd
from rgsa.config import SECURITY_TIERS, HYPERPARAMS, OUTPUT_DIR


def create_enhanced_balance(df: pd.DataFrame, dataset_name: str = ""):
    """Apply security-tier-aware balancing; inject synthetic BENIGN if missing."""
    target_benign_ratio = HYPERPARAMS['target_benign_ratio']

    benign_mask = df['attack_type'].str.upper().isin(['BENIGN', 'BENIGN ', 'NORMAL'])
    df_benign = df[benign_mask].copy()
    df_attacks = df[~benign_mask].copy()

    if len(df_attacks) == 0:
        raise ValueError("No attacks found in dataset")

    attack_counts = df['attack_type'].value_counts()
    max_attack_count = attack_counts[~attack_counts.index.isin(['BENIGN', 'BENIGN ', 'NORMAL'])].max()

    print(f"\n{'='*90}\nEnhanced Hierarchical Balancing - {dataset_name}\n{'='*90}")
    print(f"Original BENIGN count: {len(df_benign):,} samples")

    # Inject synthetic BENIGN if missing
    benign_injected = False
    if len(df_benign) == 0:
        print("\n⚠️  WARNING: No BENIGN samples found. Injecting synthetic BENIGN...")
        smallest_attack = attack_counts[~attack_counts.index.isin(['BENIGN', 'BENIGN ', 'NORMAL'])].idxmin()
        df_smallest = df_attacks[df_attacks['attack_type'] == smallest_attack].copy()
        benign_samples_needed = max(5000, int(len(df_attacks) * 0.1))
        df_benign = df_smallest.sample(n=min(len(df_smallest), benign_samples_needed),
                                       replace=True, random_state=42).copy()
        numeric_cols = [col for col in df_benign.columns if col != 'attack_type']
        for col in numeric_cols:
            if df_benign[col].dtype in [np.float32, np.float64, np.int32, np.int64]:
                reduction_factor = np.random.uniform(0.1, 0.3, size=len(df_benign))
                df_benign[col] = df_benign[col] * reduction_factor
        df_benign['attack_type'] = 'BENIGN'
        benign_injected = True
        print(f"✓ Injected {len(df_benign):,} synthetic BENIGN samples")
    else:
        print("✓ BENIGN samples exist - no injection needed")

    # Balance attack classes by security tier
    df_augmented_parts = []
    tier_stats = {'critical': [], 'moderate': [], 'common': []}

    for tier_name, attacks in SECURITY_TIERS.items():
        print(f"\nSecurity Tier: {tier_name.upper()}")
        print("-" * 70)
        for attack_type, spec in attacks.items():
            found_type = next((ct for ct in attack_counts.index if attack_type.upper() in ct.upper()), None)
            if not found_type or found_type not in df_attacks['attack_type'].values:
                continue

            df_type = df_attacks[df_attacks['attack_type'] == found_type]
            orig_count = len(df_type)
            if orig_count == 0:
                continue

            if tier_name == 'critical':
                target_samples = max(10000, max_attack_count / 30, orig_count * 2)
            elif tier_name == 'moderate':
                target_samples = max(20000, max_attack_count / 15, orig_count * 2)
            else:
                target_samples = orig_count

            factor = min(50, max(1, int(target_samples / max(orig_count, 1))))
            df_aug = pd.concat([df_type] * factor, ignore_index=True) if factor > 1 else df_type.copy()
            final_count = len(df_aug)

            tier_stats[tier_name].append({
                'attack': found_type, 'original': orig_count,
                'factor': factor, 'final': final_count,
                'cve': spec.get('cve', 'N/A'), 'severity': spec['severity']
            })
            df_augmented_parts.append(df_aug)

            marker = "🔴" if tier_name == 'critical' else ("🟡" if tier_name == 'moderate' else "🟢")
            print(f"  {marker} {found_type:<25} {orig_count:>6,} × {factor:<2} = {final_count:>7,} "
                  f"[CVE: {spec.get('cve', 'N/A')}, Severity: {spec['severity']}]")

    df_attacks_balanced = pd.concat(df_augmented_parts, ignore_index=True)
    attacks_total = len(df_attacks_balanced)
    benign_target = min(int(attacks_total * (target_benign_ratio / (1 - target_benign_ratio))), len(df_benign))
    actual_ratio = benign_target / (benign_target + attacks_total)
    df_benign_sampled = df_benign.sample(n=benign_target, random_state=42)

    print(f"\n✓ Final BENIGN sampling: {benign_target:,} samples ({actual_ratio*100:.1f}%)")
    df_balanced = pd.concat([df_benign_sampled, df_attacks_balanced], ignore_index=True)
    df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

    methodology = {
        'dataset': dataset_name, 'balancing_strategy': 'enhanced_hierarchical_with_benign_injection',
        'security_tiers': SECURITY_TIERS, 'tier_stats': tier_stats,
        'target_benign_ratio': target_benign_ratio, 'actual_benign_ratio': actual_ratio,
        'total_samples': len(df_balanced), 'benign_injected': benign_injected,
    }
    filename = f'{OUTPUT_DIR}/methodology_{dataset_name.replace("-", "_").lower()}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(methodology, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Methodology saved: {filename}")

    return df_balanced, methodology, SECURITY_TIERS