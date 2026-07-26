"""Main entry point for RGSA-Transformer v5.6.2."""
import sys
import numpy as np
import tensorflow as tf
from src.rgsa.training.pipeline import run_multi_dataset_pipeline


def main():
    print("="*90)
    print("RGSA-TRANSFORMER v5.6.2 - Risk-Gated Security Attention for IDS")
    print("CIC-IDS2017 → CIC-IDS2018 → CIC-IoT2023")
    print("="*90)

    # Set seeds for reproducibility
    np.random.seed(42)
    tf.random.set_seed(42)

    try:
        results = run_multi_dataset_pipeline()
        print("\n" + "="*90)
        print("INFO: Full execution completed successfully - v5.6.2")
        print("="*90)
        print("\nRun summary:")
        print("   - Mandatory two-stage pipeline")
        print("   - Per-sample inference time metrics (avg, P50, P90, P95, P99)")
        print("   - Throughput measurements (samples/sec)")
        print("   - Complete sample count transparency")
        print("   - Confusion matrices with RAW COUNTS")
        print("="*90)
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback; traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()