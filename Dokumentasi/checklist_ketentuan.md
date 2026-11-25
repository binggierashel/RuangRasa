# Lembar Pemeriksaan Pemenuhan Ketentuan PJBL (Checklist Rubrik)
## Proyek: Sistem Skrining Risiko Gangguan Depresi Mayor (CDC NHANES)

Dokumen ini memetakan setiap butir persyaratan dalam panduan resmi `PJBL-KETENTUAN.txt` terhadap realisasi implementasi pada repositori proyek ini.

---

### I. Pemenuhan Ketentuan Umum & Struktur Tim (Bobot 5%)

| Butir Ketentuan Panduan | Status | Realisasi dalam Proyek | Bukti File / Lokasi |
|---|:---:|---|---|
| Kelompok beranggotakan 3–4 orang dengan pembagian tugas terdefinisi | **TERPENUHI** | Struktur pembagian tugas dibuat sistematis mencakup Data Engineering, Model Tuning, App Developer, dan Academic Documentation. | `Dokumentasi/identitas_kelompok.json` |
| Seluruh anggota memahami konsep, dataset, algoritma, dan alur aplikasi | **TERPENUHI** | Dokumentasi lengkap dari teori medis PHQ-9, metrik Macro-F1, hingga arsitektur pipeline disediakan dalam laporan dan kamus data. | `Dokumentasi/laporan_project.md`<br>`Dokumentasi/kamus_data.md` |

---

### II. Pengajuan Tema & Tinjauan Pustaka (Bobot 10%)

| Butir Ketentuan Panduan | Status | Realisasi dalam Proyek | Bukti File / Lokasi |
|---|:---:|---|---|
| Tema permasalahan nyata berbasis data terukur (*Classification*) | **TERPENUHI** | Klasifikasi risiko depresi mayor (Biner: `Not Depressed` vs `Depressed`). | `Dokumentasi/pengajuan_tema.md` |
| Minimal 5 artikel jurnal ilmiah relevan dengan DOI aktif | **TERPENUHI** | Landasan PHQ-9 (Kroenke 2001) + 5 jurnal terbitan 5 tahun terakhir (Li 2024, Selvaraj 2024, Vu 2025, Salimi 2026, Cui 2026) dengan DOI terverifikasi. | Folder `Referensi_Jurnal/` |
| Tabel studi literatur komparatif (Penulis, Masalah, Dataset, Metode, Metrik, Hasil, Perbedaan) | **TERPENUHI** | Dibuat tabel matriks perbandingan komprehensif mengacu format rubrik ketentuan. | `Referensi_Jurnal/tinjauan_pustaka.md` |

---

### III. Dataset, EDA, dan Preprocessing Data (Bobot 15%)

| Butir Ketentuan Panduan | Status | Realisasi dalam Proyek | Bukti File / Lokasi |
|---|:---:|---|---|
| Dataset memiliki sumber terbuka dan legal yang jelas | **TERPENUHI** | CDC NHANES (National Health and Nutrition Examination Survey) 2005–2018 (36.259 responden riil). | `Dataset/Data_Asli/provenance.json` |
| Penjelasan lengkap fitur, tipe data, target, outlier, missing value | **TERPENUHI** | Kamus data 18 fitur klinis + 1 target biner dijelaskan secara detail beserta satuan dan makna klinisnya. | `Dokumentasi/kamus_data.md`<br>`Source_Code/reports/eda/` |
| Minimal 6 jenis visualisasi EDA dengan penjelasan naratif | **TERPENUHI** | Dihasilkan 6 visualisasi: (1) Distribusi Kelas, (2) Histogram Numerik, (3) Boxplot Outlier, (4) Matriks Korelasi, (5) Bar Kategori Kunci, (6) Scatter Usia vs Jam Tidur. | `Source_Code/reports/eda/01_*.png` s/d `06_*.png` |
| Preprocessing bebas kebocoran data (*zero data leakage*) | **TERPENUHI** | Data dipartisi 80:20 berstrata sebelum transformasi. Imputer dan Scaler hanya di-fit pada data latih di dalam Scikit-Learn `Pipeline`. | `Source_Code/depresi_project.py`<br>`Source_Code/train.py` |

---

### IV. Pengembangan & Tuning Model Machine Learning (Bobot 20%)

