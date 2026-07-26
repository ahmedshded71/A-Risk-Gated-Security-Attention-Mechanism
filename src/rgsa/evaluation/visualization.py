"""Publication-ready visualization functions."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.preprocessing import label_binarize
from rgsa.config import OUTPUT_DIR


def plot_confusion_matrix_raw_counts(y_true, y_pred, class_names, dataset_name, stage_name):
    """Confusion matrix with RAW COUNTS + percentages (300 DPI)."""
    cm_raw = confusion_matrix(y_true, y_pred)
    cm_norm = cm_raw.astype('float') / cm_raw.sum(axis=1)[:, np.newaxis]
    plt.figure(figsize=(16, 14))
    annotations = np.empty_like(cm_raw, dtype=object)
    for i in range(cm_raw.shape[0]):
        for j in range(cm_raw.shape[1]):
            annotations[i, j] = f'{cm_raw[i, j]:,}\n({cm_norm[i, j]*100:.1f}%)'

    sns.heatmap(cm_raw, annot=annotations, fmt='', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names,
                cbar_kws={'label': 'Sample Count'},
                annot_kws={"size": 11, "weight": "bold"},
                linewidths=0.5, linecolor='gray')
    plt.title(f'Confusion Matrix - {stage_name} ({dataset_name})\n[Raw Counts + Percentages]',
              fontsize=18, fontweight='bold', pad=25)
    plt.xlabel('Predicted Label', fontsize=15, fontweight='bold', labelpad=15)
    plt.ylabel('True Label', fontsize=15, fontweight='bold', labelpad=15)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.yticks(rotation=0, fontsize=12)
    plt.text(0.98, 0.02, f'Total Samples: {np.sum(cm_raw):,}',
             transform=plt.gca().transAxes, fontsize=12,
             verticalalignment='bottom', horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    plt.tight_layout()
    filename = f'{OUTPUT_DIR}/confusion_matrix_raw_{stage_name.lower().replace(" ", "_")}_{dataset_name.replace("-", "_").lower()}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"{stage_name} confusion matrix saved: {filename}")
    return filename


def plot_training_curves(history, dataset_name, stage_name):
    """Accuracy and loss training curves."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    ax1.plot(history.history['accuracy'], label='Train Accuracy', marker='o', linewidth=2)
    ax1.plot(history.history['val_accuracy'], label='Val Accuracy', marker='s', linewidth=2)
    ax1.set_title(f'{stage_name} - Accuracy ({dataset_name})', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Epoch'); ax1.set_ylabel('Accuracy')
    ax1.legend(); ax1.grid(True, alpha=0.3); ax1.set_ylim([0, 1])

    ax2.plot(history.history['loss'], label='Train Loss', marker='o', color='red', linewidth=2)
    ax2.plot(history.history['val_loss'], label='Val Loss', marker='s', color='orange', linewidth=2)
    ax2.set_title(f'{stage_name} - Loss ({dataset_name})', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Epoch'); ax2.set_ylabel('Loss')
    ax2.legend(); ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    filename = f'{OUTPUT_DIR}/training_curves_{stage_name.lower().replace(" ", "_")}_{dataset_name.replace("-", "_").lower()}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Training curves saved: {filename}")
    return filename


def plot_binary_roc_auc(y_true, y_pred_proba, dataset_name):
    """Binary ROC/AUC curve."""
    fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
    roc_auc_val = auc(fpr, tpr)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc_val:.4f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Chance')
    plt.xlim([0.0, 1.0]); plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title(f'ROC Curve - Binary Detector ({dataset_name})\nAUC: {roc_auc_val:.4f}',
              fontsize=14, fontweight='bold')
    plt.legend(loc="lower right"); plt.grid(True, alpha=0.3); plt.tight_layout()
    filename = f'{OUTPUT_DIR}/roc_auc_binary_{dataset_name.replace("-", "_").lower()}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Binary ROC/AUC saved: {filename}")
    return filename, roc_auc_val


def plot_multiclass_roc_auc(y_true, y_pred_proba, class_names, dataset_name):
    """Multiclass One-vs-Rest ROC/AUC curves."""
    n_classes = len(class_names)
    y_true_bin = label_binarize(y_true, classes=range(n_classes))
    fpr, tpr, roc_auc = dict(), dict(), dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], y_pred_proba[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    fpr["micro"], tpr["micro"], _ = roc_curve(y_true_bin.ravel(), y_pred_proba.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

    plt.figure(figsize=(12, 9))
    colors = plt.cm.tab20(np.linspace(0, 1, n_classes))
    plt.plot(fpr["micro"], tpr["micro"],
             label=f'Micro-average ROC (AUC = {roc_auc["micro"]:.4f})',
             color='deeppink', linestyle=':', linewidth=4)
    for i, color in zip(range(n_classes), colors):
        plt.plot(fpr[i], tpr[i], color=color, lw=2,
                 label=f'{class_names[i]} (AUC = {roc_auc[i]:.4f})')
    plt.plot([0, 1], [0, 1], 'k--', lw=2, label='Random Chance')
    plt.xlim([0.0, 1.0]); plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=13)
    plt.ylabel('True Positive Rate', fontsize=13)
    plt.title(f'ROC Curves - Multiclass ({dataset_name})\nMicro-AUC: {roc_auc["micro"]:.4f}',
              fontsize=15, fontweight='bold')
    plt.legend(loc="lower right", fontsize=9, ncol=2); plt.grid(True, alpha=0.3); plt.tight_layout()
    filename = f'{OUTPUT_DIR}/roc_auc_multiclass_{dataset_name.replace("-", "_").lower()}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Multiclass ROC/AUC saved: {filename}")
    return filename, roc_auc["micro"]