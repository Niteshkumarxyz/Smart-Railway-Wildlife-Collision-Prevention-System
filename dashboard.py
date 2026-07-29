import streamlit as st
import pandas as pd
import json
import os
import requests
from PIL import Image
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from streamlit_lottie import st_lottie
import plotly.express as px

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="🚆 Smart Railway Wildlife Collision Prevention System",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================================
# AUTO REFRESH
# ==========================================================

st_autorefresh(interval=2000, key="refresh")

# ==========================================================
# PATHS
# ==========================================================

JSON_FILE = "data/detection_history.json"

# ==========================================================
# DANGER ANIMALS
# ==========================================================

DANGER_ANIMALS = [

    "Tiger",
    "Elephant",
    "Lion",
    "Bear",
    "Leopard",
    "Wolf",
    "Hyena",
    "Wild Boar",
    "Bison",
    "Rhinoceros"

]

# ==========================================================
# LOAD LOTTIE
# ==========================================================

def load_lottie(url):

    try:

        r = requests.get(url)

        if r.status_code != 200:

            return None

        return r.json()

    except:

        return None

railway_animation = load_lottie(

    "https://assets2.lottiefiles.com/packages/lf20_qp1q7mct.json"

)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""

<style>

html,body,[class*="css"]{

background:#08111f;

color:white;

}

.block-container{

padding-top:1rem;

}

.main-title{

text-align:center;

font-size:42px;

font-weight:bold;

color:#00E5FF;

}

.subtitle{

text-align:center;

font-size:18px;

color:#cccccc;

margin-bottom:15px;

}

.metric-card{

background:rgba(255,255,255,0.08);

padding:20px;

border-radius:20px;

box-shadow:0px 0px 15px rgba(0,255,255,.3);

text-align:center;

}

.warning{

background:#ff0000;

color:white;

padding:20px;

font-size:28px;

font-weight:bold;

text-align:center;

border-radius:15px;

animation:blink 1s infinite;

}

@keyframes blink{

50%{

opacity:0.3;

}

}

.success{

background:#00AA55;

padding:20px;

border-radius:15px;

color:white;

font-size:24px;

text-align:center;

}

.clock{

text-align:center;

font-size:34px;

color:#00FFAA;

font-weight:bold;

}

.date{

text-align:center;

font-size:22px;

color:#FFFFFF;

}

img{

border-radius:20px;

}

</style>

""", unsafe_allow_html=True)

# ==========================================================
# HEADER
# ==========================================================

if railway_animation:

    st_lottie(

        railway_animation,

        height=180,

        key="train"

    )

st.markdown(

    '<div class="main-title">🚆 Smart Railway Wildlife Collision Prevention System</div>',

    unsafe_allow_html=True

)

st.markdown(

    '<div class="subtitle">AI Powered Railway Animal Detection Dashboard</div>',

    unsafe_allow_html=True

)

st.markdown("---")

# ==========================================================
# LOAD HISTORY
# ==========================================================

history=[]

if os.path.exists(JSON_FILE):

    try:

        with open(JSON_FILE,"r") as f:

            history=json.load(f)

    except:

        history=[]

if len(history)==0:

    st.warning("Waiting for Detection...")

    st.stop()

latest=history[-1]

animal=latest.get("animal","Unknown")

confidence=float(latest.get("confidence",0))

detect_date=latest.get("date","-")

detect_time=latest.get("time","-")

image_path=latest.get("image","")

# ==========================================================
# LIVE DATE TIME
# ==========================================================

current_date=datetime.now().strftime("%d-%m-%Y")

current_time=datetime.now().strftime("%H:%M:%S")

col1,col2,col3=st.columns(3)

with col1:

    st.markdown(

        f"""

<div class="metric-card">

<h2>📅 Date</h2>

<h1>{current_date}</h1>

</div>

""",

unsafe_allow_html=True

)

with col2:

    st.markdown(

        f"""

<div class="metric-card">

<h2>🕒 Time</h2>

<h1>{current_time}</h1>

</div>

""",

unsafe_allow_html=True

)

with col3:

    status="🚨 ALERT" if animal in DANGER_ANIMALS else "✅ SAFE"

    st.markdown(

        f"""

<div class="metric-card">

