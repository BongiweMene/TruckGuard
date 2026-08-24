import streamlit as st
import pandas as pd
from gps_service import get_test_gps_data
import time
# -----------------------------
# LOGIN SYSTEM
# -----------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_role" not in st.session_state:
    st.session_state.user_role = None

def login_page():

    st.markdown(
        """
        <div style="
            max-width: 500px;
            margin: 80px auto;
            padding: 40px;
            background: white;
            border-radius: 20px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.10);
            text-align: center;
        ">

            <div style="font-size: 60px;">
                🚛
            </div>

            <h1 style="margin-bottom: 5px;">
                TruckGuard AI
            </h1>

            <p style="color: #6b7280;">
                AI-Powered Truck Driver & Vehicle Safety System
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    username = st.text_input(
        "👤 Username",
        placeholder="Enter your username"
    )

    password = st.text_input(
        "🔑 Password",
        type="password",
        placeholder="Enter your password"
    )

    if st.button(
        "🔐 Login",
        use_container_width=True
    ):

              # DRIVER LOGIN

        if username == "driver" and password == "Driver123":

            st.session_state.logged_in = True
            st.session_state.user_role = "driver"

            st.success(
                "✅ Driver login successful!"
            )

            st.rerun()


        # MANAGER LOGIN

        elif username == "manager" and password == "Manager123":

            st.session_state.logged_in = True
            st.session_state.user_role = "manager"

            st.success(
                "✅ Manager login successful!"
            )

            st.rerun()


        # INVALID LOGIN

        else:

            st.error(
                "❌ Incorrect username or password."
            )


# -----------------------------
# SHOW LOGIN PAGE
# -----------------------------

if not st.session_state.logged_in:

    login_page()

    st.stop()

from datetime import datetime
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TruckGuard AI",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("")
st.markdown("")
st.markdown("")

st.title("🚛 TruckGuard AI")

st.write(
    "AI-Powered Truck Driver & Vehicle Safety System"
)

st.markdown("---")
# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🚛 TruckGuard")

if st.session_state.user_role == "driver":

    st.sidebar.success("👤 Logged in as Driver")

elif st.session_state.user_role == "manager":

    st.sidebar.success("👨‍💼 Logged in as Manager")

st.sidebar.markdown("---")


if st.session_state.user_role == "driver":

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Driver Monitoring",
            "AI Risk Prediction",
            "Alerts"
        ]
    )

elif st.session_state.user_role == "manager":

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Driver Monitoring",
            "Vehicle Monitoring",
            "AI Risk Prediction",
            "Alerts"
        ]
    )

st.sidebar.markdown("---")

st.sidebar.info(
    "TruckGuard AI\n\n"
    "Intelligent safety monitoring for truck drivers and vehicles."
)

st.sidebar.markdown("---")

if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):

    st.session_state.logged_in = False

    st.rerun()

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="main-header">
    <h1>🚛 TruckGuard AI</h1>
    <p>AI-Powered Truck Driver & Vehicle Safety System</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# LIVE SYSTEM STATUS
# -----------------------------

current_time = datetime.now().strftime("%H:%M:%S")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("🟢 SYSTEM ONLINE")

with col2:
    st.info(f"🕐 Last Updated: {current_time}")

with col3:
    st.info("🤖 AI Monitoring: ACTIVE")

st.caption(
    f"TruckGuard monitoring session active • {datetime.now().strftime('%A, %d %B %Y')}"
)

# ============================================================
# DASHBOARD
# ============================================================
if page == "Dashboard":
        # Get the latest AI risk result
    ai_prediction = st.session_state.get(
        "ai_prediction",
        0
    )

    ai_risk_probability = st.session_state.get(
        "ai_risk_probability",
        0.0
    )

    # -----------------------------
    # MANAGER FLEET OVERVIEW
    # -----------------------------

    if st.session_state.user_role == "manager":

        st.markdown("## 👨‍💼 Fleet Manager Dashboard")

        st.write(
            "Real-time overview of TruckGuard fleet safety."
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "🚛 Total Trucks",
                "4"
            )

        with col2:
            st.metric(
                "👤 Active Drivers",
                "4"
            )

        with col3:
            st.metric(
                "🟢 Safe Trucks",
                "3"
            )

        with col4:
            st.metric(
                "🔴 High Risk",
                "1"
            )

        st.markdown("---")

        st.markdown("### 🗺️ Live Fleet Location")

                # Fleet status driven by the AI result
                # -----------------------------
        # FLEET AI RISK STATUS
        # -----------------------------

        fleet_status = (
            "🔴 High Risk"
            if ai_prediction == 1
            else "🟢 Safe"
        )

        gps_data = pd.DataFrame({
            "truck_id": [
                "TG-001",
                "TG-002",
                "TG-003",
                "TG-004"
            ],

            "driver": [
                "Driver 001",
                "Driver 002",
                "Driver 003",
                "Driver 004"
            ],

             "status": [
                "🟢 Safe",
                "🟢 Safe",
                fleet_status,
                "🟢 Safe"
            ],

            "latitude": [
                -26.2041,
                -26.1951,
                -26.2105,
                -26.2200
            ],

            "longitude": [
                28.0473,
                28.0500,
                28.0350,
                28.0600
            ],

            "speed_kmh": [
                72,
                65,
                91,
                58
            ],

            "last_updated": [
                "2026-08-21 10:30:00",
                "2026-08-21 10:30:00",
                "2026-08-21 10:30:00",
                "2026-08-21 10:30:00"
            ]
        })

        st.map(
            gps_data,
            latitude="latitude",
            longitude="longitude"
        )

        st.markdown("### 🚛 Fleet GPS Status")

        st.dataframe(
            gps_data,
            use_container_width=True,
            hide_index=True
        )
    

       
        
    # -----------------------------
    # EXISTING SAFETY DASHBOARD
    # -----------------------------

    

    # Calculate dashboard safety score
    safety_score = 100 - ai_risk_probability

    # Determine alert status
    if ai_prediction == 1:
        active_alerts = 1
    else:
        active_alerts = 0

    st.markdown("## Safety Dashboard")

    # -----------------------------
    # LIVE AI STATUS
    # -----------------------------

    st.markdown("### 🤖 Live AI Safety Status")

    if ai_prediction == 1:
        st.error(
            f"🔴 HIGH RISK DETECTED — "
            f"AI risk probability: {ai_risk_probability:.1f}%"
        )
    else:
        st.success(
            f"🟢 LOW RISK — "
            f"AI risk probability: {ai_risk_probability:.1f}%"
        )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">👤 Driver Information</div>
            <p><strong>Driver:</strong> Demo Driver</p>
            <p><strong>Driver ID:</strong> TG-001</p>
            <p><strong>Status:</strong> 🟢 Active</p>
            <p><strong>Alertness:</strong> 92%</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">🚛 Truck Information</div>
            <p><strong>Truck ID:</strong> TG-TRUCK-001</p>
            <p><strong>Vehicle:</strong> Heavy Truck</p>
            <p><strong>Trip Status:</strong> 🟢 In Progress</p>
            <p><strong>Vehicle Health:</strong> 95%</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## Safety Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🛡️ Safety Score", "94%")

    with col2:
        st.metric("👁️ Driver Alertness", "92%")

    with col3:
        st.metric("🚛 Vehicle Health", "95%")

    with col4:
        st.metric("⚠️ Active Alerts", "0")

    st.markdown("## 📍 Current Trip")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">Starting Location</div>
            <div class="metric">Johannesburg</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">Destination</div>
            <div class="metric">Durban</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <div class="card-title">Trip Progress</div>
            <div class="metric">62%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## 🤖 AI Safety Assessment")

    risk = st.slider(
        "Simulated Driver & Vehicle Risk",
        0,
        100,
        20,
        key="dashboard_risk"
    )

    if risk < 40:
        st.success("🟢 LOW RISK — Driver and vehicle appear safe.")
    elif risk < 70:
        st.warning("🟡 MEDIUM RISK — Additional monitoring recommended.")
    else:
        st.error("🔴 HIGH RISK — Immediate attention recommended.")

    st.progress(risk / 100)


# ============================================================
# DRIVER MONITORING
# ============================================================

elif page == "Driver Monitoring":

    st.markdown("## 👤 Driver Monitoring")

    st.write(
        "Real-time driver safety and alertness monitoring."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">👤 Driver Profile</div>
            <p><strong>Name:</strong> Demo Driver</p>
            <p><strong>Driver ID:</strong> TG-001</p>
            <p><strong>Vehicle:</strong> TG-TRUCK-001</p>
            <p><strong>Trip:</strong> Johannesburg → Durban</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">🟢 Current Status</div>
            <p><strong>Status:</strong> DRIVER IS ALERT</p>
            <p><strong>Monitoring:</strong> Active</p>
            <p><strong>Last Check:</strong> Just now</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## 📊 Driver Safety Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👁️ Alertness", "92%")

    with col2:
        st.metric("😴 Fatigue Risk", "Low")

    with col3:
        st.metric("🎯 Attention", "95%")

    with col4:
        st.metric("🛡️ Safety Score", "94%")

    st.markdown("## 🔍 Driver Monitoring Controls")

    fatigue = st.slider(
        "Simulated Fatigue Level",
        0,
        100,
        15,
        key="driver_fatigue"
    )

    distraction = st.slider(
        "Simulated Distraction Level",
        0,
        100,
        10,
        key="driver_distraction"
    )

    attention = 100 - distraction

    safety_score = (
        attention + (100 - fatigue)
    ) / 2

    st.markdown("### 😴 Fatigue Assessment")

    if fatigue < 30:
        st.success(
            "🟢 LOW FATIGUE — Driver appears sufficiently alert."
        )
    elif fatigue < 60:
        st.warning(
            "🟡 MODERATE FATIGUE — Driver should be monitored."
        )
    else:
        st.error(
            "🔴 HIGH FATIGUE — Driver may require a rest break."
        )

    st.markdown("### 🎯 Attention Assessment")

    if distraction < 30:
        st.success(
            "🟢 GOOD ATTENTION — No significant distraction detected."
        )
    elif distraction < 60:
        st.warning(
            "🟡 MODERATE DISTRACTION — Continue monitoring."
        )
    else:
        st.error(
            "🔴 HIGH DISTRACTION — Safety intervention recommended."
        )

    st.markdown("## 🛡️ Overall Driver Safety Score")

    st.metric(
        "Safety Score",
        f"{safety_score:.0f}%"
    )

    st.progress(safety_score / 100)

    if safety_score >= 80:
        st.success("🟢 Driver safety status: GOOD")
    elif safety_score >= 60:
        st.warning("🟡 Driver safety status: MODERATE")
    else:
        st.error("🔴 Driver safety status: HIGH RISK")


# ============================================================
# VEHICLE MONITORING
# ============================================================

elif page == "Vehicle Monitoring":

    st.markdown("## 🚛 Vehicle Monitoring")

    st.write(
        "Real-time monitoring of important truck safety indicators."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <div class="card-title">🚛 Vehicle Information</div>
            <p><strong>Truck ID:</strong> TG-TRUCK-001</p>
            <p><strong>Vehicle Type:</strong> Heavy Truck</p>
            <p><strong>Trip Status:</strong> 🟢 In Progress</p>
            <p><strong>Vehicle Health:</strong> 95%</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <div class="card-title">🟢 Vehicle Status</div>
            <p><strong>Status:</strong> VEHICLE OPERATING NORMALLY</p>
            <p><strong>Monitoring:</strong> Active</p>
            <p><strong>Last Check:</strong> Just now</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## 📊 Vehicle Safety Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🔧 Engine", "Normal")

    with col2:
        st.metric("🛞 Tyres", "Normal")

    with col3:
        st.metric("🌡️ Temperature", "Normal")

    with col4:
        st.metric("⛽ Fuel", "78%")

    st.markdown("## 🔍 Vehicle Monitoring Controls")

    engine_temperature = st.slider(
        "Engine Temperature",
        0,
        120,
        75,
        key="engine_temperature"
    )

    tyre_pressure = st.slider(
        "Tyre Pressure",
        0,
        100,
        85,
        key="tyre_pressure"
    )

    fuel_level = st.slider(
        "Fuel Level",
        0,
        100,
        78,
        key="fuel_level"
    )

    st.markdown("### 🔧 Engine Assessment")

    if engine_temperature < 90:
        st.success(
            "🟢 ENGINE NORMAL — Temperature is within the safe range."
        )
    elif engine_temperature < 105:
        st.warning(
            "🟡 ENGINE WARNING — Temperature is elevated."
        )
    else:
        st.error(
            "🔴 ENGINE ALERT — Engine temperature is very high."
        )

    st.markdown("### 🛞 Tyre Assessment")

    if tyre_pressure >= 70:
        st.success(
            "🟢 TYRES NORMAL — Tyre condition appears acceptable."
        )
    elif tyre_pressure >= 40:
        st.warning(
            "🟡 TYRE WARNING — Check tyre pressure."
        )
    else:
        st.error(
            "🔴 TYRE ALERT — Immediate tyre inspection recommended."
        )

    st.markdown("### ⛽ Fuel Assessment")

    if fuel_level >= 30:
        st.success("🟢 FUEL LEVEL GOOD")
    elif fuel_level >= 15:
        st.warning(
            "🟡 LOW FUEL — Refuelling may be required soon."
        )
    else:
        st.error("🔴 CRITICAL FUEL LEVEL")

    vehicle_health = (
        (100 - max(0, engine_temperature - 75))
        + tyre_pressure
        + fuel_level
    ) / 3

    vehicle_health = max(
        0,
        min(100, vehicle_health)
    )

    st.markdown("## 🛡️ Overall Vehicle Health")

    st.metric(
        "Vehicle Health",
        f"{vehicle_health:.0f}%"
    )

    st.progress(vehicle_health / 100)

    if vehicle_health >= 80:
        st.success("🟢 VEHICLE STATUS: GOOD")
    elif vehicle_health >= 60:
        st.warning("🟡 VEHICLE STATUS: MODERATE")
    else:
        st.error("🔴 VEHICLE STATUS: HIGH RISK")


# ============================================================
# AI RISK PREDICTION
# ============================================================

elif page == "AI Risk Prediction":




    st.markdown("## 🤖 AI Risk Prediction")

    st.write(
        "TruckGuard uses machine learning to estimate "
        "driver and vehicle safety risk."
    )





    # -----------------------------
    # LOAD TRAINED TRUCKGUARD MODEL
    # -----------------------------




    import joblib
    from pathlib import Path
    import numpy as np

    MODEL_PATH = (
        Path(__file__).resolve().parent
        / "models"
        / "truckguard_model.pkl"
    )

    model = joblib.load(MODEL_PATH)

        # -----------------------------
    # LOAD REAL TRUCKGUARD DATA
    # -----------------------------

    DATA_PATH = (
        Path(__file__).resolve().parent
        / "data"
        / "truckguard_dataset.csv"
    )

    sensor_data = pd.read_csv(DATA_PATH)

    st.success(
        f"📊 Real sensor dataset loaded: "
        f"{len(sensor_data):,} records"
    )

    st.success(
        "🤖 TruckGuard AI model loaded successfully."
    )




    # --------------------------------------------------------
    # INPUT SECTION
    # --------------------------------------------------------

    st.markdown("### 📋 Driver & Vehicle Assessment")

    col1, col2 = st.columns(2)

    with col1:

        fatigue = st.slider(
            "😴 Driver Fatigue",
            0,
            100,
            20,
            key="ai_fatigue"
        )

        distraction = st.slider(
            "👀 Driver Distraction",
            0,
            100,
            10,
            key="ai_distraction"
        )

    with col2:

        speed_risk = st.slider(
            "🚦 Speed Risk",
            0,
            100,
            20,
            key="ai_speed"
        )

        vehicle_risk = st.slider(
            "🚛 Vehicle Risk",
            0,
            100,
            15,
            key="ai_vehicle"
        )

    # --------------------------------------------------------
    # PREDICTION
    # --------------------------------------------------------

         # -----------------------------
    # SELECT A REAL SENSOR RECORD
    # -----------------------------

    feature_columns = [
        "accel_x",
        "accel_y",
        "accel_z",

        "linear_x",
        "linear_y",
        "linear_z",

        "gyro_x",
        "gyro_y",
        "gyro_z",

        "mag_x",
        "mag_y",
        "mag_z",

        "acceleration_magnitude",
        "linear_acceleration_magnitude",
        "gyro_magnitude",
        "magnetic_magnitude"
    ]

    # Select one real record from the dataset
    sensor_record = sensor_data.sample(
        1,
        random_state=42
    )

    input_data = sensor_record[
        feature_columns
    ].copy()

    st.markdown("### 📡 Live Sensor Reading")

    st.dataframe(
        input_data,
        use_container_width=True
    )

    # -----------------------------
    # AI PREDICTION
    # -----------------------------

    prediction = model.predict(input_data)[0]

    probabilities = model.predict_proba(input_data)[0]

    # Probability of high risk
    high_risk_probability = probabilities[1] * 100


    # -----------------------------
    # SAVE AI RESULT
    # -----------------------------

    st.session_state["ai_prediction"] = int(
        prediction
    )

    st.session_state["ai_risk_probability"] = float(
        high_risk_probability
    )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    st.markdown("## 🧠 AI Prediction Result")

    if prediction == 0:

        st.success(
            f"🟢 LOW RISK\n\n"
            f"AI estimates a "
            f"{100 - high_risk_probability:.1f}% "
            f"probability of a safe condition."
        )

    else:

        st.error(
            f"🔴 HIGH RISK\n\n"
            f"AI estimates a "
            f"{high_risk_probability:.1f}% "
            f"probability of a high-risk condition."
        )

            # -----------------------------
    # AI RISK BREAKDOWN
    # -----------------------------

    st.markdown("### 🔍 Risk Factor Breakdown")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "😴 Fatigue",
            f"{fatigue}%"
        )

    with col2:
        st.metric(
            "👀 Distraction",
            f"{distraction}%"
        )

    with col3:
        st.metric(
            "🚦 Speed Risk",
            f"{speed_risk}%"
        )

    with col4:
        st.metric(
            "🚛 Vehicle Risk",
            f"{vehicle_risk}%"
        )

    # -----------------------------
    # AI EXPLANATION
    # -----------------------------

    st.markdown("### 🧠 AI Safety Explanation")

    risk_factors = []

    if fatigue >= 70:
        risk_factors.append("😴 High driver fatigue")

    elif fatigue >= 50:
        risk_factors.append("😴 Moderate driver fatigue")

    if distraction >= 70:
        risk_factors.append("👀 High driver distraction")

    elif distraction >= 50:
        risk_factors.append("👀 Moderate driver distraction")

    if speed_risk >= 70:
        risk_factors.append("🚦 High speed risk")

    elif speed_risk >= 50:
        risk_factors.append("🚦 Elevated speed risk")

    if vehicle_risk >= 70:
        risk_factors.append("🚛 High vehicle risk")

    elif vehicle_risk >= 50:
        risk_factors.append("🚛 Elevated vehicle risk")

    if len(risk_factors) == 0:

        st.success(
            "🟢 AI Assessment: No major risk factors detected. "
            "The driver and vehicle currently appear to be operating "
            "within safe simulated conditions."
        )

    else:

        st.warning(
            "⚠️ AI identified the following risk factors:"
        )

        for factor in risk_factors:
            st.write(f"• {factor}")
    # --------------------------------------------------------
    # RISK SCORE
    # --------------------------------------------------------

    st.markdown("### 📊 Risk Score")

    st.progress(
        min(high_risk_probability / 100, 1.0)
    )

    st.metric(
        "High-Risk Probability",
        f"{high_risk_probability:.1f}%"
    )

    # --------------------------------------------------------
    # MODEL INFORMATION
    # --------------------------------------------------------

    st.markdown("## 🤖 AI Model Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Model",
            "Random Forest"
        )

    with col2:
        st.metric(
            "Trees",
            "100"
        )

    with col3:
        st.metric(
            "Input Features",
            "4"
        )

    st.info(
        "TruckGuard combines driver and vehicle risk indicators "
        "to estimate overall safety risk."
    )

# ============================================================
# ALERTS
# ============================================================

elif page == "Alerts":

    st.markdown("## 🚨 Safety Alerts")

    st.write(
        "TruckGuard automatically identifies potential driver "
        "and vehicle safety risks."
    )

    # -----------------------------
    # CURRENT AI RISK STATUS
    # -----------------------------

    ai_prediction = st.session_state.get(
        "ai_prediction",
        0
    )

    ai_risk_probability = st.session_state.get(
        "ai_risk_probability",
        0.0
    )

    st.markdown("### 🤖 Current AI Risk Status")

    if ai_prediction == 1:

        st.error(
            f"🔴 HIGH RISK — "
            f"AI risk probability: {ai_risk_probability:.1f}%"
        )

    else:

        st.success(
            f"🟢 LOW RISK — "
            f"AI risk probability: {ai_risk_probability:.1f}%"
        )

            # -----------------------------
    # RISK LEVEL
    # -----------------------------

    if ai_risk_probability < 40:

        risk_level = "LOW"

    elif ai_risk_probability < 70:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"

    st.metric(
        "⚠️ Current Risk Level",
        risk_level
    )

        # -----------------------------
    # SAFETY SCORE
    # -----------------------------

    safety_score = 100 - ai_risk_probability

    st.markdown("### 🛡️ Overall Safety Score")

    st.metric(
        "Safety Score",
        f"{safety_score:.0f}%"
    )

    st.progress(
        max(0.0, min(safety_score / 100, 1.0))
    )

    if safety_score >= 80:
        st.success("🟢 SAFETY STATUS: GOOD")

    elif safety_score >= 60:
        st.warning("🟡 SAFETY STATUS: MODERATE")

    else:
        st.error("🔴 SAFETY STATUS: HIGH RISK")


    # --------------------------------------------------------
    # AI RISK STATUS
    # --------------------------------------------------------

    ai_prediction = st.session_state.get(
        "ai_prediction",
        0
    )

    ai_risk_probability = st.session_state.get(
        "ai_risk_probability",
        0.0
    )

    st.markdown("## 🤖 AI Risk Status")

    if ai_prediction == 1:

        st.error(
            f"🔴 AI HIGH-RISK DETECTION — "
            f"Risk probability: "
            f"{ai_risk_probability:.1f}%"
        )

    else:

        st.success(
            f"🟢 AI LOW-RISK DETECTION — "
            f"Risk probability: "
            f"{ai_risk_probability:.1f}%"
        )

    # --------------------------------------------------------
    # ALERT INPUTS
    # --------------------------------------------------------

    st.markdown("## 🎛️ Safety Monitoring")

    fatigue = st.slider(
        "Driver Fatigue Level",
        0,
        100,
        20,
        key="alert_fatigue"
    )

    distraction = st.slider(
        "Driver Distraction Level",
        0,
        100,
        10,
        key="alert_distraction"
    )

    speed_risk = st.slider(
        "Speed Risk",
        0,
        100,
        20,
        key="alert_speed"
    )

    vehicle_risk = st.slider(
        "Vehicle Risk",
        0,
        100,
        15,
        key="alert_vehicle"
    )

    # --------------------------------------------------------
    # CREATE ALERTS
    # --------------------------------------------------------

    alerts = []

    if fatigue >= 70:

        alerts.append(
            (
                "🔴",
                "HIGH FATIGUE",
                "Driver fatigue level is critically high."
            )
        )

    elif fatigue >= 50:

        alerts.append(
            (
                "🟡",
                "MODERATE FATIGUE",
                "Driver fatigue is increasing."
            )
        )

    if distraction >= 70:

        alerts.append(
            (
                "🔴",
                "HIGH DISTRACTION",
                "High driver distraction detected."
            )
        )

    elif distraction >= 50:

        alerts.append(
            (
                "🟡",
                "MODERATE DISTRACTION",
                "Driver attention should be monitored."
            )
        )

    if speed_risk >= 70:

        alerts.append(
            (
                "🔴",
                "HIGH SPEED RISK",
                "Speed risk is above the recommended level."
            )
        )

    elif speed_risk >= 50:

        alerts.append(
            (
                "🟡",
                "SPEED WARNING",
                "Vehicle speed requires monitoring."
            )
        )

    if vehicle_risk >= 70:

        alerts.append(
            (
                "🔴",
                "HIGH VEHICLE RISK",
                "Vehicle safety risk is high."
            )
        )

    elif vehicle_risk >= 50:

        alerts.append(
            (
                "🟡",
                "VEHICLE WARNING",
                "Vehicle condition requires attention."
            )
        )

    # --------------------------------------------------------
    # ADD AI ALERT
    # --------------------------------------------------------

    if ai_prediction == 1:

        alerts.append(
            (
                "🔴",
                "AI HIGH RISK",
                f"AI detected a high-risk probability "
                f"of {ai_risk_probability:.1f}%."
            )
        )

    # --------------------------------------------------------
    # ALERT SUMMARY
    # --------------------------------------------------------

    st.markdown("## 📊 Alert Summary")

    col1, col2, col3 = st.columns(3)

    high_alerts = sum(
        1 for alert in alerts
        if alert[0] == "🔴"
    )

    warning_alerts = sum(
        1 for alert in alerts
        if alert[0] == "🟡"
    )

    with col1:
        st.metric(
            "🔴 Critical Alerts",
            high_alerts
        )

    with col2:
        st.metric(
            "🟡 Warnings",
            warning_alerts
        )

    with col3:
        st.metric(
            "📊 Total Alerts",
            len(alerts)
        )

    # --------------------------------------------------------
    # DISPLAY ALERTS
    # --------------------------------------------------------

    st.markdown("## 🚨 Active Alerts")

    if len(alerts) == 0:

        st.success(
            "🟢 No active safety alerts. "
            "Driver and vehicle conditions appear normal."
        )

    else:

        for icon, title, message in alerts:

            if icon == "🔴":

                st.error(
                    f"{icon} **{title}**\n\n{message}"
                )

            else:

                st.warning(
                    f"{icon} **{title}**\n\n{message}"
                )

    # --------------------------------------------------------
    # SAFETY RECOMMENDATION
    # --------------------------------------------------------

    st.markdown("## 🛡️ Safety Recommendation")

    if high_alerts > 0:

        st.error(
            "🚨 IMMEDIATE ATTENTION REQUIRED — "
            "One or more critical safety risks have been detected."
        )

    elif warning_alerts > 0:

        st.warning(
            "⚠️ MONITORING REQUIRED — "
            "Potential safety risks have been detected."
        )

    else:

        st.success(
            "✅ SAFE TO CONTINUE — "
            "No significant safety risks detected."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    TruckGuard AI © 2026 | Intelligent Truck Safety System
</div>
""", unsafe_allow_html=True)