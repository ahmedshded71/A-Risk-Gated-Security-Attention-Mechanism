"""Mandatory two-stage pipeline orchestration."""
import gc
import time
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model, callbacks
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             classification_report)

from rgsa.config import HYPERPARAMS, OUTPUT_DIR
from rgsa.data.loader import load_and_preprocess
from rgsa.data.balancing import create_enhanced_balance
from rgsa.models.architecture import build_rgsa_base
from rgsa.models.losses import sparse_focal_loss
from rgsa.training.weights import calculate_hierarchical_weights
from rgsa.evaluation.metrics import (calculate_specificity, calculate_multiclass_specificity,
                                     measure_inference_time, print_inference_metrics)
from rgsa.evaluation.visualization import (plot_confusion_matrix_raw_counts, plot_training_curves,
                                           plot_binary_roc_auc, plot_multiclass_roc_auc)
from rgsa.utils.reporting import save_methodology_report, save_results_csv


def run_mandatory_two_stage_pipeline(dataset_name: str):
    """Execute the full two-stage pipeline for a single dataset."""
    print(f"\n{'='*90}\n▶️  Starting MANDATORY TWO-STAGE pipeline on: {dataset_name}\n{'='*90}")
    try:
        df, feature_cols = load_and_preprocess(dataset_name)
        df_balanced, methodology_doc, security_tiers = create_enhanced_balance(df, dataset_name)

        df_balanced['attack_type'] = df_balanced['attack_type'].str.upper().str.strip()
        df_balanced.loc[df_balanced['attack_type'].isin(['BENIGN', 'BENIGN ', 'NORMAL', '0', '0.0']),
                        'attack_type'] = 'BENIGN'

        le_multiclass = LabelEncoder()
        y_multiclass = le_multiclass.fit_transform(df_balanced['attack_type'])
        class_names = le_multiclass.classes_
        n_classes = len(class_names)
        benign_idx = np.where(class_names == 'BENIGN')[0][0]
        y_binary = (y_multiclass != benign_idx).astype(int)

        print(f"\n✓ Total classes: {n_classes} | Attack classes: {n_classes - 1}")

        X = df_balanced[feature_cols].values
        X_train, X_test, y_train_bin, y_test_bin, y_train_multi, y_test_multi = train_test_split(
            X, y_binary, y_multiclass, test_size=HYPERPARAMS['test_size'],
            random_state=42, stratify=y_binary)

        print(f"\n📊 SAMPLE COUNT BREAKDOWN - {dataset_name}")
        print(f"TOTAL: {len(df_balanced):,} | Train: {len(X_train):,} | Test: {len(X_test):,}")

        X_train = np.nan_to_num(X_train.astype('float32'), nan=0.0, posinf=1e6, neginf=0.0)
        X_test = np.nan_to_num(X_test.astype('float32'), nan=0.0, posinf=1e6, neginf=0.0)
        scaler = MinMaxScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        base_model = build_rgsa_base(X_train_scaled.shape[1])
        print(f"\n✓ Shared base architecture: {base_model.count_params():,} parameters")

        # ===== STAGE 1: BINARY DETECTOR =====
        print(f"\n{'='*90}\nSTAGE 1: BINARY DETECTOR - {dataset_name}\n{'='*90}")
        binary_output = layers.Dense(1, activation='sigmoid', name='binary_output')(base_model.output)
        binary_model = Model(base_model.input, binary_output, name='RGSA_Binary')
        binary_model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=HYPERPARAMS['learning_rate']),
            loss='binary_crossentropy',
            metrics=['accuracy', keras.metrics.Precision(name='precision'),
                     keras.metrics.Recall(name='recall')])

        binary_history = binary_model.fit(
            X_train_scaled, y_train_bin, validation_split=HYPERPARAMS['val_split'],
            batch_size=HYPERPARAMS['batch_size'], epochs=HYPERPARAMS['epochs'],
            callbacks=[
                callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.6, patience=3, min_lr=1e-6, verbose=0),
                callbacks.ModelCheckpoint(f'{OUTPUT_DIR}/best_binary_{dataset_name.replace("-", "_").lower()}.keras',
                                          monitor='val_recall', save_best_only=True, mode='max', verbose=0)
            ], verbose=1)

        binary_train_curve_file = plot_training_curves(binary_history, dataset_name, "Binary_Detector")
        binary_inference_metrics = measure_inference_time(binary_model, X_test_scaled)
        print_inference_metrics(binary_inference_metrics, "Binary_Detector", dataset_name)

        start_pred = time.perf_counter()
        y_pred_bin_proba = binary_model.predict(X_test_scaled, batch_size=512, verbose=0).flatten()
        binary_total_pred_time_sec = time.perf_counter() - start_pred
        y_pred_bin = (y_pred_bin_proba > 0.5).astype(int)

        binary_roc_file, binary_auc = plot_binary_roc_auc(y_test_bin, y_pred_bin_proba, dataset_name)
        binary_cm_file = plot_confusion_matrix_raw_counts(y_test_bin, y_pred_bin, ['BENIGN', 'ATTACK'],
                                                          dataset_name, "Binary_Detector")

        bin_accuracy = accuracy_score(y_test_bin, y_pred_bin)
        bin_precision = precision_score(y_test_bin, y_pred_bin, zero_division=0)
        bin_recall = recall_score(y_test_bin, y_pred_bin, zero_division=0)
        bin_f1 = f1_score(y_test_bin, y_pred_bin, zero_division=0)
        bin_specificity = calculate_specificity(y_test_bin, y_pred_bin)
        bin_fnr = (1 - bin_recall) * 100

        print(f"\n✓✓✓ BINARY DETECTOR PERFORMANCE ✓✓✓")
        print(f"  • Accuracy: {bin_accuracy*100:.2f}% | Precision: {bin_precision*100:.2f}%")
        print(f"  • Recall: {bin_recall*100:.2f}% | Specificity: {bin_specificity*100:.2f}%")
        print(f"  • F1: {bin_f1:.4f} | AUC: {binary_auc:.4f} | FNR: {bin_fnr:.2f}%")

        # ===== STAGE 2: MULTICLASS CLASSIFIER =====
        print(f"\n{'='*90}\nSTAGE 2: MULTICLASS CLASSIFIER - {dataset_name}\n{'='*90}")
        attack_mask_train = y_train_bin == 1
        attack_mask_test = y_test_bin == 1
        X_train_attacks = X_train_scaled[attack_mask_train]
        y_train_attacks = y_train_multi[attack_mask_train]
        X_test_attacks = X_test_scaled[attack_mask_test]
        y_test_attacks = y_test_multi[attack_mask_test]

        attack_classes = [i for i in range(n_classes) if i != benign_idx]
        attack_class_names = [class_names[i] for i in attack_classes]
        n_attack_classes = len(attack_classes)
        remap = {old_idx: new_idx for new_idx, old_idx in enumerate(attack_classes)}
        y_train_attacks_remapped = np.array([remap[y] for y in y_train_attacks if y in remap])
        y_test_attacks_remapped = np.array([remap[y] for y in y_test_attacks if y in remap])

        class_weights_multi = calculate_hierarchical_weights(y_train_attacks_remapped,
                                                             attack_class_names, security_tiers)

        multiclass_output = layers.Dense(n_attack_classes, activation='softmax',
                                         name='multiclass_output')(base_model.output)
        multiclass_model = Model(base_model.input, multiclass_output, name='RGSA_Multiclass')
        multiclass_model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=HYPERPARAMS['learning_rate'], clipnorm=1.0),
            loss=sparse_focal_loss(gamma=HYPERPARAMS['focal_gamma']),
            metrics=['accuracy'])

        multiclass_history = multiclass_model.fit(
            X_train_attacks, y_train_attacks_remapped, validation_split=HYPERPARAMS['val_split'],
            batch_size=HYPERPARAMS['batch_size'], epochs=HYPERPARAMS['epochs'],
            class_weight=class_weights_multi,
            callbacks=[
                callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.6, patience=4, min_lr=1e-6, verbose=0),
                callbacks.ModelCheckpoint(f'{OUTPUT_DIR}/best_multiclass_{dataset_name.replace("-", "_").lower()}.keras',
                                          monitor='val_loss', save_best_only=True, mode='min', verbose=0),
                callbacks.EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True, verbose=0)
            ], verbose=1)

        multi_train_curve_file = plot_training_curves(multiclass_history, dataset_name, "Multiclass_Classifier")
        multi_inference_metrics = measure_inference_time(multiclass_model, X_test_attacks)
        print_inference_metrics(multi_inference_metrics, "Multiclass_Classifier", dataset_name)

        start_pred = time.perf_counter()
        y_pred_multi_proba = multiclass_model.predict(X_test_attacks, batch_size=512, verbose=0)
        multi_total_pred_time_sec = time.perf_counter() - start_pred
        y_pred_multi_remapped = np.argmax(y_pred_multi_proba, axis=1)
        reverse_remap = {v: k for k, v in remap.items()}
        y_pred_multi = np.array([reverse_remap[y] for y in y_pred_multi_remapped])

        multi_roc_file, multi_auc = plot_multiclass_roc_auc(y_test_attacks_remapped, y_pred_multi_proba,
                                                            attack_class_names, dataset_name)
        multi_cm_file = plot_confusion_matrix_raw_counts(y_test_attacks, y_pred_multi,
                                                         attack_class_names, dataset_name, "Multiclass_Classifier")

        multi_accuracy = accuracy_score(y_test_attacks, y_pred_multi)
        multi_macro_f1 = f1_score(y_test_attacks, y_pred_multi, average='macro', zero_division=0)
        multi_weighted_f1 = f1_score(y_test_attacks, y_pred_multi, average='weighted', zero_division=0)
        multi_avg_specificity = np.mean(calculate_multiclass_specificity(y_test_attacks, y_pred_multi, attack_class_names))

        print(f"\n✓✓✓ MULTICLASS CLASSIFIER PERFORMANCE ✓✓✓")
        print(f"  • Accuracy: {multi_accuracy*100:.2f}% | Macro-F1: {multi_macro_f1:.4f}")
        print(f"  • Weighted-F1: {multi_weighted_f1:.4f} | AUC: {multi_auc:.4f}")
        print("\n" + classification_report(y_test_attacks, y_pred_multi,
                                          target_names=attack_class_names, digits=4, zero_division=0))

        # ===== INTEGRATED EVALUATION =====
        print(f"\n{'='*90}\nINTEGRATED EVALUATION - {dataset_name}\n{'='*90}")
        y_pred_final = np.zeros_like(y_test_multi)
        attack_candidates = y_pred_bin_proba > 0.5
        if np.any(attack_candidates):
            X_candidates = X_test_scaled[attack_candidates]
            start_int = time.perf_counter()
            y_pred_candidates_proba = multiclass_model.predict(X_candidates, batch_size=512, verbose=0)
            integrated_avg_time_ms = ((time.perf_counter() - start_int) / len(X_candidates)) * 1000
            y_pred_candidates = np.argmax(y_pred_candidates_proba, axis=1)
            y_pred_final[attack_candidates] = np.array([reverse_remap[y] for y in y_pred_candidates])
        y_pred_final[~attack_candidates] = benign_idx

        final_accuracy = accuracy_score(y_test_multi, y_pred_final)
        final_macro_f1 = f1_score(y_test_multi, y_pred_final, average='macro', zero_division=0)
        final_weighted_f1 = f1_score(y_test_multi, y_pred_final, average='weighted', zero_division=0)

        print(f"\n✓✓✓ INTEGRATED PERFORMANCE ✓✓✓")
        print(f"  • Overall Accuracy: {final_accuracy*100:.2f}% | Macro-F1: {final_macro_f1:.4f}")
        print(f"  • Weighted-F1: {final_weighted_f1:.4f} | Attack Candidates: {np.sum(attack_candidates):,}")

        results = {
            'Dataset': dataset_name, 'Architecture': 'Mandatory_Two_Stage_RGSA_v5.6.2',
            'Total_Classes': n_classes, 'Attack_Classes': n_attack_classes,
            'Total_Samples': len(df_balanced),
            'Train_Samples_Total': len(X_train), 'Test_Samples_Total': len(X_test),
            'Train_Samples_Benign': int(np.sum(y_train_bin == 0)),
            'Train_Samples_Attack': int(np.sum(y_train_bin == 1)),
            'Test_Samples_Benign': int(np.sum(y_test_bin == 0)),
            'Test_Samples_Attack': int(np.sum(y_test_bin == 1)),
            'Train_Samples_Multiclass': len(X_train_attacks),
            'Test_Samples_Multiclass': len(X_test_attacks),
            'Binary_Accuracy': bin_accuracy, 'Binary_Precision': bin_precision,
            'Binary_Recall': bin_recall, 'Binary_Specificity': bin_specificity,
            'Binary_F1': bin_f1, 'Binary_ROC_AUC': binary_auc, 'Binary_FNR': bin_fnr,
            'Binary_Avg_Inference_Time_ms': binary_inference_metrics['avg_time_ms'],
            'Binary_P99_Latency_ms': binary_inference_metrics['p99_ms'],
            'Binary_Throughput_samples_per_sec': binary_inference_metrics['throughput_samples_per_sec'],
            'Multiclass_Accuracy': multi_accuracy,
            'Multiclass_Macro_F1': multi_macro_f1, 'Multiclass_Weighted_F1': multi_weighted_f1,
            'Multiclass_ROC_AUC_Micro': multi_auc,
            'Multiclass_Avg_Inference_Time_ms': multi_inference_metrics['avg_time_ms'],
            'Multiclass_P99_Latency_ms': multi_inference_metrics['p99_ms'],
            'Multiclass_Throughput_samples_per_sec': multi_inference_metrics['throughput_samples_per_sec'],
            'Integrated_Accuracy': final_accuracy, 'Integrated_Macro_F1': final_macro_f1,
            'Integrated_Weighted_F1': final_weighted_f1,
        }

        save_results_csv(results, dataset_name)
        save_methodology_report(dataset_name, results)

        # Cleanup
        del df, df_balanced, X_train, X_test, X_train_scaled, X_test_scaled
        del X_train_attacks, X_test_attacks, multiclass_model, binary_model, base_model, scaler
        gc.collect()
        tf.keras.backend.clear_session()

        return results, True
    except Exception as e:
        print(f"\n❌ Error in {dataset_name}: {str(e)}")
        import traceback; traceback.print_exc()
        return {'Dataset': dataset_name, 'Status': 'Failed', 'Error': str(e)}, False


def run_multi_dataset_pipeline():
    """Execute pipeline across all configured datasets."""
    datasets_to_run = ['CIC-IDS2017', 'CIC-IDS2018', 'CIC-IoT2023']
    all_results = []
    print("\n" + "="*90 + "\n🚀 Starting MANDATORY TWO-STAGE pipeline on 3 datasets\n" + "="*90)

    for ds_name in datasets_to_run:
        try:
            result, success = run_mandatory_two_stage_pipeline(ds_name)
            all_results.append(result)
            if success:
                print(f"\n✓✓✓ Execution on {ds_name} completed successfully ✓✓✓")
        except Exception as e:
            print(f"\n❌ Fatal error processing {ds_name}: {str(e)}")
            all_results.append({'Dataset': ds_name, 'Status': 'Failed', 'Error': str(e)})

    from rgsa.utils.reporting import save_comparison_report
    save_comparison_report(all_results)
    return all_results