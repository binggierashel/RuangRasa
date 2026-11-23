"""Pembangun 5 file notebook terpisah dengan kode mandiri dan handoff melalui berkas."""
import argparse
import ast
import json
from pathlib import Path
import textwrap

SOURCE = Path(__file__).resolve().parent
NAMES = [
    "01_persiapan_data.ipynb",
    "02_eksplorasi_data.ipynb",
    "03_preprocessing.ipynb",
    "04_training_model.ipynb",
    "05_evaluasi_dan_ekspor.ipynb",
]


def function_source(text, name, body_only=False):
    node = next(n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef) and n.name == name)
    lines = text.splitlines(keepends=True)
    if body_only:
        return textwrap.dedent("".join(lines[node.body[0].lineno - 1:node.end_lineno]))
    return "".join(lines[node.lineno - 1:node.end_lineno])


def build_notebooks(force=False):
    training = (SOURCE / "train.py").read_text(encoding="utf-8")
    contract = (SOURCE / "depresi_project.py").read_text(encoding="utf-8")
    main = function_source(training, "main", body_only=True)

    def section(start, end):
        return main[main.index(start):main.index(end)].strip()

    setup = textwrap.dedent('''\
        from pathlib import Path
        import hashlib
        import importlib.metadata
        import json
        import platform
        from datetime import datetime, timezone
        import joblib
        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd
        from IPython.display import display, Image, Markdown

        ROOT = next((p for p in [Path.cwd(), *Path.cwd().parents]
                     if (p / 'Dataset/Data_Asli/nhanes_depression_raw.csv').exists()), None)
        if ROOT is None:
            raise FileNotFoundError('Buka notebook dari dalam folder proyek lengkap dengan Dataset.')
    ''')
    setup += contract[contract.index("TARGET = "):contract.index("\ndef prepare_features")]
    setup += training[training.index("SEED = 42"):training.index("\ndef save_json")]
    setup += "\nfor folder in [EDA, MODELING, ANALYSIS, PROCESSED, MODELS]:\n    folder.mkdir(parents=True, exist_ok=True)\nsource = ROOT / 'Dataset/Data_Asli/nhanes_depression_raw.csv'\n"
    setup += function_source(training, "save_json")
    setup += "\ndef save_figure(path):\n    plt.tight_layout()\n    plt.savefig(path, dpi=160, bbox_inches='tight')\n    display(Image(filename=str(path)))\n    plt.close()\n\nprint('Proyek:', ROOT)\n"

    preprocessor = "from sklearn.compose import ColumnTransformer\nfrom sklearn.impute import SimpleImputer\nfrom sklearn.preprocessing import OneHotEncoder, StandardScaler\nfrom sklearn.pipeline import Pipeline\n\n" + function_source(contract, "make_preprocessor")

    load_data = textwrap.dedent('''\
        split_file = PROCESSED / 'notebook_split.json'
        if not split_file.exists():
            raise FileNotFoundError('Jalankan 01_persiapan_data.ipynb terlebih dahulu.')
        split_state = json.loads(split_file.read_text(encoding='utf-8'))
        for relative, expected in split_state['input_hashes'].items():
            if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != expected:
                raise ValueError('Data berubah. Jalankan ulang notebook 01: ' + relative)
        raw = pd.read_csv(source, low_memory=False)
        saved_clean = pd.read_csv(PROCESSED / 'cleaned.csv', low_memory=False)
        clean = saved_clean[FEATURES + [TARGET]].copy()
        ids = saved_clean['source_seqn']
        profile_hashes = saved_clean['profile_hash'] if 'profile_hash' in saved_clean.columns else pd.util.hash_pandas_object(clean[FEATURES], index=False).astype(str)
        conflict_hashes = set()
        duplicate_mask = pd.Series([False] * len(raw))
        X, y = clean[FEATURES], clean[TARGET]
        train_idx, test_idx = split_state['train_indices'], split_state['test_indices']
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        print('Data Latih:', X_train.shape, '| Data Uji:', X_test.shape)
    ''')

    pages = []

    def page(index, title, purpose, prerequisites, outputs):
        cells = []

        def add(kind, content):
            cell = {
                'id': f'stage-{index + 1}-{len(cells):02d}',
                'cell_type': kind,
                'metadata': {},
                'source': (content.strip() + '\n').splitlines(keepends=True)
            }
            if kind == 'code':
                cell.update(execution_count=None, outputs=[])
            cells.append(cell)

        add('markdown', f'# {index + 1:02d}. {title}\n\n{purpose}\n\n'
            f'**Prasyarat:** {prerequisites}\n\n**Keluaran:** {outputs}\n\n'
            'Pilih kernel Python 3.12 dengan dependency proyek, lalu **Restart Kernel → Run All**. '
            'Tahap 01–05 dijalankan secara berurutan. '
            'Proyek edukasi data science, bukan diagnosis medis klinis.')
        add('markdown', '## A. Inisialisasi Lingkungan dan Lokasi Proyek\nMempersiapkan konstanta fitur dan folder kerja.')
        add('code', setup)
        pages.append((index, cells))
        return add

    # Notebook 01
    add = page(0, 'Persiapan dan Pembagian Data',
               'Membaca data survei CDC NHANES, verifikasi kelas target, deduplikasi, dan pembagian train-test 80:20.',
               'Dataset asli tersedia. Tidak memerlukan notebook sebelumnya.',
               '`cleaned.csv`, `train.csv`, `test.csv`, `notebook_split.json`, dan `cv_folds.csv`.')
    add('markdown', '## B. Membaca Dataset Asli\nMemuat 36.259 baris data survei kesehatan dan memeriksa sebaran kelas awal.')
    add('code', section('for folder in [EDA', 'features_all = prepare_features(raw)') + "\ndisplay(raw.head(), raw[TARGET].value_counts())")
    add('markdown', '## C. Pembersihan Fitur dan Integritas Data\nMengekstrak 18 fitur klinis dan memeriksa ada/tidaknya duplikat.')
    add('code', function_source(contract, 'prepare_features') + '\n\n' + section('features_all = prepare_features(raw)', '# Split train-test 80:20 berstrata') + "\nprint('Baris bersih:', len(clean), '| Duplikat:', int(duplicate_mask.sum()))\ndisplay(clean.head())")
    add('markdown', '## D. Pembagian Data Latih dan Uji (80:20 Stratified)\nMengunci pembagian berstrata dengan seed 42 dan menyiapkan 5-fold CV.')
    add('code', 'from sklearn.model_selection import StratifiedKFold, train_test_split\n\n' + section('# Split train-test 80:20 berstrata', '# Laporan EDA dan Kualitas Data') + "\nprint('Train:', len(train_idx), '| Test:', len(test_idx))")
    add('markdown', '## E. Menyimpan State Handoff Antar-Notebook\nMenyimpan indeks dan hash integritas data.')
    add('code', textwrap.dedent('''\
        input_paths = [source, PROCESSED / 'cleaned.csv', PROCESSED / 'train.csv', PROCESSED / 'test.csv']
        split_state = {
            'train_indices': train_idx.tolist(), 'test_indices': test_idx.tolist(),
            'input_hashes': {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in input_paths},
            'seed': SEED,
        }
        save_json(PROCESSED / 'notebook_split.json', split_state)
        print('Tahap 01 Selesai. Lanjut ke 02_eksplorasi_data.ipynb')
    '''))

    # Notebook 02
    add = page(1, 'Eksplorasi Data (EDA)',
               'Analisis statistik deskriptif, missing values, outlier, dan 6 grafik visualisasi eksploratif.',
               'Tahap 01 selesai.', 'Grafik dan laporan statistik di `Source_Code/reports/eda/`.')
    add('markdown', '## B. Memuat Data dari Tahap 01\nMemuat data bersih dan indeks train-test.')
    add('code', load_data)
    add('markdown', '## C. Statistik Deskriptif dan Deteksi Outlier (IQR)\nStatistik outlier dihitung hanya pada data latih.')
    add('code', section('# Laporan EDA dan Kualitas Data', '# 1. Distribusi Kelas') + "\ndisplay(pd.DataFrame(quality), pd.DataFrame(outliers), clean.describe(include='all'))")
    add('markdown', '## D. Enam Grafik Visualisasi EDA\nMenampilkan distribusi target, histogram, boxplot, korelasi, kategori, dan scatter plot.')
    add('code', section('# 1. Distribusi Kelas', '# Model & Hyperparameter Tuning'))

    # Notebook 03
    add = page(2, 'Preprocessing Data',
               'Mempelajari cara imputasi, standardisasi, dan One-Hot Encoding bekerja pada fitur data latih.',
               'Tahap 01 selesai.', '`preview_preprocessing_train.csv` sebagai bahan pembelajaran.')
    add('markdown', '## B. Memuat Data Latih\nData uji tidak disentuh dalam proses fitting transformer.')
    add('code', load_data)
    add('markdown', '## C. Membangun Pipeline Preprocessing\nPipeline menggabungkan SimpleImputer, StandardScaler, dan OneHotEncoder.')
    add('code', preprocessor)
    add('markdown', '## D. Fit dan Transform pada Data Latih (Preview Pembelajaran)\nMenghasilkan matriks fitur ter-encode untuk inspeksi.')
    add('code', textwrap.dedent('''\
        preview_preprocessor = make_preprocessor()
        preview_values = preview_preprocessor.fit_transform(X_train)
        preview_cols = preview_preprocessor.get_feature_names_out()
        preview = pd.DataFrame(preview_values, columns=preview_cols, index=X_train.index)
        print('Fitur sebelum encoding:', X_train.shape[1], '| Setelah encoding:', preview.shape[1])
        display(X_train.head(), preview.head())
        preview.to_csv(PROCESSED / 'preview_preprocessing_train.csv', index_label='clean_index')
        print('Tahap 03 Selesai. Lanjut ke 04_training_model.ipynb')
    '''))

    # Notebook 04
    add = page(3, 'Pelatihan dan Pemilihan Model',
               'Membandingkan 3 algoritma (Logistic Regression, Decision Tree, Random Forest) via 5-Fold Stratified CV.',
               'Tahap 01 selesai.', 'Tiga model terlatih dan `training_notebook_state.json`.')
    add('markdown', '## B. Memuat Data dan Menyusun Fold CV\nHanya data latih yang digunakan untuk tuning.')
    add('code', load_data + '\nfrom sklearn.model_selection import StratifiedKFold, GridSearchCV, cross_validate\ncv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED + 1)\n')
    add('markdown', '## C. Definisi Pipeline Model\nSetiap model digabungkan dengan pipeline preprocessing.')
    add('code', preprocessor + '\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.ensemble import RandomForestClassifier\n')
    add('markdown', '## D. Hyperparameter Tuning via GridSearchCV\nTuning menggunakan metrik evaluasi Macro-F1.')
    add('code', section('definitions = {', '# Kunci pilihan model HANYA') + '\ndisplay(pd.DataFrame(rows))')
    add('markdown', '## E. Mengunci Pilihan Model dari CV Latih\nModel terpilih dikunci sebelum melihat performa data uji.')
    add('code', textwrap.dedent('''\
        selection = max(rows, key=lambda r: r['cv_f1_mean'])['model']
        training_state = {
            'rows': rows, 'selection': selection, 'input_hashes': split_state['input_hashes'],
            'pipeline_hashes': {name: hashlib.sha256((MODELS / f'{name}_pipeline.joblib').read_bytes()).hexdigest() for name in fitted},
        }
        save_json(MODELING / 'training_notebook_state.json', training_state)
        print('Model Terpilih CV:', selection)
        print('Tahap 04 Selesai. Lanjut ke 05_evaluasi_dan_ekspor.ipynb')
    '''))

    # Notebook 05
    add = page(4, 'Evaluasi Holdout, Interpretasi, dan Ekspor',
               'Menguji model pada holdout test set, confusion matrix, analisis faktor, dan ekspor model untuk Streamlit.',
               'Tahap 01, 02, dan 04 selesai.', 'Laporan evaluasi, artefak pipeline terpilih, schema, dan metadata.')
    add('markdown', '## B. Memuat State Pelatihan dari Tahap 04\nMemuat model lokal dan memverifikasi integritas hash.')
    add('code', load_data + textwrap.dedent('''\
        state_file = MODELING / 'training_notebook_state.json'
        if not state_file.exists():
            raise FileNotFoundError('Jalankan 04_training_model.ipynb terlebih dahulu.')
        state = json.loads(state_file.read_text(encoding='utf-8'))
        rows, selection = state['rows'], state['selection']
        fitted = {}
        for name in state['pipeline_hashes']:
            fitted[name] = joblib.load(MODELS / f'{name}_pipeline.joblib')
        summary = json.loads((EDA / 'summary.json').read_text(encoding='utf-8'))
        print('Model Terpilih dari CV:', selection)
    '''))
    add('markdown', '## C. Baseline Dummy dan Fungsi Metrik\nMenghitung metrik perbandingan.')
    add('code', preprocessor + '\nfrom sklearn.dummy import DummyClassifier\nfrom sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay, f1_score, precision_score, recall_score\nfrom sklearn.inspection import permutation_importance\n\n' + function_source(training, 'metrics') + '\n' + section('dummy = Pipeline', 'fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))'))
    add('markdown', '## D. Evaluasi Ketiga Model pada Data Uji Holdout\nConfusion matrix dan classification report.')
    add('code', section('fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))', '# Interpretasi Fitur (pada data latih saja)') + '\ndisplay(results)')
    add('markdown', '## E. Interpretasi Fitur (Permutation Importance & Koefisien Logit)\nMengetahui faktor-faktor yang paling mempengaruhi prediksi.')
    add('code', section('# Interpretasi Fitur (pada data latih saja)', '# Simpan pipeline terpilih tanpa refit') + '\ndisplay(importance.head(10))')
    add('markdown', '## F. Ekspor Pipeline Terpilih, Skema Input, dan Metadata\nMenyimpan artefak final untuk aplikasi Streamlit.')
    analysis_func = function_source(training, 'write_analysis')
    add('code', analysis_func + '\n\n' + main[main.index('# Simpan pipeline terpilih tanpa refit'):])
    add('markdown', '## G. Demonstrasi Prediksi Model Tersimpan\nMenguji prediksi pada beberapa contoh profil.')
    add('code', textwrap.dedent('''\
        sample = pd.read_csv(ROOT / 'Dataset/template_input.csv')
        model = joblib.load(MODELS / 'selected_pipeline.joblib')
        display(sample.assign(Prediksi=model.predict(sample[FEATURES])))
        display(pd.DataFrame(model.predict_proba(sample[FEATURES]), columns=model.classes_))
        print('Semua tahap selesai. Jalankan aplikasi Streamlit: python -m streamlit run Source_Code/app/streamlit_app.py')
    '''))

    for index, cells in pages:
        dest = SOURCE / 'notebooks' / NAMES[index]
        if dest.exists() and not force:
            print('Dipertahankan:', dest.name)
            continue
        nb = {
            'cells': cells,
            'metadata': {
                'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                'language_info': {'name': 'python', 'version': '3.12'}
            },
            'nbformat': 4, 'nbformat_minor': 5
        }
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(nb, indent=2, ensure_ascii=False), encoding='utf-8')
        print('Dibuat:', dest.name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--force', action='store_true', help='Timpa notebook tahap yang sudah ada.')
    build_notebooks(force=parser.parse_args().force)