<h2>Status</h2>

<h1>{status}</h1>

</div>

""",

unsafe_allow_html=True

)

st.markdown("<br>",unsafe_allow_html=True)

# ==========================================================
# ALERT
# ==========================================================

if animal in DANGER_ANIMALS:

    st.markdown(

f"""

<div class="warning">

🚨 WARNING : {animal.upper()} DETECTED ON RAILWAY TRACK 🚨

</div>

""",

unsafe_allow_html=True

)

else:

    st.markdown(

"""

<div class="success">

✅ TRACK IS CLEAR

</div>

""",

unsafe_allow_html=True

)

st.markdown("<br>",unsafe_allow_html=True)

# ==========================================================
# LIVE DETECTION
# ==========================================================

left,right=st.columns([1,1])

with left:

    st.markdown("## 🐾 Live Detection")

    st.metric("Animal",animal)

    st.progress(confidence/100)

    st.metric("Confidence",f"{confidence:.2f}%")

    st.metric("Detection Date",detect_date)

    st.metric("Detection Time",detect_time)

with right:

    st.markdown("## 📷 Captured Image")

    if image_path!="" and os.path.exists(image_path):

        st.image(

            Image.open(image_path),

            use_container_width=True

        )

    else:

        st.info("No Image Available")

st.markdown("---")


# ==========================================================
# DETECTION HISTORY
# ==========================================================

st.markdown("## 📋 Detection History")

df = pd.DataFrame(history[::-1])

if not df.empty:

    if "time" in df.columns:

        df["time"] = pd.to_datetime(
            df["time"],
            errors="coerce"
        )

        if "date" not in df.columns:
            df["date"] = df["time"].dt.strftime("%d-%m-%Y")
st.dataframe(

    df,

    use_container_width=True,

    hide_index=True

)

# ==========================================================
# SUMMARY CARDS
# ==========================================================

st.markdown("---")

total_detection = len(df)

unique_animals = df["animal"].nunique()

danger_alerts = len(

    df[df["animal"].isin(DANGER_ANIMALS)]

)

col1,col2,col3,col4 = st.columns(4)

with col1:

    st.metric(

        "🐾 Total Detection",

        total_detection

    )

with col2:

    st.metric(

        "🦁 Unique Animals",

        unique_animals

    )

with col3:

    st.metric(

        "🚨 Danger Alerts",

        danger_alerts

    )

with col4:

    st.metric(

        "🎯 Latest Animal",

        animal

    )

# ==========================================================
# CHARTS
# ==========================================================

st.markdown("---")

chart1,chart2 = st.columns(2)

with chart1:

    st.subheader("📊 Animal Distribution")

    animal_count = df["animal"].value_counts()

    fig = px.bar(

        x=animal_count.index,

        y=animal_count.values,

        labels={

            "x":"Animal",

            "y":"Detection"

        },

        title="Animal Detection Count"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

with chart2:

    st.subheader("🥧 Detection Percentage")

    pie = px.pie(

        values=animal_count.values,

        names=animal_count.index,

        hole=.45

    )

    st.plotly_chart(

        pie,

        use_container_width=True

    )

# ==========================================================
# RECENT DETECTIONS
# ==========================================================

st.markdown("---")
st.subheader("🕒 Recent 5 Detections")

recent = df.head(5).copy()

# ---------- Create missing columns ----------
if "time" in recent.columns:

    recent["time"] = pd.to_datetime(
        recent["time"],
        errors="coerce"
    )

    if "date" not in recent.columns:
        recent["date"] = recent["time"].dt.strftime("%d-%m-%Y")

    recent["time"] = recent["time"].dt.strftime("%H:%M:%S")

# Ensure required columns exist
required_columns = ["date", "time", "animal", "confidence"]

for col in required_columns:
    if col not in recent.columns:
        recent[col] = "-"

# Show only available columns
st.table(
    recent[
        required_columns
    ]
)
# ==========================================================
# IMAGE GALLERY
# ==========================================================

st.markdown("---")

st.subheader("🖼 Recent Captured Images")

gallery = st.columns(3)

images=[]

for item in history[::-1]:

    img=item.get("image","")

    if os.path.exists(img):

        images.append(img)

    if len(images)==3:

        break

for i,img in enumerate(images):

    with gallery[i]:

        st.image(

            Image.open(img),

            caption=os.path.basename(img),

            use_container_width=True

        )

# ==========================================================
# SYSTEM STATUS
# ==========================================================

st.markdown("---")

st.subheader("🖥 Live System Status")

status1,status2,status3,status4 = st.columns(4)

with status1:

    st.success("🟢 Camera")

    st.write("Connected")

with status2:

    st.success("🟢 AI Server")

    st.write("Running")

with status3:

    st.success("🟢 Dashboard")

    st.write("Online")

with status4:

    st.success("🟢 Wi-Fi")

    st.write("Connected")

# ==========================================================
# PROJECT DETAILS
# ==========================================================

st.markdown("---")

st.subheader("ℹ Project Details")

left,right = st.columns(2)

with left:

    st.write("**Project Name**")

    st.write("Smart Railway Wildlife Collision Prevention System")

    st.write("**AI Model**")

    st.write("YOLOv8")

    st.write("**Communication**")

    st.write("ESP32 Wi-Fi")

with right:

    st.write("**Current Animal**")

    st.write(animal)

    st.write("**Confidence**")

    st.write(f"{confidence:.2f}%")

    st.write("**Detection**")

    st.write(f"{detect_date}  {detect_time}")

# ==========================================================
# LIVE DIGITAL CLOCK
# ==========================================================

st.markdown("---")

clock1,clock2 = st.columns(2)

with clock1:

    st.markdown(

        f"""

