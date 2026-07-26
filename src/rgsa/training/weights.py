"""Hierarchical class weight calculation based on security tiers."""
import numpy as np
from rgsa.config import SECURITY_TIERS


def calculate_hierarchical_weights(y_train: np.ndarray, class_names: list, security_tiers: dict) -> dict:
    """Assign loss weights based on NIST-aligned security tiers."""
    class_to_tier = {}
    for tier_name, attacks in security_tiers.items():
        for attack_type in attacks.keys():
            for class_name in class_names:
                if attack_type.upper() in class_name.upper():
                    class_to_tier[class_name] = tier_name

    class_weights = {}
    total = len(y_train)
    n_classes = len(np.unique(y_train))

    print("\nHierarchical class weights calculated by security tier:")
    print(f"{'Class':<25} {'Tier':<12} {'Count':>8} {'Weight':>8}")
    print("-" * 55)

    for class_idx, class_name in enumerate(class_names):
        count = np.sum(y_train == class_idx)
        base_weight = total / (n_classes * count) if count > 0 else 1.0
        tier = class_to_tier.get(class_name, 'common')

        if tier == 'critical':
            max_weight, tier_label = 50.0, "Critical"
        elif tier == 'moderate':
            max_weight, tier_label = 15.0, "Moderate"
        elif 'BENIGN' in class_name.upper():
            max_weight, tier_label = 0.7, "Benign"
        else:
            max_weight, tier_label = 1.0, "Common"

        weight = max(min(base_weight * max_weight, max_weight), 0.5)
        class_weights[class_idx] = weight
        print(f"{class_name:<25} {tier_label:<12} {count:>8} {weight:>8.2f}")

    return class_weights