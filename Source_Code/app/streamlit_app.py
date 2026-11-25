"""RuangRasa - Skrining Risiko Depresi Berbasis Machine Learning (CDC NHANES).

Fitur: prediksi individu, prediksi batch CSV, eksplorasi data, evaluasi model, informasi proyek.
Jalankan dari folder utama: python -m streamlit run Source_Code/app/streamlit_app.py
"""
import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
SRC_DIR = APP_DIR.parent
ROOT_DIR = SRC_DIR.parent
for _p in (str(SRC_DIR), str(APP_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from depresi_project import DISPLAY, TARGET, make_preprocessor, prepare_features, validate_input  # noqa: E402
from vision_scanner import render_realtime_yolo_scanner  # noqa: E402

APP_NAME = "RuangRasa"
TEAL, RED = "#0F766E", "#B42318"

st.set_page_config(page_title=f"{APP_NAME} | Skrining Risiko Depresi", page_icon="🌿", layout="centered")

css_file = APP_DIR / "styles.css"
if css_file.exists():
    st.markdown(f"<style>{css_file.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


@st.cache_resource
def load_artifacts():
    schema = json.loads((ROOT_DIR / "Model/input_schema.json").read_text(encoding="utf-8"))
    metadata = json.loads((ROOT_DIR / "Model/model_metadata.json").read_text(encoding="utf-8"))
    model_dir = ROOT_DIR / "Model/joblib untuk streamlit"
    if not model_dir.exists():
        model_dir = ROOT_DIR / "Model"
    try:
        models = {
            "Random Forest (terpilih)": joblib.load(model_dir / "random_forest_pipeline.joblib"),
            "Logistic Regression": joblib.load(model_dir / "logistic_regression_pipeline.joblib"),
            "Decision Tree": joblib.load(model_dir / "decision_tree_pipeline.joblib"),
        }
    except Exception:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import Pipeline
        from sklearn.tree import DecisionTreeClassifier

        train_df = pd.read_csv(ROOT_DIR / "Dataset/Data_Olahan/train.csv", low_memory=False)
        X_train = prepare_features(train_df)
        y_train = train_df[TARGET]
        specs = {
            "Random Forest (terpilih)": RandomForestClassifier(
                n_estimators=100, max_depth=10, class_weight="balanced", random_state=42, n_jobs=-1
            ),
            "Logistic Regression": LogisticRegression(C=1.0, max_iter=1000, random_state=42),
            "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=42),
        }
        models = {}
        for name, clf in specs.items():
            pipe = Pipeline([("preprocess", make_preprocessor()), ("model", clf)])
            pipe.fit(X_train, y_train)
            models[name] = pipe
    return schema, metadata, models


try:
    SCHEMA, METADATA, MODELS = load_artifacts()
except Exception as exc:  # noqa: BLE001
    st.error(f"Gagal memuat model: {exc}")
    st.stop()

CAT = SCHEMA["categories"]

# Contoh data untuk demo
DEFAULTS = {
    "Gender": "Female", "Age": 38, "Education Level": "College Graduate or Above",
    "Marital Status": "Married", "Household Income": "$75K+", "Sleep Hours": 7.5,
    "Trouble Sleeping History": "No", "Sedentary Time": 300.0, "Vigorous Recreation": "Yes",
    "Moderate Recreation": "Yes", "Current Smoker": "Never", "Memory Problems": "No",
    "Cant Work": "No", "Limited Work": "No", "BMI": 23.5, "Systolic": 118.0,
    "Diastolic": 76.0, "Pulse": 70.0,
}
HIGH_RISK = {
    "Gender": "Female", "Age": 46, "Education Level": "High School",
    "Marital Status": "Divorced", "Household Income": "Below $15K", "Sleep Hours": 4.5,
    "Trouble Sleeping History": "Yes", "Sedentary Time": 660.0, "Vigorous Recreation": "No",
    "Moderate Recreation": "No", "Current Smoker": "Every Day", "Memory Problems": "Yes",
    "Cant Work": "Yes", "Limited Work": "Yes", "BMI": 33.2, "Systolic": 138.0,
    "Diastolic": 88.0, "Pulse": 88.0,
}


KURS = 16_000  # asumsi kurs USD -> IDR untuk tampilan (perkiraan)

YES_NO = {"Yes": "Ya", "No": "Tidak", "Missing": "Tidak diketahui"}
ID_TEXT = {
    "Gender": {"Female": "Perempuan", "Male": "Laki-laki"},
    "Education Level": {
        "Less Than 9th Grade": "Di bawah kelas 9, belum tamat SMP",
        "9-11th Grade": "Kelas 9-11, SMP akhir sampai SMA",
        "High School": "SMA / sederajat",
        "Some College or AA Degree": "Pernah kuliah / D2-D3",
        "College Graduate or Above": "Lulusan S1 atau lebih tinggi",
        "Missing": "Tidak diketahui",
    },
    "Marital Status": {
        "Married": "Menikah", "Never Married": "Belum pernah menikah",
        "Divorced": "Cerai hidup", "Widowed": "Cerai mati",
        "Separated": "Berpisah", "Partner": "Tinggal bersama pasangan",
        "Missing": "Tidak diketahui",
    },
    "Trouble Sleeping History": YES_NO,
    "Vigorous Recreation": YES_NO,
    "Moderate Recreation": YES_NO,
    "Memory Problems": YES_NO,
    "Cant Work": YES_NO,
    "Limited Work": YES_NO,
    "Current Smoker": {
        "Every Day": "Setiap hari", "Some Days": "Kadang-kadang",
        "Never": "Tidak pernah", "Missing": "Tidak diketahui",
    },
}


def rupiah(usd: float) -> str:
    """Format nilai USD ke rupiah singkat, mis. 75.000 -> 'Rp1,2 miliar'."""
    idr = usd * KURS
    if idr >= 1e9:
        return f"Rp{idr / 1e9:.1f} miliar".replace(".", ",")
    return f"Rp{idr / 1e6:.0f} juta"


def id_label(key: str, value: str) -> str:
    """Tampilkan nilai asli (Inggris) beserta terjemahan Indonesia dalam kurung."""
    if key == "Household Income":
        if value == "Missing":
            return "Missing (Tidak diketahui)"
        digits = "".join(ch for ch in value if ch.isdigit())
        usd = float(digits) * 1000
        if value.endswith("+"):
            return f"{value} (± {rupiah(usd)}+ per tahun)"
        if value.startswith("Below"):
            return f"{value} (di bawah ± {rupiah(usd)} per tahun)"
        if value.startswith("Over"):
            return f"{value} (di atas ± {rupiah(usd)} per tahun)"
        return f"{value} (± {rupiah(usd)} per tahun)"
    translated = ID_TEXT.get(key, {}).get(value)
    return f"{value} ({translated})" if translated else value


def gauge(prob: float) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob * 100,
        number={"suffix": "%", "font": {"size": 42}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 0},
            "bar": {"color": RED if prob >= 0.5 else TEAL, "thickness": 0.28},
            "bgcolor": "#F1F5F9", "borderwidth": 0,
            "threshold": {"line": {"color": "#334155", "width": 2}, "value": 50},
        },
    ))
    fig.update_layout(height=220, margin=dict(l=20, r=20, t=10, b=0), paper_bgcolor="rgba(0,0,0,0)")
    return fig


