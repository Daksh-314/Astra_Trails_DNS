import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cosmic Radiation Risk Calculator", layout="centered")

st.title("🚀 Cosmic Radiation Risk Calculator")

st.markdown(
    """
    This app estimates the radiation dose from cosmic rays for a mission and compares it to everyday exposures.
    """
)

# --- INPUTS ---

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

# --- REAL-TIME DATA ---

st.header("🌞 Live Solar Proton Flux")

url = "https://services.swpc.noaa.gov/json/goes/primary/differential-proton-flux-1-day.json"

try:
    data = requests.get(url).json()
    flux = float(data[-1]['flux'])  # protons/cm²/s/sr
    st.success(f"Live Proton Flux (≥10 MeV): {flux:.2e} protons/cm²/s/sr")
except:
    flux = 100
    st.warning("Unable to fetch live data. Using default flux: 100 p/cm²/s/sr")

# --- CALCULATIONS ---

# Base dose model
base_dose_per_day = flux * 0.00005  # empirical factor

# Material factor
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

# Solar cycle factor (simple)
solar_factor = np.interp(solar_cycle, [0, 100], [1.2, 0.8])

daily_dose = base_dose_per_day * material_factor * attenuation_factor * location_factor * solar_factor
total_dose = daily_dose * mission_days

# Risk estimate
risk_percent = (total_dose / 1000) * 5  # linear ERR

# --- OUTPUTS ---

st.header("📊 Results")

col1, col2 = st.columns(2)
col1.metric("☢ Total Estimated Dose", f"{total_dose:.2f} mSv")
col2.metric("⚠ Estimated Cancer Risk", f"{risk_percent:.2f} %")

st.info(f"Equivalent to about {total_dose/2.4:.1f} years of average Earth background radiation (~2.4 mSv/year).")

# --- PLOT ---

st.header("📈 Dose vs. Mission Duration")

days_range = np.linspace(0, 1000, 100)
dose_range = daily_dose * days_range

fig, ax = plt.subplots()
ax.plot(days_range, dose_range)
ax.set_xlabel("Mission Duration (days)")
ax.set_ylabel("Total Dose (mSv)")
ax.set_title("Estimated Dose Over Time")
st.pyplot(fig)

# --- EDUCATION ---

with st.expander("ℹ️ Learn More About Cosmic Radiation"):
    st.markdown("""
    - **Galactic Cosmic Rays (GCRs)** come from outside our solar system.
    - **Solar Particle Events (SPEs)** are bursts from the Sun, especially during solar flares.
    - Higher altitudes and orbits increase exposure because Earth’s atmosphere shields us.
    - **Shielding** helps reduce exposure but adds weight to spacecraft — a key challenge for long missions.
    - Typical annual natural background dose on Earth: **~2.4 mSv**
    - 1 chest X-ray: **~0.1 mSv**
    - Roundtrip flight NY-London: **~0.05 mSv**
    - ISS astronauts: **~80–160 mSv per 6-month mission**
    """)

st.caption("🔬 This is a simplified educational model. Not for medical or mission-critical use.")

