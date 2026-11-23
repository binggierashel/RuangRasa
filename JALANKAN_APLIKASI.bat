@echo off
title RuangRasa - Sistem Skrining Depresi Streamlit
color 0A
echo ======================================================================
echo    RUANGRASA: SISTEM SKRINING RISIKO DEPRESI MAYOR (CDC NHANES)
echo             PROYEK PJBL MACHINE LEARNING - SEMESTER 5
echo ======================================================================
echo.
echo Sedang memeriksa lingkungan Python dan dependensi...
python -c "import streamlit, sklearn, pandas, plotly, joblib; print('Dependensi terverifikasi lengkap.')"
if %errorlevel% neq 0 (
    echo [ERROR] Gagal memuat dependensi Python. Pastikan virtual environment aktif.
    pause
    exit /b %errorlevel%
)
echo.
echo Meluncurkan Aplikasi Streamlit di browser default...
echo Tekan Ctrl+C di terminal ini untuk menghentikan aplikasi.
echo ======================================================================
echo.
python -m streamlit run Source_Code\app\streamlit_app.py --server.headless=false
pause
