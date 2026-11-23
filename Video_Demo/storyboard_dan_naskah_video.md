# Panduan Rekaman, Storyboard, dan Naskah Video Demo Aplikasi (Maksimal ≤ 7 Menit)
## Proyek: Sistem Skrining Risiko Gangguan Depresi Mayor (MindScope AI)

Dokumen ini disusun untuk memandu pembuatan video demonstrasi proyek PJBL Machine Learning agar memenuhi seluruh butir penilaian pada rubrik panduan resmi (durasi total: **~6 menit 30 detik**, di bawah batas maksimal 7 menit).

---

### I. Ringkasan Rundown Durasi & Pembagian Narasi

| Segmen | Menit | Durasi | Topik Bahasan | Visual Layar yang Ditampilkan |
|:---:|:---:|:---:|---|---|
| **1** | 00:00 – 00:45 | 45 dtk | Pembukaan, Judul Proyek & Perkenalan Anggota Kelompok | Slide Title / Halaman Informasi Tim di Web App |
| **2** | 00:45 – 01:45 | 60 dtk | Latar Belakang Masalah, Urgensi Medis & Tujuan Proyek | Slide Latar Belakang / Header MindScope |
| **3** | 01:45 – 02:45 | 60 dtk | Dataset CDC NHANES, Eksplorasi Data (EDA) & Preprocessing | Grafik EDA di Web App (`01_distribusi_kelas`, `04_korelasi`) |
| **4** | 02:45 – 04:00 | 75 dtk | Pemodelan 3 Algoritma, CV Tuning & Alasan Pemilihan Model | Tabel Perbandingan Model & Confusion Matrix |
| **5** | 04:00 – 05:45 | 105 dtk | **Demonstrasi Live Aplikasi Streamlit (Individu & Batch CSV)** | **Screen recording interaksi langsung di Web App** |
| **6** | 05:45 – 06:30 | 45 dtk | Interpretasi Faktor Risiko (*XAI*), Kesimpulan & Penutup | Grafik Feature Importance & Penutup |

---

### II. Naskah Narasi Lengkap Per Menit (Script)

#### Segmen 1: Pembukaan & Identitas Kelompok (00:00 – 00:45)
- **Tampilan Visual:** Tampilkan halaman muka presentasi atau buka modul `Tentang` pada aplikasi web Streamlit RuangRasa.
- **Narator 1 (Binggie Rashel Prasetyo):**
  > *"Halo, selamat pagi/siang kepada Bapak/Ibu Dosen Pengampu dan rekan-rekan sekalian. Kami dari Kelompok 11 mempersembahkan proyek tugas besar Machine Learning Semester 5 berjudul:*  
  > **'RuangRasa: Sistem Klasifikasi dan Skrining Risiko Gangguan Depresi Mayor Menggunakan Pendekatan Machine Learning Berbasis Data CDC NHANES'**.*  
  > *Kelompok 11 beranggotakan:*
  > 1. *Bintang Karini Br Padang (J0404241005), bertugas pada bagian Modeling dan evaluasi,*
  > 2. *Binggie Rashel Prasetyo (J0404241009), bertugas pada bagian Dataset, EDA, dan preprocessing,*
  > 3. *Gregorius Gil Ovidio Sebayang (J0404241088), bertugas pada bagian Implementasi aplikasi dan deployment.*  
  > *Mari kita simak latar belakang mengapa proyek ini sangat penting untuk dikembangkan."*

---

