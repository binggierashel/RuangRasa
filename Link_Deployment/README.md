# Panduan Deployment Aplikasi Web RuangRasa (Streamlit)

Repositori ini siap dijalankan secara lokal maupun dideploy otomatis dari GitHub ke **Streamlit Community Cloud** (atau **Hugging Face Spaces**).

---

### I. Tautan Proyek & Deployment (Untuk Pengumpulan PJBL)

- **URL Aplikasi Cloud:** `https://ruangrasa.streamlit.app` *(Ganti dengan URL aktif setelah deploy di Streamlit Community Cloud)*
- **URL Repositori GitHub:** `https://github.com/binggierashel/RuangRasa`
- **Video Demo Aplikasi (Google Drive / YouTube):** `https://youtu.be/[link-video-demo]`

---

### II. Demo Web Otomatis via GitHub + Streamlit Community Cloud (Direkomendasikan)

Setiap kali Anda melakukan `git push` ke branch `main`, Streamlit Community Cloud otomatis memperbarui aplikasi web demo.

1. **Pastikan Perubahan Terbaru Sudah di-Push ke GitHub:**
   ```bash
   git add .
   git commit -m "chore: update deployment config and CI workflow"
   git push origin main
   ```

2. **Hubungkan Repositori ke Streamlit Community Cloud:**
   - Buka [share.streamlit.io](https://share.streamlit.io/) dan masuk (*Sign In*) dengan akun GitHub.
   - Klik **"Create app"** / **"Deploy a public app from GitHub"**.
   - Isi konfigurasi berikut:
     - **Repository:** `binggierashel/RuangRasa`
     - **Branch:** `main`
     - **Main file path:** `streamlit_app.py` *(atau `Source_Code/app/streamlit_app.py`)*
     - **App URL (opsional):** `ruangrasa` (menjadi `https://ruangrasa.streamlit.app`)
   - Klik **"Deploy!"**.

3. **Selesai:**
   - Aplikasi akan online dalam 1–3 menit dengan HTTPS aktif (sehingga fitur webcam pada tab **Kamera AI** dapat berjalan).
   - Setiap commit baru yang di-push ke `main` otomatis membangun ulang demo web.

> **Catatan tentang GitHub Pages:** GitHub Pages (`*.github.io`) hanya melayani file statis HTML/JS dan tidak menjalankan server Python (`scikit-learn`, `joblib`, `pandas`), sehingga tidak disarankan untuk aplikasi Streamlit ini.

---

### III. Cara Menjalankan Aplikasi Secara Lokal (Offline)

#### Cara 1: Klik Ganda File Batch (Windows)
- Klik ganda `JALANKAN_APLIKASI.bat` di folder utama proyek.

#### Cara 2: Melalui Terminal / Command Prompt
```bash
cd "D:\KULIAH\sem-5\MACHINE LEARNING\PJBL\RuangRasa"
python -m streamlit run streamlit_app.py
```
Buka browser pada `http://localhost:8501`.