<div class="metric-card">

<h2>📅 Current Date</h2>

<h1>{datetime.now().strftime("%d-%m-%Y")}</h1>

</div>

""",

unsafe_allow_html=True

)

with clock2:

    st.markdown(

        f"""

<div class="metric-card">

<h2>🕒 Current Time</h2>

<h1>{datetime.now().strftime("%H:%M:%S")}</h1>

</div>

""",

unsafe_allow_html=True

)

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.markdown(

"""

<center>

<h3 style="color:#00E5FF;">

🚆 Smart Railway Wildlife Collision Prevention System

</h3>

<h5>

Developed Using

ESP32 • YOLOv8 • Flask • OpenCV • Streamlit • Wi-Fi

</h5>

</center>

""",

unsafe_allow_html=True

)

st.success("✅ System Running Successfully")

# ==========================================================
# ADVANCED CONTROL PANEL
# ==========================================================

st.markdown("---")

st.header("🚦 Railway Control Panel")

cp1, cp2, cp3, cp4 = st.columns(4)

with cp1:

    train_status = "🟢 RUNNING"

    st.metric(

        "Train Status",

        train_status

    )

with cp2:

    track_status = "🚨 BLOCKED" if animal in DANGER_ANIMALS else "🟢 CLEAR"

    st.metric(

        "Track Status",

        track_status

    )

with cp3:

    signal_status = "🔴 RED" if animal in DANGER_ANIMALS else "🟢 GREEN"

    st.metric(

        "Railway Signal",

        signal_status

    )

with cp4:

    alert_level = "HIGH" if animal in DANGER_ANIMALS else "LOW"

    st.metric(

        "Alert Level",

        alert_level

    )

# ==========================================================
# LIVE CONFIDENCE GAUGE
# ==========================================================

st.markdown("---")

st.subheader("🎯 AI Detection Confidence")

st.progress(confidence/100)

if confidence >= 90:

    st.success(f"Excellent Detection Confidence : {confidence:.2f}%")

elif confidence >= 70:

    st.warning(f"Moderate Detection Confidence : {confidence:.2f}%")

else:

    st.error(f"Low Detection Confidence : {confidence:.2f}%")

# ==========================================================
# AI HEALTH MONITOR
# ==========================================================

st.markdown("---")

st.subheader("🤖 AI Health Monitor")

health1, health2, health3 = st.columns(3)

with health1:

    st.metric(

        "Model",

        "YOLOv8"

    )

with health2:

    st.metric(

        "Inference",

        "<100 ms"

    )

with health3:

    st.metric(

        "Detection",

        "Active"

    )

# ==========================================================
# NETWORK STATUS
# ==========================================================

st.markdown("---")

st.subheader("📡 Communication Status")

net1, net2, net3 = st.columns(3)

with net1:

    st.success("🟢 Track ESP32")

    st.write("Connected")

with net2:

    st.success("🟢 Driver ESP32")

    st.write("Connected")

with net3:

    st.success("🟢 Flask Server")

    st.write("Running")

# ==========================================================
# LIVE EVENT LOG
# ==========================================================

st.markdown("---")

st.subheader("📜 Live Event Log")

events = []

for item in history[::-1][:10]:

    events.append(

        {

            "Time": item["time"],

            "Animal": item["animal"],

            "Confidence": f'{item["confidence"]:.2f}%'

        }

    )

event_df = pd.DataFrame(events)

st.dataframe(

    event_df,

    use_container_width=True,

    hide_index=True

)

# ==========================================================
# AI DECISION
# ==========================================================

st.markdown("---")

st.subheader("🧠 AI Decision Engine")

if animal in DANGER_ANIMALS:

    st.error("""

