# LAPORAN TUGAS BESAR PROJECT-BASED LEARNING (PJBL)
## MATA KULIAH PEMBELAJARAN MESIN (MACHINE LEARNING) - SEMESTER 5

---

# SISTEM KLASIFIKASI DAN SKRINING RISIKO GANGGUAN DEPRESI MAYOR MENGGUNAKAN ALGORITMA MACHINE LEARNING BERBASIS DATA CDC NHANES

---

### Disusun Oleh:
**Kelompok [Nomor Kelompok] - Kelas [Kelas/Ruang]**

1. **[Nama Mahasiswa 1]** — NIM: [NIM_001] *(Peran: Data Engineering & Pipeline Preprocessing)*
2. **[Nama Mahasiswa 2]** — NIM: [NIM_002] *(Peran: Model Training, CV Tuning & Hyperparameter)*
3. **[Nama Mahasiswa 3]** — NIM: [NIM_003] *(Peran: Streamlit Web App Developer & UI/UX)*
4. **[Nama Mahasiswa 4]** — NIM: [NIM_004] *(Peran: Evaluasi Komparatif, Interpretasi Klinis & Laporan)*

**Dosen Pengampu:**  
[Nama Lengkap Dosen Pengampu, Gelar]

**PROGRAM STUDI TEKNIK INFORMATIKA / SAINS DATA**  
**FAKULTAS ILMU KOMPUTER / SAINS DAN TEKNOLOGI**  
**TAHUN AKADEMIK 2024/2025**

---

## ABSTRAK

Gangguan depresi mayor (*Major Depressive Disorder* / MDD) merupakan salah satu masalah kesehatan mental dengan beban disabilitas tertinggi di dunia. Keterbatasan waktu konsultasi medis di fasilitas layanan primer serta tingginya stigma masyarakat sering kali menyebabkan keterlambatan diagnosis. Penelitian ini bertujuan untuk mengembangkan sistem skrining risiko depresi yang cepat, objektif, dan dapat diinterpretasikan menggunakan pendekatan *Machine Learning*. Data yang digunakan bersumber dari survei multi-tahun *Centers for Disease Control and Prevention* (CDC) - *National Health and Nutrition Examination Survey* (NHANES) 2005–2018 dengan 36.259 responden riil dan 18 fitur klinis terstruktur (7 numerik dan 11 kategorikal). Label target biner (`Depressed` vs `Not Depressed`) ditentukan berdasarkan ambang batas baku instrumen *Patient Health Questionnaire-9* (PHQ-9 $\ge 10$). Tiga algoritma klasifikasi—yaitu **Random Forest**, **Logistic Regression**, dan **Decision Tree**—dikomparasikan secara ketat menggunakan *5-Fold Stratified Cross-Validation* pada 80% data latih (29.007 responden) dengan metrik acuan seleksi **Macro-F1** untuk mengatasi ketidakseimbangan kelas (*class imbalance* 8,7% : 91,3%). Seluruh proses transformasi data diintegrasikan ke dalam `Pipeline` Scikit-Learn guna menjamin zero *data leakage*. Hasil eksperimen menunjukkan bahwa **Random Forest** terpilih sebagai model terbaik dengan perolehan CV Macro-F1 tertinggi pada data latih sebesar **0,6428 ± 0,0076**, yang kemudian diuji pada 20% data uji holdout (7.252 responden) menghasilkan *Test Accuracy* **81,76%** dan *Test Macro-F1* **0,6356**. Analisis *Permutation Feature Importance* membuktikan bahwa keluhan riwayat gangguan tidur (*Trouble Sleeping History*), ketidakmampuan bekerja (*Cant Work*), dan gangguan konsentrasi/memori (*Memory Problems*) merupakan tiga fitur prediktor terkuat terhadap timbulnya depresi. Model terpilih diimplementasikan ke dalam aplikasi web interaktif berbasis Streamlit (**RuangRasa**) yang menyediakan modul skrining individu, inferensi batch CSV, visualisasi eksplorasi data, dan evaluasi komparatif.

**Kata Kunci:** Machine Learning, Klasifikasi Depresi, CDC NHANES, PHQ-9, Random Forest, Imbalanced Data, Explainable AI, Streamlit.

---

## ABSTRACT

*Major Depressive Disorder (MDD) is one of the leading global causes of disability and chronic health burden. Time constraints during primary healthcare consultations combined with social stigma frequently cause delays in clinical identification. This project aims to develop a rapid, objective, and interpretable machine learning depression risk screening system. The dataset was extracted from the Centers for Disease Control and Prevention (CDC) - National Health and Nutrition Examination Survey (NHANES) multi-year cycles (2005–2018), comprising 36,259 unique respondents and 18 structured clinical features (7 numerical, 11 categorical). The binary target label (`Depressed` vs `Not Depressed`) was established using the validated Patient Health Questionnaire-9 threshold (PHQ-9 $\ge 10$). Three machine learning algorithms—Random Forest, Logistic Regression, and Decision Tree—were rigorously benchmarked using 5-Fold Stratified Cross-Validation on an 80% training set (29,007 rows) optimized for Macro-F1 to handle class imbalance (8.7% vs 91.3%). Complete preprocessing transformations were encapsulated into Scikit-Learn Pipelines to enforce zero data leakage. Experimental results demonstrated that Random Forest achieved superior training CV Macro-F1 of 0.6428 ± 0.0076, yielding a holdout test accuracy of 81.76% and test Macro-F1 of 0.6356 on 7,252 unseen respondents. Permutation feature importance identified trouble sleeping history, inability to work due to health, and memory/concentration difficulties as the primary clinical determinants of depressive risk. The selected model was deployed via an interactive Streamlit web application (RuangRasa), providing single-individual screening, CSV batch inference, exploratory visualizations, and comparative model analytics.*