| Butir Ketentuan Panduan | Status | Realisasi dalam Proyek | Bukti File / Lokasi |
|---|:---:|---|---|
| Minimal 3 algoritma Machine Learning dikomparasikan | **TERPENUHI** | 3 Algoritma dievaluasi: **Random Forest**, **Logistic Regression**, dan **Decision Tree**. | `Source_Code/train.py` |
| Alasan pemilihan algoritma jelas dan berbasis literatur | **TERPENUHI** | Regresi logistik sebagai baseline probabilistik linear, Decision Tree sebagai pohon keputusan interpretable, dan Random Forest sebagai ensemble bagging anti-overfitting. | `Dokumentasi/metodologi.md` |
| Pembagian Data Latih dan Uji (80:20) berstrata | **TERPENUHI** | 29.007 data latih dan 7.252 data uji holdout dipartisi menggunakan `StratifiedKFold` (`random_state=42`). | `Dataset/Data_Olahan/train.csv`<br>`Dataset/Data_Olahan/test.csv` |
| Hyperparameter tuning sistematis (K-Fold CV) | **TERPENUHI** | Tuning dilakukan via `GridSearchCV` 5-Fold Stratified Cross-Validation pada data latih dengan metrik optimasi `f1_macro`. | `Source_Code/reports/modeling/cv_results_*.csv` |

---

### V. Evaluasi & Analisis Mendalam Model (Bobot 20%)

| Butir Ketentuan Panduan | Status | Realisasi dalam Proyek | Bukti File / Lokasi |
|---|:---:|---|---|
| Metrik evaluasi lengkap (Accuracy, Precision, Recall, F1-Score, Confusion Matrix) | **TERPENUHI** | Evaluasi komparatif mencakup Macro-Precision, Macro-Recall, Macro-F1, Akurasi, dan Confusion Matrix untuk seluruh algoritma. | `Source_Code/reports/modeling/model_comparison.csv` |
| Pemilihan model terbaik berbasis bukti evaluasi | **TERPENUHI** | **Random Forest** dipilih karena meraih rerata CV Macro-F1 tertinggi pada data latih (0,6428 ± 0,0076) dan Test Macro-F1 (0,6356). | `Model/model_metadata.json` |
| Analisis komparatif, overfitting/underfitting, dan error prediction | **TERPENUHI** | Analisis generalisasi (Train vs CV vs Test), selisih gap overfit, serta identifikasi baris kesalahan prediksi model diekspor. | `Source_Code/reports/modeling/errors_*.csv`<br>`Source_Code/reports/analysis/` |
| Analisis faktor/fitur berpengaruh (*Feature Importance*) | **TERPENUHI** | *Permutation Feature Importance* (Random Forest) dan analisis koefisien logit (Logistic Regression) mengonfirmasi pentingnya insomnia dan disabilitas kerja. | `Source_Code/reports/analysis/permutation_importance_train.csv` |

---

### VI. Implementasi Aplikasi & Pengujian (Bobot 20%)

| Butir Ketentuan Panduan | Status | Realisasi dalam Proyek | Bukti File / Lokasi |
|---|:---:|---|---|
| Aplikasi antarmuka pengguna interaktif (Streamlit) | **TERPENUHI** | Aplikasi web 5 modul lengkap dengan styling kustom (`styles.css`), tombol profil demo, visualisasi probabilitas, dan responsif. | `Source_Code/app/streamlit_app.py` |
| Fitur Input Lengkap (Input Tunggal & Batch CSV) | **TERPENUHI** | Mendukung formulir skrining individu dan unggah berkas CSV massal disertai template unduhan. | Tab Prediksi Individu & Batch |
| Validasi Input Ketat | **TERPENUHI** | Memvalidasi tipe numerik, rentang biometrik logis (Sistolik > Diastolik), serta pencegahan nilai anomali. | `Source_Code/depresi_project.py` (`validate_input`) |
| Source code terstruktur rapi dan dapat direproduksi | **TERPENUHI** | 5 Jupyter Notebook berurutan dengan output riil, script Python modular, dan runner eksekusi otomatis. | `Source_Code/notebooks/`<br>`Source_Code/run_split_notebooks.py` |
| Unit Testing & Integritas Pipeline | **TERPENUHI** | Script automated testing komprehensif menguji skema, data, validasi, dan prediksi pipeline dengan kelulusan 100%. | `Source_Code/tests/test_project.py`<br>`Source_Code/run_tests.py` |
| Kemudahan Menjalankan Aplikasi (*One-Click Run*) | **TERPENUHI** | Disediakan script batch Windows untuk langsung meluncurkan Streamlit via klik ganda. | `JALANKAN_APLIKASI.bat` |

---

### VII. Video Demo & Dokumentasi Akhir (Bobot 10%)

| Butir Ketentuan Panduan | Status | Realisasi dalam Proyek | Bukti File / Lokasi |
|---|:---:|---|---|
| Panduan / Storyboard Video Demo durasi $\le 7$ menit | **TERPENUHI** | Disediakan naskah narasi per menit, alur demonstrasi layar, dan petunjuk teknis perekaman lengkap. | `Video_Demo/storyboard_dan_naskah_video.md` |
| Laporan Proyek Lengkap (Markdown & Word `.docx`) | **TERPENUHI** | Laporan akademis komprehensif mencakup Bab I Pendahuluan hingga Bab V Penutup dan Daftar Pustaka. | `Dokumentasi/laporan_project.md`<br>`Dokumentasi/laporan_project.docx` |
