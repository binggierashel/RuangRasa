# Ringkasan Artikel Jurnal Ilmiah 6

- **Judul Artikel:** An Interpretable Stacking Ensemble Model with SHAP for Geriatric Depression Prediction: Analysis of the NHANES 2005-2023 Database
- **Penulis:** Manman Cui, Xian Li, Wei Gong
- **Tahun Publikasi:** 2026
- **Nama Jurnal:** *EAI Endorsed Transactions on Pervasive Health and Technology*, Volume 11
- **DOI:** [10.4108/eetpht.11.11671](https://doi.org/10.4108/eetpht.11.11671)

---

### 1. Masalah Penelitian
Membangun model prediksi depresi yang akurat sekaligus transparan secara klinis pada data survei NHANES multi-siklus yang memiliki ketidakseimbangan kelas berat.

### 2. Dataset & Responden
Data **CDC NHANES siklus 2005–2023** dengan sampel **8.760 partisipan** berusia ≥ 65 tahun dan target depresi berbasis **PHQ-9 ≥ 10**.

### 3. Metode & Algoritma
Menggunakan normalisasi data, kombinasi penyeimbangan kelas **SMOTE + Random Under-Sampling (RUS)**, seleksi fitur **RFE-RF**, serta model **Stacking Ensemble** (menggabungkan Random Forest, XGBoost, SVM, dan Logistic Regression) dan interpretasi **SHAP**.

### 4. Hasil Utama
Model *stacking ensemble* yang dipadukan dengan SHAP meningkatkan kinerja prediksi sekaligus transparansi faktor risiko, sehingga membantu identifikasi awal individu berisiko depresi.

### 5. Kontribusi terhadap Proyek RuangRasa
- Menguatkan pendekatan multi-siklus NHANES (2005–2018 pada RuangRasa) dengan label PHQ-9 ≥ 10, penanganan *class imbalance*, dan penyajian interpretasi fitur agar hasil model mudah dijelaskan kepada pengguna.
