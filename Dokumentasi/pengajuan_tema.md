# Formulir Pengajuan Tema & Rencana Proyek Pembelajaran Berbasis Proyek (PJBL)
## Mata Kuliah: Machine Learning (Semester 5)

---

### I. Informasi Umum Proyek
- **Judul Proyek:** Sistem Klasifikasi dan Skrining Risiko Gangguan Depresi Mayor Menggunakan Pendekatan Machine Learning Berbasis Data CDC NHANES
- **Tema Bidang:** Kesehatan Mental, Biomedis, dan Kebiasaan Gaya Hidup (*Mental Health & Clinical Lifestyle Analytics*)
- **Target Variabel:** `Depression` (Klasifikasi Biner: `Not Depressed` vs `Depressed`)
- **Standar Label Klinis:** Patient Health Questionnaire-9 (PHQ-9) dengan batas skor $\ge 10$ mengindikasikan risiko depresi klinis mayor (*moderate-to-severe depression*) berdasarkan validasi Kroenke et al. (2001).
- **Dataset Acuan:** Centers for Disease Control and Prevention (CDC) - *National Health and Nutrition Examination Survey* (NHANES) siklus 2005–2018 (36.259 responden unik).

---

### II. Latar Belakang & Urgensi
Gangguan depresi mayor (*Major Depressive Disorder* / MDD) adalah salah satu penyebab utama disabilitas dan beban penyakit global (*Global Burden of Disease*). Menurut World Health Organization (WHO), lebih dari 280 juta orang di seluruh dunia hidup dengan depresi. Depresi tidak hanya mengganggu suasana hati, tetapi juga berdampak langsung pada produktivitas harian, kualitas tidur, kapasitas kognitif, hingga memicu risiko bunuh diri.

Tantangan utama penanganan depresi terletak pada rendahnya angka deteksi dini. Banyak penderita tidak menyadari gejala awal atau enggan mencari pertolongan medis karena stigma sosial. Di sisi lain, dokter pada fasilitas layanan primer sering kali tidak memiliki waktu memadai untuk melakukan wawancara diagnostik psikiatri lengkap.

Oleh karena itu, pemanfaatan teknik *Machine Learning* untuk mengidentifikasi pola multivariat dari data kesehatan rutin (demografi, riwayat tidur, aktivitas fisik harian, status disabilitas kerja, kognisi, dan tanda vital) menjadi solusi inovatif sebagai sistem skrining awal (*early screening tool*) yang cepat, objektif, dan terukur.

---

### III. Rumusan Masalah
1. Bagaimana merancang pipeline *Machine Learning* yang mampu mengklasifikasikan risiko depresi mayor secara akurat dari data survei klinis terstruktur CDC NHANES?
2. Bagaimana perbandingan performa antara tiga algoritma klasifikasi—yaitu **Random Forest**, **Logistic Regression**, dan **Decision Tree**—khususnya dalam mengatasi ketidakseimbangan kelas (*class imbalance*)?
3. Faktor atau fitur kesehatan apa yang paling dominan mempengaruhi probabilitas risiko depresi berdasarkan teknik interpretasi model (*permutation feature importance* & koefisien logit)?
4. Bagaimana mengemas model machine learning terpilih ke dalam aplikasi berbasis web (Streamlit) yang interaktif, mudah digunakan tenaga kesehatan maupun masyarakat, dan dilengkapi validasi input yang ketat?

---

### IV. Tujuan Proyek
1. Mengembangkan pipeline prapemrosesan data yang terhindar dari *data leakage* menggunakan standardisasi numerik, imputasi median/modus, dan *One-Hot Encoding*.
2. Membandingkan kinerja tiga algoritma klasifikasi secara objektif menggunakan *5-Fold Stratified Cross-Validation* pada data latih dengan metrik acuan **Macro-F1**.
3. Menganalisis faktor-faktor risiko kunci penyebab depresi untuk menghasilkan interpretasi ilmiah (*explainable AI*) yang selaras dengan literatur kedokteran psikiatri.
4. Menyediakan aplikasi inferensi interaktif berbasis Streamlit yang mendukung prediksi individu (skrining mandiri) dan prediksi massal (*batch processing* file CSV).

---

### V. Ruang Lingkup & Metodologi
1. **Data:** 36.259 baris data riil tanpa duplikasi dari survei CDC NHANES, terdiri dari 18 fitur prediktor (7 numerik, 11 kategorikal) dan 1 kolom target biner.
2. **Partisi Data:** 80% Data Latih (29.007 responden) dan 20% Data Uji Holdout (7.252 responden) dipartisi secara berstrata (*stratified*).
3. **Optimasi Model:** Hyperparameter tuning dilakukan secara sistematis via `GridSearchCV` hanya pada data latih melalui 5-Fold Stratified Cross-Validation (`random_state=43`).
4. **Kunci Pemilihan:** Model terbaik dipilih murni berdasarkan rata-rata skor *Validation Macro-F1* tertinggi sebelum menyentuh data uji holdout.
5. **Implementasi Aplikasi:** Antarmuka web dibangun menggunakan Streamlit dengan 5 modul: Prediksi Individu, Prediksi Batch CSV, Eksplorasi Data (EDA), Evaluasi & Komparasi Model, serta Informasi Proyek & Tim.
6. **Batasan Etika & Klinis:** Aplikasi dirancang untuk tujuan edukatif dan skrining awal, **bukan pengganti diagnosis klinis resmi oleh psikiater atau dokter spesialis kedokteran jiwa**.

---

### VI. Luaran yang Dihasilkan
1. **5 Notebook Jupyter Terpisah (Sequential):**
   - `01_persiapan_data.ipynb`
   - `02_eksplorasi_data.ipynb`
   - `03_preprocessing.ipynb`
   - `04_training_model.ipynb`
   - `05_evaluasi_dan_ekspor.ipynb`
2. **Artefak Model Terlatih:** Format `.joblib` untuk 3 pipeline algoritma, skema input JSON, dan metadata model lengkap.
3. **Aplikasi Web Interaktif:** Streamlit Dashboard dengan kustomisasi CSS, validasi input, visualisasi probabilitas, dan fitur unduh hasil inferensi CSV.
4. **Laporan Akademik & Dokumentasi:** Laporan lengkap format Markdown dan Word (`.docx`), kamus data, metodologi, dan review 5 jurnal terindeks dengan DOI aktif.
5. **Pengujian Otomatis:** Script unit testing dan integritas pipeline (`test_project.py` dan `run_tests.py`) dengan tingkat kelulusan 100%.
