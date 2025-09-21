import streamlit as st
import numpy as np
import pickle
import sklearn


model_path = "rockfall_model.pkl"   
with open(model_path, "rb") as f:
    model1 = pickle.load(f)

with open('model.pkl', "rb") as f:
    model2 = pickle.load(f)
st.set_page_config(page_title="Rockfall Prediction", layout="centered")
st.title("⛏️ Rockfall Probability Prediction in Mine Pits")

st.markdown("Adjust the real-time sensor/weather inputs to predict rockfall probability.")


SlopeAngle_deg = st.slider("Slope Angle (°)", 10, 70, 30)
SlopeHeight_m = st.slider("Slope Height (m)", 5, 300, 50)
AspectRatio = st.slider("Aspect Ratio", 0.5, 3.0, 1.5, step=0.01)
Curvature_1_per_m = st.slider("Curvature (1/m)", -0.5, 0.5, 0.0, step=0.01)
Roughness_m = st.slider("Roughness (m)", 0.01, 5.0, 1.0, step=0.01)
Displacement_mm_per_day = st.slider("Displacement (mm/day)", 0.0, 50.0, 5.0, step=0.1)
Strain = st.slider("Strain (dimensionless)", 0.0, 0.05, 0.01, step=0.001)
PorePressure_kPa = st.slider("Pore Pressure (kPa)", 0, 500, 100)
Rainfall_mm_per_day = st.slider("Rainfall (mm/day)", 0, 300, 10)
Prev_Day_Rainfall_mm = st.slider("Prev_Day_Rainfall_mm", 0, 300, 10)
Temperature_C = st.slider("Temperature (°C)", -10, 50, 25)
Vibration_mm_s = st.slider("Vibration (mm/s PPV)", 0.0, 100.0, 5.0, step=0.5)


features2 = np.array([[
    SlopeAngle_deg,
    SlopeHeight_m,
    AspectRatio,
    Curvature_1_per_m,
    Roughness_m,
    Displacement_mm_per_day,
    Strain,
    PorePressure_kPa,
    Rainfall_mm_per_day,
    
    Temperature_C,
    Vibration_mm_s,
    Prev_Day_Rainfall_mm
]])

features1 = np.array([[
    SlopeAngle_deg,
    SlopeHeight_m,
    AspectRatio,
    Curvature_1_per_m,
    Roughness_m,
    Displacement_mm_per_day,
    Strain,
    PorePressure_kPa,
    (Prev_Day_Rainfall_mm + Rainfall_mm_per_day) / 2,  # averaged rainfall
    Temperature_C,
    Vibration_mm_s
]])


if st.button("Predict Rockfall Probability"):
    probability1 = model1.predict(features1)[0]
    st.subheader(f"Predicted Rockfall Probability Model1: **{probability1:.2f}**")
    probability2 = model2.predict(features2)[0]
    st.subheader(f"Predicted Rockfall Probability Model2: **{probability2:.2f}**")

    probability=(probability1+probability2)/2
    st.subheader(f"Predicted Rockfall Probability Both models: **{probability:.2f}**")

    if probability >= 0.7:
        risk = "🔴 HIGH Risk"
    elif probability >= 0.4:
        risk = "🟠 MEDIUM Risk"
    else:
        risk = "🟢 LOW Risk"
    
    st.markdown(f"### Risk Category: {risk}")

