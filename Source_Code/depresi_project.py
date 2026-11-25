"""Kontrak input, fitur, dan preprocessing bersama untuk pelatihan, aplikasi, dan pengujian."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
TARGET = "Depression"
LABELS = ["Not Depressed", "Depressed"]
DISPLAY = {
    "Not Depressed": "Tidak Terindikasi Depresi Mayor",
    "Depressed": "Berisiko Mengalami Depresi (PHQ-9 ≥ 10)"
}

CATEGORICAL = [
    "Gender", "Education Level", "Marital Status", "Household Income",
    "Trouble Sleeping History", "Vigorous Recreation", "Moderate Recreation",
    "Current Smoker", "Memory Problems", "Cant Work", "Limited Work"
]
NUMERIC = [
    "Age", "Sleep Hours", "Sedentary Time", "BMI", "Systolic", "Diastolic", "Pulse"
]
FEATURES = CATEGORICAL + NUMERIC

RANGES = {
    "Age": (18, 120),
    "Sleep Hours": (0.0, 24.0),
    "Sedentary Time": (0.0, 1440.0),
    "BMI": (0.0, 150.0),
    "Systolic": (0.0, 300.0),
    "Diastolic": (0.0, 200.0),
    "Pulse": (0.0, 250.0),
}


def prepare_features(frame):
    """Transformasi deterministik input tanpa membocorkan statistik data uji/global."""
    data = frame.copy()
    missing = sorted(set(FEATURES) - set(data.columns))
    if missing:
        raise ValueError("Kolom wajib belum tersedia: " + ", ".join(missing))
    data = data[FEATURES].copy()
    for col in CATEGORICAL:
        data[col] = data[col].astype(str).replace(r"^\s*$", np.nan, regex=True)
    for col in NUMERIC:
        original = data[col]
        data[col] = pd.to_numeric(original, errors="coerce")
        invalid = original.notna() & original.astype(str).str.strip().ne("") & data[col].isna()
        if invalid.any():
            raise ValueError(f"Kolom {col} berisi nilai yang tidak dapat diubah menjadi numerik.")
        if np.isinf(data[col].to_numpy(dtype=float)).any():
            raise ValueError(f"Kolom {col} tidak boleh berisi nilai infinity.")
    return data


def validate_input(frame, schema):
    """Validasi masukan pengguna; rentang batasan bertujuan mencegah kesalahan input."""
    if frame.empty:
        raise ValueError("Data input kosong.")
    data = prepare_features(frame)
    if data.isna().any().any():
        raise ValueError("Lengkapi seluruh fitur sebelum melakukan prediksi.")
    for col, (low, high) in RANGES.items():
        if not data[col].between(low, high).all():
            raise ValueError(f"{col} harus berada pada rentang {low}–{high}.")
    valid_bp = (data["Systolic"] == 0) | (data["Diastolic"] == 0) | (data["Systolic"] > data["Diastolic"])
    if not valid_bp.all():
        raise ValueError("Tekanan darah sistolik harus lebih besar daripada diastolik.")
    for col in CATEGORICAL:
        known = set(schema["categories"].get(col, []))
        unknown = sorted(set(data[col]) - known)
        if unknown:
            raise ValueError(f"Kategori {col} tidak dikenal: {', '.join(unknown)}")
    return data


def make_preprocessor():
    """Membangun objek ColumnTransformer baru yang belum di-fit."""
    num_pipeline = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler())
    ])
    cat_pipeline = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("encode", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])
    return ColumnTransformer([
        ("numeric", num_pipeline, NUMERIC),
        ("categorical", cat_pipeline, CATEGORICAL)
    ])
