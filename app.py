import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Cosmic Radiation Risk Calculator", layout="centered")

st.title("🚀 Cosmic Radiation Risk Calculator")

st.markdown(
    """
    Estimate cosmic ray exposure, simulate solar flares, and understand your risk!
    """
)

# ---------------------------
# 1️⃣ Solar Flare Event Toggle
# ---------------------------
st.header("🔧 Mission Parameters")

mission_days = st.slider("Mission Duration (days)", 1, 1000, 180)

shielding_material = st.selectbox(
    "Shielding Material",
    ["None", "Aluminum", "Polyethylene"]
)

thickness_cm = 0
if shielding_material != "None":
    thickness_cm = st.slider("Shielding Thickness (cm)", 1, 20, 5)

location = st.selectbox(
    "Mission Environment",
    ["Sea Level", "Airplane (~10 km)", "ISS Orbit (~400 km)"]
)

solar_cycle = st.slider(
    "Solar Activity (0 = Solar Minimum, 100 = Solar Maximum)", 0, 100, 50
)

# Solar Flare event toggle
solar_flare = st.checkbox("☀️ Simulate Solar Flare Event (Increases flux by 10x for 2 days)")

# ---------------------------
# 3️⃣ Genetic Risk Factors
# ---------------------------
st.header("🧬 Personal Risk Factors")

age = st.slider("Your Age", 18, 80, 30)
sex = st.selectbox("Sex Assigned at Birth", ["Male", "Female"])
genetic_sensitivity = st.selectbox("Known Genetic Sensitivity to Radiation?", ["No", "Yes"])

st.write("✅ Test: The app did not crash so far!")

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
st.pyplot(fig)


# ---------------------------
# Real-Time Data
# ---------------------------
st.header("🌞 Live Solar Proton Flux")

url = "https://services.swpc.noaa.gov/json/goes/primary/differential-proton-flux-1-day.json"

try:
    data = requests.get(url).json()
    flux = float(data[-1]['flux'])
    st.success(f"Live Proton Flux (≥10 MeV): {flux:.2e} protons/cm²/s/sr")
except:
    flux = 1
