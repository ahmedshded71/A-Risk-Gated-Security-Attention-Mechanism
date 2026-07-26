#!/bin/bash
set -e

# ==============================================================================
# RGSA-Transformer Entrypoint Script
# ==============================================================================

echo "=========================================================================================="
echo "[LAUNCH] RGSA-Transformer v5.6.2 - Container Starting"
echo "=========================================================================================="

# Display environment info
echo "[INFO] Environment Information:"
echo "  • Python: $(python --version)"
echo "  • TensorFlow: $(python -c 'import tensorflow as tf; print(tf.__version__)')"
echo "  • NumPy: $(python -c 'import numpy as np; print(np.__version__)')"
echo "  • Working Directory: $(pwd)"
echo "  • User: $(whoami)"
echo ""

# Check GPU availability
echo "[GPU] GPU Status:"
python -c "
import tensorflow as tf
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f'  [SUCCESS] Found {len(gpus)} GPU(s):')
    for gpu in gpus:
        print(f'    - {gpu.name}')
    for gpu in gpus:
        try:
            tf.config.experimental.set_memory_growth(gpu, True)
            print(f'  [SUCCESS] Memory growth enabled for {gpu.name}')
        except RuntimeError as e:
            print(f'  [WARNING] {e}')
else:
    print('  [INFO] No GPU detected - running on CPU')
" 2>/dev/null || echo "  [WARNING] GPU check skipped"
echo ""

# Check datasets
echo "[DATA] Dataset Check:"
for dataset in "combine.csv" "merged_dataset.csv" "cic_iot2023.csv"; do
    if [ -f "/app/data/$dataset" ]; then
        size=$(du -h "/app/data/$dataset" | cut -f1)
        echo "  [SUCCESS] $dataset ($size)"
    else
        echo "  [ERROR] $dataset (NOT FOUND)"
    fi
done
echo ""

# Check outputs directory
echo "[OUTPUT] Output Directory:"
if [ -d "/app/outputs" ]; then
    count=$(ls -1 /app/outputs 2>/dev/null | wc -l)
    echo "  [SUCCESS] /app/outputs exists ($count files)"
else
    echo "  [ERROR] /app/outputs not found"
    mkdir -p /app/outputs
fi
echo ""

echo "=========================================================================================="
echo "[RUN] Executing: $@"
echo "=========================================================================================="

# Execute the main command
exec "$@"