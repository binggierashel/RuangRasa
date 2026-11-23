# Metodologi Pengembangan Model Machine Learning (CRISP-DM)
## Proyek Skrining Risiko Gangguan Depresi Mayor (CDC NHANES)

Pengembangan sistem machine learning pada proyek ini mengadopsi standar industri **CRISP-DM (Cross-Industry Standard Process for Data Mining)** yang terbukti handal untuk domain kesehatan dan analitik biomedis.

```
       ┌────────────────────────────────────────────────────────┐
       │ 1. Business & Clinical Understanding (PHQ-9 Screener)  │
       └───────────────────────────┬────────────────────────────┘
                                   │
       ┌───────────────────────────▼────────────────────────────┐
       │ 2. Data Understanding (CDC NHANES 2005-2018, 36.259)   │
       └───────────────────────────┬────────────────────────────┘
                                   │
       ┌───────────────────────────▼────────────────────────────┐
       │ 3. Data Preparation (No Leakage Preprocessing Pipeline)│
       └───────────────────────────┬────────────────────────────┘
                                   │
       ┌───────────────────────────▼────────────────────────────┐
       │ 4. Modeling (3 Algoritma & 5-Fold Stratified CV Tuning) │
       └───────────────────────────┬────────────────────────────┘
                                   │
       ┌───────────────────────────▼────────────────────────────┐
       │ 5. Evaluation (Holdout Test Set & Feature Importance)  │
       └───────────────────────────┬────────────────────────────┘
                                   │
       ┌───────────────────────────▼────────────────────────────┐
       │ 6. Deployment (Aplikasi Streamlit Interaktif & Skrining)│
       └────────────────────────────────────────────────────────┘
```

---

### Fase 1: Business & Clinical Understanding (Pemahaman Masalah Klinis)
- **Konteks Klinis:** Depresi adalah gangguan suasana hati persisten yang mempengaruhi lebih dari 280 juta individu di seluruh dunia. Skrining konvensional memerlukan wawancara dokter atau kuesioner mandiri yang sering kali terlambat dilakukan.
- **Standar Label Target:** Pengukuran depresi didasarkan pada instrumen baku **Patient Health Questionnaire-9 (PHQ-9)** yang divalidasi oleh Kroenke et al. (2001). Skor total $\ge 10$ ditetapkan sebagai ambang batas klinis (`Depressed`), yang memiliki sensitivitas dan spesifisitas sebesar 88% untuk Major Depressive Disorder (MDD). Skor $< 10$ dikategorikan sebagai `Not Depressed`.
- **Kriteria Keberhasilan:** Mengembangkan model klasifikasi yang mampu mengatasi ketidakseimbangan kelas (*class imbalance*) secara optimal, dievaluasi menggunakan metrik **Macro-F1** agar kedua kelas diprioritaskan secara seimbang.

---

### Fase 2: Data Understanding (Pemahaman Data)
- **Sumber Data:** Centers for Disease Control and Prevention (CDC) - National Health and Nutrition Examination Survey (NHANES) multi-tahun (2005–2018).
- **Karakteristik Data Awal:** 36.259 baris data responden unik dengan 18 fitur prediktor (7 numerik, 11 kategorikal) dan 1 kolom target biner.
- **Pemeriksaan Integritas:**
  - Duplikasi baris utuh: 0 baris (seluruh responden memiliki nomor identifikasi `SEQN` unik).
  - Profil fitur bertentangan (*conflicting profiles*): 0 baris.
  - Distribusi target: 33.091 responden (91,26%) `Not Depressed` dan 3.168 responden (8,74%) `Depressed`.
- **Eksplorasi Statistik:**
  - Analisis outlier numerik menggunakan metode rentang antar-kuartil (*Interquartile Range* / IQR).
  - Evaluasi korelasi Pearson antarfitur numerik untuk memeriksa multikolinearitas.
  - Analisis tabulasi silang (*crosstab*) pada fitur kategorikal untuk menemukan asosiasi kuat dengan label target.

---

### Fase 3: Data Preparation (Persiapan & Prapemrosesan Data)
- **Pencegahan Kebocoran Data (Data Leakage):**
  - Pembagian partisi data dilakukan terlebih dahulu sebelum tahap transformasi apapun: 80% Data Latih (29.007 responden) dan 20% Data Uji Holdout (7.252 responden) dengan stratifikasi target (`random_state=42`).
  - Seluruh parameter transformer (median imputasi numerik, modus imputasi kategorikal, rata-rata dan deviasi standar untuk *StandardScaler*, serta kategori unik *OneHotEncoder*) **hanya di-fit pada data latih**. Data uji holdout murni diperlakukan sebagai masukan baru tak terlihat (*unseen data*).
