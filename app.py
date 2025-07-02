# -----------------------------
# Cosmic Radiation Risk App
# FINAL CLEAN VERSION
# -----------------------------

import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Cosmic Radiation Risk Calculator", layout="centered")

st.title("🚀 Cosmic Radiation Risk Calculator")

st.markdown(
    """
    This app estimates your cosmic ray dose, lets you simulate a solar flare,
    adjust for personal risk factors, see historical sunspot data,
    and enjoy fun cosmic facts!
    """
)

# --------------------------------
# 🚀 Mission Parameters
# --------------------------------
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

solar_flare = st.checkbox("☀️ Simulate Solar Flare Event (10x flux for 2 days)")

# --------------------------------
# 🧬 Personal Risk Factors
# --------------------------------
st.header("🧬 Personal Risk Factors")

age = st.slider("Your Age", 18, 80, 30)
sex = st.selectbox("Sex Assigned at Birth", ["Male", "Female"])
genetic_sensitivity = st.selectbox("Known Genetic Sensitivity to Radiation?", ["No", "Yes"])

# --------------------------------
# 🌞 Real-Time Proton Flux
# --------------------------------
st.header("🌞 Live Solar Proton Flux")

url = "https://services.swpc.noaa.gov/json/goes/primary/differential-proton-flux-1-day.json"

try:
    data = requests.get(url).json()
    flux = float(data[-1]['flux'])
    st.success(f"Live Proton Flux (≥10 MeV): {flux:.2e} protons/cm²/s/sr")
except Exception as e:
    flux = 100
    st.warning(f"Unable to fetch live data. Using fallback flux: 100 p/cm²/s/sr")

# --------------------------------
# ☢ Dose Model
# --------------------------------

# Split flare and normal days
if solar_flare:
    flare_days = min(2, mission_days)
    normal_days = mission_days - flare_days
else:
    flare_days = 0
    normal_days = mission_days

# Base dose (empirical scale)
base_dose_per_day = flux * 0.00005

# Shielding factor
shield_factors = {'None': 1.0, 'Aluminum': 0.7, 'Polyethylene': 0.5}
material_factor = shield_factors[shielding_material]

# Thickness factor
attenuation_factor = np.exp(-0.1 * thickness_cm) if shielding_material != "None" else 1.0

# Location factor
location_factors = {
    "Sea Level": 1,
    "Airplane (~10 km)": 30,
    "ISS Orbit (~400 km)": 250
}
location_factor = location_factors[location]

# Solar cycle factor
solar_factor = np.interp(solar_cycle, [0, 100], [1.2, 0.8])

# Final daily dose
daily_dose = base_dose_per_day * material_factor * attenuation_factor * location_factor * solar_factor

# Apply flare
total_dose = daily_dose * normal_days + daily_dose * 10 * flare_days

# Base risk
risk_percent = (total_dose / 1000) * 5

# Adjust for personal factors
if age > 50:
    risk_percent *= 1.1
if sex == "Female":
    risk_percent *= 1.2
if genetic_sensitivity == "Yes":
    risk_percent *= 1.5

# --------------------------------
# 📊 Results
# --------------------------------
st.header("📊 Results")

col1, col2 = st.columns(2)
col1.metric("☢ Estimated Total Dose", f"{total_dose:.2f} mSv")
col2.metric("⚠ Estimated Cancer Risk", f"{risk_percent:.2f} %")

if risk_percent > 3:
    st.error("🚨 WARNING: Risk is high! Add shielding or shorten mission.")
else:
    st.success("✅ Risk is within safe range for short missions.")

st.info(f"Approx. {total_dose/2.4:.1f} years of average Earth background dose (~2.4 mSv/year).")

# --------------------------------
# ☀️ Historical Solar Cycle
# --------------------------------
st.header("☀️ Historical Solar Cycle (Sunspot Number)")

years = np.arange(2012, 2024)
sunspots = [95, 80, 68, 55, 50, 40, 35, 60, 85, 95, 110, 120]  # Example

fig, ax = plt.subplots()
ax.plot(years, sunspots, marker='o')
ax.set_xlabel("Year")
ax.set_ylabel("Sunspot Number")
ax.set_title("Approx. Sunspot Cycle")
st.pyplot(fig)

# --------------------------------
# ✨ Fun Fact
# --------------------------------
fun_facts = [
    "💡 Did you know? The ISS crew receives 80–160 mSv per 6-month mission.",
    "💡 Cosmic rays can flip bits in satellites — Single Event Upsets (SEUs).",
    "💡 Airline pilots get ~3 mSv/year due to high-altitude exposure.",
    "💡 Mars has no magnetic shield → cosmic rays freely hit its surface.",
    "💡 Solar storms can disrupt power grids & satellites on Earth!"
]

st.sidebar.header("✨ Cosmic Fact")
st.sidebar.info(random.choice(fun_facts))

st.caption("🔬 Educational tool only — not for medical or mission planning use.")
