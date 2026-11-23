# Ringkasan Artikel Jurnal Ilmiah 1

- **Judul Artikel:** The PHQ-9: Validity of a Brief Depression Severity Measure
- **Penulis:** Kurt Kroenke, Robert L. Spitzer, Janet B. W. Williams
- **Tahun Publikasi:** 2001
- **Nama Jurnal:** *Journal of General Internal Medicine*, Volume 16, Issue 9, Halaman 606–613
- **DOI:** [10.1046/j.1525-1497.2001.016009606.x](https://doi.org/10.1046/j.1525-1497.2001.016009606.x)

---

### 1. Masalah Penelitian
Kebutuhan mendesak di layanan kesehatan primer akan instrumen skrining depresi yang ringkas, memiliki validitas psikometrik tinggi, serta dapat diisi mandiri oleh pasien untuk menilai derajat keparahan depresi mayor berdasarkan kriteria diagnostik DSM-IV.

### 2. Dataset & Responden
Studi melibatkan 6.000 pasien (3.000 pasien dari 8 klinik rawat jalan layanan primer dan 3.000 pasien dari 7 klinik obstetri-ginekologi di Amerika Serikat).

### 3. Metode & Validasi
Validasi kriteria dilakukan dengan membandingkan skor PHQ-9 (9 item dengan skala Likert 0–3, skor total 0–27) terhadap wawancara psikiatri terstruktur terstandar oleh profesional kesehatan mental independen.

### 4. Metrik & Hasil Utama
- Pada skor ambang batas $\ge 10$, instrumen PHQ-9 menghasilkan **sensitivitas 88%** dan **spesifisitas 88%** untuk diagnosis *Major Depressive Disorder* (MDD).
- Konsistensi internal sangat baik dengan Cronbach's $\alpha = 0.89$ pada layanan primer dan $\alpha = 0.86$ pada klinik ob-gyn.
- Korelasi kuat terbukti antara skor PHQ-9 dan disabilitas fungsional (SF-20), hari tidak masuk kerja (*sick days*), dan pemanfaatan fasilitas kesehatan.

### 5. Kontribusi & Relevansi Langsung terhadap Proyek
Makalah ini menjadi landasan klinis ilmiah penentuan variabel target pada proyek ini:
- Kolom target `Depression` pada dataset CDC NHANES diturunkan dari kuesioner PHQ-9.
- Batas skor $\ge 10$ dijadikan ambang pemisah kelas biner (`Depressed` vs `Not Depressed`), menjamin bahwa target klasifikasi memiliki dasar pembuktian empiris kedokteran yang sah dan diakui secara global.
