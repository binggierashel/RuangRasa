# Ringkasan Artikel Jurnal Ilmiah 2

- **Judul Artikel:** Fusing Data Mining, Machine Learning and Traditional Statistics to Detect Biomarkers Associated with Depression
- **Penulis:** Joanna F. Dipnall, Julie A. Pasco, Michael Berk, Lana J. Williams, Seetal Dodd, Felice N. Jacka, Denny Meyer
- **Tahun Publikasi:** 2016
- **Nama Jurnal:** *PLOS ONE*, Volume 11, Issue 2, e0148195
- **DOI:** [10.1371/journal.pone.0148195](https://doi.org/10.1371/journal.pone.0148195)

---

### 1. Masalah Penelitian
Kompleksitas etiologi depresi yang melibatkan interaksi multivariat antara faktor gaya hidup, biomarker metabolik, inflamasi, dan demografi sering kali sulit dimodelkan secara komprehensif menggunakan analisis regresi linear univariat tradisional.

### 2. Dataset & Responden
Menggunakan dataset **CDC NHANES** (National Health and Nutrition Examination Survey) siklus 2007–2008 dan 2009–2010, mencakup ribuan responden dewasa di Amerika Serikat yang dinilai status depresinya menggunakan kuesioner PHQ-9.

### 3. Metode & Pendekatan Machine Learning
Menerapkan pendekatan hibrida menggabungkan pemodelan data mining, *ensemble tree-based machine learning*, dan *Generalized Additive Models* (GAM) untuk menyeleksi dan mendeteksi prediktor paling signifikan terhadap gejala depresi.

### 4. Metrik & Hasil Utama
- Mengidentifikasi kelompok variabel gaya hidup dan fisik—khususnya pola tidur terganggu, parameter waktu duduk/sedentari, indeks massa tubuh (BMI), dan status merokok—sebagai faktor penjelas kuat terhadap risiko depresi mayor.
- Model berbasis tree ensemble menunjukkan keunggulan dibandingkan analisis linier standar dalam menangkap hubungan non-linear dan interaksi multivariat antarfitur biologis.

### 5. Kontribusi & Relevansi Langsung terhadap Proyek
- Menjustifikasi pemanfaatan survei kesehatan publik berskala besar **CDC NHANES** sebagai sumber data primer berkualitas tinggi untuk pemodelan machine learning depresi.
- Mengonfirmasi pemilihan variabel prediktor klinis yang digunakan dalam proyek ini: durasi tidur (`Sleep Hours`), riwayat keluhan tidur (`Trouble Sleeping History`), tingkat sedentari (`Sedentary Time`), dan kebiasaan merokok (`Current Smoker`).