- **Arsitektur Pipeline:**
  - **Fitur Numerik (7 variabel):** `SimpleImputer(strategy="median")` $\rightarrow$ `StandardScaler()`.
  - **Fitur Kategorikal (11 variabel):** `SimpleImputer(strategy="most_frequent")` $\rightarrow$ `OneHotEncoder(handle_unknown="ignore", sparse_output=False)`.
  - Menggabungkan kedua cabang melalui `ColumnTransformer`, menghasilkan 50 dimensi fitur siap latih.

---

### Fase 4: Modeling (Pemodelan & Hyperparameter Tuning)
Sesuai ketentuan PJBL, dilakukan komparasi terhadap 3 algoritma machine learning:
1. **Logistic Regression (Linear / Probabilistik Baseline):**
   - Ruang pencarian: `C: [0.1, 1.0, 10.0]`, `class_weight: ['balanced', None]`.
   - Konfigurasi terbaik: `C = 1.0`, `class_weight = None`.
2. **Decision Tree Classifier (Algoritma Non-linear Berbasis Aturan):**
   - Ruang pencarian: `max_depth: [4, 6, 8]`, `class_weight: ['balanced', None]`.
   - Konfigurasi terbaik: `max_depth = 6`, `class_weight = None`.
3. **Random Forest Classifier (Ensemble Bagging dengan Random Subspaces):**
   - Ruang pencarian: `n_estimators: [100]`, `max_depth: [6, 10]`, `class_weight: ['balanced']`.
   - Konfigurasi terbaik: `n_estimators = 100`, `max_depth = 10`, `class_weight = 'balanced'`.

**Prosedur Tuning:**
- Menggunakan `GridSearchCV` yang diintegrasikan dalam `Pipeline` Scikit-Learn.
- Evaluasi tuning dilakukan via **5-Fold Stratified Cross-Validation** pada data latih (`random_state=43`).
- **Aturan Penguncian Model:** Model terbaik dipilih murni berdasarkan nilai rerata **CV Macro-F1** tertinggi pada data latih sebelum mengevaluasi data uji holdout.

---

### Fase 5: Evaluation (Evaluasi Komparatif & Interpretasi)
- **Metrik Evaluasi:**
  - Macro-Averaged F1-Score (metrik seleksi utama).
  - Accuracy, Precision Macro, Recall Macro.
  - Matriks Konfusi (*Confusion Matrix*).
  - Perbandingan terhadap *Dummy Classifier* (baseline mayoritas).
- **Hasil Evaluasi Komparatif:**
  - **Random Forest (Model Terpilih):**
    - 5-Fold CV Macro-F1 Data Latih: **0.6428 ± 0.0076** (Peringkat 1)
    - Test Macro-F1: **0.6356**
    - Test Accuracy: **81.76%**
    - Test Recall Depressed: **48.74%** (kemampuan menangkap kasus depresi lebih tinggi berkat `class_weight='balanced'`).
  - **Decision Tree:**
    - 5-Fold CV Macro-F1: **0.6299 ± 0.0091** | Test Accuracy: **90.89%** | Test Macro-F1: **0.6105**
  - **Logistic Regression:**
    - 5-Fold CV Macro-F1: **0.6216 ± 0.0049** | Test Accuracy: **91.52%** | Test Macro-F1: **0.6075**
- **Interpretasi Model (Explainable AI):**
  - Menerapkan *Permutation Feature Importance* pada model Random Forest terpilih (dihitung pada data latih).
  - Menganalisis koefisien regresi logistik terstandardisasi untuk validasi arah pengaruh faktor risiko (positif vs protektif).

---

### Fase 6: Deployment (Implementasi Aplikasi & Inferensi)
- **Aplikasi Web Interaktif:** Dibangun dengan Streamlit (`Source_Code/app/streamlit_app.py`).
- **Fitur Utama:**
  1. *Prediksi Individu:* Formulir input terstruktur lengkap dengan tombol profil demo risiko tinggi/rendah.
  2. *Prediksi Batch CSV:* Fasilitas unggah file CSV, validasi skema otomatis, download template, dan download hasil inferensi.
  3. *Eksplorasi Data (EDA):* Ringkasan statistik dan 6 grafik visualisasi resolusi tinggi.
  4. *Evaluasi & Komparasi Model:* Tabel komparasi 3 algoritma, matriks konfusi, dan grafik *feature importance*.
  5. *Informasi Proyek:* Referensi 5 jurnal ber-DOI aktif, profil tim pengembang, dan catatan etika/disclaimer klinis.
- **Validasi Input:** Diimplementasikan fungsi `validate_input()` untuk memverifikasi tipe numerik, rentang biologis logis (misal Sistolik > Diastolik), dan mencegah masukan kategori anomali.
