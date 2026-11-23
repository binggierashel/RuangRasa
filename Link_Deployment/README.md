# Panduan Deployment Aplikasi Web MindScope (Streamlit)

Repositori ini siap untuk dijalankan baik secara lokal maupun dideploy ke layanan cloud publik seperti **Streamlit Community Cloud**, **Hugging Face Spaces**, atau **Render**.

---

### I. Template Tautan Deployment Publik (Untuk Pengumpulan PJBL)

- **URL Aplikasi Cloud:** `https://ruangrasa.streamlit.app` *(Ganti dengan URL aktif setelah proses deploy di Streamlit Cloud)*
- **URL Repositori GitHub:** `https://github.com/binggierashel/RuangRasa`
- **Video Demo Aplikasi (Google Drive / YouTube):** `https://youtu.be/[link-video-demo]`

---

### II. Panduan Deployment ke Streamlit Community Cloud (Gratis & Mudah)

1. **Inisialisasi Git & Unggah ke GitHub:**
   ```bash
   cd prediksi_gangguan_depresi
   git init
   git add .
   git commit -m "feat: complete depression screening PJBL machine learning system"
   git branch -M main
   git remote add origin https://github.com/[username-kelompok]/prediksi_gangguan_depresi.git
   git push -u origin main
   ```

2. **Daftar & Hubungkan ke Streamlit Community Cloud:**
   - Kunjungi [share.streamlit.io](https://share.streamlit.io/).
   - Masuk (*Sign In*) menggunakan akun GitHub Anda.
   - Klik tombol **"New app"**.

3. **Pengaturan Konfigurasi Aplikasi:**
   - **Repository:** Pilih repositori GitHub Anda (`[username]/prediksi_gangguan_depresi`).
   - **Branch:** `main`
   - **Main file path:** `Source_Code/app/streamlit_app.py`
   - Klik **"Deploy!"**.

4. **Selesai:** Aplikasi akan online dalam waktu 1–2 menit dan mendapatkan URL publik aktif. Salin tautan tersebut ke dokumen laporan akhir Anda.

---

### III. Cara Menjalankan Aplikasi Secara Lokal (Offline)

#### Cara 1: Menggunakan File Batch Windows (Klik Ganda)
- Cukup klik ganda pada file `JALANKAN_APLIKASI.bat` yang terletak di folder utama proyek. Script akan memeriksa dependensi dan otomatis membuka antarmuka Streamlit di browser.

#### Cara 2: Melalui Terminal / Command Prompt
```bash
# Pindah ke direktori proyek
cd D:\KULIAH\sem-5\MACHINE LEARNING\PJBL\prediksi_gangguan_depresi

# Jalankan Streamlit
python -m streamlit run Source_Code/app/streamlit_app.py
```
Aplikasi dapat diakses melalui browser pada alamat lokal: `http://localhost:8501`.
