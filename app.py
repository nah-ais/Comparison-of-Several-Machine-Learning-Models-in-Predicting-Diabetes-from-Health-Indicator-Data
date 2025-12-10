import streamlit as st
import pandas as pd
import pickle
import time

# ======================================================
# LOAD MODEL
# ======================================================
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# ======================================================
# FEATURE LIST (SAME AS TRAINING)
# ======================================================
FEATURES = [
    'HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke',
    'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies',
    'HvyAlcoholConsump', 'GenHlth', 'MentHlth', 'PhysHlth', 'DiffWalk',
    'Sex', 'Age'
]

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Diabetes Prediction",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ======================================================
# AESTHETIC CSS
# ======================================================
st.markdown("""
<style>
.stCard {
    background-color: rgba(255, 255, 255, 0.08); 
    padding: 25px 30px;
    border-radius: 18px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    border: 1.5px solid #e2e8f0;
}
.title {
    font-size: 32px;
    font-weight: 700;
    color: #1f4e79;
    text-align: center;
    margin-bottom: 5px;
}
.subtitle {
    font-size: 16px;
    color: #4a5568;
    text-align: center;
    margin-bottom: 25px;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# SIDEBAR
# ======================================================
st.sidebar.title("ℹ️ Panduan Input")
st.sidebar.write("""
Pilih salah satu template untuk mengisi form secara otomatis  
atau masukkan angka Anda sendiri.
""")

# ======================================================
# TEMPLATE DATA
# ======================================================
templates = {
    "Sehat / Low Risk": {
        'HighBP': 0, 'HighChol': 0, 'CholCheck': 1, 'BMI': 23,
        'Smoker': 0, 'Stroke': 0, 'HeartDiseaseorAttack': 0,
        'PhysActivity': 1, 'Fruits': 1, 'Veggies': 1,
        'HvyAlcoholConsump': 0, 'GenHlth': 2,
        'MentHlth': 1, 'PhysHlth': 1, 'DiffWalk': 0,
        'Sex': 1, 'Age': 30
    },

    "Pre-Diabetes / Medium Risk": {
        'HighBP': 1, 'HighChol': 1, 'CholCheck': 1, 'BMI': 30,
        'Smoker': 1, 'Stroke': 0, 'HeartDiseaseorAttack': 0,
        'PhysActivity': 0, 'Fruits': 0, 'Veggies': 1,
        'HvyAlcoholConsump': 1, 'GenHlth': 3,
        'MentHlth': 5, 'PhysHlth': 7, 'DiffWalk': 0,
        'Sex': 0, 'Age': 45
    },

    "Diabetes / High Risk": {
        'HighBP': 1, 'HighChol': 1, 'CholCheck': 1, 'BMI': 37,
        'Smoker': 1, 'Stroke': 1, 'HeartDiseaseorAttack': 1,
        'PhysActivity': 0, 'Fruits': 0, 'Veggies': 0,
        'HvyAlcoholConsump': 1, 'GenHlth': 4,
        'MentHlth': 10, 'PhysHlth': 15, 'DiffWalk': 1,
        'Sex': 1, 'Age': 60
    }
}

st.sidebar.subheader("🎯 Template Cepat")
selected_template = st.sidebar.selectbox(
    "Pilih contoh data:",
    ["Tidak ada", "Sehat / Low Risk", "Pre-Diabetes / Medium Risk", "Diabetes / High Risk"]
)

# ======================================================
# HEADER
# ======================================================
st.markdown('<p class="title">🩺 Diabetes Health Risk Predictor</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Prediksi risiko diabetes berdasarkan indikator kesehatan</p>', unsafe_allow_html=True)

st.markdown('<div class="stCard">', unsafe_allow_html=True)

# ======================================================
# INPUT AREA
# ======================================================
st.subheader("Masukkan Data Kesehatan:")

col1, col2 = st.columns(2)
user_input = {}

# Jika template dipilih, gunakan template
prefill = templates[selected_template] if selected_template in templates else None

for i, feature in enumerate(FEATURES):
    with (col1 if i % 2 == 0 else col2):
        default_value = prefill[feature] if prefill else 0.0
        user_input[feature] = st.number_input(
            f"{feature}",
            value=float(default_value),
            help=f"Masukkan nilai untuk {feature}"
        )

st.markdown('</div>', unsafe_allow_html=True)

# Convert to DataFrame
input_df = pd.DataFrame([user_input], columns=FEATURES)

# ======================================================
# PREDICTION BUTTON
# ======================================================
if st.button("🔍 Prediksi Sekarang"):
    with st.spinner("Menghitung prediksi..."):
        time.sleep(1.2)
        pred = model.predict(input_df)[0]

    label_map = {0: "Tidak Diabetes", 1: "Pre-Diabetes", 2: "Diabetes"}
    colors = {0: "#38a169", 1: "#d69e2e", 2: "#e53e3e"}

    st.subheader("📊 Hasil Prediksi:")
    st.markdown(
        f"""
        <div class="stCard" style="background-color: {colors[pred]}20;">
            <h2 style="color: {colors[pred]}; text-align:center; font-weight:700;">
                {label_map[pred]}
            </h2>
            <p style="text-align:center; color:#4a5568;">
                Berdasarkan indikator kesehatan yang Anda masukkan.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