#### Segmen 2: Latar Belakang Masalah & Urgensi Klinis (00:45 – 01:45)
- **Tampilan Visual:** Tunjukkan infografis depresi atau cuplikan latar belakang dari `Dokumentasi/laporan_project.md`.
- **Narator 2:**
  > *"Menurut WHO, lebih dari 280 juta orang di dunia menderita depresi mayor. Di Indonesia dan secara global, tantangan terbesarnya adalah rendahnya deteksi dini karena waktu konsultasi dokter layanan primer yang sangat terbatas serta stigma sosial di masyarakat.*  
  > *Padahal, jika terdeteksi sejak awal, penanganan depresi memiliki tingkat keberhasilan terapi yang sangat tinggi.*  
  > *Oleh sebab itu, tujuan utama proyek ini adalah membangun sistem skrining berbasis Machine Learning yang mampu mengidentifikasi risiko depresi secara cepat, objektif, dan non-invasif menggunakan data kebiasaan hidup, pola tidur, dan pengukuran fisik harian.*  
  > *Sebagai landasan medis, kami merujuk pada 5 jurnal internasional ber-DOI aktif, di mana label depresi ditentukan secara ilmiah dari ambang baku kuesioner Patient Health Questionnaire-9 atau PHQ-9 dengan skor lebih besar atau sama dengan 10."*

---

#### Segmen 3: Dataset NHANES, EDA & Preprocessing (01:45 – 02:45)
- **Tampilan Visual:** Buka tab `Eksplorasi Data (EDA)` di Streamlit, scroll grafik distribusi kelas, histogram, dan korelasi.
- **Narator 1:**
  > *"Dataset yang kami gunakan bersumber dari survei resmi CDC NHANES periode 2005 hingga 2018 dengan 36.259 responden riil dan 18 fitur klinis terstruktur.*  
  > *Pada tahap eksplorasi data, kami mendapati tantangan ketidakseimbangan kelas atau class imbalance, di mana 8,7% responden berisiko depresi dan 91,3% tidak depresi.*  
  > *Untuk mencegah data leakage, seluruh data kami bagi terlebih dahulu menjadi 80% data latih (29.007 responden) dan 20% data uji holdout (7.252 responden) secara berstrata.*  
  > *Kemudian, di dalam Scikit-Learn Pipeline, fitur numerik diimputasi median dan distandarisasi Z-score, sedangkan fitur kategorikal diimputasi modus dan diubah melalui One-Hot Encoding. Seluruh fitting transformer dilakukan murni pada data latih."*

---

#### Segmen 4: Pemodelan, K-Fold CV Tuning & Pemilihan Model (02:45 – 04:00)
- **Tampilan Visual:** Buka tab `Evaluasi & Komparasi Model` di Streamlit, tunjukkan tabel perbandingan metrik dan confusion matrix.
- **Narator 2:**
  > *"Sesuai ketentuan PJBL, kami membandingkan tiga algoritma klasifikasi:*
  > 1. *Logistic Regression sebagai baseline linier probabilistik,*
  > 2. *Decision Tree sebagai model pohon keputusan,*
  > 3. *Random Forest sebagai ensemble bagging.*  
  > *Tuning hyperparameter dilakukan menggunakan 5-Fold Stratified Cross-Validation pada data latih dengan metrik seleksi utama Macro-F1 guna memastikan kelas minoritas depresi tidak terabaikan.*  
  > *Hasilnya:*
  > - *Logistic Regression meraih CV Macro-F1: 0,6216,*
  > - *Decision Tree meraih CV Macro-F1: 0,6299,*
  > - *dan **Random Forest** keluar sebagai pemenang dengan CV Macro-F1 tertinggi, yaitu **0,6428**.*  
  > *Pilihan model dikunci berdasarkan performa validasi data latih sebelum menguji data holdout.*  
  > *Pada data uji independen 7.252 baris, Random Forest mempertahankan Test Accuracy 81,76% dan Test Macro-F1 0,6356, serta memiliki Recall depresi 48,74%—tiga kali lebih tinggi dibanding model regresi yang hanya 16,7%."*

---

