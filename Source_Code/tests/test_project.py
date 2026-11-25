"""Unit testing komprehensif untuk integritas dataset, preprocessing, skema, dan inferensi model."""
import hashlib
import json
from pathlib import Path
import unittest
import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Source_Code"

import sys
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from depresi_project import (
    TARGET, LABELS, FEATURES, NUMERIC, CATEGORICAL, RANGES,
    prepare_features, validate_input
)


class TestDepressionProject(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema_path = ROOT / "Model/input_schema.json"
        cls.metadata_path = ROOT / "Model/model_metadata.json"
        cls.assertTrue(cls.schema_path.exists(), "input_schema.json harus ada.")
        cls.assertTrue(cls.metadata_path.exists(), "model_metadata.json harus ada.")
        cls.schema = json.loads(cls.schema_path.read_text(encoding="utf-8"))
        cls.metadata = json.loads(cls.metadata_path.read_text(encoding="utf-8"))

    def test_01_raw_dataset_integrity(self):
        """Memverifikasi dataset asli dan SHA-256 hash kesesuaian provenance."""
        raw_path = ROOT / "Dataset/Data_Asli/nhanes_depression_raw.csv"
        prov_path = ROOT / "Dataset/Data_Asli/provenance.json"
        self.assertTrue(raw_path.exists())
        self.assertTrue(prov_path.exists())

        raw_df = pd.read_csv(raw_path, low_memory=False)
        self.assertEqual(len(raw_df), 36259)
        self.assertIn(TARGET, raw_df.columns)
        self.assertEqual(set(raw_df[TARGET].unique()), set(LABELS))

        prov = json.loads(prov_path.read_text(encoding="utf-8"))
        calc_sha = hashlib.sha256(raw_path.read_bytes()).hexdigest()
        self.assertEqual(calc_sha, prov["sha256"])

    def test_02_data_partitions_stratification(self):
        """Memverifikasi rasio pembagian data train:test 80:20 dan stratifikasi."""
        train_path = ROOT / "Dataset/Data_Olahan/train.csv"
        test_path = ROOT / "Dataset/Data_Olahan/test.csv"
        self.assertTrue(train_path.exists())
        self.assertTrue(test_path.exists())

        train_df = pd.read_csv(train_path, low_memory=False)
        test_df = pd.read_csv(test_path, low_memory=False)

        self.assertEqual(len(train_df), 29007)
        self.assertEqual(len(test_df), 7252)
        self.assertEqual(len(train_df) + len(test_df), 36259)

        train_dep_ratio = (train_df[TARGET] == "Depressed").mean()
        test_dep_ratio = (test_df[TARGET] == "Depressed").mean()
        self.assertAlmostEqual(train_dep_ratio, 0.08735, places=3)
        self.assertAlmostEqual(test_dep_ratio, 0.08742, places=3)

    def test_03_feature_contract(self):
        """Memverifikasi daftar fitur numerik, kategorikal, dan totalnya."""
        self.assertEqual(len(NUMERIC), 7)
        self.assertEqual(len(CATEGORICAL), 11)
        self.assertEqual(len(FEATURES), 18)
        self.assertEqual(set(FEATURES), set(NUMERIC + CATEGORICAL))

    def test_04_validation_rejection_rules(self):
        """Memverifikasi validasi masukan mendeteksi anomali biologis dan kategori salah."""
        template_df = pd.read_csv(ROOT / "Dataset/template_input.csv")
        sample = template_df.iloc[[0]].copy()

        # 1. Valid sample harus lolos
        validated = validate_input(sample, self.schema)
        self.assertEqual(len(validated), 1)

        # 2. Input kosong
        with self.assertRaises(ValueError):
            validate_input(pd.DataFrame(), self.schema)

        # 3. Kolom hilang
        broken_cols = sample.drop(columns=["Age"])
        with self.assertRaises(ValueError):
            validate_input(broken_cols, self.schema)

        # 4. Kategori asing tidak dikenal
        bad_gender = sample.copy()
        bad_gender["Gender"] = "Alien"
        with self.assertRaises(ValueError):
            validate_input(bad_gender, self.schema)

        # 5. Nilai biologis di luar batas
        bad_age = sample.copy()
        bad_age["Age"] = 150
        with self.assertRaises(ValueError):
            validate_input(bad_age, self.schema)

        # 6. Tekanan darah terbalik (Sistolik <= Diastolik saat keduanya > 0)
        bad_bp = sample.copy()
        bad_bp["Systolic"] = 80.0
        bad_bp["Diastolic"] = 120.0
        with self.assertRaises(ValueError):
            validate_input(bad_bp, self.schema)

    def test_05_trained_models_inference(self):
        """Memverifikasi seluruh model pipeline dapat memprediksi dan menghasilkan probabilitas valid."""
        models = [
            "random_forest_pipeline.joblib",
            "logistic_regression_pipeline.joblib",
            "decision_tree_pipeline.joblib",
            "selected_pipeline.joblib"
        ]
        sample_df = pd.read_csv(ROOT / "Dataset/template_input.csv")

        model_dir = ROOT / "Model/joblib untuk streamlit"
        if not model_dir.exists():
            model_dir = ROOT / "Model"

        for m_name in models:
            m_path = model_dir / m_name
            self.assertTrue(m_path.exists(), f"Model {m_name} harus ada.")
            pipeline = joblib.load(m_path)

            preds = pipeline.predict(sample_df)
            self.assertEqual(len(preds), len(sample_df))
            for p in preds:
                self.assertIn(p, LABELS)

            probs = pipeline.predict_proba(sample_df)
            self.assertEqual(probs.shape, (len(sample_df), 2))
            np.testing.assert_allclose(probs.sum(axis=1), 1.0, rtol=1e-5)

    def test_06_notebook_execution(self):
        """Memverifikasi bahwa notebook lengkap telah dieksekusi dengan output riil."""
        nb_path = ROOT / "Source_Code/notebooks/RuangRasa_Prediksi_Depresi.ipynb"
        self.assertTrue(nb_path.exists(), "Notebook RuangRasa_Prediksi_Depresi.ipynb harus ada.")
        nb = json.loads(nb_path.read_text(encoding="utf-8"))
        code_cells = [c for c in nb.get("cells", []) if c.get("cell_type") == "code"]
        self.assertGreater(len(code_cells), 0)
        for cell in code_cells:
            self.assertIsNotNone(cell.get("execution_count"))
            self.assertGreater(len(cell.get("outputs", [])), 0)

    def test_07_model_evaluation_metrics_consistency(self):
        """Memverifikasi perbandingan ketiga model dan konsistensi Random Forest terpilih."""
        comp_path = ROOT / "Source_Code/reports/modeling/model_comparison.csv"
        self.assertTrue(comp_path.exists())
        df_comp = pd.read_csv(comp_path)
        self.assertEqual(len(df_comp), 3)
        self.assertIn("random_forest", df_comp["model"].values)
        self.assertIn("logistic_regression", df_comp["model"].values)
        self.assertIn("decision_tree", df_comp["model"].values)

        rf_row = df_comp[df_comp.model == "random_forest"].iloc[0]
        self.assertTrue(rf_row["selected_by_cv"])
        self.assertGreater(rf_row["cv_f1_mean"], 0.63)
        self.assertGreater(rf_row["test_f1_macro"], 0.62)


if __name__ == "__main__":
    unittest.main()