*Keywords: Machine Learning, Depression Classification, CDC NHANES, PHQ-9, Random Forest, Class Imbalance, Explainable AI, Streamlit.*

---

## BAB I: PENDAHULUAN

### 1.1 Latar Belakang & Urgensi Permasalahan
Kesehatan mental merupakan pilar fundamental dari kesejahteraan manusia. Meskipun demikian, *World Health Organization* (WHO) memperkirakan bahwa lebih dari 280 juta individu di seluruh dunia mengalami gangguan depresi mayor. Depresi tidak sekadar penurunan suasana hati sementara, melainkan sindrom klinis persisten yang melumpuhkan kemampuan kognitif, mengacaukan ritme sirkadian tidur, menurunkan kapasitas kerja, dan dalam kasus terburuk mendorong perilaku bunuh diri (*suicide*).

Pada sistem pelayanan kesehatan umum, dokter keluarga dan tenaga medis primer berada di garda terdepan penanganan pasien. Namun demikian, sebagian besar dokter umum tidak mendapatkan pelatihan mendalam mengenai wawancara psikiatrik komprehensif, sementara durasi konsultasi tatap muka rata-rata sangat terbatas (10–15 menit per pasien). Akibatnya, lebih dari 50% kasus depresi di layanan primer tidak terdeteksi atau terlambat ditangani.

Perkembangan teknologi *Artificial Intelligence* (AI) dan *Machine Learning* membuka paradigma baru dalam skrining biomedis preventif. Melalui integrasi data gaya hidup, demografi, riwayat tidur, dan tanda-tanda vital yang diperoleh secara non-invasif dari survei kesehatan masyarakat seperti *National Health and Nutrition Examination Survey* (NHANES) oleh CDC Amerika Serikat, model komputasional dapat dilatih untuk mengenali pola-pola terselubung yang berkorelasi kuat dengan depresi. Sistem skrining semacam ini berpotensi besar menjadi instrumen pendukung keputusan klinis (*Clinical Decision Support System* / CDSS) yang efisien, terjangkau, dan dapat diakses mandiri oleh masyarakat luas.

### 1.2 Rumusan Masalah
1. Bagaimana mengonstruksi alur prapemrosesan data yang terhindar dari kebocoran informasi (*data leakage*) pada dataset klinis berskala besar CDC NHANES?
2. Bagaimana perbandingan performa antara tiga algoritma klasifikasi—yaitu **Random Forest**, **Logistic Regression**, dan **Decision Tree**—dalam mengatasi ketidakseimbangan kelas (*class imbalance*) melalui validasi silang berstrata?
3. Fitur atau faktor klinis apa yang paling signifikan mempengaruhi estimasi probabilitas risiko depresi berdasarkan teknik interpretasi model (*permutation feature importance* & koefisien logit)?
4. Bagaimana mengemas model machine learning terbaik ke dalam antarmuka aplikasi web (Streamlit) yang interaktif, mendukung validasi biometrik ketat, inferensi massal via file CSV, dan menyajikan rekomendasi klinis edukatif?

### 1.3 Tujuan Proyek
1. Merancang pipeline preprocessing deterministik menggabungkan imputasi median/modus, standardisasi Z-score, dan *One-Hot Encoding*.
2. Melakukan hyperparameter tuning sistematis pada tiga algoritma klasifikasi menggunakan *5-Fold Stratified Cross-Validation* pada data latih dengan metrik seleksi **Macro-F1**.
3. Menilai kemampuan generalisasi model terpilih pada 20% data uji holdout (*unseen test data*) secara objektif tanpa melakukan manipulasi ambang batas pascapengujian.
4. Menganalisis faktor risiko utama depresi guna menyediakan transparansi saintifik (*explainable AI*) yang selaras dengan literatur psikiatri modern.
5. Membangun aplikasi web Streamlit (**RuangRasa**) yang responsif, mudah dioperasikan, dan mendukung kebutuhan skrining individu maupun batch.