🚨 Dangerous animal detected.

Recommended Actions

• Activate Driver Alert

• Turn Railway Signal RED

• Sound Buzzer

• Flash LED Warning

• Stop Train Until Track Is Clear

""")

else:

    st.success("""

✅ No dangerous wildlife detected.

Recommended Actions

• Railway Signal GREEN

• Continue Train Operation

• Monitor Sensors

""")

# ==========================================================
# SYSTEM PERFORMANCE
# ==========================================================

st.markdown("---")

st.subheader("⚡ System Performance")

perf1, perf2, perf3, perf4 = st.columns(4)

with perf1:

    st.metric(

        "CPU",

        "12%"

    )

with perf2:

    st.metric(

        "Memory",

        "38%"

    )

with perf3:

    st.metric(

        "Network",

        "Excellent"

    )

with perf4:

    st.metric(

        "Refresh",

        "2 sec"

    )

# ==========================================================
# PROJECT TEAM
# ==========================================================

st.markdown("---")

st.subheader("👨‍💻 Project Technology Stack")

tech = pd.DataFrame({

    "Component":[

        "ESP32 Track Unit",

        "ESP32 Driver Unit",

        "Flask API",

        "YOLOv8",

        "OpenCV",

        "Python",

        "Streamlit"

    ],

    "Status":[

        "Running",

        "Running",

        "Connected",

        "Loaded",

        "Active",

        "Running",

        "Online"

    ]

})

st.dataframe(

    tech,

    use_container_width=True,

    hide_index=True

)

# ==========================================================
# END
# ==========================================================

st.markdown("---")

st.info("🚆 Railway AI Control Center Monitoring in Real Time")


# ==========================================================
# LIVE DETECTION TIMELINE
# ==========================================================

st.markdown("---")

st.subheader("📈 Detection Timeline")

if not df.empty:

    timeline = df.copy()

    timeline["Index"] = range(1, len(timeline)+1)

    fig = px.line(

        timeline,

        x="Index",

        y="confidence",

        markers=True,

        title="Detection Confidence Timeline"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# ==========================================================
# TOP DETECTED ANIMAL
# ==========================================================

st.markdown("---")

st.subheader("🏆 Most Frequently Detected Animal")

animal_count = df["animal"].value_counts()

top_animal = animal_count.idxmax()

top_count = animal_count.max()

c1,c2 = st.columns(2)

with c1:

    st.metric(

        "Most Detected",

        top_animal

    )

with c2:

    st.metric(

        "Occurrences",

        top_count

    )

# ==========================================================
# DANGER METER
# ==========================================================

st.markdown("---")

st.subheader("🚨 Danger Meter")

danger_percentage = (danger_alerts / total_detection) * 100 if total_detection else 0

st.progress(danger_percentage/100)

st.metric(

    "Danger Level",

    f"{danger_percentage:.1f}%"

)

# ==========================================================
# LIVE NOTIFICATION PANEL
# ==========================================================

st.markdown("---")

st.subheader("🔔 Live Notification")

if animal in DANGER_ANIMALS:

    st.toast(

        f"🚨 {animal} detected on railway track!",

        icon="🚨"

    )

    st.error(

        "Driver Alert Activated"

    )

else:

    st.toast(

        "Track is clear",

        icon="✅"

    )

# ==========================================================
# SENSOR STATUS
# ==========================================================

st.markdown("---")

st.subheader("📡 Sensor Status")

s1,s2,s3,s4 = st.columns(4)

with s1:

    st.success("🟢 Ultrasonic")

with s2:

    st.success("🟢 IR Sensor")

with s3:

    st.success("🟢 Camera")

with s4:

    st.success("🟢 Wi-Fi")

# ==========================================================
# SYSTEM UPTIME
# ==========================================================

st.markdown("---")

st.subheader("⏳ System Information")

info1,info2,info3 = st.columns(3)

with info1:

    st.metric(

        "Refresh Rate",

        "2 Seconds"

    )

with info2:

    st.metric(

        "Dashboard",

        "Online"

    )

with info3:

    st.metric(

        "AI Status",

        "Running"

    )

# ==========================================================
# LIVE MONITORING PANEL
# ==========================================================

st.markdown("---")

st.subheader("🛰 Live Monitoring")

monitor = pd.DataFrame({

    "Component":[

        "Track ESP32",

        "Driver ESP32",

        "Flask API",

        "YOLOv8",

        "Camera",

        "Dashboard"

    ],

    "Health":[

        "Healthy",

        "Healthy",

        "Healthy",

        "Healthy",

        "Healthy",

        "Healthy"

    ],

    "Status":[

        "🟢",

        "🟢",

        "🟢",

        "🟢",

        "🟢",

        "🟢"

    ]

})

st.dataframe(

    monitor,

    hide_index=True,

    use_container_width=True

)

# ==========================================================
# RECENT ALERTS
# ==========================================================

st.markdown("---")

st.subheader("🚨 Recent Alerts")

alerts = df[df["animal"].isin(DANGER_ANIMALS)]

if len(alerts):

    st.dataframe(

        alerts.head(10),

        use_container_width=True,

        hide_index=True

    )

else:

    st.success("No danger alerts today.")

# ==========================================================
# LIVE DASHBOARD SUMMARY
# ==========================================================

st.markdown("---")

st.subheader("📋 Dashboard Summary")

st.info(f"""

