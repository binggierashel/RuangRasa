# Hasil Pelatihan & Evaluasi Model (RuangRasa)

Dokumen ini merangkum isi file JSON (`model_metadata.json` dan `input_schema.json`) serta hasil evaluasi model ke dalam format yang mudah dibaca.

---

## 1. Ringkasan Data & Pembagian Dataset
- **Sumber Data:** CDC NHANES (2005–2018), target berbasis skor PHQ-9 $\ge 10$ (`Depressed` vs `Not Depressed`).
- **Total Data Bersih:** **36.259 responden** (18 fitur input, 0 duplikat).
  - `Not Depressed` (Tidak Depresi): **33.091** responden (91,26%)
  - `Depressed` (Berisiko Depresi): **3.168** responden (8,74%)
- **Pembagian Data (80% : 20% Stratified, `seed = 42`):**
  - **Data Latih (Train):** **29.007 responden** (`Not Depressed`: 26.473 | `Depressed`: 2.534)
  - **Data Uji Holdout (Test):** **7.252 responden** (`Not Depressed`: 6.618 | `Depressed`: 634)
- **Metode Seleksi Model:** *5-Fold Stratified Cross-Validation* pada data latih saja menggunakan metrik **Macro-F1** (tanpa menyentuh data uji saat tuning, sehingga bebas *data leakage*).

---

## 2. Perbandingan Performa Model

| Algoritma | Parameter Terbaik | CV Macro-F1 (Data Latih) | Train Macro-F1 | Test Accuracy | Test Precision Macro | Test Recall Macro | Test Macro-F1 | Status |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **Random Forest** | `n_estimators=100`, `max_depth=10`, `class_weight="balanced"` | **0,6428 ± 0,0074** | 0,6999 | 81,76% | 0,6145 | **0,7346** | **0,6356** | **TERPILIH** |
| **Decision Tree** | `max_depth=6`, `class_weight=None` | 0,6299 ± 0,0140 | 0,6572 | 90,89% | 0,6884 | 0,5850 | 0,6105 | Pembanding |
| **Logistic Regression** | `C=1.0`, `class_weight=None` | 0,6216 ± 0,0037 | 0,6219 | **91,52%** | **0,7368** | 0,5784 | 0,6075 | Pembanding |
| *Dummy (Majority)* | Tebak mayoritas saja | - | - | 91,26% | 0,4563 | 0,5000 | 0,4771 | Baseline |

### Kenapa Random Forest Dipilih?
1. **Skor Validasi (CV Macro-F1) Tertinggi:** Meraih rata-rata **0,6428** pada 5-Fold Cross-Validation data latih.
2. **Skor Uji (Test Macro-F1) Tertinggi:** Meraih **0,6356** pada data uji yang belum pernah dilihat model.
3. **Paling Sensitif Mendeteksi Kasus Depresi:** Karena data sangat tidak seimbang (hanya 8,74% kelas `Depressed`), akurasi tinggi pada *Logistic Regression* (91,52%) dan *Decision Tree* (90,89%) menipu karena hampir semua responden ditebak tidak depresi.
   - **Random Forest** berhasil mendeteksi **402 dari 634 kasus depresi** (**Recall 63,41%**).
   - **Decision Tree** hanya mendeteksi **122 dari 634 kasus** (**Recall 19,24%**).
   - **Logistic Regression** hanya mendeteksi **108 dari 634 kasus** (**Recall 17,03%**).

---

## 3. Detail Confusion Matrix pada Data Uji (7.252 Responden)

| Model | Benar `Depressed` (TP) | Salah Tebak Sehat (FN) | Salah Tebak Depresi (FP) | Benar `Not Depressed` (TN) | Recall Kelas `Depressed` | Precision Kelas `Depressed` | F1 Kelas `Depressed` |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Random Forest** | **402** | 232 | 1.091 | 5.527 | **63,41%** | 26,93% | **0,3780** |
| **Decision Tree** | 122 | 512 | 149 | 6.469 | 19,24% | 45,02% | 0,2696 |
| **Logistic Regression** | 108 | 526 | 89 | 6.529 | 17,03% | **54,82%** | 0,2599 |

---