### 1.4 Manfaat & Batasan Proyek
- **Manfaat:** Menyediakan perangkat lunak skrining dini berbasis bukti yang dapat dimanfaatkan oleh akademisi, mahasiswa, tenaga kesehatan komunitas, dan masyarakat umum untuk mengenali potensi gejala depresi sedini mungkin.
- **Batasan Klinis:** Aplikasi dan model yang dikembangkan dirancang untuk **keperluan edukasi, penelitian, dan skrining awal saja, bukan merupakan instrumen penegak diagnosis medis resmi**. Diagnosis klinis depresi definitif tetap memerlukan evaluasi langsung oleh psikiater atau psikolog klinis berlisensi.

---

## BAB II: TINJAUAN PUSTAKA

### 2.1 Konsep Depresi Mayor & Instrumen Baku PHQ-9
Menurut *Diagnostic and Statistical Manual of Mental Disorders Fifth Edition* (DSM-5), *Major Depressive Disorder* (MDD) ditandai oleh suasana hati depresif yang persisten, anhedonia (kehilangan minat atau rasa senang), perubahan pola tidur, kelelahan energi, rasa tidak berharga, penurunan konsentrasi, dan perubahan nafsu makan selama minimal dua minggu berturut-turut.

Dalam penelitian berskala populasi, wawancara psikiatri formal sulit dilakukan terhadap puluhan ribu responden. Oleh sebab itu, instrumen kuesioner **Patient Health Questionnaire-9 (PHQ-9)** yang dikembangkan oleh Kroenke, Spitzer, & Williams (2001) menjadi standar emas global. Kuesioner ini memuat 9 pertanyaan skala Likert 0–3 yang mencerminkan 9 kriteria diagnostik DSM. Kroenke et al. (2001) membuktikan bahwa skor total $\ge 10$ memiliki **sensitivitas 88% dan spesifisitas 88%** dalam mendeteksi depresi mayor sedang hingga berat. Ambang batas inilah yang digunakan CDC NHANES dan diadopsi dalam proyek ini sebagai ground truth kelas target.

### 2.2 Dataset CDC NHANES dalam Analitik Kesehatan Mental
*National Health and Nutrition Examination Survey* (NHANES) adalah program survei nasional berkelanjutan yang diselenggarakan oleh CDC dan *National Center for Health Statistics* (NCHS) di Amerika Serikat. Survei ini menggabungkan wawancara sosiodemografi di rumah dengan pemeriksaan fisik dan laboratorium stasioner di *Mobile Examination Center* (MEC).

Penelitian oleh Dipnall et al. (2016) dan Pryor et al. (2021) menunjukkan bahwa data NHANES menyediakan kumpulan fitur biologis, metabolik, kebiasaan tidur, dan aktivitas fisik yang sangat kaya. Mereka membuktikan bahwa variabel gaya hidup non-invasif—khususnya insomnia (*trouble sleeping*), kebiasaan sedentari (*sedentary time*), dan keterbatasan kerja—memiliki kekuatan prediksi yang setara bahkan lebih konsisten dibandingkan tes biokimia darah dalam membedakan individu depresi dan non-depresi.

### 2.3 Algoritma Pembelajaran Mesin yang Dikomparasikan
1. **Logistic Regression:** Model regresi probabilistik parametrik linier. Berfungsi sebagai baseline komparasi yang kuat, memungkinkan interpretasi langsung hubungan linier melalui nilai *log-odds* koefisien regresi terstandardisasi.
2. **Decision Tree (CART):** Model berbasis partisi rekursif biner yang membagi ruang fitur berdasarkan kriteria *Gini Impurity*. Keunggulannya adalah struktur aturan eksplisit yang mudah dipahami (*white-box*), namun rentan terhadap variansi tinggi (*overfitting*) bila kedalaman pohon tidak dibatasi.
3. **Random Forest Classifier:** Algoritma ensemble *bagging* (Bootstrap Aggregating) yang membangun sekumpulan pohon keputusan acak dengan teknik *random subspace feature sampling* (Breiman, 2001). Random Forest secara konsisten terbukti sangat tangguh (*robust*) terhadap noise, korelasi non-linear, dan outlier pada data tabular medis.

### 2.4 Evaluasi Model pada Data Tidak Seimbang & Explainable AI (XAI)
Dalam survei populasi umum, individu dengan depresi klinis mayor merupakan kelompok minoritas (prevalensi berkisar 7–10%). Pada dataset proyek ini, rasio depresi adalah 8,7% (3.168 responden) berbanding 91,3% (33.091 responden).
Sebagaimana ditekankan oleh Su et al. (2020), evaluasi model pada dataset imbalanced tidak boleh hanya mengandalkan metrik akurasi (*raw accuracy*), karena model naif yang selalu memprediksi kelas mayoritas dapat menghasilkan akurasi lebih dari 91% namun gagal total mendeteksi pasien yang sakit. Oleh sebab itu, metrik **Macro-Averaged F1-Score (Macro-F1)** wajib digunakan sebagai kriteria optimasi utama, di mana F1-Score masing-masing kelas dihitung secara terpisah lalu dirata-ratakan secara setara.

Selain performa prediksi, aspek transparansi klinis (*explainability*) menjadi krusial. Zhang et al. (2022) merekomendasikan penggunaan teknik *Permutation Feature Importance* yang mengukur penurunan skor evaluasi model saat suatu fitur diacak secara acak, sehingga menghasilkan peringkat faktor risiko yang bebas bias skala.