def show_image(path: Path, caption: str) -> None:
    if path.exists():
        st.image(str(path), caption=caption, width="stretch")


# ------------------------------------------------------------------ Header
st.markdown(
    f"""
    <div class="header">
        <div class="logo">🌿 {APP_NAME}</div>
        <div class="tagline">Skrining awal risiko depresi berbasis machine learning</div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_single, tab_camera, tab_batch, tab_data, tab_about = st.tabs(
    ["Skrining", "Kamera AI", "Batch CSV", "Data", "Tentang"]
)

# Pilihan model (dipakai pada tab Skrining dan Batch)
with st.expander("Pengaturan model", expanded=False):
    model_name = st.selectbox(
        "Algoritma", list(MODELS.keys()), index=0,
        help="Random Forest dipilih berdasarkan Macro-F1 tertinggi pada 5-Fold Stratified CV.",
    )
model = MODELS[model_name]

# ------------------------------------------------------------------ Skrining
with tab_single:
    if "inputs" not in st.session_state:
        st.session_state["inputs"] = dict(DEFAULTS)
        st.session_state["preset_id"] = 0

    c1, c2, c3 = st.columns(3)
    if c1.button("Contoh risiko rendah", width="stretch"):
        st.session_state["inputs"] = dict(DEFAULTS)
        st.session_state["preset_id"] = st.session_state.get("preset_id", 0) + 1
    if c2.button("Contoh risiko tinggi", width="stretch"):
        st.session_state["inputs"] = dict(HIGH_RISK)
        st.session_state["preset_id"] = st.session_state.get("preset_id", 0) + 1
    if c3.button("Reset", width="stretch"):
        st.session_state["inputs"] = dict(DEFAULTS)
        st.session_state["preset_id"] = st.session_state.get("preset_id", 0) + 1
    v = st.session_state["inputs"]
    pid = st.session_state.get("preset_id", 0)

    def pick(col, label, key):
        return col.selectbox(
            label, CAT[key], index=CAT[key].index(v[key]),
            format_func=lambda x: id_label(key, x),
            key=f"sel_{key}_{pid}",
        )

    with st.form("skrining"):
        st.markdown("##### Profil")
        a, b, c = st.columns(3)
        gender = pick(a, "Jenis kelamin", "Gender")
        age = b.number_input("Usia", 18, 100, int(v["Age"]), key=f"num_age_{pid}")
        marital = pick(c, "Status pernikahan", "Marital Status")
        a, b = st.columns(2)
        edu = pick(a, "Pendidikan", "Education Level")
        income = pick(b, "Pendapatan rumah tangga per tahun (USD, ± Rp)", "Household Income")

        st.markdown("##### Tidur & aktivitas")
        a, b = st.columns(2)
        sleep = a.slider("Durasi tidur (jam)", 1.0, 18.0, float(v["Sleep Hours"]), step=0.5, key=f"num_sleep_{pid}")
        trouble = pick(b, "Riwayat gangguan tidur", "Trouble Sleeping History")
        a, b, c, d = st.columns(4)
        sedentary = float(a.slider("Waktu duduk (menit/hari)", 0, 1440, int(v["Sedentary Time"]), step=30, key=f"num_sed_{pid}"))
        vigorous = pick(b, "Olahraga berat", "Vigorous Recreation")
        moderate = pick(c, "Olahraga sedang", "Moderate Recreation")
        smoker = pick(d, "Status merokok", "Current Smoker")

        st.markdown("##### Kondisi fungsional")
        a, b, c = st.columns(3)
        memory = pick(a, "Masalah memori / fokus", "Memory Problems")
        cant = pick(b, "Tidak mampu bekerja", "Cant Work")
        limited = pick(c, "Pekerjaan terbatas", "Limited Work")

        st.markdown("##### Pengukuran tubuh")
        a, b, c, d = st.columns(4)
        bmi = a.slider("BMI", 12.0, 70.0, float(v["BMI"]), step=0.1, key=f"num_bmi_{pid}")
        sys_bp = float(b.slider("Sistolik", 70, 240, int(v["Systolic"]), step=1, key=f"num_sys_{pid}"))
        dia_bp = float(c.slider("Diastolik", 40, 150, int(v["Diastolic"]), step=1, key=f"num_dia_{pid}"))
        pulse = float(d.slider("Nadi (bpm)", 40, 200, int(v["Pulse"]), step=1, key=f"num_pulse_{pid}"))

        submitted = st.form_submit_button("Analisis", type="primary", width="stretch")

    if submitted:
        row = {
            "Gender": gender, "Education Level": edu, "Marital Status": marital,
            "Household Income": income, "Trouble Sleeping History": trouble,
            "Vigorous Recreation": vigorous, "Moderate Recreation": moderate,
            "Current Smoker": smoker, "Memory Problems": memory, "Cant Work": cant,
            "Limited Work": limited, "Age": age, "Sleep Hours": sleep,
            "Sedentary Time": sedentary, "BMI": bmi, "Systolic": sys_bp,
            "Diastolic": dia_bp, "Pulse": pulse,
        }
        try:
            valid = validate_input(pd.DataFrame([row]), SCHEMA)
            pred = model.predict(valid)[0]
            probs = dict(zip(model.classes_, model.predict_proba(valid)[0]))
            p_dep = float(probs.get("Depressed", 0.0))
            st.session_state["last_clinical_prob"] = p_dep
            high = pred == "Depressed"

            st.divider()
            left, right = st.columns([1.1, 1])
            with left:
                st.plotly_chart(gauge(p_dep), width="stretch", config={"displayModeBar": False})
            with right:
                if high:
                    st.markdown('<span class="pill pill-high">Risiko tinggi</span>', unsafe_allow_html=True)
                    st.markdown("#### Terindikasi berisiko depresi")
                    st.write("Profil ini mirip responden dengan skor PHQ-9 ≥ 10. "
                             "Disarankan berkonsultasi dengan psikolog atau tenaga kesehatan.")
                else:
                    st.markdown('<span class="pill pill-low">Risiko rendah</span>', unsafe_allow_html=True)
                    st.markdown("#### Tidak terindikasi berisiko")
                    st.write("Profil ini lebih mirip responden tanpa depresi. "
                             "Jaga kualitas tidur, aktivitas fisik, dan kelola stres.")
            st.caption(f"Model: {model_name}. Garis pada gauge = ambang 50%. "
                       "Hasil ini skrining berbasis model, **bukan diagnosis medis**.")
        except Exception as err:  # noqa: BLE001
            st.error(f"Input tidak valid: {err}")

# ------------------------------------------------------------------ Kamera AI
with tab_camera:
    st.markdown("Deteksi wajah, bukaan mata, dan ekspresi secara langsung sebagai sinyal pendukung.")
    render_realtime_yolo_scanner()
    st.caption(
        "Sinyal visual ini hanya indikator pendukung terkait kelelahan tidur dan afek, "
        "**bukan diagnosis medis**."
    )

    st.markdown("##### Arsitektur deteksi visual")
    vision_spec = pd.DataFrame([
        {
            "Komponen": "Deteksi wajah",
            "Model / Metode": "TinyFaceDetector (Tiny-YOLOv2)",
            "Fungsi": "Mendeteksi kotak wajah (bounding box) dan confidence score secara real-time di browser.",
        },
        {
            "Komponen": "Titik anatomi & mata",
            "Model / Metode": "FaceLandmark68TinyNet + Eye Aspect Ratio (EAR)",
            "Fungsi": "Memetakan 68 titik wajah untuk mengukur bukaan kelopak mata sebagai indikator kelelahan/kurang tidur.",
        },
        {
            "Komponen": "Klasifikasi ekspresi",
            "Model / Metode": "FaceExpressionNet (CNN)",
            "Fungsi": "Mengukur proporsi ekspresi netral (afek datar) serta mikro-ekspresi sedih/tegang.",
        },
    ])
    st.dataframe(vision_spec, hide_index=True, width="stretch")

# ------------------------------------------------------------------ Batch
with tab_batch:
    st.markdown("Unggah CSV berisi banyak responden untuk diprediksi sekaligus.")
    d1, d2 = st.columns(2)
    template = ROOT_DIR / "Dataset/template_input.csv"
    sample = ROOT_DIR / "Dataset/contoh_prediksi.csv"
    if template.exists():
        d1.download_button("Unduh template CSV", template.read_bytes(), "template_input.csv",
                           "text/csv", width="stretch")
    if sample.exists():
        d2.download_button("Unduh contoh data (10 baris)", sample.read_bytes(), "contoh_prediksi.csv",
                           "text/csv", width="stretch")

    with st.expander("Panduan nilai kolom CSV (Inggris dan artinya)"):
        rows = [
            {"Kolom": k, "Nilai CSV": val, "Arti": id_label(k, val)}
            for k in ["Gender", "Education Level", "Marital Status", "Household Income",
                      "Trouble Sleeping History", "Current Smoker"]
            for val in CAT[k]
        ]
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
        st.caption(f"Konversi rupiah memakai kurs perkiraan 1 USD = Rp{KURS:,}".replace(",", "."))

    up = st.file_uploader("Berkas CSV", type=["csv"], label_visibility="collapsed")
    if up is not None:
        try:
            df = pd.read_csv(up)
            st.caption(f"{df.shape[0]:,} baris × {df.shape[1]} kolom")
            st.dataframe(df.head(10), width="stretch")
            if st.button("Jalankan prediksi", type="primary", width="stretch"):
                with st.spinner("Memproses..."):
                    valid = validate_input(df, SCHEMA)
                    preds = model.predict(valid)
                    probs = model.predict_proba(valid)
                    out = df.copy()
                    out["Prediksi"] = preds
                    for i, cls in enumerate(model.classes_):
                        out[f"Peluang_{cls}"] = np.round(probs[:, i], 4)
                n_dep = int((preds == "Depressed").sum())
                m1, m2, m3 = st.columns(3)
                m1.metric("Total", f"{len(preds):,}")
                m2.metric("Berisiko", f"{n_dep:,}", f"{n_dep / len(preds) * 100:.1f}%", delta_color="off")
                m3.metric("Tidak berisiko", f"{len(preds) - n_dep:,}")
                st.dataframe(out, width="stretch")
                st.download_button("Unduh hasil (CSV)", out.to_csv(index=False).encode("utf-8"),
                                   "hasil_prediksi.csv", "text/csv", width="stretch")
        except Exception as err:  # noqa: BLE001
            st.error(f"Gagal memproses CSV: {err}")

# ------------------------------------------------------------------ Data
with tab_data:
    eda = SRC_DIR / "reports/eda"
    rep_data = SRC_DIR / "reports/modeling"
    summary = eda / "summary.json"
    if summary.exists():
        s = json.loads(summary.read_text(encoding="utf-8"))
        m1, m2, m3 = st.columns(3)
        m1.metric("Responden", f"{s['clean_rows']:,}")
        m2.metric("Fitur", s["model_features"])
        m3.metric("Berisiko depresi", f"{s['class_counts_raw'].get('Depressed', 0) / s['clean_rows'] * 100:.1f}%")
    st.caption("Sumber: CDC NHANES 2005-2018. Label depresi: skor PHQ-9 ≥ 10. "
               "Kelas sangat tidak seimbang, sehingga model dipilih dengan Macro-F1.")

    opt = st.radio(
        "Visualisasi",
        [
            "Distribusi kelas",
            "Sebaran numerik",
            "Outlier",
            "Korelasi",
            "Fitur kategorikal",
            "Confusion matrix",
            "Perbandingan 3 algoritma",
            "Faktor berpengaruh",
        ],
        horizontal=True, label_visibility="collapsed",
    )
    if opt == "Distribusi kelas":
        show_image(eda / "01_distribusi_kelas.png", "Distribusi label depresi pada data latih dan uji")
    elif opt == "Sebaran numerik":
        show_image(eda / "02_histogram_train.png", "Histogram fitur numerik (data latih)")
    elif opt == "Outlier":
        show_image(eda / "03_boxplot_train.png", "Boxplot fitur numerik; outlier IQR dipertahankan")
        out_file = eda / "outliers_train.csv"
        if out_file.exists():
            st.dataframe(pd.read_csv(out_file), width="stretch")
    elif opt == "Korelasi":
        show_image(eda / "04_korelasi_train.png", "Matriks korelasi Pearson antarfitur numerik")
    elif opt == "Fitur kategorikal":
        show_image(eda / "05_kategorikal_train.png", "Proporsi depresi per kategori kunci")
        show_image(eda / "06_scatter_train.png", "Usia vs jam tidur")
    elif opt == "Confusion matrix":
        show_image(rep_data / "01_confusion_matrices.png", "Confusion matrix ketiga algoritma pada data uji (N = 7.252)")
        st.markdown("##### Tabel Evaluasi Matrix (Data Uji, N = 7.252)")
        matrix_rows = []
        for m_key, m_label in [
            ("random_forest", "Random Forest (Terpilih)"),
            ("decision_tree", "Decision Tree"),
            ("logistic_regression", "Logistic Regression"),
        ]:
            pred_file = rep_data / f"predictions_{m_key}.csv"
            cr_file = rep_data / f"classification_report_{m_key}.json"
            if pred_file.exists() and cr_file.exists():
                p_df = pd.read_csv(pred_file, usecols=["actual", "predicted"])
                cr = json.loads(cr_file.read_text(encoding="utf-8"))
                tp = int(((p_df["actual"] == "Depressed") & (p_df["predicted"] == "Depressed")).sum())
                fn = int(((p_df["actual"] == "Depressed") & (p_df["predicted"] == "Not Depressed")).sum())
                fp = int(((p_df["actual"] == "Not Depressed") & (p_df["predicted"] == "Depressed")).sum())
                tn = int(((p_df["actual"] == "Not Depressed") & (p_df["predicted"] == "Not Depressed")).sum())
                dep = cr.get("Depressed", {})
                macro = cr.get("macro avg", {})
                matrix_rows.append({
                    "Model": m_label,
                    "TP": tp,
                    "FN": fn,
                    "FP": fp,
                    "TN": tn,
                    "Precision (Depressed)": dep.get("precision", 0.0),
                    "Recall (Depressed)": dep.get("recall", 0.0),
                    "F1 (Depressed)": dep.get("f1-score", 0.0),
                    "Accuracy": cr.get("accuracy", 0.0),
                    "Macro-F1": macro.get("f1-score", 0.0),
                })
        if matrix_rows:
            df_mat = pd.DataFrame(matrix_rows)
            float_cols = ["Precision (Depressed)", "Recall (Depressed)", "F1 (Depressed)", "Accuracy", "Macro-F1"]
            st.dataframe(
                df_mat.style.format({c: "{:.4f}" for c in float_cols})
                .highlight_max(subset=["TP", "Recall (Depressed)", "F1 (Depressed)", "Macro-F1"], color="#CCFBF1"),
                hide_index=True,
                width="stretch",
            )
            st.caption("TP = Depresi terdeteksi benar · FN = Depresi luput · FP = Tidak depresi diprediksi depresi · TN = Tidak depresi terdeteksi benar.")
    elif opt == "Perbandingan 3 algoritma":
        show_image(rep_data / "02_model_comparison.png", "Perbandingan kinerja 3 algoritma (CV Macro-F1, Test Macro-F1, dan Accuracy)")
        comp_data = rep_data / "model_comparison.csv"
        if comp_data.exists():
            df_cmp = pd.read_csv(comp_data)[["model", "cv_f1_mean", "cv_f1_std", "train_f1_macro", "test_accuracy",
                                             "test_precision_macro", "test_recall_macro", "test_f1_macro"]]
            df_cmp.columns = ["Model", "CV Macro-F1", "CV Std", "Train Macro-F1", "Accuracy",
                              "Precision", "Recall", "Test Macro-F1"]
            st.dataframe(df_cmp.style.format({c: "{:.4f}" for c in df_cmp.columns[1:]})
                         .highlight_max(subset=["CV Macro-F1", "Test Macro-F1"], color="#CCFBF1"),
                         hide_index=True, width="stretch")
        st.caption("Model dipilih dari Macro-F1 validasi silang, bukan dari accuracy. "
                   "Accuracy tinggi pada kelas mayoritas (91%) menyesatkan.")
    else:
        ana_data = SRC_DIR / "reports/analysis"
        show_image(ana_data / "02_permutation_importance.png", "Permutation importance (Random Forest)")
        show_image(ana_data / "03_logistic_coefficients.png", "Koefisien Logistic Regression")
        st.markdown("Faktor teratas: riwayat gangguan tidur, usia, ketidakmampuan bekerja, dan masalah memori.")

# ------------------------------------------------------------------ Tentang
with tab_about:
    st.markdown(
        f"**{APP_NAME}** adalah proyek PJBL Machine Learning (Semester 5) untuk skrining awal risiko "
        "depresi dari data survei kesehatan CDC NHANES. Aplikasi ini bukan alat diagnosis."
    )
    ident_file = ROOT_DIR / "Dokumentasi/identitas_kelompok.json"
    anggota = None
    if ident_file.exists():
        ident = json.loads(ident_file.read_text(encoding="utf-8"))
        anggota = ident.get("anggota")
    if not anggota:
        anggota = [
            {
                "No": 1,
                "Nama": "Bintang Karini Br Padang",
                "NIM": "J0404241005",
                "Pembagian Tugas": "Modeling dan evaluasi",
            },
            {
                "No": 2,
                "Nama": "Binggie Rashel Prasetyo",
                "NIM": "J0404241009",
                "Pembagian Tugas": "Dataset, EDA, dan preprocessing",
            },
            {
                "No": 3,
                "Nama": "Gregorius Gil Ovidio Sebayang",
                "NIM": "J0404241088",
                "Pembagian Tugas": "Implementasi aplikasi dan deployment",
            },
        ]
    st.markdown("##### Tim (Kelompok 11 — Kelas B)")
    st.dataframe(pd.DataFrame(anggota), hide_index=True, width="stretch")

    st.markdown("##### Referensi")
    refs = [
        ("Li, Ai & Liang (2024). A machine learning model to predict the risk of depression in US adults with obstructive sleep apnea hypopnea syndrome. Front Public Health.", "10.3389/fpubh.2023.1348803"),
        ("Selvaraj & Mohandoss (2024). Enhancing Depression Detection: A Stacked Ensemble Model with Feature Selection and RF Feature Importance Analysis Using NHANES Data. Appl Sci.", "10.3390/app14167366"),
        ("Vu et al. (2025). Prediction of depressive disorder using machine learning approaches: findings from the NHANES. BMC Med Inform Decis Mak.", "10.1186/s12911-025-02903-1"),
        ("Salimi et al. (2026). Interpretable machine learning for depression symptom classification in NHANES. IBRO Neurosci Rep.", "10.1016/j.ibneur.2026.08.009"),
        ("Cui, Li & Gong (2026). An Interpretable Stacking Ensemble Model with SHAP for Geriatric Depression Prediction: Analysis of the NHANES 2005-2023 Database. EAI Endorsed Trans Pervasive Health Technol.", "10.4108/eetpht.11.11671"),
    ]
    for i, (text, doi) in enumerate(refs, 1):
        st.markdown(f"{i}. {text} [{doi}](https://doi.org/{doi})")

    st.markdown("##### Spesifikasi")
    pk = METADATA.get("packages", {})
    st.markdown(
        f"- Python {METADATA.get('python', '-')}, scikit-learn {pk.get('scikit-learn', '-')}\n"
        f"- Split stratified 80:20, validasi 5-Fold Stratified CV\n"
        f"- Model terpilih: **{METADATA.get('selected_model', 'Random Forest')}**"
    )

st.markdown(
    f'<div class="footer">{APP_NAME} · PJBL Machine Learning 2026 · Data: CDC NHANES · '
    "Bukan pengganti diagnosis medis</div>",
    unsafe_allow_html=True,
)
