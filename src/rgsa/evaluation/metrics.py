"""Evaluation metrics and inference time profiling."""
import time
import numpy as np
from sklearn.metrics import confusion_matrix


def calculate_specificity(y_true, y_pred) -> float:
    """Binary specificity (True Negative Rate)."""
    tn, fp, _, _ = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return tn / (tn + fp) if (tn + fp) > 0 else 0.0


def calculate_multiclass_specificity(y_true, y_pred, class_names: list) -> list:
    """Per-class specificity for multiclass setting."""
    cm = confusion_matrix(y_true, y_pred)
    specificity_scores = []
    for i in range(len(class_names)):
        tn = np.sum(np.delete(np.delete(cm, i, axis=0), i, axis=1))
        fp = np.sum(cm[:, i]) - cm[i, i]
        specificity_scores.append(tn / (tn + fp) if (tn + fp) > 0 else 0.0)
    return specificity_scores


def measure_inference_time(model, X_samples, batch_size: int = 512,
                           warmup_runs: int = 10, measurement_runs: int = 1000) -> dict:
    """Measure per-sample inference latency with warmup."""
    for _ in range(warmup_runs):
        _ = model.predict(X_samples[:min(len(X_samples), batch_size)],
                          batch_size=batch_size, verbose=0)

    latencies_ms = []
    num_batches = max(1, measurement_runs // batch_size)
    for _ in range(num_batches):
        batch_indices = np.random.randint(0, len(X_samples), size=min(batch_size, len(X_samples)))
        batch = X_samples[batch_indices]
        start = time.perf_counter()
        _ = model.predict(batch, batch_size=batch_size, verbose=0)
        latency_ms = (time.perf_counter() - start) * 1000 / len(batch)
        latencies_ms.append(latency_ms)

    latencies_ms = np.array(latencies_ms)
    return {
        'avg_time_ms': np.mean(latencies_ms),
        'std_time_ms': np.std(latencies_ms),
        'p50_ms': np.percentile(latencies_ms, 50),
        'p90_ms': np.percentile(latencies_ms, 90),
        'p95_ms': np.percentile(latencies_ms, 95),
        'p99_ms': np.percentile(latencies_ms, 99),
        'throughput_samples_per_sec': 1000 / np.mean(latencies_ms) if np.mean(latencies_ms) > 0 else 0,
        'num_samples_measured': len(latencies_ms) * batch_size,
    }


def print_inference_metrics(metrics: dict, stage_name: str, dataset_name: str):
    """Print inference metrics in a readable format."""
    print(f"\n{'='*90}\nINFERENCE TIME METRICS - {stage_name} ({dataset_name})\n{'='*90}")
    print(f"  • Average Latency:      {metrics['avg_time_ms']:.4f} ms/sample")
    print(f"  • Median (P50):         {metrics['p50_ms']:.4f} ms/sample")
    print(f"  • P90 Latency:          {metrics['p90_ms']:.4f} ms/sample")
    print(f"  • P95 Latency:          {metrics['p95_ms']:.4f} ms/sample")
    print(f"  • P99 Latency:          {metrics['p99_ms']:.4f} ms/sample")
    print(f"  • Throughput:           {metrics['throughput_samples_per_sec']:,.0f} samples/sec")
    print(f"{'='*90}")