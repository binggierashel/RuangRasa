# Hasil Eksperimen dan Analisis Model Prediksi Gangguan Depresi

Seluruh metrik dan visualisasi dihasilkan secara riil oleh eksekusi kode eksperimen proyek.

## Ringkasan Data
- Data asli: 36259 responden, 20 kolom awal.
- Setelah seleksi fitur klinis terarah dan pemeriksaan integritas: 36259 baris lengkap dengan 36259 profil independen.
- Pembagian data: 29007 baris data latih (80%) dan 7252 baris data uji holdout (20%) secara berstrata.
- Evaluasi tuning dilakukan via 5-Fold Stratified Cross-Validation pada data latih saja.

## Perbandingan Tiga Model Machine Learning
| Model | CV Macro-F1 ± SD | Train Macro-F1 | Test Accuracy | Test Precision Macro | Test Recall Macro | Test Macro-F1 |
|---|---:|---:|---:|---:|---:|---:|
| logistic_regression | 0.6216 ± 0.0037 | 0.6219 | 0.9152 | 0.7368 | 0.5784 | 0.6075 |
| decision_tree | 0.6299 ± 0.0140 | 0.6572 | 0.9089 | 0.6884 | 0.5850 | 0.6105 |
| random_forest | 0.6428 ± 0.0074 | 0.6999 | 0.8176 | 0.6145 | 0.7346 | 0.6356 |

## Pemilihan Model
- Model terpilih untuk deployment aplikasi adalah **random_forest** dengan CV Macro-F1 tertinggi (0.6428).
- Pilihan model dikunci sebelum data uji dievaluasi, sehingga tidak terjadi kebocoran informasi (*data leakage*).

## Faktor-Faktor Paling Berpengaruh
- Berdasarkan *Permutation Importance* pada data latih model terpilih:
  - **Trouble Sleeping History**: penurunan F1 sebesar 0.0577 ± 0.0012
  - **Age**: penurunan F1 sebesar 0.0225 ± 0.0002
  - **Cant Work**: penurunan F1 sebesar 0.0197 ± 0.0020
  - **Memory Problems**: penurunan F1 sebesar 0.0185 ± 0.0016
  - **Moderate Recreation**: penurunan F1 sebesar 0.0149 ± 0.0021

## Catatan Klinis dan Batasan
- Aplikasi ini bertujuan untuk edukasi dan skrining awal, **bukan alat penegak diagnosis medis resmi**.
- Label depresi berasal dari ambang batas skor kuesioner PHQ-9 (≥ 10) pada survei CDC NHANES.
- Konsultasi langsung dengan psikiater atau psikolog klinis tetap menjadi rujukan utama.