#### Segmen 5: Demonstrasi Live Aplikasi Web Streamlit (04:00 – 05:45)
- **Tampilan Visual:** Masuk ke tab `Prediksi Individu`, klik tombol `🟢 Muat Contoh Risiko Rendah`, lalu klik `🔴 Muat Contoh Risiko Tinggi`, submit prediksi dan lihat perubahannya. Kemudian pindah ke tab `Prediksi Batch (CSV)`, unggah file `contoh_prediksi.csv`, klik proses, dan unduh hasilnya.
- **Narator 3:**
  > *"Sekarang kita beralih ke demonstrasi langsung aplikasi web MindScope yang dibangun menggunakan Streamlit.*  
  > *Pada menu 'Prediksi Individu', pengguna dapat memasukkan 18 parameter kesehatan yang dikelompokkan ke dalam 5 bagian: demografi, pola tidur, aktivitas fisik, kapasitas kerja/memori, dan tanda vital.*  
  > *Terdapat fitur demo praktis: jika kita klik tombol 'Muat Contoh Risiko Rendah', seluruh input terisi responden dengan tidur cukup dan olahraga rutin. Ketika tombol 'Lakukan Skrining' ditekan, sistem menampilkan badge hijau: 'Tidak Terindikasi Depresi Mayor' dengan probabilitas di atas 90%.*  
  > *Sebaliknya, jika kita muat 'Contoh Risiko Tinggi'—yaitu individu dengan riwayat sulit tidur, tidak mampu bekerja, gangguan memori, dan waktu duduk tinggi—sistem mendeteksi badge merah: 'Berisiko Mengalami Depresi' dengan probabilitas depresi tinggi dan rekomendasi klinis untuk berkonsultasi ke tenaga medis.*  
  > *Selanjutnya pada menu 'Prediksi Batch (CSV)', pengguna dapat mengunduh format template CSV atau mengunggah data ratusan responden sekaligus. Mari kita unggah contoh file CSV 10 responden... klik 'Mulai Prediksi Batch'... dalam sekejap sistem memproses inferensi, menampilkan ringkasan metrik, grafik sebaran, dan tombol unduh hasil CSV lengkap dengan probabilitasnya."*

---

#### Segmen 6: Interpretasi Fitur, Kesimpulan & Penutup (05:45 – 06:30)
- **Tampilan Visual:** Tampilkan grafik `Permutation Feature Importance` pada tab evaluasi, lalu kembali ke slide penutup atau profil tim.
- **Narator 4:**
  > *"Dari segi interpretasi model menggunakan Permutation Importance, faktor paling berpengaruh terhadap risiko depresi secara berurutan adalah: riwayat keluhan tidur kronis (trouble sleeping), disabilitas kerja (cant work), gangguan memori dan konsentrasi (memory problems), serta waktu sedentari harian.*  
  > *Kesimpulannya, proyek ini berhasil membangun sistem skrining depresi yang akurat, transparan, dan teruji secara ketat tanpa kebocoran data.*  
  > *Aplikasi ini kami persembahkan sebagai media edukasi dan skrining dini untuk mendukung kesehatan mental masyarakat.*  
  > *Sekian presentasi dan demonstrasi dari kelompok kami. Terima kasih atas perhatian Bapak/Ibu dosen dan rekan-rekan semua. Salam sehat jiwa!"*

---

### III. Petunjuk Teknis Perekaman Layar (*Screen Recording Tips*)
1. **Perangkat Lunak:** Gunakan OBS Studio (gratis dan tanpa watermark) atau fitur bawaan *Windows Game Bar* (`Win + G`).
2. **Resolusi Rekaman:** Setel resolusi 1920×1080 (Full HD, 30 fps atau 60 fps) dengan rasio aspek 16:9.
3. **Audio:** Gunakan mikrofon headset atau mikrofon eksternal di ruangan hening agar suara narasi terdengar jernih dan bebas gaung.
4. **Kecepatan Mouse & Zoom:** Gerakkan kursor secara tenang dan terarah saat mendemonstrasikan tombol dan formulir di Streamlit; perbesar tampilan browser (100% atau 110%) agar tulisan terbaca tajam.
5. **Verifikasi Durasi:** Pastikan file video final berdurasi antara **5 menit 30 detik hingga 6 menit 45 detik** (tidak melebihi 7 menit).