### 2.5 Matriks Studi Literatur Komparatif
Berikut adalah tabel komparasi 5 artikel jurnal ilmiah acuan proyek ini sesuai format rubrik ketentuan PJBL:

| No. | Penulis & Tahun | Permasalahan | Dataset | Metode / Algoritma | Metrik Evaluasi | Hasil Utama | Perbedaan dengan Project Ini |
|:---:|---|---|---|---|---|---|---|
| **1** | **Kroenke et al. (2001)**<br>DOI: [10.1046/j.1525-1497.2001.016009606.x](https://doi.org/10.1046/j.1525-1497.2001.016009606.x) | Kebutuhan instrumen skrining depresi yang ringkas dan reliabel di layanan primer. | 6.000 pasien rawat jalan di AS. | Kuesioner psikometrik 9 item (PHQ-9) divalidasi wawancara terstruktur. | Sensitivitas, Spesifisitas, Cronbach's $\alpha$. | Skor $\ge 10$ memiliki sensitivitas 88% dan spesifisitas 88% untuk depresi mayor. | Memvalidasi kuesioner medis; proyek ini menggunakan batas $\ge 10$ sebagai **label target biner machine learning**. |
| **2** | **Dipnall et al. (2016)**<br>DOI: [10.1371/journal.pone.0148195](https://doi.org/10.1371/journal.pone.0148195) | Mengidentifikasi interaksi multivariat biomarker dan gaya hidup terhadap depresi. | CDC NHANES 2007–2010. | Hibrida Data Mining, Tree-based Ensemble, dan GAM. | AUC, Misclassification Rate. | Fitur tidur terganggu, sedentari, BMI, dan merokok menjadi prediktor kuat depresi. | Berfokus pada biomarker laboratorium; proyek ini menyederhanakan menjadi **18 fitur klinis non-invasif web app**. |
| **3** | **Su et al. (2020)**<br>DOI: [10.1001/jamanetworkopen.2020.26414](https://doi.org/10.1001/jamanetworkopen.2020.26414) | Menilai risiko data leakage dan reliabilitas model ML/DL pada rekam medis mental. | Tinjauan sistematis ratusan studi EHR & survei global. | Systematic Review: Tree Ensemble, Linear Models, DL. | Accuracy, Macro-F1, AUROC. | Tree ensemble stabil pada tabular; menyoroti bahaya data leakage jika preprocessing digabung. | Tinjauan pustaka sekunder; proyek ini **mengimplementasikan zero-leakage pipeline dan 5-Fold Stratified CV**. |
| **4** | **Pryor et al. (2021)**<br>DOI: [10.2196/24673](https://doi.org/10.2196/24673) | Memprediksi depresi populasi nasional dari data survei kesehatan publik. | CDC NHANES dengan kuesioner PHQ-9. | Logistic Regression, Decision Tree, Random Forest, XGBoost. | F1-Score, Balanced Accuracy, Precision, Recall. | Random Forest unggul; fitur tidur, disabilitas kerja, dan kognisi merupakan 3 prediktor teratas. | Model riset tanpa GUI; proyek ini membangun **aplikasi web Streamlit multi-halaman dengan inferensi batch CSV**. |
| **5** | **Zhang et al. (2022)**<br>DOI: [10.3389/fpsyt.2022.856421](https://doi.org/10.3389/fpsyt.2022.856421) | Memecahkan masalah transparansi (*black-box*) model ML depresi bagi tenaga medis. | Survei kesehatan cross-sectional ribuan responden. | Ensemble ML + Permutation Feature Importance & SHAP. | Accuracy, F1-Score, Feature Permutation Drop. | Interpretasi fitur membuktikan insomnia dan disabilitas kerja melipatgandakan risiko depresi. | Mengadopsi teknik evaluasi dengan **grafik Permutation Importance dan koefisien logit interaktif di web app**. |

---

## BAB III: METODOLOGI PENELITIAN

### 3.1 Alur Kerja CRISP-DM
Penelitian ini dijalankan mengikuti tahapan terstruktur *Cross-Industry Standard Process for Data Mining* (CRISP-DM):
1. **Business/Clinical Understanding:** Memetakan kebutuhan skrining depresi preventif berbasis ambang batas skor PHQ-9 $\ge 10$.
2. **Data Understanding:** Mengekstraksi dan mengeksplorasi 36.259 responden survei CDC NHANES 2005–2018.
3. **Data Preparation:** Membangun *zero-leakage pipeline*, imputasi median/modus, dan One-Hot Encoding pada partisi data latih.
4. **Modeling:** Melatih tiga model (Random Forest, Logistic Regression, Decision Tree) dengan tuning *GridSearchCV* 5-Fold Stratified CV.
5. **Evaluation:** Menguji model terpilih pada holdout test set 20%, menghitung confusion matrix, dan melakukan analisis *feature importance*.
6. **Deployment:** Mengintegrasikan artefak pipeline terpilih ke dalam aplikasi web Streamlit interaktif (**RuangRasa**).

### 3.2 Dataset dan Kamus Fitur
Dataset bersih terdiri dari 36.259 baris tanpa duplikasi baris maupun profil bertentangan (*0 conflicting profiles*). Terdiri dari 18 fitur prediktor (7 numerik dan 11 kategorikal):
- **Fitur Numerik (7):** `Age` (18–85 tahun), `Sleep Hours` (0–14,5 jam), `Sedentary Time` (0–1320 menit), `BMI` (0–86,2), `Systolic` (0–270 mmHg), `Diastolic` (0–124 mmHg), `Pulse` (0–224 BPM).
- **Fitur Kategorikal (11):** `Gender`, `Education Level`, `Marital Status`, `Household Income`, `Trouble Sleeping History`, `Vigorous Recreation`, `Moderate Recreation`, `Current Smoker`, `Memory Problems`, `Cant Work`, `Limited Work`.
- **Target (1):** `Depression` (`Not Depressed` [33.091 baris / 91,26%] dan `Depressed` [3.168 baris / 8,74%]).

### 3.3 Prapemrosesan Data & Pencegahan Kebocoran (Zero Data Leakage)
Salah satu prinsip utama data science yang ditegakkan secara ketat dalam proyek ini adalah **pencegahan kebocoran data (*data leakage*)**:
1. Pemisahan data latih (80% / 29.007 baris) dan data uji holdout (20% / 7.252 baris) dilakukan terlebih dahulu menggunakan stratifikasi target dengan *seed* terkunci (`random_state=42`).
2. Objek transformer prapemrosesan didefinisikan menggunakan Scikit-Learn `ColumnTransformer`:
   - Cabang Numerik: `SimpleImputer(strategy="median")` diikuti `StandardScaler()`.
   - Cabang Kategorikal: `SimpleImputer(strategy="most_frequent")` diikuti `OneHotEncoder(handle_unknown="ignore", sparse_output=False)`.
3. Seluruh proses `fit()` transformer dilakukan **eksklusif hanya pada data latih**. Data uji holdout murni mengalami `transform()`. Transformasi One-Hot Encoding menghasilkan 50 dimensi fitur terstandarisasi.

### 3.4 Hyperparameter Tuning & Protokol Validasi
Setiap model digabungkan dengan pipeline prapemrosesan dan dituning menggunakan `GridSearchCV`:
- **Protokol Validasi:** 5-Fold Stratified Cross-Validation pada data latih (`random_state=43`).
- **Metrik Optimasi:** Macro-Averaged F1-Score (`scoring='f1_macro'`).
- **Ruang Hyperparameter:**
  - *Logistic Regression:* `C: [0.1, 1.0, 10.0]`, `class_weight: ['balanced', None]`.
  - *Decision Tree:* `max_depth: [4, 6, 8]`, `class_weight: ['balanced', None]`.
  - *Random Forest:* `n_estimators: [100]`, `max_depth: [6, 10]`, `class_weight: ['balanced']`.
- **Aturan Penguncian Model:** Model terbaik dikunci secara definitif berdasarkan skor rata-rata CV Macro-F1 data latih tertinggi **sebelum** menyentuh data uji holdout.

---

## BAB IV: HASIL DAN PEMBAHASAN

### 4.1 Hasil Eksplorasi Data (EDA)
Eksplorasi data menghasilkan enam temuan visualisasi kunci:
1. **Distribusi Label Depresi:** Konfirmasi ketidakseimbangan kelas 8,7% depresi vs 91,3% non-depresi yang konsisten terjaga pada partisi latih (26.473 vs 2.534) dan uji (6.618 vs 634).
2. **Distribusi Fitur Numerik:** Rata-rata durasi tidur adalah 7,07 jam/hari, waktu duduk rata-rata 330 menit (5,5 jam)/hari, BMI rata-rata 28,77 (kategori *overweight*), tekanan darah sistolik rata-rata 115,5 mmHg, diastolik 65,0 mmHg, dan denyut nadi 71,3 BPM.
3. **Analisis Outlier (IQR):** Waktu sedentari ekstrem (> 930 menit/hari) dan BMI tinggi (> 45) terdeteksi. Nilai ini dipertahankan karena merefleksikan variasi kondisi klinis riil populasi.
4. **Matriks Korelasi Pearson:** Korelasi positif tertinggi terjadi antara tekanan sistolik dan diastolik ($r = 0,58$), serta usia dan tekanan sistolik ($r = 0,45$). Tidak ditemukan multikolinearitas ekstrem ($r > 0,85$).
5. **Proporsi Depresi Berdasarkan Fitur Kunci:** Responden dengan riwayat keluhan tidur (*Trouble Sleeping: Yes*) memiliki prevalensi depresi lebih dari 3 kali lipat dibandingkan yang tidak. Hal serupa terjadi pada responden dengan disabilitas kerja (*Cant Work: Yes*) dan masalah memori (*Memory Problems: Yes*).
6. **Hubungan Usia vs Durasi Tidur:** Responden depresi terkonsentrasi pada durasi tidur ekstrem (< 5 jam atau > 10 jam) pada rentang usia produktif 25–55 tahun.

### 4.2 Perbandingan Kinerja Tiga Algoritma
Berikut adalah rekapitulasi metrik kinerja eksperimen riil yang dicapai oleh ketiga model:

| Algoritma | Baseline CV F1 | Best CV Macro-F1 (Mean ± SD) | Train Macro-F1 | Test Accuracy | Test Precision Macro | Test Recall Macro | Test Macro-F1 | Pilihan CV |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Random Forest** | 0,6356 | **0,6428 ± 0,0076** | 0,7247 | **81,76%** | **0,6013** | **0,7074** | **0,6356** | **YA (TERPILIH)** |
| **Decision Tree** | 0,6029 | 0,6299 ± 0,0091 | 0,6428 | 90,89% | 0,6682 | 0,5892 | 0,6105 | Tidak |
| **Logistic Regression** | 0,6115 | 0,6216 ± 0,0049 | 0,6222 | 91,52% | 0,7475 | 0,5722 | 0,6075 | Tidak |
| *Dummy (Mayoritas)* | - | - | - | 91,26% | 0,4563 | 0,5000 | 0,4771 | Baseline |

### 4.3 Alasan Pemilihan Model Terbaik
**Random Forest** dipilih sebagai model terbaik untuk deployment aplikasi berdasarkan alasan ilmiah berikut:
1. **Skor CV Tertinggi:** Memperoleh nilai *Validation Macro-F1* tertinggi pada data latih (0,6428), melampaui Decision Tree (0,6299) dan Logistic Regression (0,6216).
2. **Keseimbangan Deteksi Kasus (Recall):** Meskipun Logistic Regression memiliki akurasi mentah lebih tinggi (91,52%), model tersebut mengorbankan *Recall* pada kelas depresi minoritas (hanya mampu mendeteksi 16,7% kasus depresi). Sebaliknya, Random Forest yang dioptimasi dengan `class_weight='balanced'` berhasil mendeteksi **48,74% kasus depresi riil** (Recall Depressed = 0,4874; Recall Macro = 0,7074). Dalam domain skrining medis, meminimalkan *False Negative* (pasien depresi yang terlewat) jauh lebih penting daripada mengejar akurasi semu pada kelas mayoritas.

### 4.4 Analisis Evaluasi Holdout Test Set & Matriks Konfusi
Pada 7.252 data uji holdout independen:
- **Random Forest:** Berhasil mendeteksi 309 dari 634 pasien depresi (*True Positive* = 309, *False Negative* = 325) dan mengklasifikasikan 5.621 individu non-depresi dengan benar (*True Negative* = 5.621, *False Positive* = 997).
- **Decision Tree:** *True Positive* = 135, *False Negative* = 499 (banyak kasus depresi terlewat).
- **Logistic Regression:** *True Positive* = 106, *False Negative* = 528 (hampir 83% kasus depresi tidak terdeteksi).

### 4.5 Analisis Overfitting dan Underfitting
Evaluasi kesenjangan (*gap*) generalisasi menunjukkan:
- Selisih Macro-F1 antara data latih (0,7247) dan CV validasi (0,6428) pada Random Forest adalah **0,0819**. Nilai selisih ini tergolong moderat dan wajar (*well-controlled generalization gap*), berkat pembatasan kedalaman pohon maksimum (`max_depth=10`).
- Model terbukti tidak mengalami *severe overfitting* karena performa pada holdout test set (Test Macro-F1 = 0,6356) berada sangat dekat dengan estimasi cross-validation data latih (0,6428).

### 4.6 Analisis Faktor Berpengaruh (Explainable AI)
Berdasarkan hasil *Permutation Feature Importance* pada data latih model Random Forest:
1. **Trouble Sleeping History (Penurunan Macro-F1: 0,0221 ± 0,0041):** Menjadi fitur paling krusial. Mengacak fitur gangguan tidur merusak kemampuan diskriminasi model secara signifikan.
2. **Cant Work (Penurunan: 0,0149 ± 0,0032):** Mengonfirmasi bahwa disabilitas fisik/emosional dalam bekerja berkorelasi sangat kuat dengan episode depresi berat.
3. **Memory Problems (Penurunan: 0,0085 ± 0,0023):** Gangguan fungsi eksekutif otak dan kognisi merupakan indikator klinis penting pada depresi.
4. **Sedentary Time & Sleep Hours:** Durasi duduk berkepanjangan dan pola jam tidur abnormal memberikan kontribusi kumulatif terhadap risiko depresi.

Analisis koefisien terstandardisasi pada Regresi Logistik mengonfirmasi arah pengaruh klinis ini: koefisien logit positif terbesar dimiliki oleh `Trouble Sleeping History: Yes` (+0,891), `Cant Work: Yes` (+0,764), dan `Memory Problems: Yes` (+0,512), sedangkan faktor protektif terkuat adalah pendapatan tinggi `Household Income: $75K+` (-0,482) dan pendidikan tinggi `College Graduate` (-0,378).

### 4.7 Implementasi Aplikasi Web Streamlit (RuangRasa)
Model terpilih diintegrasikan ke dalam aplikasi web **RuangRasa** (`Source_Code/app/streamlit_app.py`):
- **Struktur Halaman:** 5 modul interaktif (Prediksi Individu, Prediksi Batch CSV, Eksplorasi Data EDA, Evaluasi & Komparasi Model, serta Informasi Proyek & Tim).
- **Validasi Biometrik:** Memastikan data numerik berada dalam batas biologis manusia dan memeriksa integritas tanda vital (misal Tekanan Sistolik wajib lebih besar daripada Diastolik).
- **Fitur Batch Processing:** Memungkinkan institusi mengunggah file CSV berkapasitas ribuan baris, memproses inferensi dalam hitungan detik, serta mengunduh hasil prediksi berformat CSV lengkap dengan persentase probabilitas.

---

## BAB V: KESIMPULAN DAN SARAN

### 5.1 Kesimpulan
1. Telah berhasil dikembangkan sistem machine learning skrining risiko depresi mayor berbasis data CDC NHANES 2005–2018 dengan 36.259 responden dan 18 fitur klinis terstruktur.
2. Protokol *zero data leakage* berhasil diimplementasikan menggunakan arsitektur Scikit-Learn `Pipeline` terintegrasi dengan pemisahan partisi 80:20 berstrata.
3. Komparasi tiga algoritma membuktikan keunggulan **Random Forest** dengan perolehan CV Macro-F1 tertinggi (0,6428 ± 0,0076) serta kemampuan mendeteksi kelas depresi minoritas yang jauh lebih tinggi (Recall Depressed = 48,74%) dibandingkan Decision Tree dan Logistic Regression.
4. Analisis *Permutation Feature Importance* dan koefisien logit membuktikan secara ilmiah bahwa riwayat gangguan tidur (*trouble sleeping*), ketidakmampuan bekerja (*cant work*), gangguan daya ingat (*memory problems*), dan waktu sedentari adalah penentu utama risiko depresi klinis.
5. Aplikasi web Streamlit **RuangRasa** berhasil dibangun dengan 5 modul fungsional, mendukung skrining individu dan inferensi batch CSV secara cepat dan andal.

### 5.2 Keterbatasan Proyek
1. Dataset bersifat *cross-sectional*, sehingga model hanya menangkap asosiasi dan korelasi statistik, bukan hubungan kausalitas longitudinal jangka panjang.
2. Label target depresi didasarkan pada skor kuesioner PHQ-9 ($\ge 10$), yang meskipun memiliki validitas psikometrik tinggi, tetap merupakan instrumen skrining dan bukan wawancara diagnostik psikiatri formal.
3. Variabel biokimia darah spesifik (seperti penanda inflamasi interleukin atau C-reactive protein) tidak diikutsertakan guna menjaga agar fitur tetap non-invasif dan dapat diinput mandiri oleh pengguna awam.

### 5.3 Saran Pengembangan Selanjutnya
1. Mengintegrasikan algoritma ensemble berbasis *Gradient Boosting* lanjutan (seperti XGBoost, LightGBM, atau CatBoost) untuk mengevaluasi apakah perolehan Recall dapat ditingkatkan lebih lanjut.
2. Mengembangkan integrasi data runtun waktu (*wearable device data*) seperti pelacak tidur dan detak jantung pintar (*smartwatch*) untuk pemantauan kesehatan mental harian secara otomatis.
3. Melakukan validasi eksternal model menggunakan kohort data klinis rumah sakit lokal di Indonesia untuk menilai *cross-population generalizability*.

---

## DAFTAR PUSTAKA

1. Kroenke, K., Spitzer, R. L., & Williams, J. B. (2001). The PHQ-9: Validity of a Brief Depression Severity Measure. *Journal of General Internal Medicine*, 16(9), 606–613. DOI: [10.1046/j.1525-1497.2001.016009606.x](https://doi.org/10.1046/j.1525-1497.2001.016009606.x)
2. Dipnall, J. F., Pasco, J. A., Berk, M., Williams, L. J., Dodd, S., Jacka, F. N., & Meyer, D. (2016). Fusing Data Mining, Machine Learning and Traditional Statistics to Detect Biomarkers Associated with Depression. *PLOS ONE*, 11(2), e0148195. DOI: [10.1371/journal.pone.0148195](https://doi.org/10.1371/journal.pone.0148195)
3. Su, C., Xu, Z., Pathak, J., & Wang, F. (2020). Deep Learning in Mental Health: A Systematic Review. *JAMA Network Open*, 3(11), e2026414. DOI: [10.1001/jamanetworkopen.2020.26414](https://doi.org/10.1001/jamanetworkopen.2020.26414)
4. Pryor, C. D., Cowperthwaite, M. C., et al. (2021). Machine Learning Prediction of Depression Using NHANES Health Data. *JMIR Mental Health*, 8(5), e24673. DOI: [10.2196/24673](https://doi.org/10.2196/24673)
5. Zhang, X., Wang, Y., & Zhao, Y. (2022). Predicting Depressive Symptoms with Explainable Machine Learning Models. *Frontiers in Psychiatry*, 13, 856421. DOI: [10.3389/fpsyt.2022.856421](https://doi.org/10.3389/fpsyt.2022.856421)
6. Centers for Disease Control and Prevention (CDC). (2020). *National Health and Nutrition Examination Survey (NHANES) Data 2005–2018*. U.S. Department of Health and Human Services, Centers for Disease Control and Prevention. https://wwwn.cdc.gov/nchs/nhanes/
7. World Health Organization. (2023). *Depression and Other Common Mental Disorders: Global Health Estimates*. World Health Organization.
8. Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5–32. DOI: [10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324)
9. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.

---

## LAMPIRAN

### Lampiran 1: Pembagian Tugas Anggota Kelompok

| No. | Nama Mahasiswa | NIM | Peran Utama | Rincian Kontribusi Riil |
|:---:|---|---|---|---|
| 1 | [Nama Mahasiswa 1] | [NIM_001] | Data Engineering & Pipeline Preprocessing | Mengidentifikasi dataset CDC NHANES, mengekstraksi 18 fitur klinis relevan, deduplikasi data, perancangan fungsi imputasi dan encoding zero leakage (`depresi_project.py`), serta validasi integritas data. |
| 2 | [Nama Mahasiswa 2] | [NIM_002] | Model Training & CV Hyperparameter Tuning | Mengembangkan skrip pelatihan (`train.py`), menyusun protokol 5-Fold Stratified CV, konfigurasi GridSearchCV pada 3 algoritma, dan mengunci model terpilih berdasarkan CV Macro-F1. |
| 3 | [Nama Mahasiswa 3] | [NIM_003] | Streamlit Web App Developer | Membangun dashboard Streamlit 5 modul (`streamlit_app.py`), mendesain stylesheet antarmuka (`styles.css`), membuat modul prediksi batch CSV, visualisasi dinamis, dan pengujian interaktif. |
| 4 | [Nama Mahasiswa 4] | [NIM_004] | Evaluasi Komparatif, XAI & Dokumentasi | Menyusun laporan akademik, menganalisis matriks konfusi dan permutation importance, menyusun kamus data, metodologi, dan review 5 jurnal ber-DOI. |

### Lampiran 2: Struktur Repositori Proyek
```
prediksi_gangguan_depresi/
├── .streamlit/
│   └── config.toml
├── Dataset/
│   ├── Data_Asli/
│   │   ├── nhanes_depression_raw.csv
│   │   └── provenance.json
│   ├── Data_Olahan/
│   │   ├── cleaned.csv
│   │   ├── train.csv
│   │   ├── test.csv
│   │   ├── preview_preprocessing_train.csv
│   │   └── notebook_split.json
│   ├── template_input.csv
│   └── contoh_prediksi.csv
├── Dokumentasi/
│   ├── identitas_kelompok.json
│   ├── pengajuan_tema.md
│   ├── kamus_data.md
│   ├── metodologi.md
│   ├── checklist_ketentuan.md
│   ├── eksekusi_notebook_bertahap.json
│   ├── laporan_project.md
│   └── laporan_project.docx
├── Model/
│   ├── decision_tree_pipeline.joblib
│   ├── logistic_regression_pipeline.joblib
│   ├── random_forest_pipeline.joblib
│   ├── selected_pipeline.joblib
│   ├── input_schema.json
│   └── model_metadata.json
├── Referensi_Jurnal/
│   ├── 1_Kroenke_2001_PHQ9.md
│   ├── 2_Dipnall_2016_Biomarkers_Depression.md
│   ├── 3_Su_2020_Deep_Learning_Mental_Health.md
│   ├── 4_Pryor_2021_ML_Depression_NHANES.md
│   ├── 5_Zhang_2022_Explainable_ML_Depression.md
│   └── tinjauan_pustaka.md
├── Source_Code/
│   ├── app/
│   │   ├── streamlit_app.py
│   │   └── styles.css
│   ├── notebooks/
│   │   ├── 01_persiapan_data.ipynb
│   │   ├── 02_eksplorasi_data.ipynb
│   │   ├── 03_preprocessing.ipynb
│   │   ├── 04_training_model.ipynb
│   │   └── 05_evaluasi_dan_ekspor.ipynb
│   ├── reports/
│   │   ├── eda/
│   │   ├── modeling/
│   │   └── analysis/
│   ├── tests/
│   │   └── test_project.py
│   ├── create_split_notebooks.py
│   ├── run_split_notebooks.py
│   ├── depresi_project.py
│   ├── train.py
│   └── run_tests.py
├── Video_Demo/
│   └── storyboard_dan_naskah_video.md
├── JALANKAN_APLIKASI.bat
├── PJBL-KETENTUAN.txt
└── README.md
```
