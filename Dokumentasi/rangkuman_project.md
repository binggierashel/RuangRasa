# Rangkuman Proyek: Klasifikasi Risiko Gangguan Depresi Menggunakan Machine Learning

---

## 1. Latar Belakang
- **Urgensi Kesehatan Mental:** Menurut data *World Health Organization* (WHO), lebih dari 280 juta penduduk dunia mengalami gangguan depresi mayor yang mengganggu fungsi kognitif, ritme tidur, produktivitas kerja, serta meningkatkan risiko bunuh diri.
- **Keterbatasan Layanan Kesehatan Primer:** Di fasilitas kesehatan umum, lebih dari 50% kasus depresi gagal terdeteksi sejak dini akibat sempitnya durasi konsultasi medis (10–15 menit) dan keterbatasan pelatihan wawancara psikiatris khusus.
- **Solusi Pendukung Keputusan Klinis:** Pemanfaatan *Machine Learning* memungkinkan skrining risiko depresi secara cepat, objektif, dan non-invasif (tanpa tes darah atau laboratorium mahal) dengan memanfaatkan data gaya hidup, demografi, riwayat tidur, kapasitas kerja, dan tanda vital tubuh.

---

## 2. Data yang Digunakan
- **Sumber Data:** Survei kesehatan nasional terbuka **CDC NHANES** (*National Health and Nutrition Examination Survey*) periode **2005–2018** (7 siklus dua tahunan: Siklus D hingga Siklus J).
- **Alasan Pemilihan Rentang 2005–2018:**
  1. Kuesioner skrining depresi standar **PHQ-9** (*Patient Health Questionnaire-9*) baru diadopsi secara lengkap oleh CDC NHANES mulai siklus **2005–2006**.
  2. Siklus **2017–2018** merupakan siklus penuh terakhir sebelum survei lapangan terganggu akibat pandemi COVID-19 pada awal 2020.
- **Jumlah Sampel & Distribusi Kelas:** Total **36.259 responden unik** (0 duplikat), terdiri atas:
  - **Not Depressed** (skor PHQ-9 < 10): **33.091 responden (91,26%)**
  - **Depressed** (skor PHQ-9 >= 10): **3.168 responden (8,74%)**
  - Kondisi ini menunjukkan adanya ketidakseimbangan kelas (*class imbalance*).
- **Variabel & Fitur (20 Kolom Total):**
  - **1 Kolom Identitas:** `SEQN` (*Respondent Sequence Number* — digunakan untuk pelacakan & relasi tabel, dikeluarkan sebelum pelatihan model agar tidak terjadi kebocoran data).
  - **1 Kolom Target Biner:** `Depression` (`Depressed` vs `Not Depressed`).
  - **7 Fitur Numerik:** `Age`, `Sleep Hours`, `Sedentary Time`, `BMI`, `Systolic`, `Diastolic`, `Pulse`.
  - **11 Fitur Kategorikal:** `Gender`, `Education Level`, `Marital Status`, `Household Income`, `Trouble Sleeping History`, `Vigorous Recreation`, `Moderate Recreation`, `Current Smoker`, `Memory Problems`, `Cant Work`, `Limited Work`.
- **Protokol Pembagian & Pembersihan Data (*Zero Data Leakage*):**
  - Data dipartisi secara berstrata (**80% Data Latih** = 29.007 baris : **20% Data Uji Holdout** = 7.252 baris).
  - Seluruh transformasi (imputasi median/modus, standardisasi Z-score, dan *One-Hot Encoding*) dibungkus di dalam Scikit-Learn `Pipeline` yang hanya di-*fit* pada data latih.

---

## 3. Tujuan Proyek
1. Merancang alur prapemrosesan data (*preprocessing pipeline*) yang deterministik dan bebas kebocoran data (*zero data leakage*).
2. Membandingkan kinerja tiga algoritma klasifikasi (**Logistic Regression**, **Decision Tree**, dan **Random Forest**) melalui *5-Fold Stratified Cross-Validation* dengan fokus optimasi pada data tidak seimbang.
3. Mengukur kemampuan generalisasi model terbaik secara objektif pada 20% data uji *holdout*.
4. Menganalisis faktor risiko klinis paling berpengaruh menggunakan pendekatan *Explainable AI* (*Permutation Feature Importance* dan koefisien logit).
5. Mengimplementasikan model terbaik ke dalam aplikasi web interaktif berbasis **Streamlit (RuangRasa)** untuk kebutuhan skrining individu maupun *batch CSV*.

---

## 4. Model yang Dipilih Beserta Alasannya

