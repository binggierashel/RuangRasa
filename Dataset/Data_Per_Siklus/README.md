# Dataset CDC NHANES (2005 - 2018) Per Siklus

Dataset survei kesehatan nasional CDC NHANES (*National Health and Nutrition Examination Survey*) dirilis secara berkala dalam siklus 2 tahunan (*2-year survey cycles*). Masing-masing siklus memiliki rentang nomor urut responden (*Respondent Sequence Number* / `SEQN`) yang unik dan terstandarisasi.

Berikut adalah pembagian dataset per siklus dari tahun 2005 hingga 2018 tanpa digabung:

| File | Siklus Survei | Kode Siklus | Rentang SEQN | Total Responden | Not Depressed | Depressed | Prevalensi Depresi (%) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `nhanes_2005_2006.csv` | 2005–2006 | Siklus D | 31131 – 41473 | 4.799 | 4.502 | 297 | 6,19% |
| `nhanes_2007_2008.csv` | 2007–2008 | Siklus E | 41475 – 51623 | 5.415 | 4.892 | 523 | 9,66% |
| `nhanes_2009_2010.csv` | 2009–2010 | Siklus F | 51624 – 62160 | 5.546 | 5.023 | 523 | 9,43% |
| `nhanes_2011_2012.csv` | 2011–2012 | Siklus G | 62161 – 71915 | 4.925 | 4.485 | 440 | 8,93% |
| `nhanes_2013_2014.csv` | 2013–2014 | Siklus H | 73557 – 83727 | 5.372 | 4.861 | 511 | 9,51% |
| `nhanes_2015_2016.csv` | 2015–2016 | Siklus I | 83732 – 93702 | 5.134 | 4.719 | 415 | 8,08% |
| `nhanes_2017_2018.csv` | 2017–2018 | Siklus J | 93705 – 102956 | 5.068 | 4.609 | 459 | 9,06% |
| **Total (Semua Siklus)** | **2005–2018** | **D – J** | **31131 – 102956** | **36.259** | **33.091** | **3.168** | **8,74%** |

### Struktur Kolom (20 Kolom per File)
1. `SEQN`: Respondent Sequence Number (ID unik)
2. `Depression`: Target klasifikasi biner (`Depressed` vs `Not Depressed` berdasarkan PHQ-9 >= 10)
3. 18 Fitur Klinis Prediktor:
   - 7 Fitur Numerik: `Age`, `Sleep Hours`, `Sedentary Time`, `BMI`, `Systolic`, `Diastolic`, `Pulse`
   - 11 Fitur Kategorikal: `Gender`, `Education Level`, `Marital Status`, `Household Income`, `Trouble Sleeping History`, `Vigorous Recreation`, `Moderate Recreation`, `Current Smoker`, `Memory Problems`, `Cant Work`, `Limited Work`
