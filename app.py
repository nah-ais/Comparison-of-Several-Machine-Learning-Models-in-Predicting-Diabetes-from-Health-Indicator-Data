import streamlit as st
import pandas as pd
import pickle
import time
import random
import streamlit.components.v1 as components

# ======================================================
# LOAD MODEL
# ======================================================
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# ======================================================
# MODEL ACCURACY (REAL FROM NOTEBOOK)
# ======================================================
MODEL_ACCURACY = 0.850776568905708

# ======================================================
# FEATURES
# ======================================================
FEATURES = [
    'HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke',
    'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies',
    'HvyAlcoholConsump', 'GenHlth', 'MentHlth', 'PhysHlth', 'DiffWalk',
    'Sex', 'Age'
]

# ======================================================
# QUOTES
# ======================================================
QUOTES = [
    "Langkah kecil menuju hidup sehat lebih baik daripada tidak melangkah sama sekali. 💚",
    "Tubuh sehat dimulai dari keputusan kecil setiap hari.",
    "Jaga kesehatanmu — itu aset paling berharga yang kamu punya. 🌿",
    "Tetap semangat! Perubahan besar dimulai dari niat kecil. 💪",
    "Kesehatan adalah perjalanan, bukan tujuan."
]

# ======================================================
# STREAMLIT PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Diabetes Health Risk Predictor",
    page_icon="🩺",
    layout="centered"
)

# ======================================================
# CSS FIX FOR DARK MODE + GLASS CARD
# ======================================================
st.markdown("""
<style>
.title {
    font-size: 32px;
    font-weight: 800;
    color: #8ab4f8;
    text-align: center;
    margin-bottom: 5px;
}
.subtitle {
    font-size: 16px;
    color: #b0b8c2;
    text-align: center;
    margin-bottom: 30px;
}
.stCard {
    background-color: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(8px);
    padding: 25px 30px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.18);
    margin-bottom: 20px;
}
label {
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# SIDEBAR TEMPLATE INPUT
# ======================================================
st.sidebar.title("🎯 Template Input")
st.sidebar.write("Pilih salah satu template untuk auto-fill:")

templates = {
    "Sehat / Low Risk": {
        'HighBP': 0, 'HighChol': 0, 'CholCheck': 1, 'BMI': 23,
        'Smoker': 0, 'Stroke': 0, 'HeartDiseaseorAttack': 0,
        'PhysActivity': 1, 'Fruits': 1, 'Veggies': 1,
        'HvyAlcoholConsump': 0, 'GenHlth': 2,
        'MentHlth': 1, 'PhysHlth': 1, 'DiffWalk': 0,
        'Sex': 1, 'Age': 28
    },

    "Pre-Diabetes / Medium Risk": {
        'HighBP': 1, 'HighChol': 1, 'CholCheck': 1, 'BMI': 30,
        'Smoker': 1, 'Stroke': 0, 'HeartDiseaseorAttack': 0,
        'PhysActivity': 0, 'Fruits': 0, 'Veggies': 1,
        'HvyAlcoholConsump': 1, 'GenHlth': 3,
        'MentHlth': 4, 'PhysHlth': 6, 'DiffWalk': 0,
        'Sex': 0, 'Age': 43
    },

    "Diabetes / High Risk": {
        'HighBP': 1, 'HighChol': 1, 'CholCheck': 1, 'BMI': 42,
        'Smoker': 1, 'Stroke': 1, 'HeartDiseaseorAttack': 1,
        'PhysActivity': 0, 'Fruits': 0, 'Veggies': 0,
        'HvyAlcoholConsump': 1, 'GenHlth': 5,
        'MentHlth': 14, 'PhysHlth': 25, 'DiffWalk': 1,
        'Sex': 1, 'Age': 62
    }
}

selected_template = st.sidebar.selectbox(
    "Pilih template:",
    ["Tidak ada", *templates.keys()]
)

# ======================================================
# HEADER
# ======================================================
st.markdown('<p class="title">🩺 Diabetes Health Risk Predictor</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Prediksi risiko diabetes berdasarkan indikator kesehatan Anda</p>', unsafe_allow_html=True)

# ======================================================
# MOTIVATIONAL QUOTE CARD
# ======================================================
st.markdown('<div class="stCard">', unsafe_allow_html=True)
st.subheader("✨ Motivasi Hari Ini")
st.write(random.choice(QUOTES))
st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# INPUT FORM
# ======================================================
prefill = templates.get(selected_template, None)

st.markdown('<div class="stCard">', unsafe_allow_html=True)
st.subheader("Masukkan Data Kesehatan:")

col1, col2 = st.columns(2)
user_input = {}

for i, feature in enumerate(FEATURES):
    with (col1 if i % 2 == 0 else col2):
        user_input[feature] = st.number_input(
            feature,
            value=float(prefill[feature]) if prefill else 0.0,
        )

input_df = pd.DataFrame([user_input], columns=FEATURES)

st.markdown('</div>', unsafe_allow_html=True)


# ======================================================
# PREDICTION LOGIC
# ======================================================
if st.button("🔍 Prediksi Sekarang"):

    with st.spinner("Menghitung prediksi..."):
        time.sleep(1.3)

        pred = model.predict(input_df)[0]
        probs = model.predict_proba(input_df)[0]

    label_map = {0: "Tidak Diabetes", 1: "Pre-Diabetes", 2: "Diabetes"}
    colors = {0: "#4ade80", 1: "#facc15", 2: "#f87171"}

    # HTML Result Rendering

    html_result = f"""
    <div style="
        background-color: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(8px);
        padding: 25px;
        border-radius: 16px;
        border-left: 6px solid {colors[pred]};
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-top: 20px;
        font-family: 'Segoe UI', sans-serif;
        color: #e2e8f0;
    ">
        
        <h2 style="color:{colors[pred]}; text-align:center; font-weight:700; margin-bottom:5px;">
            {label_map[pred]}
        </h2>

        <p style="text-align:center; font-size:16px;">
            Akurasi model: <b>{MODEL_ACCURACY * 100:.2f}%</b>
        </p>

        <p style="text-align:center; font-size:14px; margin-top:15px;">
            <b>Probabilitas Prediksi:</b><br>
            Tidak Diabetes: {probs[0]:.3f}<br>
            Pre-Diabetes: {probs[1]:.3f}<br>
            Diabetes: {probs[2]:.3f}
        </p>

        <p style="text-align:center; font-size:12px; margin-top:15px; color:#cbd5e1;">
            *Prediksi ini hanya estimasi berbasis data. Untuk hasil yang lebih pasti, konsultasikan dengan tenaga kesehatan.*
        </p>

    </div>
    """

    components.html(html_result, height=350)
