# Ringkasan Artikel Jurnal Ilmiah 4

- **Judul Artikel:** Prediction of depressive disorder using machine learning approaches: findings from the NHANES
- **Penulis:** Thien Vu, Research Dawadi, Masaki Yamamoto, Jie Ting Tay, Naoki Watanabe, Yuki Kuriya, Ai Oya, Phap Ngoc Hoang Tran, Michihiro Araki
- **Tahun Publikasi:** 2025
- **Nama Jurnal:** *BMC Medical Informatics and Decision Making*
- **DOI:** [10.1186/s12911-025-02903-1](https://doi.org/10.1186/s12911-025-02903-1)

---

### 1. Masalah Penelitian
Membandingkan beberapa algoritma pembelajaran mesin terawasi untuk memprediksi gangguan depresi dari data survei kesehatan publik tanpa bergantung pada metode statistik tradisional semata.

### 2. Dataset & Responden
Dataset **CDC NHANES 2013–2014** dengan target depresi sedang–berat berdasarkan skor **PHQ-9 ≥ 10**, dibagi menjadi **80% data latih dan 20% data uji**.

### 3. Metode & Algoritma
Membandingkan enam algoritma *supervised learning*: **Logistic Regression**, **Random Forest**, **Naive Bayes**, **Support Vector Machine (SVM)**, **XGBoost**, dan **LightGBM**, dilengkapi interpretasi **SHAP**.

### 4. Metrik & Hasil Utama
- Dievaluasi menggunakan *Accuracy*, *Sensitivity*, *Specificity*, *Precision*, *AUC*, dan *F1-Score*.
- **XGBoost** mencapai skor tertinggi secara keseluruhan pada *Accuracy*, *AUC*, dan *F1-Score*.
- Analisis SHAP mengidentifikasi faktor dominan seperti rasio pendapatan terhadap kemiskinan, jenis kelamin, hipertensi, BMI, tingkat pendidikan, serta penanda paparan rokok.

### 5. Kontribusi terhadap Proyek RuangRasa
- Menjadi acuan langsung skema partisi **80:20**, pembandingan **Logistic Regression** dan **Random Forest**, serta penggunaan fitur demografi, tekanan darah, BMI, pendapatan, dan merokok dari data NHANES dengan label PHQ-9 ≥ 10.
