# RuangRasa: Sistem Klasifikasi & Skrining Risiko Gangguan Depresi Mayor
### Proyek Pembelajaran Berbasis Proyek (PJBL) Mata Kuliah Machine Learning — Semester 5

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9.1-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.66.1-red.svg)
![Dataset](https://img.shields.io/badge/Dataset-CDC%20NHANES-green.svg)
![Tests](https://img.shields.io/badge/Tests-7%20Passed%20(100%25)-brightgreen.svg)
![License](https://img.shields.io/badge/License-Academic-lightgrey.svg)

---

## 📌 Ringkasan Proyek

**RuangRasa** adalah sistem berbasis *Machine Learning* untuk mengidentifikasi dan menskrining tingkat risiko seseorang terhadap **Gangguan Depresi Mayor (*Major Depressive Disorder* / MDD)**. Sistem memanfaatkan data kebiasaan gaya hidup, pola tidur, kapasitas fungsional, dan pengukuran fisik non-invasif yang diekstraksi dari survei kesehatan berkala **Centers for Disease Control and Prevention (CDC) - National Health and Nutrition Examination Survey (NHANES)** periode multi-tahun (2005–2018).

Label target depresi diturunkan dari instrumen skrining baku **Patient Health Questionnaire-9 (PHQ-9)** dengan ambang batas skor $\ge 10$ yang memiliki sensitivitas dan spesifisitas sebesar 88% untuk depresi sedang hingga berat (*Kroenke et al., 2001*).

Tiga algoritma supervised learning dikomparasikan secara ketat mengacu pada rubrik evaluasi PJBL:
1. **Random Forest Classifier** *(Model Terpilih)*
2. **Logistic Regression**
3. **Decision Tree Classifier**

Seluruh proses transformasi prapemrosesan diintegrasikan dalam arsitektur `Pipeline` Scikit-Learn dengan isolasi partisi 80% Latih : 20% Uji holdout berstrata guna menjamin **zero data leakage**.

---

## 📊 Hasil Eksperimen dan Komparasi Model

Evaluasi model dikunci berdasarkan **5-Fold Stratified Cross-Validation pada data latih (29.007 responden)** menggunakan metrik seleksi **Macro-F1** untuk menangani ketidakseimbangan kelas (*imbalance ratio* 8,7% : 91,3%). Model terpilih kemudian diuji pada **7.252 responden data uji holdout (*unseen test data*)**:

| Algoritma | Baseline CV F1 | CV Macro-F1 Data Latih (Mean ± SD) | Train Macro-F1 | Test Accuracy | Test Precision Macro | Test Recall Macro | Test Macro-F1 | Status Pemilihan |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 🌲 **Random Forest** | 0,6356 | **0,6428 ± 0,0076** | 0,7247 | **81,76%** | **0,6013** | **0,7074** | **0,6356** | 🏆 **TERPILIH (Juara CV)** |
| 🌳 **Decision Tree** | 0,6029 | 0,6299 ± 0,0091 | 0,6428 | 90,89% | 0,6682 | 0,5892 | 0,6105 | Tidak Terpilih |
| 📈 **Logistic Regression**| 0,6115 | 0,6216 ± 0,0049 | 0,6222 | 91,52% | 0,7475 | 0,5722 | 0,6075 | Tidak Terpilih |
| ⚖️ *Dummy (Majority)* | - | - | - | 91,26% | 0,4563 | 0,5000 | 0,4771 | Baseline Naif |

### Alasan Pemilihan Random Forest:
1. **Skor Validasi Tertinggi:** Memperoleh nilai *Validation Macro-F1* tertinggi secara konsisten di seluruh fold CV (0,6428).
2. **Sensitivitas Terhadap Kasus Depresi:** Pada evaluasi holdout, Random Forest menghasilkan *Recall* depresi sebesar **48,74%** (mendeteksi 309 kasus depresi riil), hampir 3 kali lipat lebih sensitif dibandingkan Logistic Regression (16,72%) yang mengalami bias ekstrem terhadap kelas mayoritas non-depresi.
3. **Generalisasi Stabil:** Kesenjangan (*gap*) antara F1-score data latih dan uji terkontrol dengan baik (0,0819) berkat pembatasan `max_depth=10`.

---

## 🔍 Temuan Kunci Faktor Risiko (Explainable AI)

Berdasarkan *Permutation Feature Importance* pada model Random Forest dan analisis koefisien logit:
1. **Trouble Sleeping History (Riwayat Gangguan Tidur / Insomnia):** Faktor paling berpengaruh terhadap risiko depresi mayor (penurunan skor F1 terbesar jika nilai fitur diacak).
2. **Cant Work (Ketidakmampuan Bekerja Akibat Kesehatan):** Indikator disabilitas fungsional yang memiliki korelasi linear positif tertinggi (+0,764 pada bobot logit).
3. **Memory Problems (Gangguan Konsentrasi & Daya Ingat):** Manifestasi kognitif signifikan pada responden yang berisiko depresi.
4. **Sedentary Time & Sleep Hours:** Durasi duduk yang tinggi (> 10 jam/hari) dan durasi tidur ekstrem (< 5 jam atau > 10 jam) secara kumulatif memperberat risiko depresi.
5. **Faktor Protektif:** Tingkat pendidikan tinggi (*College Graduate*) dan pendapatan keluarga memadai (*$75K+*) bertindak sebagai variabel protektif terhadap kejadian depresi.

---

## 📁 Struktur Direktori Repositori

```
prediksi_gangguan_depresi/
├── .streamlit/
│   └── config.toml                        # Konfigurasi tema & server Streamlit
├── Dataset/
│   ├── Data_Asli/
│   │   ├── nhanes_depression_raw.csv      # Data survei CDC NHANES (36.259 baris riil)
│   │   └── provenance.json                # SHA-256 hash & asal usul dataset
│   ├── Data_Olahan/
│   │   ├── cleaned.csv                    # Data bersih lengkap
│   │   ├── train.csv                      # Partisi data latih (29.007 baris, 80%)
│   │   ├── test.csv                       # Partisi data uji holdout (7.252 baris, 20%)
│   │   ├── preview_preprocessing_train.csv# Matriks 50 fitur hasil encoding
│   │   └── notebook_split.json            # State handoff indeks partisi antar-notebook
│   ├── template_input.csv                 # Template CSV untuk input batch pengguna
│   └── contoh_prediksi.csv                # Sampel 10 data uji untuk demo inferensi
├── Dokumentasi/
│   ├── identitas_kelompok.json            # Data anggota kelompok, NIM & dosen
│   ├── pengajuan_tema.md                  # Formulir pengajuan proposal proyek
│   ├── kamus_data.md                      # Definisi 18 fitur klinis & target PHQ-9
│   ├── metodologi.md                      # Dokumentasi metodologi CRISP-DM
│   ├── checklist_ketentuan.md             # Matriks checklist rubrik ketentuan PJBL
│   ├── eksekusi_notebook_bertahap.json    # Bukti eksekusi sukses 5 notebook
│   ├── laporan_project.md                 # Laporan akademik lengkap (Markdown)
│   └── laporan_project.docx               # Laporan akademik lengkap format Word (.docx)
├── Link_Deployment/
│   └── README.md                          # Panduan deployment ke Streamlit Cloud & URL
├── Model/
│   ├── decision_tree_pipeline.joblib      # Pipeline terlatih Decision Tree
│   ├── logistic_regression_pipeline.joblib# Pipeline terlatih Logistic Regression
│   ├── random_forest_pipeline.joblib      # Pipeline terlatih Random Forest
│   ├── selected_pipeline.joblib           # Pipeline model terpilih untuk aplikasi
│   ├── input_schema.json                  # Kontrak fitur & rentang kategori
│   └── model_metadata.json                # Metadata, metrik evaluasi & lingkungan latih
├── Referensi_Jurnal/
│   ├── 1_Kroenke_2001_PHQ9.md             # Ringkasan studi validasi PHQ-9 (DOI aktif)
│   ├── 2_Li_2024_NHANES_Depression_Sleep.md      # Prediksi depresi & gangguan tidur NHANES
│   ├── 3_Selvaraj_2024_NHANES_Ensemble_RF.md     # Stacked ensemble & RF feature importance
│   ├── 4_Vu_2025_NHANES_ML_Depression.md         # Komparasi 6 algoritma ML pada NHANES
│   ├── 5_Salimi_2026_NHANES_Interpretable_ML.md  # Klasifikasi depresi populasi penuh NHANES
│   ├── 6_Cui_2026_NHANES_Stacking_SHAP.md        # Stacking ensemble + SHAP NHANES 2005–2023
│   └── tinjauan_pustaka.md                # Tabel komparasi jurnal sesuai format PJBL
├── Source_Code/
│   ├── app/
│   │   ├── streamlit_app.py               # Aplikasi web multi-halaman Streamlit
│   │   └── styles.css                     # Stylesheet tampilan UI RuangRasa
│   ├── notebooks/
│   │   ├── 01_persiapan_data.ipynb        # Tahap 1: Pembacaan data & partisi 80:20
│   │   ├── 02_eksplorasi_data.ipynb       # Tahap 2: Statistik deskriptif & 6 plot EDA
│   │   ├── 03_preprocessing.ipynb         # Tahap 3: Pipeline imputasi & One-Hot Encoding
│   │   ├── 04_training_model.ipynb        # Tahap 4: Pelatihan 3 model & CV tuning
│   │   └── 05_evaluasi_dan_ekspor.ipynb   # Tahap 5: Evaluasi test set & ekspor artefak
│   ├── reports/
│   │   ├── eda/                           # Grafik dan laporan CSV hasil EDA
│   │   ├── modeling/                      # Matriks konfusi, kurva & laporan metrik
│   │   └── analysis/                      # Permutation importance & analisis bobot
│   ├── tests/
│   │   └── test_project.py                # Unit test data, validasi, dan inferensi
│   ├── create_split_notebooks.py          # Generator 5 file notebook berurutan
│   ├── run_split_notebooks.py             # Eksekutor 5 notebook pada kernel mandiri
│   ├── depresi_project.py                 # Kontrak fitur, validasi & preprocessing
│   ├── train.py                           # Skrip pelatihan end-to-end mandiri
│   ├── generate_docx.py                   # Generator dokumen Word laporan akademik
│   └── run_tests.py                       # Runner automated unit testing
├── Video_Demo/
│   └── storyboard_dan_naskah_video.md     # Naskah video demo & panduan rekaman (≤ 7 mnt)
├── JALANKAN_APLIKASI.bat                  # Script klik ganda peluncur aplikasi Windows
├── PJBL-KETENTUAN.txt                     # Salinan panduan dan rubrik penilaian PJBL
├── requirements.txt                       # Daftar dependensi modul Python
└── README.md                              # Dokumentasi utama proyek ini
```

---

## 🚀 Panduan Menjalankan Proyek Secara Mandiri

### 1. Prasyarat Lingkungan
Pastikan Anda menggunakan Python 3.10, 3.11, atau 3.12:
```bash
python --version
```

### 2. Instalasi Dependensi
```bash
pip install -r requirements.txt
```

### 3. Melatih Ulang Model & Memperbarui Artefak
```bash
python Source_Code/train.py
```

### 4. Menjalankan 5 Jupyter Notebook Secara Otomatis
```bash
python Source_Code/run_split_notebooks.py
```

### 5. Menjalankan Unit Testing Otomatis (100% Passed)
```bash
python Source_Code/run_tests.py
```

### 6. Meluncurkan Aplikasi Web Streamlit
**Cara 1 (Windows One-Click):**
Klik ganda pada file `JALANKAN_APLIKASI.bat`.

**Cara 2 (Command Line):**
```bash
python -m streamlit run Source_Code/app/streamlit_app.py
```
Buka browser pada alamat: `http://localhost:8501`.

---

## 📚 Referensi Jurnal Ilmiah (DOI Terverifikasi: Dasar PHQ-9 + 5 Jurnal 2024–2026)

1. **Kroenke, K., Spitzer, R. L., & Williams, J. B. (2001).** *The PHQ-9: Validity of a Brief Depression Severity Measure.* Journal of General Internal Medicine, 16(9), 606–613.  
   DOI: [10.1046/j.1525-1497.2001.016009606.x](https://doi.org/10.1046/j.1525-1497.2001.016009606.x)
2. **Li, E., Ai, F., & Liang, C. (2024).** *A machine learning model to predict the risk of depression in US adults with obstructive sleep apnea hypopnea syndrome: a cross-sectional study.* Frontiers in Public Health, 11, 1348803.  
   DOI: [10.3389/fpubh.2023.1348803](https://doi.org/10.3389/fpubh.2023.1348803)
3. **Selvaraj, A., & Mohandoss, L. (2024).** *Enhancing Depression Detection: A Stacked Ensemble Model with Feature Selection and RF Feature Importance Analysis Using NHANES Data.* Applied Sciences.  
   DOI: [10.3390/app14167366](https://doi.org/10.3390/app14167366)
4. **Vu, T., Dawadi, R., Yamamoto, M., Tay, J. T., Watanabe, N., Kuriya, Y., Oya, A., Tran, P. N. H., & Araki, M. (2025).** *Prediction of depressive disorder using machine learning approaches: findings from the NHANES.* BMC Medical Informatics and Decision Making.  
   DOI: [10.1186/s12911-025-02903-1](https://doi.org/10.1186/s12911-025-02903-1)
5. **Salimi, O., Ghahramani, Z., Taghavi Zenouz, M., et al. (2026).** *Interpretable machine learning for depression symptom classification in NHANES: Performance in a curated high-confidence corpus and the full survey population.* IBRO Neuroscience Reports, 21, 738–746.  
   DOI: [10.1016/j.ibneur.2026.08.009](https://doi.org/10.1016/j.ibneur.2026.08.009)
6. **Cui, M., Li, X., & Gong, W. (2026).** *An Interpretable Stacking Ensemble Model with SHAP for Geriatric Depression Prediction: Analysis of the NHANES 2005-2023 Database.* EAI Endorsed Transactions on Pervasive Health and Technology, Vol. 11.  
   DOI: [10.4108/eetpht.11.11671](https://doi.org/10.4108/eetpht.11.11671)

---

## 👥 Identitas Anggota Kelompok — Kelompok 11

| No. | Nama Mahasiswa | NIM | Pembagian Tugas |
|:---:|---|---|---|
| 1 | **Bintang Karini Br Padang** | J0404241005 | Modeling dan evaluasi |
| 2 | **Binggie Rashel Prasetyo** | J0404241009 | Dataset, EDA, dan preprocessing |
| 3 | **Gregorius Gil Ovidio Sebayang** | J0404241088 | Implementasi aplikasi dan deployment |

- **Kelompok:** Kelompok 11
- **Mata Kuliah:** Machine Learning (Semester 5)

---

## ⚠️ Pernyataan Etika & Batasan Medis Klinis (*Disclaimer*)
Aplikasi **RuangRasa** dikembangkan murni untuk keperluan **penelitian akademis, edukasi, dan skrining awal risiko depresi**. Aplikasi ini **bukan merupakan alat diagnosis medis resmi** dan tidak dimaksudkan untuk menggantikan konsultasi langsung dengan dokter spesialis kedokteran jiwa (psikiater) atau psikolog klinis berlisensi.