Dari tiga algoritma yang dikomparasikan (**Logistic Regression**, **Decision Tree**, dan **Random Forest**), model yang dipilih untuk sistem akhir adalah **Random Forest Classifier** (`n_estimators=100`, `max_depth=10`, `class_weight='balanced'`).

### Mengapa Membandingkan 3 Model Tersebut?
- **Logistic Regression:** Dipilih sebagai *baseline* linier sederhana dan transparan (menghasilkan arah pengaruh/koefisien logit).
- **Decision Tree:** Dipilih untuk menguji model aturan bercabang (`IF-THEN`) non-linier yang mudah dipahami menyerupai alur diagnosis klinis.
- **Random Forest:** Dipilih sebagai model *ensemble bagging* (gabungan 100 pohon keputusan) yang tangguh terhadap *noise*, *outlier*, dan pola non-linier kompleks pada data tabel medis.

### Alasan Random Forest Terpilih sebagai Model Terbaik
1. **Skor Validasi Silang Tertinggi:** Memperoleh nilai rata-rata **5-Fold CV Macro-F1 tertinggi sebesar 0,6428 ± 0,0074** pada data latih, mengungguli Decision Tree (0,6299) dan Logistic Regression (0,6216).
2. **Keunggulan Mendeteksi Kasus Depresi (Recall Tertinggi):**
   - Logistic Regression dan Decision Tree memang memiliki akurasi mentah di atas 90%, tetapi gagal mendeteksi sebagian besar pasien depresi (masing-masing hanya menangkap **17,03%** dan **19,24%** kasus depresi).
   - Sebaliknya, Random Forest dengan `class_weight='balanced'` berhasil mendeteksi **63,41% kasus depresi riil** pada data uji (*Recall Macro* = 0,7346). Dalam skrining medis, menekan jumlah pasien depresi yang terlewat (*False Negative*) jauh lebih krusial daripada mengejar akurasi semu.
3. **Generalisasi Terkendali:** Selisih performa latih vs validasi terkendali baik berkat pembatasan kedalaman pohon (`max_depth=10`), dengan hasil Test Macro-F1 (**0,6356**) yang konsisten mendekati skor CV latih (**0,6428**).

---

## 5. Evaluasi Metrik yang Digunakan

### A. Metrik Utama: Macro-Averaged F1-Score (`Macro-F1`)
- **Definisi:** Menghitung F1-Score kelas *Depressed* dan *Not Depressed* secara terpisah, kemudian merata-ratakannya dengan bobot setara (50:50).
- **Alasan Pemilihan:** Karena proporsi kelas tidak seimbang (91,26% sehat vs 8,74% depresi), metrik **Akurasi biasa** sangat menyesatkan (model yang selalu menebak "Sehat" akan memperoleh akurasi 91,26% meskipun gagal total mendeteksi orang depresi). `Macro-F1` memaksa model memberikan performa seimbang di kedua kelas.

### B. Metrik Klinis Pendukung
- **Recall (Sensitivitas) Kelas Depressed:** Mengukur proporsi pasien depresi sesungguhnya yang berhasil terdeteksi oleh model ($\frac{TP}{TP + FN}$). Semakin tinggi *Recall*, semakin sedikit kasus depresi yang terlewat.
- **Precision:** Mengukur ketepatan tebakan positif model ($\frac{TP}{TP + FP}$).
- **Confusion Matrix:** Tabel rincian 4 kuadran (*True Positive*, *True Negative*, *False Positive*, *False Negative*) untuk memantau jenis kesalahan prediksi secara langsung.

### C. Tabel Perbandingan Hasil Evaluasi Model (7.252 Data Uji Holdout)

| Algoritma | CV Macro-F1 (Latih) | Test Accuracy | Test Macro-F1 | Test Recall Macro | Recall Kelas Depressed | Status Pemilihan |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Random Forest** | **0,6428** | 81,76% | **0,6356** | **0,7346** | **63,41%** | **TERPILIH** |
| **Decision Tree** | 0,6299 | 90,89% | 0,6105 | 0,5850 | 19,24% | Tidak |
| **Logistic Regression** | 0,6216 | 91,52% | 0,6075 | 0,5784 | 17,03% | Tidak |
| *Baseline Dummy (Mayoritas)* | - | 91,26% | 0,4771 | 0,5000 | 0,00% | Pembanding |

### D. Confusion Matrix Model Terpilih (Random Forest pada 7.252 Data Uji)

| Kondisi Asli \ Tebakan Model | Ditebak: **Depressed** | Ditebak: **Not Depressed** | Total Aktual |
|---|:---:|:---:|:---:|
| **Asli: Depressed** | **402** *(True Positive)* | **232** *(False Negative)* | **634** |
| **Asli: Not Depressed** | **1.091** *(False Positive)* | **5.527** *(True Negative)* | **6.618** |
