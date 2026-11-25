"""Pelatihan model prediksi depresi, evaluasi komparatif 3 algoritma, dan ekspor artefak."""
import hashlib
import importlib.metadata
import json
import platform
from datetime import datetime, timezone
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, classification_report, confusion_matrix,
    ConfusionMatrixDisplay, f1_score, precision_score, recall_score
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

from depresi_project import (
    ROOT, TARGET, LABELS, FEATURES, NUMERIC, CATEGORICAL,
    prepare_features, make_preprocessor
)

SEED = 42
REPORTS = ROOT / "Source_Code/reports"
EDA = REPORTS / "eda"
MODELING = REPORTS / "modeling"
ANALYSIS = REPORTS / "analysis"
PROCESSED = ROOT / "Dataset/Data_Olahan"
MODELS = ROOT / "Model"


def save_json(path, value):
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False,
                   default=lambda x: x.item() if isinstance(x, np.generic) else str(x)),
        encoding="utf-8"
    )


def save_figure(path):
    plt.tight_layout()
    plt.savefig(path, dpi=160, bbox_inches="tight")
    plt.close()


def metrics(y, prediction):
    return {
        "accuracy": accuracy_score(y, prediction),
        "precision_macro": precision_score(y, prediction, labels=LABELS, average="macro", zero_division=0),
        "recall_macro": recall_score(y, prediction, labels=LABELS, average="macro", zero_division=0),
        "f1_macro": f1_score(y, prediction, labels=LABELS, average="macro", zero_division=0)
    }


