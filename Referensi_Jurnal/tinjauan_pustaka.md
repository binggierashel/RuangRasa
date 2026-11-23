# Tinjauan Pustaka & Matriks Studi Literatur Komparatif
## Proyek Skrining Risiko Gangguan Depresi Mayor (CDC NHANES)

---

### I. Sintesis Teori dan Dasar Keilmuan
Pengembangan sistem prediksi risiko depresi mayor pada proyek ini berlandaskan pada integrasi tiga pilar keilmuan:
1. **Validitas Klinis Psikiatri:** Penentuan variabel target bersandar pada instrumen baku **PHQ-9 (Patient Health Questionnaire-9)** dengan ambang skor $\ge 10$ yang divalidasi oleh Kroenke et al. (2001). Batas ini terbukti memiliki sensitivitas 88% dan spesifisitas 88% untuk Major Depressive Disorder (MDD).
2. **Representasi Epidemiologi Terbuka:** Pemanfaatan data survei multi-tahun **CDC NHANES (National Health and Nutrition Examination Survey)** yang terbukti efektif dalam memetakan interaksi multivariat faktor biologis, kebiasaan tidur, dan gaya hidup terhadap depresi (Dipnall et al., 2016; Pryor et al., 2021).
3. **Metodologi Machine Learning & Explainable AI (XAI):** Pengujian tiga algoritma klasifikasi (Random Forest, Logistic Regression, Decision Tree) dengan validasi silang berstrata 5-fold pada data latih guna mengatasi ketidakseimbangan kelas (*class imbalance*), serta penerapan *Permutation Feature Importance* dan koefisien logit untuk transparansi klinis (Su et al., 2020; Zhang et al., 2022).

---

### II. Tabel Matriks Studi Literatur Komparatif
Format matriks di bawah ini disusun secara sistematis mengacu pada panduan resmi `PJBL-KETENTUAN.txt`:

| No. | Penulis & Tahun | Permasalahan | Dataset | Metode / Algoritma | Metrik Evaluasi | Hasil Utama | Perbedaan dengan Project Ini |
|:---:|---|---|---|---|---|---|---|
| **1** | **Kroenke, Spitzer, & Williams (2001)**<br>DOI: [10.1046/j.1525-1497.2001.016009606.x](https://doi.org/10.1046/j.1525-1497.2001.016009606.x) | Kebutuhan instrumen skrining depresi yang ringkas, reliabel, dan valid untuk layanan kesehatan primer. | 6.000 pasien klinik rawat jalan primer dan obstetri-ginekologi di AS. | Kuesioner psikometrik 9 item skala Likert (PHQ-9) divalidasi wawancara klinis terstruktur. | Sensitivitas, Spesifisitas, Cronbach's $\alpha$, ROC AUC. | Skor $\ge 10$ memiliki sensitivitas 88% dan spesifisitas 88% untuk Major Depressive Disorder; korelasi tinggi dengan hari sakit. | Kroenke et al. memvalidasi instrumen kuisioner secara psikometrik medis; sedangkan proyek ini menggunakan ambang batas tersebut sebagai **label target biner** untuk melatih model machine learning prediktif. |
| **2** | **Dipnall, Pasco, Berk, et al. (2016)**<br>DOI: [10.1371/journal.pone.0148195](https://doi.org/10.1371/journal.pone.0148195) | Mengidentifikasi interaksi multivariat biomarker metabolik, inflamasi, dan gaya hidup terhadap depresi. | CDC NHANES (2007–2010), ribuan responden dewasa di AS. | Hibrida Data Mining, Tree-based Ensemble, dan Generalized Additive Models (GAM). | AUC, Misclassification Rate, P-value signifikansi. | Fitur tidur terganggu, waktu sedentari, BMI, dan merokok menjadi prediktor kuat depresi melebihi biomarker darah tunggal. | Dipnall et al. berfokus pada eksplorasi biomarker laboratorium dan penelitian asosiasi asosiatif; proyek ini menyederhanakan input menjadi **18 fitur klinis non-invasif** yang dapat diakses mandiri oleh pengguna dalam web app interaktif. |
| **3** | **Su, Xu, Pathak, & Wang (2020)**<br>DOI: [10.1001/jamanetworkopen.2020.26414](https://doi.org/10.1001/jamanetworkopen.2020.26414) | Menilai reliabilitas metodologi, risiko *data leakage*, dan keefektifan model ML/DL pada rekam medis kesehatan mental. | Tinjauan sistematis ratusan studi rekam medis elektronik (EHR) dan data survei global. | Systematic Review: Komparasi Tree Ensemble, Linear Models, SVM, dan Deep Neural Networks. | Accuracy, Precision, Recall, Macro-F1, AUROC. | Model tree ensemble dan regularized logistic regression lebih stabil pada tabular terstruktur; menyoroti bahaya kebocoran data (*data leakage*) jika preprocessing tidak dipisah. | Studi Su et al. merupakan tinjauan pustaka sekunder; proyek ini mengimplementasikan rekomendasi mereka secara langsung: **pemisahan pipeline transformasi ketat (zero leakage), 5-Fold Stratified CV, dan metrik seleksi Macro-F1**. |
| **4** | **Pryor, Cowperthwaite, et al. (2021)**<br>DOI: [10.2196/24673](https://doi.org/10.2196/24673) | Memprediksi depresi populasi nasional dari data survei kesehatan publik menggunakan model machine learning. | CDC NHANES ribuan responden dengan instrumen PHQ-9. | Logistic Regression, Decision Tree, Random Forest, XGBoost. | F1-Score, Balanced Accuracy, Precision, Recall, AUC. | Random Forest unggul dalam stabilitas generalisasi; fitur kesulitan tidur, disabilitas kerja, dan kognisi merupakan 3 pilar prediktor teratas. | Pryor et al. mempublikasikan model riset tanpa antarmuka pengguna; proyek ini mengintegrasikan model ke dalam **aplikasi web Streamlit multi-halaman**, mendukung prediksi batch CSV, visualisasi interaktif, dan validasi biologis ketat. |
| **5** | **Zhang, Wang, & Zhao (2022)**<br>DOI: [10.3389/fpsyt.2022.856421](https://doi.org/10.3389/fpsyt.2022.856421) | Memecahkan masalah transparansi (*black-box*) model machine learning depresi agar dapat diterima tenaga medis. | Survei kesehatan cross-sectional berbasis populasi ribuan responden. | Ensemble ML (Random Forest, GBDT) dipadukan dengan Permutation Feature Importance dan SHAP. | Accuracy, F1-Score, Feature Permutation Drop, Odds Ratio. | Interpretasi fitur membuktikan riwayat gangguan tidur dan keterbatasan kerja melipatgandakan *odds* depresi, meningkatkan kepercayaan klinis. | Proyek ini mengadopsi teknik evaluasi Zhang et al. dengan menyertakan grafik **Permutation Importance dan koefisien logit** secara transparan langsung di dashboard web Streamlit dan laporan akademik Word/Markdown. |

---

### III. Kesimpulan Tinjauan Pustaka
Dari telaah kelima jurnal ilmiah di atas:
1. Instrumen PHQ-9 memiliki reliabilitas diagnostik yang sangat kuat sebagai penentu label ground truth.
2. Dataset CDC NHANES memiliki cakupan representatif dengan fitur-fitur non-invasif yang valid.
3. Random Forest terbukti sebagai kandidat algoritma paling kokoh pada data klinis tabular dengan penanganan bobot kelas.
4. Transparansi model melalui *Permutation Importance* menjamin luaran aplikasi dapat dipertanggungjawabkan secara saintifik.
