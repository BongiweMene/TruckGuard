# TruckGuard™
# AI-Powered Fleet Safety & Hazardous Cargo Monitoring System
# Developed by Bongiwe Mene
# © 2026 Bongiwe Mene. All rights reserved.

import streamlit as st
import pandas as pd
import time
from pathlib import Path
from datetime import datetime

import folium
from streamlit_folium import st_folium
from sklearn.ensemble import RandomForestClassifier
import joblib

from gps_service import get_test_gps_data
from osiris_service import get_weather_data, normalize_weather_events


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TruckGuard™ | Bongiwe Mene",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# TRUCKGUARD GLOBAL UI
# ============================================================

st.markdown("""
<style>

    /* Main application background */
    .stApp {
        background: #020b16;
        color: #f5f7fa;
    }

    /* Main content */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #03101e;
        border-right: 1px solid #19354b;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] * {
        color: #f5f7fa;
    }

    /* Headings */
    h1, h2, h3 {
        color: #f5f7fa;
    }

    /* TruckGuard title */
    .truckguard-title {
        font-size: 36px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0;
    }

    .truckguard-title span {
        color: #1687ff;
    }

    .truckguard-subtitle {
        color: #8198ac;
        font-size: 15px;
        margin-top: 2px;
        margin-bottom: 20px;
    }

    /* Cards */
    .card {
        background: #041322;
        border: 1px solid #19354b;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }

    .card-title {
        color: #ffffff;
        font-size: 17px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: #041322;
        border: 1px solid #19354b;
        border-radius: 12px;
        padding: 15px;
    }

    [data-testid="stMetricLabel"] {
        color: #8198ac;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 700;
        border: 1px solid #24506d;
    }

    /* Inputs */
    div[data-baseweb="input"],
    div[data-baseweb="select"] {
        background: #041322;
    }

    /* Horizontal line */
    hr {
        border-color: #19354b;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #62788b;
        font-size: 12px;
        padding: 25px 0 10px 0;
        margin-top: 30px;
        border-top: 1px solid #19354b;
    }

</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_role" not in st.session_state:
    st.session_state.user_role = None

if "trip_started" not in st.session_state:
    st.session_state.trip_started = False

if "trip_deviation" not in st.session_state:
    st.session_state.trip_deviation = False

if "trip_progress" not in st.session_state:
    st.session_state.trip_progress = 0.0

if "truck_latitude" not in st.session_state:
    st.session_state.truck_latitude = -33.9249

if "truck_longitude" not in st.session_state:
    st.session_state.truck_longitude = 18.4241

if "truck_speed" not in st.session_state:
    st.session_state.truck_speed = 0

if "distance_from_route" not in st.session_state:
    st.session_state.distance_from_route = 0

if "ai_prediction" not in st.session_state:
    st.session_state.ai_prediction = 0

if "ai_risk_probability" not in st.session_state:
    st.session_state.ai_risk_probability = 0.0


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 38px;
        font-weight: 800;
    }

    .card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        margin-bottom: 15px;
    }

    .login-box {
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #ddd;
    }

    .footer {
        text-align: center;
        margin-top: 40px;
        padding: 20px;
        color: #777;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOGIN PAGE
# ============================================================

def login_page():

    st.markdown(
        "<h1 style='text-align:center;'>🚛 TruckGuard AI</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>AI-Powered Truck Driver & Vehicle Safety System</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.subheader("🔐 Login")

        role = st.radio(
            "Select account type",
            ["driver", "manager"],
            horizontal=True,
            format_func=lambda x:
                "🚛 Driver" if x == "driver"
                else "👨‍💼 Manager"
        )

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "🔐 Login",
            use_container_width=True,
            type="primary"
        ):

            username_clean = username.strip().lower()
            password_clean = password.strip()

            if (
                role == "driver"
                and username_clean == "driver"
                and password_clean == "Driver123"
            ):

                st.session_state.logged_in = True
                st.session_state.user_role = "driver"

                st.rerun()

            elif (
                role == "manager"
                and username_clean == "manager"
                and password_clean == "Manager123"
            ):

                st.session_state.logged_in = True
                st.session_state.user_role = "manager"

                st.rerun()

            else:

                st.error(
                    f"❌ Incorrect {role} username or password."
                )

        st.markdown("---")

        if role == "driver":

            st.info(
                "Demo login: driver / Driver123"
            )

        else:

            st.info(
                "Demo login: manager / Manager123"
            )


# ============================================================
# DASHBOARD
# ============================================================

def dashboard():

    st.markdown("""
    <div style="
        background: linear-gradient(90deg, #06111e, #020b16);
        border: 1px solid #19324a;
        border-radius: 12px;
        padding: 22px 25px;
        margin-bottom: 20px;
    ">

        <div style="
            color: #1687ff;
            font-size: 34px;
            font-weight: 800;
        ">
            🚛 TruckGuard <span style="color:#ffffff;">AI</span>
        </div>

        <div style="
            color: #ffffff;
            font-size: 22px;
            font-weight: 700;
            margin-top: 8px;
        ">
            Fleet Manager Dashboard
        </div>

        <div style="
            color: #8198ac;
            font-size: 14px;
            margin-top: 5px;
        ">
            Real-time overview of fleet safety and vehicle activity.
        </div>

    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🚛 Total Trucks",
            "4"
        )

    with col2:
        st.metric(
            "🟢 Active Drivers",
            "4"
        )

    with col3:
        st.metric(
            "🛡️ Safe Trucks",
            "3"
        )

    with col4:
        st.metric(
            "⚠️ High Risk",
            "1"
        )

    st.markdown("---")

    st.subheader("📍 Live Fleet Location")

    try:

        gps_data = get_test_gps_data()

        if isinstance(gps_data, pd.DataFrame):

            st.map(gps_data)

        else:

            st.info(
                "GPS simulation data is currently unavailable."
            )

    except Exception as e:

        st.warning(
            f"GPS data unavailable: {e}"
        )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="card">

            <h3>🛡️ Fleet Safety</h3>

            <p>
            TruckGuard AI continuously monitors driver,
            vehicle and route safety indicators.
            </p>

            <p>
            <strong>Status:</strong>
            🟢 Monitoring Active
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="card">

            <h3>🤖 AI Monitoring</h3>

            <p>
            Machine learning is used to identify
            potential safety risks.
            </p>

            <p>
            <strong>Status:</strong>
            🟢 AI System Online
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# DRIVER VIEW
# ============================================================

def driver_view():

    st.title("🚛 Driver View")

    st.subheader("Welcome, Lerato Maseko")

    st.markdown("---")

    col1, col2 = st.columns([2.5, 1])

    # --------------------------------------------------------
    # MAP
    # --------------------------------------------------------

    with col1:

        cape_town = (-33.9249, 18.4241)

        port_elizabeth = (-33.9608, 25.6022)

        route_points = [
            cape_town,
            (-34.05, 20.2),
            (-34.15, 22.2),
            (-34.05, 24.0),
            port_elizabeth
        ]

        truck_position = (
            st.session_state.truck_latitude,
            st.session_state.truck_longitude
        )

        m = folium.Map(
            location=(-34.2, 22.0),
            zoom_start=6,
            tiles="OpenStreetMap"
        )

        folium.PolyLine(
            route_points,
            color="#19d8c0",
            weight=5,
            opacity=0.9,
            dash_array="12,8",
            tooltip="Approved Safe Route"
        ).add_to(m)

        folium.Marker(
            cape_town,
            tooltip="Cape Town Harbor",
            popup="Starting Location: Cape Town Harbor",
            icon=folium.Icon(
                color="green",
                icon="home"
            )
        ).add_to(m)

        truck_color = (
            "red"
            if st.session_state.trip_deviation
            else "blue"
        )

        folium.Marker(
            truck_position,
            tooltip="TRK-003",
            popup=(
                f"TRK-003 | "
                f"Speed: {st.session_state.truck_speed} km/h"
            ),
            icon=folium.Icon(
                color=truck_color,
                icon="truck"
            )
        ).add_to(m)

        folium.Marker(
            port_elizabeth,
            tooltip="Port Elizabeth Depot",
            popup="Destination: Port Elizabeth Depot",
            icon=folium.Icon(
                color="red",
                icon="flag"
            )
        ).add_to(m)

        st_folium(
            m,
            width=None,
            height=600,
            returned_objects=[]
        )

    # --------------------------------------------------------
    # DRIVER INFORMATION
    # --------------------------------------------------------

    with col2:

        st.info(
            "ⓘ SIMULATED DEMO DATA"
        )

        if st.session_state.trip_deviation:

            st.error(
                "⚠️ ROUTE DEVIATION DETECTED"
            )

            st.write(
                "Driver is outside the approved safe route."
            )

        else:

            st.success(
                "🛡️ ON APPROVED ROUTE"
            )

            st.write(
                "Driver is following the approved safe route."
            )

        st.markdown("---")

        st.subheader("📦 Current Trip")

        st.write("🚚 **TRK-003**")
        st.write("📦 Hydrochloric Acid")
        st.write("⚖️ 16,000 kg")
        st.write("📍 Cape Town Harbor")
        st.write("🚩 Port Elizabeth Depot")
        st.write("🛣️ Cape Town → Port Elizabeth")

        st.markdown("---")

        st.subheader("📊 Route Status")

        st.metric(
            "🚦 Speed",
            f"{st.session_state.truck_speed} km/h"
        )

        st.metric(
            "📊 Trip Progress",
            f"{st.session_state.trip_progress:.1f}%"
        )

        st.progress(
            st.session_state.trip_progress / 100
        )

        st.metric(
            "📍 Distance From Route",
            f"{st.session_state.distance_from_route}m"
        )

        st.metric(
            "⏱️ ETA",
            "4h 57m"
            if st.session_state.trip_started
            else "Not started"
        )

        st.markdown("---")

        st.subheader("🛰️ GPS Simulation")

        if st.button(
            "▶ Start Trip",
            use_container_width=True
        ):

            st.session_state.trip_started = True
            st.session_state.trip_deviation = False
            st.session_state.truck_speed = 72
            st.session_state.trip_progress = 45.5

            st.success(
                "Trip started successfully!"
            )

            st.rerun()

        if st.button(
            "⚠ Simulate Deviation",
            use_container_width=True
        ):

            st.session_state.trip_deviation = True
            st.session_state.distance_from_route = 850

            st.warning(
                "Route deviation detected!"
            )

            st.rerun()

        if st.button(
            "↻ Reset Trip",
            use_container_width=True
        ):

            st.session_state.trip_started = False
            st.session_state.trip_deviation = False
            st.session_state.trip_progress = 0.0
            st.session_state.truck_latitude = -33.9249
            st.session_state.truck_longitude = 18.4241
            st.session_state.truck_speed = 0
            st.session_state.distance_from_route = 0

            st.rerun()

    # --------------------------------------------------------
    # SAFETY WARNING
    # --------------------------------------------------------

    st.markdown("---")

    st.subheader("🔔 Safety Warnings")

    if st.session_state.trip_deviation:

        st.error(
            "⚠️ Route Deviation Detected — "
            "Driver is outside the approved safe route."
        )

    else:

        st.success(
            "🛡️ All Clear — No active warnings."
        )


# ============================================================
# DRIVER MONITORING
# ============================================================

def driver_monitoring():

    st.title("👤 Driver Monitoring")

    st.write(
        "Real-time driver safety and alertness monitoring."
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="card">

            <h3>👤 Driver Profile</h3>

            <p><strong>Name:</strong> Demo Driver</p>
            <p><strong>Driver ID:</strong> TG-001</p>
            <p><strong>Vehicle:</strong> TG-TRUCK-001</p>
            <p><strong>Trip:</strong> Johannesburg → Durban</p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="card">

            <h3>🟢 Current Status</h3>

            <p><strong>Status:</strong> DRIVER IS ALERT</p>
            <p><strong>Monitoring:</strong> Active</p>
            <p><strong>Last Check:</strong> Just now</p>

            </div>
            """,
            unsafe_allow_html=True
        )

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

    st.markdown("---")

    st.subheader("🔍 Driver Monitoring Controls")

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

    st.progress(
        safety_score / 100
    )


# ============================================================
# VEHICLE MONITORING
# ============================================================

def vehicle_monitoring():

    st.title("🚛 Vehicle Monitoring")

    st.write(
        "Real-time monitoring of important truck safety indicators."
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="card">

            <h3>🚛 Vehicle Information</h3>

            <p><strong>Truck ID:</strong> TG-TRUCK-001</p>
            <p><strong>Vehicle Type:</strong> Heavy Truck</p>
            <p><strong>Trip Status:</strong> 🟢 In Progress</p>
            <p><strong>Vehicle Health:</strong> 95%</p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="card">

            <h3>🟢 Vehicle Status</h3>

            <p><strong>Status:</strong> VEHICLE OPERATING NORMALLY</p>
            <p><strong>Monitoring:</strong> Active</p>
            <p><strong>Last Check:</strong> Just now</p>

            </div>
            """,
            unsafe_allow_html=True
        )

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

    st.markdown("---")

    st.subheader("🔍 Vehicle Monitoring Controls")

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

        st.error(
            "🔴 CRITICAL FUEL LEVEL"
        )


# ============================================================
# AI RISK PREDICTION
# ============================================================

def ai_risk_prediction():

    st.title("🤖 AI Risk Prediction")

    st.write(
        "TruckGuard uses machine learning to estimate "
        "driver and vehicle safety risk."
    )

    st.markdown("---")

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

    st.markdown("---")

    # --------------------------------------------------------
    # LOAD MODEL
    # --------------------------------------------------------

    model_path = (
        Path(__file__).resolve().parent
        / "models"
        / "truckguard_model.pkl"
    )

    if model_path.exists():

        try:

            model = joblib.load(model_path)

            st.success(
                "🤖 TruckGuard AI model loaded successfully."
            )

            # ------------------------------------------------
            # LOAD DATA
            # ------------------------------------------------

            data_path = (
                Path(__file__).resolve().parent
                / "data"
                / "truckguard_dataset.csv"
            )

            if data_path.exists():

                sensor_data = pd.read_csv(
                    data_path
                )

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

                available_features = [
                    col
                    for col in feature_columns
                    if col in sensor_data.columns
                ]

                if len(available_features) == len(feature_columns):

                    sensor_record = sensor_data.sample(
                        1,
                        random_state=42
                    )

                    input_data = sensor_record[
                        feature_columns
                    ]

                    prediction = model.predict(
                        input_data
                    )[0]

                    probabilities = model.predict_proba(
                        input_data
                    )[0]

                    if len(probabilities) > 1:

                        high_risk_probability = (
                            probabilities[1] * 100
                        )

                    else:

                        high_risk_probability = 0.0

                    st.session_state.ai_prediction = int(
                        prediction
                    )

                    st.session_state.ai_risk_probability = float(
                        high_risk_probability
                    )

                    st.markdown(
                        "### 📡 Live Sensor Reading"
                    )

                    st.dataframe(
                        input_data,
                        use_container_width=True
                    )

                else:

                    st.warning(
                        "Dataset does not contain all required sensor features."
                    )

            else:

                st.warning(
                    "truckguard_dataset.csv was not found."
                )

        except Exception as e:

            st.error(
                f"Unable to load AI model: {e}"
            )

    else:

        st.warning(
            "TruckGuard model not found. "
            "Please make sure truckguard_model.pkl is inside the models folder."
        )

        # Simple fallback demonstration

        combined_risk = (
            fatigue
            + distraction
            + speed_risk
            + vehicle_risk
        ) / 4

        st.session_state.ai_risk_probability = (
            combined_risk
        )

        st.session_state.ai_prediction = (
            1 if combined_risk >= 70 else 0
        )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    st.markdown("## 🧠 AI Prediction Result")

    prediction = st.session_state.ai_prediction

    probability = st.session_state.ai_risk_probability

    if prediction == 0:

        st.success(
            f"🟢 LOW RISK — "
            f"AI estimates a "
            f"{100 - probability:.1f}% "
            f"probability of a safe condition."
        )

    else:

        st.error(
            f"🔴 HIGH RISK — "
            f"AI estimates a "
            f"{probability:.1f}% "
            f"probability of a high-risk condition."
        )

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

    st.markdown("### 📊 Risk Score")

    st.progress(
        min(probability / 100, 1.0)
    )

    st.metric(
        "High-Risk Probability",
        f"{probability:.1f}%"
    )

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
            "16"
        )


