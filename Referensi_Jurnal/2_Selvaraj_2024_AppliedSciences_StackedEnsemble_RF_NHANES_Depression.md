# Ringkasan Artikel Jurnal Ilmiah 2

- **Judul Artikel:** Enhancing Depression Detection: A Stacked Ensemble Model with Feature Selection and RF Feature Importance Analysis Using NHANES Data
- **Penulis:** Annapoorani Selvaraj, L. Mohandoss
- **Tahun Publikasi:** 2024
- **Nama Jurnal:** *Applied Sciences*
- **DOI:** [10.3390/app14167366](https://doi.org/10.3390/app14167366)

---

### 1. Masalah Penelitian
Meningkatkan performa deteksi depresi pada data survei kesehatan populasi **NHANES** yang memiliki ketidakseimbangan kelas signifikan (~8,08% kasus depresi) serta memilih fitur yang paling informatif.

### 2. Dataset & Responden
Dataset **CDC NHANES** siklus 2015–2016 dengan distribusi kelas tidak seimbang (~8,08% responden terdiagnosis depresi).

### 3. Metode & Algoritma
Mengembangkan model *stacked ensemble* (*Depression Ensemble Stacking Generalization Model* / DESGM) yang dipadukan dengan seleksi fitur dan analisis *Random Forest Feature Importance*.

### 4. Metrik & Hasil Utama
- **Accuracy:** 98,17%
- **F1-Score:** 0,9904
- Membuktikan bahwa metode berbasis *ensemble* dan analisis tingkat kepentingan fitur *Random Forest* efektif mengidentifikasi variabel kunci pada data NHANES.

### 5. Kontribusi terhadap Proyek RuangRasa
- Menunjukkan kesesuaian penggunaan **Random Forest** dan analisis *feature importance* pada dataset NHANES yang tidak seimbang (~8,74% kelas `Depressed` pada proyek RuangRasa).