def main():
    for folder in [EDA, MODELING, ANALYSIS, PROCESSED, MODELS]:
        folder.mkdir(parents=True, exist_ok=True)

    source = ROOT / "Dataset/Data_Asli/nhanes_depression_raw.csv"
    raw = pd.read_csv(source, low_memory=False)

    if set(raw[TARGET].unique()) != set(LABELS):
        raise ValueError("Label dataset tidak sesuai dengan kontrak kelas target.")

    features_all = prepare_features(raw)
    canonical = features_all.assign(**{TARGET: raw[TARGET]})
    duplicate_mask = canonical.duplicated(keep="first")
    raw.loc[duplicate_mask].to_csv(EDA / "duplicate_records.csv", index=False)

    clean = canonical.loc[~duplicate_mask].copy().reset_index(drop=True)
    ids = raw.loc[~duplicate_mask, "SEQN"].reset_index(drop=True)

    # Deteksi profil identik dengan label bertentangan jika ada
    profile_hashes = pd.util.hash_pandas_object(clean[FEATURES], index=False).astype(str)
    conflict_counts = clean.assign(profile_hash=profile_hashes).groupby("profile_hash")[TARGET].nunique()
    conflict_hashes = set(conflict_counts[conflict_counts > 1].index)
    clean.assign(profile_hash=profile_hashes).loc[profile_hashes.isin(conflict_hashes)].to_csv(
        EDA / "conflicting_profiles.csv", index=False
    )

    clean.assign(source_seqn=ids, profile_hash=profile_hashes).to_csv(
        PROCESSED / "cleaned.csv", index=False
    )

    X = clean[FEATURES]
    y = clean[TARGET]

    # Split train-test 80:20 berstrata
    X_train, X_test, y_train, y_test, train_idx, test_idx = train_test_split(
        X, y, clean.index, test_size=0.20, stratify=y, random_state=SEED
    )

    # K-Fold Cross Validation berstrata 5 fold pada data latih
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED + 1)
    fold_records = []
    for fold, (fit_idx, val_idx) in enumerate(cv.split(X_train, y_train), 1):
        for role, indexes in [("fit", fit_idx), ("validation", val_idx)]:
            for pos in indexes:
                fold_records.append({
                    "fold": fold, "role": role,
                    "clean_index": int(X_train.index[pos]),
                    "label": y_train.iloc[pos]
                })
    pd.DataFrame(fold_records).to_csv(MODELING / "cv_folds.csv", index=False)

    for name, indices in [("train", train_idx), ("test", test_idx)]:
        clean.loc[indices].assign(source_seqn=ids.loc[indices]).to_csv(
            PROCESSED / f"{name}.csv", index=False
        )

    # Laporan EDA dan Kualitas Data
    raw.describe(include="all").to_csv(EDA / "descriptive_raw.csv")
    clean.describe(include="all").to_csv(EDA / "descriptive_cleaned.csv")

    quality = []
    for col in raw.columns:
        quality.append({
            "feature": col,
            "dtype": str(raw[col].dtype),
            "missing_count": int(raw[col].isna().sum()),
            "unique_count": int(raw[col].nunique())
        })
    pd.DataFrame(quality).to_csv(EDA / "data_quality.csv", index=False)

    outliers = []
    for col in NUMERIC:
        q1, q3 = X_train[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        outliers.append({
            "feature": col, "lower_iqr": low, "upper_iqr": high,
            "outlier_count_train": int(((X_train[col] < low) | (X_train[col] > high)).sum())
        })
    pd.DataFrame(outliers).to_csv(EDA / "outliers_train.csv", index=False)

    pd.DataFrame({
        "raw": raw[TARGET].value_counts(),
        "cleaned": y.value_counts(),
        "train": y_train.value_counts(),
        "test": y_test.value_counts()
    }).reindex(LABELS).to_csv(EDA / "class_distribution.csv")

    summary = {
        "raw_rows": len(raw),
        "raw_columns": len(raw.columns),
        "model_features": len(FEATURES),
        "duplicates_removed": int(duplicate_mask.sum()),
        "clean_rows": len(clean),
        "unique_profiles": int(profile_hashes.nunique()),
        "conflicting_profiles": len(conflict_hashes),
        "train_rows": len(train_idx),
        "test_rows": len(test_idx),
        "seed": SEED,
        "selection_metric": "Stratified 5-Fold Training CV Macro-F1",
        "split_ratio": "80% Train : 20% Test Stratified",
        "class_counts_raw": raw[TARGET].value_counts().to_dict(),
        "class_counts_train": y_train.value_counts().to_dict(),
        "class_counts_test": y_test.value_counts().to_dict(),
    }
    save_json(EDA / "summary.json", summary)

    # 1. Distribusi Kelas
    plt.figure(figsize=(7, 4.5))
    pd.DataFrame({"Data Latih": y_train.value_counts(), "Data Uji": y_test.value_counts()}).reindex(LABELS).plot.bar(ax=plt.gca(), rot=0)
    plt.ylabel("Jumlah Responden")
    plt.title("Distribusi Label Depresi pada Data Latih dan Uji")
    save_figure(EDA / "01_distribusi_kelas.png")

    # 2. Histogram Numerik
    X_train[NUMERIC].hist(figsize=(12, 8), bins=15, color="#1e5f74", edgecolor="#112d4e")
    plt.suptitle("Distribusi Fitur Numerik Data Latih")
    save_figure(EDA / "02_histogram_train.png")

    # 3. Boxplot Outlier
    fig, axes = plt.subplots(2, 4, figsize=(14, 7))
    for ax, col in zip(axes.flat, NUMERIC):
        ax.boxplot(X_train[col].dropna())
        ax.set_title(col)
        ax.set_xticks([])
    if len(NUMERIC) < len(axes.flat):
        for ax in axes.flat[len(NUMERIC):]:
            ax.axis("off")
    save_figure(EDA / "03_boxplot_train.png")

    # 4. Korelasi Matriks
    correlation = X_train[NUMERIC].corr()
    correlation.to_csv(EDA / "correlation_train.csv")
    plt.figure(figsize=(8, 7))
    plt.imshow(correlation, vmin=-1, vmax=1, cmap="coolwarm")
    plt.xticks(range(len(NUMERIC)), NUMERIC, rotation=45, ha="right")
    plt.yticks(range(len(NUMERIC)), NUMERIC)
    plt.colorbar(label="Korelasi Pearson")
    plt.title("Matriks Korelasi Antarfitur Numerik")
    save_figure(EDA / "04_korelasi_train.png")

    # 5. Visualisasi Fitur Kategorikal Kunci
    fig, axes = plt.subplots(2, 2, figsize=(13, 8))
    key_cats = ["Trouble Sleeping History", "Memory Problems", "Cant Work", "Gender"]
    for ax, col in zip(axes.flat, key_cats):
        counts = pd.crosstab(X_train[col], y_train, normalize="index") * 100
        counts.reindex(columns=LABELS).plot.bar(stacked=True, ax=ax, rot=0, color=["#4f8a8b", "#ea5455"])
        ax.set_title(f"Proporsi Depresi Berdasarkan {col}")
        ax.set_ylabel("Persentase (%)")
    save_figure(EDA / "05_kategorikal_train.png")

    # 6. Scatter Plot Hubungan Usia vs Durasi Tidur
    plt.figure(figsize=(8, 5))
    for label, color in [("Not Depressed", "#3f72af"), ("Depressed", "#e84545")]:
        sub = X_train.loc[y_train == label]
        plt.scatter(sub["Age"], sub["Sleep Hours"], label=label, alpha=0.35, s=20, c=color)
    plt.xlabel("Usia (Tahun)")
    plt.ylabel("Durasi Tidur (Jam/Hari)")
    plt.title("Pola Usia vs Durasi Tidur terhadap Status Depresi")
    plt.legend()
    save_figure(EDA / "06_scatter_train.png")

    # Model & Hyperparameter Tuning
    definitions = {
        "logistic_regression": (
            LogisticRegression(max_iter=500, random_state=SEED),
            {"model__C": [0.1, 1.0, 10.0], "model__class_weight": ["balanced", None]}
        ),
        "decision_tree": (
            DecisionTreeClassifier(random_state=SEED),
            {"model__max_depth": [4, 6, 8], "model__class_weight": ["balanced", None]}
        ),
        "random_forest": (
            RandomForestClassifier(random_state=SEED, n_jobs=-1),
            {"model__n_estimators": [100], "model__max_depth": [6, 10], "model__class_weight": ["balanced"]}
        )
    }

    fitted, rows = {}, []
    for name, (model, params) in definitions.items():
        pipeline = Pipeline([("preprocess", make_preprocessor()), ("model", model)])
        baseline = cross_validate(pipeline, X_train, y_train, cv=cv, scoring="f1_macro", n_jobs=-1)
        search = GridSearchCV(
            pipeline, params, cv=cv, scoring="f1_macro", n_jobs=-1,
            return_train_score=True, error_score="raise"
        )
        search.fit(X_train, y_train)
        fitted[name] = search.best_estimator_
        table = pd.DataFrame(search.cv_results_)
        table.to_csv(MODELING / f"cv_results_{name}.csv", index=False)
        best_idx = search.best_index_
        rows.append({
            "model": name,
            "baseline_cv_f1": float(np.mean(baseline["test_score"])),
            "cv_f1_mean": float(search.best_score_),
            "cv_f1_std": float(table.loc[best_idx, "std_test_score"]),
            "cv_train_f1": float(table.loc[best_idx, "mean_train_score"]),
            "best_params": json.dumps(search.best_params_)
        })
        joblib.dump(search.best_estimator_, MODELS / f"{name}_pipeline.joblib")
        print(f"{name} -> CV Macro-F1: {search.best_score_:.4f}")

    # Kunci pilihan model HANYA berdasarkan CV Data Latih
    selection = max(rows, key=lambda r: r["cv_f1_mean"])["model"]
    print("Model Terpilih Berdasarkan CV Latih:", selection)

    # Baseline Dummy (Mayoritas)
    dummy = Pipeline([("preprocess", make_preprocessor()), ("model", DummyClassifier(strategy="most_frequent"))])
    dummy.fit(X_train, y_train)
    save_json(MODELING / "dummy_baseline.json", metrics(y_test, dummy.predict(X_test)))

    # Evaluasi Holdout Test Set
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    for ax, row in zip(axes, rows):
        name = row["model"]
        estimator = fitted[name]
        pred_test = estimator.predict(X_test)
        pred_train = estimator.predict(X_train)

        row.update({"train_" + k: v for k, v in metrics(y_train, pred_train).items()})
        row.update({"test_" + k: v for k, v in metrics(y_test, pred_test).items()})
        row["selected_by_cv"] = (name == selection)
        row["train_cv_gap"] = float(row["cv_train_f1"] - row["cv_f1_mean"])

        save_json(
            MODELING / f"classification_report_{name}.json",
            classification_report(y_test, pred_test, labels=LABELS, output_dict=True, zero_division=0)
        )

        ConfusionMatrixDisplay(
            confusion_matrix(y_test, pred_test, labels=LABELS), display_labels=LABELS
        ).plot(ax=ax, colorbar=False, cmap="Blues")
        ax.set_title(f"{name}\n(F1: {row['test_f1_macro']:.3f})")

        probs = estimator.predict_proba(X_test)
        records = X_test.copy().assign(
            clean_index=X_test.index,
            actual=y_test,
            predicted=pred_test,
            correct=(y_test.to_numpy() == pred_test)
        )
        for j, label in enumerate(estimator.classes_):
            records[f"probability_{label}"] = probs[:, j]
        records.to_csv(MODELING / f"predictions_{name}.csv", index=False)
        records.loc[~records.correct].to_csv(MODELING / f"errors_{name}.csv", index=False)

    save_figure(MODELING / "01_confusion_matrices.png")

    results = pd.DataFrame(rows)
    results.to_csv(MODELING / "model_comparison.csv", index=False)

    # Visualisasi Perbandingan Model
    results.set_index("model")[["cv_f1_mean", "test_f1_macro", "test_accuracy"]].plot.bar(
        figsize=(8, 4.5), ylim=(0, 1), rot=15
    )
    plt.ylabel("Skor Metrik")
    plt.title("Perbandingan Kinerja 3 Algoritma (Pemilihan dari CV Data Latih)")
    save_figure(MODELING / "02_model_comparison.png")

    results.set_index("model")[["cv_train_f1", "cv_f1_mean", "test_f1_macro"]].plot.bar(
        figsize=(8, 4.5), ylim=(0, 1), rot=15
    )
    plt.ylabel("Macro-F1")
    plt.title("Diagnostik Generalisasi (Train vs CV vs Test)")
    save_figure(ANALYSIS / "01_generalization.png")

    # Interpretasi Fitur (pada data latih saja)
    perm = permutation_importance(fitted[selection], X_train, y_train, scoring="f1_macro", n_repeats=5, random_state=SEED, n_jobs=-1)
    importance = pd.DataFrame({
        "feature": FEATURES,
        "importance_mean": perm.importances_mean,
        "importance_std": perm.importances_std
    }).sort_values("importance_mean", ascending=False)
    importance.to_csv(ANALYSIS / "permutation_importance_train.csv", index=False)

    importance.head(10).sort_values("importance_mean").plot.barh(
        x="feature", y="importance_mean", xerr="importance_std", figsize=(9, 5), legend=False, color="#16817a"
    )
    plt.xlabel("Penurunan Macro-F1 setelah Permutasi Fitur")
    plt.title(f"10 Fitur Paling Berpengaruh pada Model Terpilih ({selection})")
    save_figure(ANALYSIS / "02_permutation_importance.png")

    # Koefisien Regresi Logistik
    logistic = fitted["logistic_regression"]
    feature_names = logistic["preprocess"].get_feature_names_out()
    coef = logistic["model"].coef_[0]
    coefficients = pd.DataFrame({"feature": feature_names, "coefficient": coef}).sort_values("coefficient")
    coefficients.to_csv(ANALYSIS / "logistic_coefficients.csv", index=False)

    top_coef = pd.concat([coefficients.head(7), coefficients.tail(7)])
    top_coef.plot.barh(x="feature", y="coefficient", figsize=(10, 6), legend=False, color="#e27802")
    plt.xlabel("Nilai Koefisien Logit (Numerik Terstandardisasi)")
    plt.title("Koefisien Fitur Terbesar pada Regresi Logistik")
    save_figure(ANALYSIS / "03_logistic_coefficients.png")

    # Simpan pipeline terpilih tanpa refit
    joblib.dump(fitted[selection], MODELS / "selected_pipeline.joblib")

    schema = {
        "features": FEATURES,
        "categories": {col: sorted(X_train[col].dropna().unique().tolist()) for col in CATEGORICAL},
        "training_ranges": {
            col: {
                "min": float(X_train[col].min()),
                "max": float(X_train[col].max()),
                "median": float(X_train[col].median())
            } for col in NUMERIC
        }
    }
    save_json(MODELS / "input_schema.json", schema)

    metadata = {
        "title": "Klasifikasi Risiko Gangguan Depresi Menggunakan Algoritma Machine Learning",
        "selected_model": selection,
        "selection_rule": "Rata-rata Macro-F1 tertinggi pada 5-Fold Stratified Cross-Validation Data Latih.",
        "primary_method": "random_forest",
        "labels": LABELS,
        "summary": summary,
        "results": rows,
        "dataset_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "trained_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "packages": {p: importlib.metadata.version(p) for p in ["scikit-learn", "pandas", "numpy", "matplotlib", "joblib"]},
        "refit_on_test": False,
        "clinical_use": False
    }
    save_json(MODELS / "model_metadata.json", metadata)

    # Template dan sampel input
    X_test.head(5).to_csv(ROOT / "Dataset/template_input.csv", index=False)
    X_test.head(10).copy().assign(actual=y_test.head(10)).to_csv(ROOT / "Dataset/contoh_prediksi.csv", index=False)

    write_analysis(metadata, results, importance)
    print("Selesai. Ringkasan Hasil:")
    print(results[["model", "cv_f1_mean", "test_accuracy", "test_f1_macro"]].to_string(index=False))


def write_analysis(metadata, results, importance):
    s = metadata["summary"]
    chosen = results.loc[results.model == metadata["selected_model"]].iloc[0]
    lines = [
        "# Hasil Eksperimen dan Analisis Model Prediksi Gangguan Depresi",
        "",
        "Seluruh metrik dan visualisasi dihasilkan secara riil oleh eksekusi kode eksperimen proyek.",
        "",
        "## Ringkasan Data",
        f"- Data asli: {s['raw_rows']} responden, {s['raw_columns']} kolom awal.",
        f"- Setelah seleksi fitur klinis terarah dan pemeriksaan integritas: {s['clean_rows']} baris lengkap dengan {s['unique_profiles']} profil independen.",
        f"- Pembagian data: {s['train_rows']} baris data latih (80%) dan {s['test_rows']} baris data uji holdout (20%) secara berstrata.",
        "- Evaluasi tuning dilakukan via 5-Fold Stratified Cross-Validation pada data latih saja.",
        "",
        "## Perbandingan Tiga Model Machine Learning",
        "| Model | CV Macro-F1 ± SD | Train Macro-F1 | Test Accuracy | Test Precision Macro | Test Recall Macro | Test Macro-F1 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for _, r in results.iterrows():
        lines.append(
            f"| {r['model']} | {r.cv_f1_mean:.4f} ± {r.cv_f1_std:.4f} | {r.train_f1_macro:.4f} | "
            f"{r.test_accuracy:.4f} | {r.test_precision_macro:.4f} | {r.test_recall_macro:.4f} | {r.test_f1_macro:.4f} |"
        )
    lines += [
        "",
        "## Pemilihan Model",
        f"- Model terpilih untuk deployment aplikasi adalah **{chosen['model']}** dengan CV Macro-F1 tertinggi ({chosen.cv_f1_mean:.4f}).",
        "- Pilihan model dikunci sebelum data uji dievaluasi, sehingga tidak terjadi kebocoran informasi (*data leakage*).",
        "",
        "## Faktor-Faktor Paling Berpengaruh",
        "- Berdasarkan *Permutation Importance* pada data latih model terpilih:",
    ]
    for _, imp in importance.head(5).iterrows():
        lines.append(f"  - **{imp.feature}**: penurunan F1 sebesar {imp.importance_mean:.4f} ± {imp.importance_std:.4f}")
    lines += [
        "",
        "## Catatan Klinis dan Batasan",
        "- Aplikasi ini bertujuan untuk edukasi dan skrining awal, **bukan alat penegak diagnosis medis resmi**.",
        "- Label depresi berasal dari ambang batas skor kuesioner PHQ-9 (≥ 10) pada survei CDC NHANES.",
        "- Konsultasi langsung dengan psikiater atau psikolog klinis tetap menjadi rujukan utama."
    ]
    (ANALYSIS / "analisis_model.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