# ============================================================
# ALERTS
# ============================================================

def alerts_page():

    st.title("🚨 Safety Alerts")

    st.write(
        "TruckGuard automatically identifies potential driver "
        "and vehicle safety risks."
    )

    st.markdown("---")

    ai_prediction = st.session_state.ai_prediction

    ai_risk_probability = (
        st.session_state.ai_risk_probability
    )

    st.subheader("🤖 Current AI Risk Status")

    if ai_prediction == 1:

        st.error(
            f"🔴 HIGH RISK — "
            f"AI risk probability: "
            f"{ai_risk_probability:.1f}%"
        )

    else:

        st.success(
            f"🟢 LOW RISK — "
            f"AI risk probability: "
            f"{ai_risk_probability:.1f}%"
        )

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

    safety_score = (
        100 - ai_risk_probability
    )

    st.markdown("### 🛡️ Overall Safety Score")

    st.metric(
        "Safety Score",
        f"{safety_score:.0f}%"
    )

    st.progress(
        max(
            0.0,
            min(
                safety_score / 100,
                1.0
            )
        )
    )

    if safety_score >= 80:

        st.success(
            "🟢 SAFETY STATUS: GOOD"
        )

    elif safety_score >= 60:

        st.warning(
            "🟡 SAFETY STATUS: MODERATE"
        )

    else:

        st.error(
            "🔴 SAFETY STATUS: HIGH RISK"
        )

    st.markdown("---")

    st.subheader("🎛️ Safety Monitoring")

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

    if ai_prediction == 1:

        alerts.append(
            (
                "🔴",
                "AI HIGH RISK",
                f"AI detected a high-risk probability "
                f"of {ai_risk_probability:.1f}%."
            )
        )

    st.markdown("## 📊 Alert Summary")

    high_alerts = sum(
        1
        for alert in alerts
        if alert[0] == "🔴"
    )

    warning_alerts = sum(
        1
        for alert in alerts
        if alert[0] == "🟡"
    )

    col1, col2, col3 = st.columns(3)

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

    st.markdown("## 🚨 Active Alerts")

    if len(alerts) == 0:

        st.success(
            "🟢 No active safety alerts."
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

    st.markdown("## 🛡️ Safety Recommendation")

    if high_alerts > 0:

        st.error(
            "🚨 IMMEDIATE ATTENTION REQUIRED — "
            "Critical safety risks detected."
        )

    elif warning_alerts > 0:

        st.warning(
            "⚠️ MONITORING REQUIRED — "
            "Potential safety risks detected."
        )

    else:

        st.success(
            "✅ SAFE TO CONTINUE — "
            "No significant safety risks detected."
        )


# ============================================================
# MAIN APPLICATION
# ============================================================

if not st.session_state.logged_in:

    login_page()

    st.stop()


# ============================================================
# DRIVER
# ============================================================

if st.session_state.user_role == "driver":

    driver_view()


# ============================================================
# MANAGER
# ============================================================

else:

    st.sidebar.title("🚛 TruckGuard AI")

    st.sidebar.success(
        "👨‍💼 Logged in as Manager"
    )

    st.sidebar.markdown("---")

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

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user_role = None

        st.rerun()

    if page == "Dashboard":

        dashboard()

    elif page == "Driver Monitoring":

        driver_monitoring()

    elif page == "Vehicle Monitoring":

        vehicle_monitoring()

    elif page == "AI Risk Prediction":

        ai_risk_prediction()

    elif page == "Alerts":

        alerts_page()

# ============================================================
# OSIRIS ENVIRONMENTAL INTELLIGENCE
# ============================================================

st.subheader("🌦️ OSIRIS Environmental Intelligence")

with st.spinner("Loading live environmental intelligence..."):
    weather_payload = get_weather_data()

weather_events = normalize_weather_events(weather_payload)

if isinstance(weather_payload, dict) and weather_payload.get("error"):
    st.warning(
        "⚠️ OSIRIS weather intelligence is temporarily unavailable. "
        "The rest of TruckGuard will continue working normally."
    )

elif weather_events:

    # Identify potentially severe events
    high_keywords = {
        "high",
        "severe",
        "extreme",
        "critical",
        "red"
    }

    severe_events = [
        event
        for event in weather_events
        if (
            str(event.get("Severity", "")).strip().lower()
            in high_keywords
            or any(
                word in str(event.get("Event", "")).lower()
                for word in (
                    "storm",
                    "hurricane",
                    "tornado",
                    "cyclone",
                    "flood"
                )
            )
        )
    ]

    # Summary metrics
    w1, w2, w3 = st.columns(3)

    with w1:
        st.metric(
            "🌦️ Weather Events",
            len(weather_events)
        )

    with w2:
        st.metric(
            "⚠️ Severe Events",
            len(severe_events)
        )

    with w3:
        environmental_status = (
            "HIGH ATTENTION"
            if severe_events
            else "MONITORING"
        )

        st.metric(
            "🛰️ Environmental Status",
            environmental_status
        )

    # Weather event table
    weather_df = pd.DataFrame(weather_events)

    display_columns = [
        "Event",
        "Category",
        "Severity",
        "Location",
        "Date"
    ]

    display_columns = [
        column
        for column in display_columns
        if column in weather_df.columns
    ]

    st.dataframe(
        weather_df[display_columns].head(10),
        use_container_width=True,
        hide_index=True
    )

    # Safety notification
    if severe_events:
        st.warning(
            f"⚠️ {len(severe_events)} environmental event(s) "
            "may require additional route monitoring."
        )
    else:
        st.success(
            "🟢 No severe environmental events were flagged "
            "by the current OSIRIS feed."
        )

else:
    st.info(
        "🟢 OSIRIS is connected, but there are currently "
        "no environmental events to display."
    )

# ============================================================
# FOOTER
# ============================================================


# ============================================================
# TRUCKGUARD OWNERSHIP FOOTER
# ============================================================

st.markdown("""
<div style="
    text-align: center;
    color: #5f7182;
    font-size: 12px;
    padding: 25px 0 10px 0;
    margin-top: 30px;
    border-top: 1px solid #19354b;
">
    TruckGuard™ · Developed by Bongiwe Mene · © 2026
</div>
""", unsafe_allow_html=True)
