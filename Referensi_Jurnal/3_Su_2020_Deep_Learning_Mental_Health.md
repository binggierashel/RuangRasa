# Ringkasan Artikel Jurnal Ilmiah 3

- **Judul Artikel:** Deep Learning in Mental Health: A Systematic Review
- **Penulis:** Chang Su, Zhenxing Xu, Jyotishman Pathak, Fei Wang
- **Tahun Publikasi:** 2020
- **Nama Jurnal:** *JAMA Network Open*, Volume 3, Issue 11, Halaman e2026414
- **DOI:** [10.1001/jamanetworkopen.2020.26414](https://doi.org/10.1001/jamanetworkopen.2020.26414)

---

### 1. Masalah Penelitian
Menilai secara sistematis efektivitas, validitas metodologi, risiko kebocoran data (*data leakage*), dan tantangan interpretasi dari berbagai model machine learning dan deep learning dalam memprediksi gangguan kesehatan mental (khususnya depresi dan gangguan kecemasan).

### 2. Dataset & Metodologi Tinjauan
Tinjauan sistematis terhadap studi-studi kesehatan mental komputasional yang dipublikasikan secara global, mencakup ratusan ribu rekam medis elektronik (*Electronic Health Records* / EHR) dan data survei populasi terstruktur.

### 3. Temuan Metodologis Kunci
- Pada data tabular terstruktur dan survei kesehatan epidemiologi, model *tree ensemble* (seperti Random Forest dan Gradient Boosting) serta regresi berbobot (*penalized/weighted logistic regression*) sering kali memberikan performa yang setara atau bahkan lebih unggul daripada arsitektur jaringan saraf dalam (*deep neural networks*).
- Menekankan risiko fatal *over-optimistic performance* apabila validasi model tidak menerapkan partisi holdout yang ketat dan *cross-validation* berstrata pada data yang memiliki ketidakseimbangan kelas (*class imbalance*).
- Menyoroti keharusan pelaporan metrik komprehensif (Macro-F1, Precision, Recall) bukan hanya akurasi mentah (*raw accuracy*) yang bias terhadap kelas mayoritas.

### 4. Kontribusi & Relevansi Langsung terhadap Proyek
- Menjadi landasan kuat dalam perancangan arsitektur metodologi: pembagian 80:20 berstrata, 5-Fold Stratified Cross-Validation pada data latih, dan penguncian model berbasis **Macro-F1**.
- Memberikan justifikasi akademis mengapa Random Forest dan Logistic Regression diikutsertakan sebagai algoritma komparasi utama dalam proyek skrining risiko depresi ini.