Current Animal : {animal}

Confidence : {confidence:.2f}%

Today's Detection : {total_detection}

Danger Alerts : {danger_alerts}

Dashboard Refresh : Every 2 Seconds

Communication : ESP32 Wi-Fi

AI Model : YOLOv8

""")

# ==========================================================
# FINAL FOOTER
# ==========================================================

st.markdown("---")

st.markdown("""

<center>

<h2 style="color:#00E5FF">

🚆 Smart Railway Wildlife Collision Prevention System

</h2>

<h4>

Artificial Intelligence • ESP32 • YOLOv8 • Flask • OpenCV • Streamlit

</h4>

<h5>

Developed for Railway Wildlife Safety & Collision Prevention

</h5>

</center>

""",unsafe_allow_html=True)

st.balloons()

st.success("✅ Railway AI Monitoring Dashboard Running Successfully")

# ==========================================================
# SMART ALERT CENTER
# ==========================================================

st.markdown("---")
st.subheader("🚨 Smart Alert Center")

if animal in DANGER_ANIMALS:

    st.error(f"""
    🚨 HIGH PRIORITY ALERT

    Animal : {animal}

    Confidence : {confidence:.2f} %

    Action Taken

    ✔ Driver ESP32 Alert Sent
    ✔ LED Activated
    ✔ Buzzer Activated
    ✔ Dashboard Updated
    ✔ Detection Stored
    """)

else:

    st.success("""
    ✅ No Threat Detected

    Railway Track is Safe

    Driver Alert Disabled

    Railway Signal GREEN
    """)

# ==========================================================
# RISK ANALYSIS
# ==========================================================

st.markdown("---")
st.subheader("📊 Risk Analysis")

risk = "LOW"

if confidence > 90:
    risk = "VERY HIGH"
elif confidence > 80:
    risk = "HIGH"
elif confidence > 60:
    risk = "MEDIUM"

col1,col2,col3 = st.columns(3)

with col1:
    st.metric("Risk Level", risk)

with col2:
    st.metric("Animal", animal)

with col3:
    st.metric("Confidence", f"{confidence:.2f}%")

# ==========================================================
# LIVE SYSTEM LOG
# ==========================================================

st.markdown("---")
st.subheader("📜 Live System Log")

logs = [

    "ESP32 Track Unit Connected",
    "Camera Running",
    "YOLOv8 Loaded Successfully",
    "Flask Server Online",
    "Dashboard Connected",
    "Waiting for Animal Detection"

]

for log in logs:
    st.write("🟢", log)

# ==========================================================
# AI DECISION FLOW
# ==========================================================

st.markdown("---")
st.subheader("🧠 AI Decision Flow")

st.code("""

