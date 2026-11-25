# Tinjauan Pustaka & Matriks Studi Literatur Komparatif
## Proyek RuangRasa: Skrining Risiko Gangguan Depresi Mayor (CDC NHANES)

---

### I. Sintesis Teori dan Dasar Keilmuan
Pengembangan sistem prediksi risiko depresi mayor pada **RuangRasa** berlandaskan tiga pilar keilmuan:
1. **Validitas Klinis Psikiatri:** Penentuan variabel target bersandar pada instrumen skrining baku **PHQ-9 (Patient Health Questionnaire-9)** dengan ambang skor $\ge 10$ untuk depresi sedang hingga berat pada data survei NHANES.
2. **Representasi Epidemiologi Terbuka (Studi 2024–2026):** Pemanfaatan data survei multi-tahun **CDC NHANES** untuk memprediksi depresi dari faktor tidur, demografi, sosioekonomi, dan tanda vital sebagaimana dikaji pada lima studi terkini (Li et al., 2024; Selvaraj & Mohandoss, 2024; Vu et al., 2025; Salimi et al., 2026; Cui et al., 2026).
3. **Metodologi Machine Learning & Interpretabilitas:** Perbandingan algoritma *Random Forest*, *Logistic Regression*, dan *Decision Tree* dengan validasi silang berstrata 5-fold, seleksi metrik **Macro-F1** pada populasi tidak seimbang, serta analisis *Permutation Importance* dan koefisien logit (Salimi et al., 2026).

---

### II. Tabel Matriks Studi Literatur Komparatif
Format matriks mengacu pada panduan resmi PJBL menggunakan **5 jurnal terbitan terbaru (2024–2026)** yang seluruhnya dapat diakses penuh (*open access*):

| No. | Penulis & Tahun | Permasalahan | Dataset | Metode / Algoritma | Metrik Evaluasi | Hasil Utama | Perbedaan dengan Project Ini |
|:---:|---|---|---|---|---|---|---|
| **1** | **Li, Ai, & Liang (2024)**<br>*Frontiers in Public Health*<br>DOI: [10.3389/fpubh.2023.1348803](https://doi.org/10.3389/fpubh.2023.1348803) | Memprediksi risiko depresi pada orang dewasa AS dengan gangguan tidur (*sleep apnea*). | CDC NHANES (responden dewasa AS, skor PHQ-9). | Pemodelan klasifikasi *Machine Learning* berbasis fitur klinis dan tidur. | Evaluasi performa klasifikasi & diskriminasi model. | Mengonfirmasi hubungan erat antara gangguan tidur, faktor fisiologis, dan risiko depresi pada NHANES. | Berfokus pada subpopulasi *sleep apnea*; proyek ini memodelkan **populasi umum 36.259 responden** dan menyajikannya dalam web app interaktif. |
| **2** | **Selvaraj & Mohandoss (2024)**<br>*Applied Sciences*<br>DOI: [10.3390/app14167366](https://doi.org/10.3390/app14167366) | Meningkatkan deteksi depresi pada data NHANES yang tidak seimbang (~8,08% depresi). | CDC NHANES 2015–2016 (dengan survei SF-36). | *Stacked Ensemble* (DESGM), seleksi fitur, dan *Random Forest Feature Importance*. | Accuracy, F1-Score. | Model DESGM mencapai Accuracy 98,17% dan F1-Score 0,9904. | Menggunakan *stacked ensemble* pada 1 siklus survei; proyek ini menggunakan **7 siklus (2005–2018)** dengan 18 fitur non-invasif & validasi *zero data leakage*. |
| **3** | **Vu, Dawadi, Yamamoto, et al. (2025)**<br>*BMC Medical Informatics and Decision Making*<br>DOI: [10.1186/s12911-025-02903-1](https://doi.org/10.1186/s12911-025-02903-1) | Memprediksi gangguan depresi dari data survei nasional tanpa tes laboratorium invasif. | CDC NHANES 2013–2014 (PHQ-9 $\ge 10$), split 80:20. | Logistic Regression, Random Forest, Naive Bayes, SVM, XGBoost, LightGBM + SHAP. | Accuracy, Sensitivity, Specificity, Precision, AUC, F1-Score. | XGBoost unggul; faktor dominan meliputi rasio pendapatan-kemiskinan, jenis kelamin, hipertensi, BMI, dan pendidikan. | Riset komparasi 6 model tanpa antarmuka web; proyek ini menerapkan **Random Forest terpilih + validasi input biometrik** ke aplikasi Streamlit (**RuangRasa**). |
| **4** | **Salimi, Ghahramani, Zenouz, et al. (2026)**<br>*IBRO Neuroscience Reports*<br>DOI: [10.1016/j.ibneur.2026.08.009](https://doi.org/10.1016/j.ibneur.2026.08.009) | Mengukur keandalan dan interpretabilitas model ML depresi pada populasi survei penuh yang tidak seimbang. | CDC NHANES (37.959 partisipan dengan PHQ-9 valid). | LightGBM, XGBoost, Logistic Regression, Random Forest, SVM + SHAP. | Metrik klasifikasi, kalibrasi, SHAP importance. | Keluhan tidur (*trouble sleeping*) menjadi fitur paling dominan; performa pada populasi penuh lebih moderat dibanding korpus seimbang. | Menggunakan ambang PHQ-9 $\ge 5$; proyek ini memakai ambang klinis **PHQ-9 $\ge 10$**, seleksi **Macro-F1**, dan *Permutation Importance*. |
| **5** | **Cui, Li, & Gong (2026)**<br>*EAI Endorsed Trans. Pervasive Health Technol.*<br>DOI: [10.4108/eetpht.11.11671](https://doi.org/10.4108/eetpht.11.11671) | Memprediksi depresi pada populasi lansia dari data NHANES multi-tahun yang tidak seimbang. | CDC NHANES 2005–2023 (8.760 partisipan usia $\ge 65$, PHQ-9 $\ge 10$). | Stacking Ensemble (RF, XGBoost, SVM, LR), RFE-RF, SMOTE+RUS, dan SHAP. | Metrik klasifikasi & interpretabilitas SHAP. | Menggabungkan seleksi fitur, penyeimbangan kelas, dan SHAP meningkatkan transparansi risiko depresi. | Fokus pada lansia $\ge 65$ tahun; proyek ini mencakup **usia dewasa 18–85 tahun** serta menyediakan prediksi individu, batch CSV, dan edukasi visual. |

---

### III. Kesimpulan Tinjauan Pustaka
1. Instrumen **PHQ-9 ≥ 10** menjadi standar klinis untuk menentukan label *ground truth* depresi sedang hingga berat pada data survei NHANES.
2. Penelitian terbaru tahun 2024–2026 konsisten membuktikan kelayakan **CDC NHANES** untuk pemodelan *machine learning* risiko depresi dengan fitur gaya hidup, tidur, sosioekonomi, dan tanda vital.
3. Ketidakseimbangan kelas (~8–9% depresi) dan keluhan tidur (*trouble sleeping*) merupakan tantangan sekaligus temuan utama di populasi penuh NHANES (Selvaraj & Mohandoss, 2024; Salimi et al., 2026), yang ditangani pada proyek ini melalui `class_weight='balanced'`, seleksi **Macro-F1**, dan analisis *Permutation Importance*.
