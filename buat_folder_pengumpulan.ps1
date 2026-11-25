# Membuat folder pengumpulan final PJBL: ML2026_B_Kelompok11_PrediksiGangguanDepresi
# Jalankan dari dalam folder RuangRasa: powershell -ExecutionPolicy Bypass -File .\buat_folder_pengumpulan.ps1

$ErrorActionPreference = "Stop"
$src = $PSScriptRoot
$dst = Join-Path (Split-Path $src -Parent) "ML2026_B_Kelompok11_PrediksiGangguanDepresi"

if (Test-Path $dst) {
    Remove-Item -Recurse -Force $dst
}

$folders = @(
    "01_PPT_Laporan",
    "02_Source_Code",
    "03_Dataset",
    "04_Model",
    "05_Video_Demo",
    "06_Jurnal_Referensi",
    "07_Tabel_Studi_Literatur",
    "08_Link_Deployment",
    "Dokumentasi"
)
foreach ($f in $folders) {
    New-Item -ItemType Directory -Force (Join-Path $dst $f) | Out-Null
}

# 02_Source_Code (salin aplikasi, notebook, laporan, dan tes; buang cache & file sisa)
Copy-Item "$src\streamlit_app.py", "$src\requirements.txt", "$src\README.md", "$src\JALANKAN_APLIKASI.bat" "$dst\02_Source_Code\"
Copy-Item -Recurse "$src\.streamlit" "$dst\02_Source_Code\.streamlit"
Copy-Item -Recurse "$src\Source_Code" "$dst\02_Source_Code\Source_Code"
Get-ChildItem "$dst\02_Source_Code" -Recurse -Force |
    Where-Object { $_.Name -in @("__pycache__", "generate_docx.py", "convert_xpt_to_csv.py") -or $_.Extension -in @(".bak", ".pyc") } |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# 03_Dataset (hanya dataset yang dipakai proyek, tanpa Data_XPT dan Data_Per_Siklus)
Copy-Item -Recurse "$src\Dataset\Data_Asli" "$dst\03_Dataset\Data_Asli"
Copy-Item -Recurse "$src\Dataset\Data_Olahan" "$dst\03_Dataset\Data_Olahan"
Copy-Item "$src\Dataset\template_input.csv", "$src\Dataset\contoh_prediksi.csv" "$dst\03_Dataset\"

# 04_Model
Copy-Item "$src\Model\*" "$dst\04_Model\" -Recurse -Force

# 06_Jurnal_Referensi (5 jurnal terbaru 2024-2026: ringkasan .md dan berkas .pdf)
Get-ChildItem "$src\Referensi_Jurnal" -File |
    Where-Object { $_.Name -ne "tinjauan_pustaka.md" -and $_.Extension -in @(".md", ".pdf") } |
    Copy-Item -Destination "$dst\06_Jurnal_Referensi\" -Force

# 07_Tabel_Studi_Literatur (format Excel)
Copy-Item "$src\Referensi_Jurnal\tabel_studi_literatur.xlsx" "$dst\07_Tabel_Studi_Literatur\" -Force

# 08_Link_Deployment
if (Test-Path "$src\Link_Deployment") {
    Copy-Item "$src\Link_Deployment\*" "$dst\08_Link_Deployment\" -Force
}

# Dokumentasi pendukung
Get-ChildItem "$src\Dokumentasi" -File |
    Where-Object { $_.Extension -in @(".md", ".json", ".docx", ".pdf") } |
    Copy-Item -Destination "$dst\Dokumentasi\" -Force

# 01_PPT_Laporan dan 05_Video_Demo sengaja dibiarkan kosong sampai berkas final siap.
Write-Host "Berhasil membuat struktur folder pengumpulan di: $dst"