## 4. 5 Fitur Paling Berpengaruh (*Permutation Importance* Random Forest)
1. **Trouble Sleeping History** (Riwayat gangguan tidur): penurunan F1 sebesar **0,0577 ± 0,0012**
2. **Age** (Usia): penurunan F1 sebesar **0,0225 ± 0,0002**
3. **Cant Work** (Tidak bisa bekerja karena kondisi kesehatan): penurunan F1 sebesar **0,0197 ± 0,0020**
4. **Memory Problems** (Masalah daya ingat/konsentrasi): penurunan F1 sebesar **0,0185 ± 0,0016**
5. **Moderate Recreation** (Aktivitas rekreasi/olahraga sedang): penurunan F1 sebesar **0,0149 ± 0,0021**

---

## 5. Daftar 18 Fitur Input Model (Ringkasan `input_schema.json`)

### A. 11 Fitur Kategori
| Fitur | Nilai yang Diterima |
|---|---|
| `Gender` | `Female`, `Male` |
| `Education Level` | `Less Than 9th Grade`, `9-11th Grade`, `High School`, `Some College or AA Degree`, `College Graduate or Above`, `Missing` |
| `Marital Status` | `Married`, `Widowed`, `Divorced`, `Separated`, `Never Married`, `Partner`, `Missing` |
| `Household Income` | `Below $5K`, `Below $10K`, `Below $15K`, `Below $20K`, `Over $20K`, `Below $25K`, `Below $35K`, `Below $45K`, `Below $55K`, `Below $65K`, `Below $75K`, `$75K+`, `Missing` |
| `Trouble Sleeping History` | `No`, `Yes` |
| `Vigorous Recreation` | `No`, `Yes`, `Missing` |
| `Moderate Recreation` | `No`, `Yes`, `Missing` |
| `Current Smoker` | `Never`, `Some Days`, `Every Day`, `Missing` |
| `Memory Problems` | `No`, `Yes` |
| `Cant Work` | `No`, `Yes` |
| `Limited Work` | `No`, `Yes` |

### B. 7 Fitur Numerik (Rentang Data Latih)
| Fitur | Minimum | Median | Maksimum |
|---|---:|---:|---:|
| `Age` (tahun) | 18,0 | 47,0 | 85,0 |
| `Sleep Hours` (jam/hari) | 0,0 | 7,0 | 14,5 |
| `Sedentary Time` (menit/hari) | 0,0 | 300,0 | 1320,0 |
| `BMI` | 0,0 | 27,8 | 86,2 |
| `Systolic` (mmHg) | 0,0 | 120,0 | 270,0 |
| `Diastolic` (mmHg) | 0,0 | 70,0 | 124,0 |
| `Pulse` (bpm) | 0,0 | 72,0 | 224,0 |

---

## 6. Penjelasan Isi Folder `Model/`
- **`joblib untuk streamlit/`** — Berisi 4 file model siap pakai yang dimuat oleh aplikasi web Streamlit:
  - `selected_pipeline.joblib` : Model final terpilih (**Random Forest**).
  - `random_forest_pipeline.joblib` : Model terlatih **Random Forest**.
  - `decision_tree_pipeline.joblib` : Model terlatih **Decision Tree**.
  - `logistic_regression_pipeline.joblib` : Model terlatih **Logistic Regression**.
- **`ipynb model/`** — Berisi 1 notebook Jupyter (`.ipynb`) lengkap dari persiapan data hingga evaluasi dan ekspor model:
  - `RuangRasa_Prediksi_Depresi.ipynb` : Persiapan data, 6 grafik EDA, preprocessing, pelatihan & *5-Fold Stratified CV* 3 algoritma, *confusion matrix*, *permutation importance*, dan ekspor model.
- `HASIL_MODEL.md` : Rangkuman hasil pelatihan dan evaluasi model (file ini).
- `01_confusion_matrices.png` : Gambar matriks prediksi benar vs salah untuk ketiga model.
- `02_model_comparison.png` : Grafik perbandingan skor akurasi, presisi, recall, dan Macro-F1 ketiga model.
- `03_permutation_importance.png` : Grafik urutan fitur yang paling berpengaruh pada Random Forest.
- `ringkasan_perbandingan_model.csv` : Tabel perbandingan metrik model (bisa langsung dibuka di Excel).
- `model_metadata.json` & `input_schema.json` : File konfigurasi teknis yang dibaca otomatis oleh kode aplikasi Python/Streamlit (Python 3.12.4, scikit-learn 1.9.1, dilatih 4 November 2026).

> **Catatan:** Model ini dibuat untuk skrining awal dan edukasi, **bukan alat diagnosis medis resmi**.
