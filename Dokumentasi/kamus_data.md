# Kamus Data (Data Dictionary)
## Proyek Skrining Risiko Gangguan Depresi Mayor (CDC NHANES)

Dataset ini bersumber dari survei berkala **Centers for Disease Control and Prevention (CDC) - National Health and Nutrition Examination Survey (NHANES)** periode siklus 2005 hingga 2018. Data telah diproses dan diekstrak menjadi 18 fitur klinis prediktor serta 1 variabel target biner dengan total 36.259 responden.

---

### I. Variabel Target (Dependen)

| Nama Kolom | Tipe Data | Kategori Nilai | Definisi & Relevansi Medis |
|---|---|---|---|
| `Depression` | Kategorikal (Biner) | - `Not Depressed` (Tidak Terindikasi Depresi Mayor)<br>- `Depressed` (Berisiko Depresi Mayor) | Ditentukan dari skor kuesioner **Patient Health Questionnaire-9 (PHQ-9)**.<br>Skor $\ge 10$ diklasifikasikan sebagai `Depressed` (ambang baku klinis depresi sedang hingga berat dengan sensitivitas 88% dan spesifisitas 88%; Kroenke et al., 2001). Skor $< 10$ diklasifikasikan sebagai `Not Depressed`. |

---

### II. Variabel Prediktor: Demografi & Sosioekonomi (Kategorikal & Numerik)

| Nama Kolom | Tipe Data | Satuan / Nilai Kategori | Deskripsi Klinis & Nilai Imputasi |
|---|---|---|---|
| `Age` | Numerik (Diskrit) | Tahun (Rentang: 18 – 85 tahun) | Usia responden saat dilakukan pemeriksaan survei. Faktor risiko demografi karena prevalensi depresi bervariasi pada kelompok usia dewasa muda dan lanjut usia. |
| `Gender` | Kategorikal | - `Female`<br>- `Male` | Jenis kelamin biologis responden. Studi epidemiologi menunjukkan prevalensi depresi klinis pada wanita umumnya hampir dua kali lipat pria. |
| `Education Level` | Kategorikal | - `Less Than 9th Grade`<br>- `9-11th Grade`<br>- `High School`<br>- `Some College or AA Degree`<br>- `College Graduate or Above`<br>- `Missing` | Jenjang pendidikan formal tertinggi responden. Tingkat pendidikan berhubungan erat dengan literasi kesehatan dan stabilitas ekonomi keluarga. |
| `Marital Status` | Kategorikal | - `Married`<br>- `Partner`<br>- `Never Married`<br>- `Divorced`<br>- `Separated`<br>- `Widowed`<br>- `Missing` | Status pernikahan responden. Kehilangan pasangan (perceraian atau kematian pasangan) dikenal sebagai salah satu pemicu stres psikososial terberat. |
| `Household Income` | Kategorikal | - `Below $5K`<br>- `Below $10K`<br>- `Below $15K`<br>- `Below $20K`<br>- `Below $25K`<br>- `Below $35K`<br>- `Below $45K`<br>- `Below $55K`<br>- `Below $65K`<br>- `Below $75K`<br>- `$75K+`<br>- `Over $20K`<br>- `Missing` | Rentang pendapatan kotor tahunan keluarga responden. Ketimpangan dan kesulitan ekonomi secara konsisten terbukti meningkatkan kerentanan depresi. |

---

### III. Variabel Prediktor: Pola Tidur & Riwayat Gangguan Tidur

| Nama Kolom | Tipe Data | Satuan / Nilai Kategori | Deskripsi Klinis & Nilai Imputasi |
|---|---|---|---|
| `Sleep Hours` | Numerik (Kontinu) | Jam per hari (Rentang: 0.0 – 14.5 jam, median: 7.0 jam) | Estimasi rata-rata durasi tidur harian responden pada hari kerja/biasa. Durasi tidur sangat pendek (< 6 jam) atau berlebih (> 9 jam) diasosiasikan dengan gangguan afektif. |
| `Trouble Sleeping History` | Kategorikal (Biner) | - `No`<br>- `Yes` | Riwayat apakah responden pernah mengeluhkan sulit tidur, insomnia berkepanjangan, atau telah berkonsultasi ke dokter terkait gangguan tidur. Merupakan salah satu prediktor depresi terkuat. |

---

### IV. Variabel Prediktor: Gaya Hidup & Aktivitas Fisik

