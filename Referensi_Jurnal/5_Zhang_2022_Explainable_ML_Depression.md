# Ringkasan Artikel Jurnal Ilmiah 5

- **Judul Artikel:** Predicting Depressive Symptoms with Explainable Machine Learning Models
- **Penulis:** Xiaocheng Zhang, Yali Wang, Yifan Zhao
- **Tahun Publikasi:** 2022
- **Nama Jurnal:** *Frontiers in Psychiatry*, Volume 13, Article 856421
- **DOI:** [10.3389/fpsyt.2022.856421](https://doi.org/10.3389/fpsyt.2022.856421)

---

### 1. Masalah Penelitian
Tantangan adopsi machine learning dalam dunia medis klinis sering terhambat oleh sifat kotak hitam (*black-box models*). Dokter dan tenaga kesehatan membutuhkan model yang tidak hanya akurat, tetapi juga dapat diinterpretasikan secara transparan (*explainable artificial intelligence* / XAI).

### 2. Dataset & Responden
Survei kesehatan cross-sectional berbasis populasi dengan ribuan subjek dewasa yang mengevaluasi status kesehatan mental, kebiasaan gaya hidup, dan riwayat kesehatan.

### 3. Metode & Pendekatan XAI
Menggunakan model klasifikasi ensemble (Random Forest, Gradient Boosting) dipadukan dengan teknik interpretasi pascapemodelan seperti *Permutation Feature Importance*, SHAP (*SHapley Additive exPlanations*), dan analisis koefisien logistik.

### 4. Metrik & Hasil Utama
- Permutation Importance membuktikan bahwa mengacak nilai fitur terkait tidur dan keterbatasan aktivitas menghasilkan penurunan terbesar pada metrik diskriminasi model (Macro-F1 dan AUC).
- Koefisien logit menunjukkan arah pengaruh logis: insomnia dan gangguan memori meningkatkan *odds ratio* depresi secara eksponensial, sedangkan status ekonomi memadai dan pendidikan tinggi bertindak sebagai faktor protektif.
- Menunjukkan bahwa interpretasi fitur meningkatkan kepercayaan praktisi medis terhadap luaran sistem kecerdasan buatan dalam skrining layanan primer.

### 5. Kontribusi & Relevansi Langsung terhadap Proyek
- Menjadi rujukan utama metodologi interpretasi model di proyek ini:
  - Implementasi *Permutation Feature Importance* pada model Random Forest terpilih (dihitung khusus pada data latih).
  - Ekstraksi koefisien logit terstandardisasi pada Logistic Regression untuk menjelaskan arah pengaruh faktor risiko di laporan dan dashboard Streamlit.
