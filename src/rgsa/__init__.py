"""
RGSA-Transformer v5.6.2
Risk-Gated Security Attention Mechanism for Real-Time IDS
"""

__version__ = "5.6.2"
__author__ = "Eslam Fouda, Ahmed Saad, Dr shimaa"

# Import main components for easy access
from rgsa.models.architecture import (
    SecurityTokenizer,
    RiskGatedSecurityAttention,
    build_rgsa_base,
)
from rgsa.models.losses import sparse_focal_loss
from rgsa.data.loader import load_and_preprocess, find_dataset_path
from rgsa.data.balancing import create_enhanced_balance
from rgsa.training.pipeline import (
    run_mandatory_two_stage_pipeline,
    run_multi_dataset_pipeline,
)
from rgsa.config import (
    DATASET_PATHS,
    UNIFIED_ATTACK_MAPPING,
    SECURITY_TIERS,
    HYPERPARAMS,
    OUTPUT_DIR,
)

__all__ = [
    "__version__",
    "SecurityTokenizer",
    "RiskGatedSecurityAttention",
    "build_rgsa_base",
    "sparse_focal_loss",
    "load_and_preprocess",
    "find_dataset_path",
    "create_enhanced_balance",
    "run_mandatory_two_stage_pipeline",
    "run_multi_dataset_pipeline",
    "DATASET_PATHS",
    "UNIFIED_ATTACK_MAPPING",
    "SECURITY_TIERS",
    "HYPERPARAMS",
    "OUTPUT_DIR",
]