| Nama Kolom | Tipe Data | Satuan / Nilai Kategori | Deskripsi Klinis & Nilai Imputasi |
|---|---|---|---|
| `Sedentary Time` | Numerik (Kontinu) | Menit per hari (Rentang: 0 – 1320 menit, median: 300 menit) | Total waktu yang dihabiskan dalam posisi duduk atau berbaring (di luar waktu tidur) per hari. Perilaku sedentari berkorelasi dengan isolasi sosial dan peradangan sistemik. |
| `Vigorous Recreation` | Kategorikal | - `No`<br>- `Yes`<br>- `Missing` | Partisipasi aktif dalam olahraga berat/intensitas tinggi (menyebabkan peningkatan napas dan denyut jantung secara nyata, misal lari, sepak bola) minimal 10 menit berturut-turut. |
| `Moderate Recreation` | Kategorikal | - `No`<br>- `Yes`<br>- `Missing` | Partisipasi aktif dalam olahraga atau aktivitas rekreasi sedang (misal jalan cepat, bersepeda santai, berenang) minimal 10 menit berturut-turut. |
| `Current Smoker` | Kategorikal | - `Every Day`<br>- `Some Days`<br>- `Never`<br>- `Missing` | Kebiasaan merokok tembakau saat periode survei. Konsumsi nikotin kronis memiliki hubungan timbal balik dengan disregulasi sistem dopaminergik pada depresi. |

---

### V. Variabel Prediktor: Kapasitas Fungsional & Kognisi

| Nama Kolom | Tipe Data | Satuan / Nilai Kategori | Deskripsi Klinis & Nilai Imputasi |
|---|---|---|---|
| `Memory Problems` | Kategorikal (Biner) | - `No`<br>- `Yes` | Responden melaporkan adanya keluhan gangguan daya ingat, sering lupa, atau penurunan konsentrasi dalam kehidupan sehari-hari (disfungsi kognitif umum pada depresi). |
| `Cant Work` | Kategorikal (Biner) | - `No`<br>- `Yes` | Responden menyatakan tidak mampu bekerja akibat masalah kesehatan fisik atau emosional/mental. Indikator disabilitas fungsional berat. |
| `Limited Work` | Kategorikal (Biner) | - `No`<br>- `Yes` | Responden menyatakan adanya keterbatasan jenis pekerjaan atau jumlah beban kerja yang mampu dilakukan akibat masalah kesehatan. |

---

### VI. Variabel Prediktor: Pengukuran Fisiologis & Tanda Vital

| Nama Kolom | Tipe Data | Satuan / Rentang Latih | Deskripsi Klinis & Nilai Imputasi |
|---|---|---|---|
| `BMI` | Numerik (Kontinu) | $kg/m^2$ (Rentang: 0.0 – 86.2, median: 27.8) | Indeks Massa Tubuh (*Body Mass Index*), dihitung dari berat badan (kg) dibagi kuadrat tinggi badan ($m^2$). Obesitas berkaitan dengan peradangan neuro-imunologis. |
| `Systolic` | Numerik (Kontinu) | mmHg (Rentang: 0.0 – 270.0, median: 120.0) | Tekanan darah sistolik pada saat pemeriksaan fisik stasioner NHANES. Nilai 0 menunjukkan data tidak terambil dan diimputasi oleh pipeline. |
| `Diastolic` | Numerik (Kontinu) | mmHg (Rentang: 0.0 – 124.0, median: 70.0) | Tekanan darah diastolik pada saat pemeriksaan fisik stasioner NHANES. |
| `Pulse` | Numerik (Kontinu) | BPM / Detak per menit (Rentang: 0.0 – 224.0, median: 72.0) | Frekuensi denyut nadi istirahat selama 60 detik. Detak jantung istirahat tinggi mencerminkan dominasi aktivitas saraf simpatis saat stres kronis. |

---

### VII. Ringkasan Fitur Menurut Perlakuan Preprocessing

```
Seluruh Fitur (18 Variabel Input)
├── Fitur Numerik (7 variabel) -> Imputasi Median -> Standarisasi Z-score (StandardScaler)
│   ├── Age
│   ├── Sleep Hours
│   ├── Sedentary Time
│   ├── BMI
│   ├── Systolic
│   ├── Diastolic
│   └── Pulse
│
└── Fitur Kategorikal (11 variabel) -> Imputasi Modus -> One-Hot Encoding (OHE)
    ├── Gender (2 kategori)
    ├── Education Level (6 kategori)
    ├── Marital Status (7 kategori)
    ├── Household Income (13 kategori)
    ├── Trouble Sleeping History (2 kategori)
    ├── Vigorous Recreation (3 kategori)
    ├── Moderate Recreation (3 kategori)
    ├── Current Smoker (4 kategori)
    ├── Memory Problems (2 kategori)
    ├── Cant Work (2 kategori)
    └── Limited Work (2 kategori)
```
Total fitur setelah One-Hot Encoding pada data latih: **50 kolom fitur numerik terstandardisasi**.