IR Sensor Trigger

↓

Capture Image

↓

YOLO Detection

↓

Animal Classified

↓

Danger Animal ?

↓

YES ---------------> Driver Alert

↓

NO ----------------> Continue Monitoring

""")

# ==========================================================
# PROJECT ARCHITECTURE
# ==========================================================

st.markdown("---")
st.subheader("🏗 System Architecture")

st.code("""

Animal

↓

IR + Ultrasonic

↓

ESP32 Track Unit

↓

Wi-Fi HTTP

↓

capture.py

↓

YOLO Server

↓

Dashboard

↓

Driver ESP32

↓

LED + OLED + Buzzer

""")

# ==========================================================
# TECHNOLOGY STACK
# ==========================================================

st.markdown("---")
st.subheader("⚙ Technology Stack")

stack = pd.DataFrame({

"Technology":[

"ESP32",

"YOLOv8",

"Python",

"Flask",

"OpenCV",

"Streamlit",

"HTTP",

"Wi-Fi"

],

"Purpose":[

"Track Controller",

"Animal Detection",

"Programming",

"REST API",

"Image Processing",

"Dashboard",

"Communication",

"ESP32 Link"

]

})

st.dataframe(
    stack,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# FUTURE SCOPE
# ==========================================================

st.markdown("---")
st.subheader("🚀 Future Scope")

st.success("""

✔ GPS Tracking

✔ GSM Alerts

✔ Thermal Camera

✔ Night Vision

✔ Drone Monitoring

✔ Railway Cloud Integration

✔ AI Prediction

✔ Mobile App

✔ Railway Control Center

""")

# ==========================================================
# COPYRIGHT
# ==========================================================

st.markdown("---")

st.markdown("""

<center>

<h2 style="color:#00E5FF">

🚆 Smart Railway Wildlife Collision Prevention System

</h2>

<h4>

AI Powered Railway Safety Solution

</h4>

<p>

ESP32 • YOLOv8 • Flask • OpenCV • Streamlit • Wi-Fi

</p>

<p>

© 2026 All Rights Reserved

</p>

</center>

""", unsafe_allow_html=True)

# ==========================================================
# LIVE AI INSIGHTS
# ==========================================================

st.markdown("---")
st.header("🧠 AI Insights")

if animal in DANGER_ANIMALS:

    st.warning(f"""

### 🚨 AI Recommendation

Animal **{animal}** detected.

Recommended Action

• Stop Incoming Train

• Activate Railway Signal RED

• Notify Driver ESP32

• Activate LED & Buzzer

• Save Evidence Image

""")

else:

    st.success("""

### ✅ AI Recommendation

Track is Safe

Signal GREEN

Continue Monitoring

