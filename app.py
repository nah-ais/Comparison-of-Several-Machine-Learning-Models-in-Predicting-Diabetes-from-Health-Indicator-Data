import streamlit as st
import pandas as pd
import pickle

# ======================================================
# LOAD MODEL
# ======================================================
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# ======================================================
# DAFTAR FITUR (HASIL print(X.columns))
# ======================================================
FEATURES = [
    'HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke',
    'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies',
    'HvyAlcoholConsump', 'GenHlth', 'MentHlth', 'PhysHlth', 'DiffWalk',
    'Sex', 'Age'
]

st.title("🩺 Diabetes Prediction App")
st.write("Masukkan indikator kesehatan untuk memprediksi status diabetes berdasarkan indikator kesehatan pribadi Anda.")

# ======================================================
# INPUT USER
# ======================================================
st.subheader("Input Data Kesehatan:")

user_input = {}
for feature in FEATURES:
    # Untuk fitur yang pasti integer (seperti Sex, Age), kita bisa tetap pakai number_input supaya aman
    user_input[feature] = st.number_input(f"{feature}", value=0.0)

# Convert ke dataframe sesuai urutan fitur
input_df = pd.DataFrame([user_input], columns=FEATURES)

# ======================================================
# PREDIKSI
# ======================================================
if st.button("Prediksi"):
    pred = model.predict(input_df)[0]
    label_map = {0: "Tidak Diabetes", 1: "Pre-Diabetes", 2: "Diabetes"}

    st.subheader("Hasil Prediksi:")
    st.success(f"🎯 {label_map[pred]}")
