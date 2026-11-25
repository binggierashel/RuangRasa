# Ringkasan Artikel Jurnal Ilmiah 4

- **Judul Artikel:** Interpretable machine learning for depression symptom classification in NHANES: Performance in a curated high-confidence corpus and the full survey population
- **Penulis:** Omid Salimi, Zahra Ghahramani, Mahsa Taghavi Zenouz, Marziyeh Heidari, Alireza Amini, Fatemeh Nouroozi, Mobina Fathi, Arian Tavasol, Mohammad Reza Bateni
- **Tahun Publikasi:** 2026
- **Nama Jurnal:** *IBRO Neuroscience Reports*, Volume 21, Halaman 738–746
- **DOI:** [10.1016/j.ibneur.2026.08.009](https://doi.org/10.1016/j.ibneur.2026.08.009)

---

### 1. Masalah Penelitian
Mengevaluasi perbedaan performa dan keterbacaan (*interpretability*) model pembelajaran mesin untuk klasifikasi gejala depresi antara korpus terkurasi seimbang dan populasi survei penuh NHANES yang sangat tidak seimbang.

### 2. Dataset & Responden
Sebanyak **37.959 partisipan CDC NHANES** dengan skor **PHQ-9** yang valid (ambang batas gejala ringan–berat PHQ-9 ≥ 5) beserta variabel demografi, pola makan, dan tidur.

### 3. Metode & Algoritma
Membandingkan **LightGBM**, **XGBoost**, **Logistic Regression**, **Random Forest**, dan **SVM** disertai analisis interpretabilitas berbasis **SHAP**.

### 4. Metrik & Hasil Utama
- Menemukan bahwa keluhan tidur (*self-reported trouble sleeping*) merupakan fitur kontributor paling dominan dalam klasifikasi gejala depresi.
- Menunjukkan bahwa performa pada korpus terkurasi jauh lebih tinggi dibandingkan populasi penuh, di mana model populasi penuh memiliki presisi dan kalibrasi yang lebih moderat akibat ketidakseimbangan dan heterogenitas data nyata.

### 5. Kontribusi terhadap Proyek RuangRasa
- Memberikan landasan empiris mengapa nilai *Macro-F1* pada data NHANES populasi penuh (36.259 responden di RuangRasa) berada di kisaran moderat (~0,64) dan memvalidasi temuan *Permutation Importance* bahwa `Trouble Sleeping History` adalah fitur paling berpengaruh.