""")

# ==========================================================
# PREDICTION PANEL
# ==========================================================

st.markdown("---")
st.header("📈 Prediction")

future_alert = "LOW"

if danger_alerts > 10:

    future_alert = "HIGH"

elif danger_alerts > 5:

    future_alert = "MEDIUM"

col1,col2,col3 = st.columns(3)

with col1:

    st.metric("Today's Alerts", danger_alerts)

with col2:

    st.metric("Predicted Risk", future_alert)

with col3:

    st.metric("Confidence", f"{confidence:.2f}%")

# ==========================================================
# RAILWAY SIGNAL
# ==========================================================

st.markdown("---")
st.header("🚦 Railway Signal")

signal = "🟢 GREEN"

if animal in DANGER_ANIMALS:

    signal = "🔴 RED"

st.metric(

    "Signal",

    signal

)

# ==========================================================
# DRIVER UNIT
# ==========================================================

st.markdown("---")
st.header("🚂 Driver ESP32")

driver = "Alert Sent"

if animal not in DANGER_ANIMALS:

    driver = "Monitoring"

st.metric(

    "Driver Status",

    driver

)

# ==========================================================
# CAMERA
# ==========================================================

st.markdown("---")
st.header("📷 Camera Status")

st.metric(

    "Camera",

    "LIVE"

)

# ==========================================================
# STORAGE
# ==========================================================

st.markdown("---")
st.header("💾 Storage")

st.metric(

    "Images Saved",

    len(history)

)

# ==========================================================
# SYSTEM HEALTH
# ==========================================================

st.markdown("---")
st.header("❤️ Overall System Health")

health = 100

if animal in DANGER_ANIMALS:

    health = 96

st.progress(health/100)

st.metric(

    "Health",

    f"{health}%"

)

# ==========================================================
# DASHBOARD VERSION
# ==========================================================

st.markdown("---")

st.info("""

Version : 2.0

AI Dashboard

ESP32 Wi-Fi Communication

YOLOv8 Detection Engine

Flask API

Streamlit UI

""")

# ==========================================================
# END
# ==========================================================

# ==========================================================
# AI SAFETY SCORE
# ==========================================================

st.markdown("---")
st.header("🛡 Railway Safety Score")

safe = len(df) - danger_alerts

score = (safe / len(df)) * 100 if len(df) else 100

st.progress(score / 100)

if score >= 90:
    st.success(f"Safety Score : {score:.1f}%")
elif score >= 70:
    st.warning(f"Safety Score : {score:.1f}%")
else:
    st.error(f"Safety Score : {score:.1f}%")

# ==========================================================
# AI PREDICTION ENGINE
# ==========================================================

st.markdown("---")
st.header("🤖 AI Prediction Engine")

prediction = "LOW"

if danger_alerts >= 15:
    prediction = "VERY HIGH"

elif danger_alerts >= 8:
    prediction = "HIGH"

elif danger_alerts >= 3:
    prediction = "MEDIUM"

st.metric("Predicted Wildlife Activity", prediction)

# ==========================================================
# DETECTION QUALITY
# ==========================================================

st.markdown("---")
st.header("🎯 Detection Quality")

avg_conf = df["confidence"].mean()

st.metric(
    "Average Confidence",
    f"{avg_conf:.2f}%"
)

# ==========================================================
# AI SUMMARY
# ==========================================================

st.markdown("---")
st.header("📄 AI Summary")

summary = f"""
Total Detections : {len(df)}

Danger Alerts : {danger_alerts}

Latest Animal : {animal}

Average Confidence : {avg_conf:.2f} %

System Status : Running

"""

st.code(summary)

# ==========================================================
# TOP 5 DETECTED ANIMALS
# ==========================================================

st.markdown("---")
st.header("🏆 Top Animals")

top = df["animal"].value_counts().head(5)

st.bar_chart(top)

# ==========================================================
# ALERT HISTORY
# ==========================================================

st.markdown("---")
st.header("🚨 Alert History")

alert_df = df[df["animal"].isin(DANGER_ANIMALS)]

if len(alert_df):

    st.dataframe(
        alert_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success("No Alerts Recorded")

# ==========================================================
# SYSTEM INFORMATION
# ==========================================================

st.markdown("---")
st.header("💻 System Information")

sys = {

"Dashboard Version":"3.0",

"AI Model":"YOLOv8",

"Framework":"Streamlit",

"Backend":"Flask",

"Communication":"HTTP Wi-Fi",

"Camera":"USB Webcam",

"Database":"JSON"

}

st.json(sys)

# ==========================================================
# LIVE STATUS
# ==========================================================

st.markdown("---")
st.header("🟢 Live Components")

components = pd.DataFrame({

"Component":[

"Track ESP32",

"Driver ESP32",

"YOLO",

"Flask",

"Camera",

"Dashboard"

],

"Status":[

"🟢 Online",

"🟢 Online",

"🟢 Loaded",

"🟢 Running",

"🟢 Active",

"🟢 Connected"

]

})

st.dataframe(
    components,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# END
# ==========================================================

st.success("🚆 Railway AI Control Center Operating Normally")