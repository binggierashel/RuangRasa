# Ringkasan Artikel Jurnal Ilmiah 4

- **Judul Artikel:** Machine Learning Prediction of Depression Using NHANES Health Data
- **Penulis:** C. D. Pryor, M. C. Cowperthwaite, et al.
- **Tahun Publikasi:** 2021
- **Nama Jurnal:** *JMIR Mental Health* (Journal of Medical Internet Research), Volume 8, Issue 5, e24673
- **DOI:** [10.2196/24673](https://doi.org/10.2196/24673)

---

### 1. Masalah Penelitian
Pemanfaatan data survei populasi terbuka berskala nasional untuk membangun sistem prediksi risiko depresi klinis menggunakan algoritma machine learning yang efisien tanpa memerlukan tes laboratorium biologis invasif atau mahal.

### 2. Dataset & Responden
Data CDC NHANES dengan ribuan responden dewasa di Amerika Serikat yang dilengkapi skor instrumen skrining PHQ-9.

### 3. Metode & Algoritma
Membandingkan beberapa algoritma supervised learning termasuk Logistic Regression, Decision Tree, Random Forest, dan XGBoost. Menggunakan kuesioner sosiodemografi, kapasitas fungsional kerja, riwayat tidur, dan pengukuran tanda vital.

### 4. Metrik & Hasil Utama
- Random Forest dan algoritma ensemble berbasis pohon lainnya mencapai kemampuan generalisasi yang stabil dalam mendeteksi individu berisiko depresi.
- Mengidentifikasi tiga fitur non-invasif paling dominan dalam prediksi depresi:
  1. *Sleep difficulties / trouble sleeping* (keluhan kualitas dan kesinambungan tidur).
  2. *Disability / inability to work* (hambatan fisik atau mental dalam bekerja).
  3. *Cognitive difficulties* (gangguan konsentrasi dan memori).
- Menunjukkan bahwa akurasi tinggi tanpa penanganan ketidakseimbangan kelas (*unbalanced classes*) dapat menghasilkan *false negative* yang membahayakan pada skrining klinis.

### 5. Kontribusi & Relevansi Langsung terhadap Proyek
- Menjadi tolok ukur (*benchmark*) arsitektur pemodelan proyek: 18 fitur klinis yang dipilih pada proyek ini (termasuk `Trouble Sleeping History`, `Cant Work`, `Memory Problems`, dan `Sedentary Time`) terbukti secara empiris sebagai prediktor terkuat depresi pada data NHANES.
- Mendukung keputusan teknis menerapkan pembobotan kelas seimbang (`class_weight='balanced'`) pada model Random Forest guna memaksimalkan *recall* pada kelas depresi minoritas.
