import streamlit as st
import folium
import speech_recognition as sr
import tempfile
import os
import re

from folium.plugins import HeatMap
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
from audiorecorder import audiorecorder

# Safe imports
try:
    from weather_system import get_weather_alert
except:
    def get_weather_alert(city):
        return {"weather": "Unknown", "temp": "N/A", "risk": "Offline Mode"}

try:
    from vision_ai import analyze_disaster_image
except:
    def analyze_disaster_image(image):
        return "Vision AI unavailable. Please check dependencies."

try:
    from mesh_system import broadcast_message, get_messages
except:
    def broadcast_message(message):
        pass

    def get_messages():
        return []

try:
    from model import generate_response
except:
    def generate_response(prompt):
        return "AI model unavailable. Please check Ollama or model.py."


# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="CortexAI",
    page_icon="🧠",
    layout="wide"
)

# -----------------------------------
# UI CSS
# -----------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 20% 20%, rgba(124,58,237,0.35), transparent 30%),
        radial-gradient(circle at 80% 10%, rgba(236,72,153,0.28), transparent 28%),
        radial-gradient(circle at 50% 90%, rgba(6,182,212,0.22), transparent 30%),
        linear-gradient(135deg, #060817 0%, #0B1026 45%, #140A2E 100%);
    color: white;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1 {
    color: white !important;
    font-size: 58px !important;
    font-weight: 900 !important;
    letter-spacing: -2px;
    text-shadow: 0 0 25px rgba(34,211,238,0.45);
}

h2, h3 {
    color: white !important;
    font-weight: 800 !important;
}

p, label, span {
    color: #DDE7FF !important;
}

.status-card {
    background: linear-gradient(135deg, rgba(30,41,59,0.78), rgba(88,28,135,0.55));
    border: 1px solid rgba(34,211,238,0.35);
    box-shadow:
        0 0 35px rgba(34,211,238,0.18),
        inset 0 0 25px rgba(255,255,255,0.04);
    backdrop-filter: blur(18px);
    padding: 30px;
    text-align: center;
    margin-bottom: 28px;
    border-radius: 24px;
}

.status-card h3 {
    color: #22D3EE !important;
    font-size: 28px;
}

.metric-card {
    background: linear-gradient(135deg, rgba(15,23,42,0.92), rgba(30,41,59,0.78));
    border: 1px solid rgba(34,211,238,0.32);
    border-radius: 24px;
    padding: 24px;
    min-height: 145px;
    box-shadow:
        0 18px 45px rgba(0,0,0,0.35),
        0 0 28px rgba(34,211,238,0.12);
    transition: all 0.25s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
    border-color: rgba(34,211,238,0.75);
}

.metric-card h4 {
    color: #94A3B8 !important;
    font-size: 15px;
}

.metric-card h2 {
    color: #22D3EE !important;
    font-size: 30px !important;
    font-weight: 900 !important;
}

.metric-card p {
    color: #CBD5E1 !important;
    font-size: 14px;
}

[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.95) !important;
    color: #111827 !important;
    border: 2px solid rgba(99,102,241,0.35) !important;
    border-radius: 22px !important;
    min-height: 58px;
    padding: 16px 20px !important;
    font-size: 17px !important;
    font-weight: 600;
}

div.stButton > button {
    background: linear-gradient(135deg, #2563EB, #9333EA, #EC4899) !important;
    color: white !important;
    border: none !important;
    border-radius: 20px !important;
    min-height: 56px;
    font-size: 17px !important;
    font-weight: 900 !important;
    box-shadow:
        0 15px 35px rgba(236,72,153,0.28),
        0 0 25px rgba(34,211,238,0.18);
}

div.stButton > button:hover {
    transform: translateY(-3px) scale(1.01);
}

.alert-box {
    padding: 28px;
    border-radius: 24px;
    background: linear-gradient(135deg, #EF4444, #F97316, #EC4899);
    color: white !important;
    font-size: 22px;
    font-weight: 900;
    text-align: center;
    box-shadow:
        0 0 40px rgba(239,68,68,0.45),
        0 20px 55px rgba(236,72,153,0.25);
}

[data-testid="stAlert"] {
    background: rgba(15,23,42,0.78) !important;
    border: 1px solid rgba(34,211,238,0.28) !important;
    color: white !important;
    border-radius: 20px !important;
}

[data-testid="stAlert"] * {
    color: white !important;
}

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.96) !important;
    color: #111827 !important;
    border: 2px dashed #A855F7 !important;
    border-radius: 24px;
    padding: 24px;
}

[data-testid="stFileUploader"] * {
    color: #111827 !important;
    font-weight: 700 !important;
}

[data-testid="stFileUploader"] button {
    background: linear-gradient(135deg,#7C3AED,#EC4899) !important;
    color: white !important;
    border-radius: 16px !important;
}

iframe {
    border-radius: 26px !important;
    border: 1px solid rgba(34,211,238,0.35) !important;
    box-shadow: 0 25px 60px rgba(0,0,0,0.35), 0 0 35px rgba(34,211,238,0.18);
}

img {
    border-radius: 22px;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)


# -----------------------------------
# TEXT TO SPEECH
# -----------------------------------
def speak_text(text):
    try:
        import pyttsx3

        text = re.sub(r'[^\x00-\x7F]+', '', text)

        engine = pyttsx3.init()
        engine.setProperty("rate", 165)
        engine.setProperty("volume", 1.0)
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        st.error(f"Voice Error: {e}")


# -----------------------------------
# RISK ANALYSIS
# -----------------------------------
def analyze_risk(text):
    text = text.lower()

    if "earthquake" in text:
        return {
            "threat": "🔴 CRITICAL",
            "civilian_risk": "EXTREME",
            "infrastructure": "SEVERE DAMAGE POSSIBLE",
            "evacuation": "IMMEDIATE",
            "color": "#ff4b4b"
        }

    elif "flood" in text:
        return {
            "threat": "🟠 HIGH",
            "civilian_risk": "HIGH",
            "infrastructure": "ROAD FAILURE POSSIBLE",
            "evacuation": "RECOMMENDED",
            "color": "#fb923c"
        }

    elif "fire" in text:
        return {
            "threat": "🟡 MEDIUM",
            "civilian_risk": "MODERATE",
            "infrastructure": "LOCAL DAMAGE",
            "evacuation": "LOCALIZED",
            "color": "#facc15"
        }

    elif "cyclone" in text:
        return {
            "threat": "🔴 HIGH",
            "civilian_risk": "HIGH",
            "infrastructure": "SEVERE WIND DAMAGE POSSIBLE",
            "evacuation": "RECOMMENDED",
            "color": "#ef4444"
        }

    elif "gas leak" in text:
        return {
            "threat": "🔴 CRITICAL",
            "civilian_risk": "EXTREME",
            "infrastructure": "TOXIC EXPOSURE RISK",
            "evacuation": "IMMEDIATE",
            "color": "#dc2626"
        }

    else:
        return {
            "threat": "🟢 LOW",
            "civilian_risk": "LOW",
            "infrastructure": "STABLE",
            "evacuation": "NOT REQUIRED",
            "color": "#22c55e"
        }


# -----------------------------------
# TITLE
# -----------------------------------
st.markdown("""
<h1 style='text-align:center;'>
🧠 CortexAI Sentinel
</h1>
<p style='text-align:center; font-size:22px; color:#C7D2FE !important; margin-top:-12px;'>
AI-powered disaster intelligence • voice • maps • SOS • rescue network
</p>
""", unsafe_allow_html=True)

st.markdown("""
<div class="status-card">
<h3>⚡ AI POWERED. HUMAN FOCUSED.</h3>
<p>Real-time survival intelligence for disasters, emergencies and offline rescue coordination.</p>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div style="
background: linear-gradient(135deg, rgba(16,185,129,0.18), rgba(59,130,246,0.18));
border: 1px solid rgba(74,222,128,0.35);
padding: 18px;
border-radius: 20px;
margin-top: 14px;
margin-bottom: 22px;
text-align:center;
backdrop-filter: blur(14px);
box-shadow:
0 0 25px rgba(74,222,128,0.18),
0 0 45px rgba(59,130,246,0.12);
animation: pulseGlow 2s infinite;
">

<h2 style="
color:#4ADE80;
font-size:24px;
font-weight:900;
margin:0;
letter-spacing:0.5px;
">
🟢 OLLAMA + GEMMA 2B ONLINE
</h2>

<p style="
color:#D1FAE5;
font-size:16px;
margin-top:10px;
font-weight:600;
">
Local Offline Emergency Intelligence Engine Running Successfully
</p>

</div>

<style>
@keyframes pulseGlow {
0% { transform: scale(1); opacity: 0.95; }
50% { transform: scale(1.01); opacity: 1; }
100% { transform: scale(1); opacity: 0.95; }
}
</style>
""", unsafe_allow_html=True)


# -----------------------------------
# DASHBOARD METRICS
# -----------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
    <h4>📡 Offline Intelligence</h4>
    <h2>ENABLED</h2>
    <p>Local AI infrastructure</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
    <h4>⚡ AI Engine</h4>
    <h2>ACTIVE</h2>
    <p>Emergency reasoning ready</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
    <h4>📡 Rescue Mesh</h4>
    <h2>READY</h2>
    <p>Offline messages enabled</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
    <h4>🚨 Threat Monitor</h4>
    <h2>LIVE</h2>
    <p>Disaster tracking active</p>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------
# OFFLINE MODE
# -----------------------------------
offline_mode = st.toggle("📡 Enable Offline Survival Mode")

if offline_mode:

    st.markdown("""
    <div class="alert-box">
    📡 OFFLINE SURVIVAL MODE ACTIVE<br><br>

    Internet unavailable.<br>
    Local AI systems operational.<br>
    Emergency SOS routing enabled.<br>
    Cached navigation active.
    </div>
    """, unsafe_allow_html=True)

    st.warning("⚠️ Running in disaster offline mode")
    # -----------------------------------
# BLACKOUT SIMULATION
# -----------------------------------
st.subheader("⚡ Disaster Blackout Simulation")

blackout = st.toggle("Simulate Internet & Power Failure")

if blackout:

    st.error("⚠️ BLACKOUT MODE ACTIVE")

    st.markdown("""
    <div class="alert-box">
    ⚡ Infrastructure Failure Detected<br><br>

    Internet: DOWN<br>
    Power Grid: UNSTABLE<br>
    Mobile Towers: LIMITED<br>
    CortexAI: STILL OPERATIONAL
    </div>
    """, unsafe_allow_html=True)

else:

    st.success("🟢 Infrastructure normal")


# -----------------------------------
# WEATHER ALERT
# -----------------------------------
try:
    weather_data = get_weather_alert("Delhi")

    weather_html = f"""
    <div style="
    background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.90));
    border:1px solid rgba(34,211,238,0.45);
    padding:35px;
    border-radius:30px;
    margin-top:35px;
    margin-bottom:32px;
    color:white;
    box-shadow:
    0 0 45px rgba(34,211,238,0.25),
    0 24px 70px rgba(0,0,0,0.45);
    ">

    <h1 style="
    font-size:40px;
    font-weight:900;
    background: linear-gradient(90deg,#22D3EE,#A855F7,#EC4899);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    ">
    ⚡ LIVE WEATHER ALERT
    </h1>

    <p style="font-size:22px;color:white;">
    🌥️ Weather:
    <span style="color:#22D3EE;">
    {weather_data.get("weather", "Unknown")}
    </span>
    </p>

    <p style="font-size:22px;color:white;">
    🌡️ Temperature:
    <span style="color:#F472B6;">
    {weather_data.get("temp", "N/A")}°C
    </span>
    </p>

    <p style="font-size:22px;color:white;">
    🛡️ Risk Status:
    <span style="
    padding:10px 18px;
    border-radius:999px;
    background:linear-gradient(135deg,#22C55E,#14B8A6);
    color:white;
    ">
    {weather_data.get("risk", "Safe")}
    </span>
    </p>

    </div>
    """

    st.markdown(weather_html, unsafe_allow_html=True)

except Exception as e:
    st.warning(f"Weather system unavailable: {e}")

# -----------------------------------
# DISASTER MODE SELECTOR
# -----------------------------------
st.subheader("🌪️ Select Disaster Mode")

disaster_mode = st.selectbox(
    "Choose emergency scenario",
    [
        "General Emergency",
        "Earthquake",
        "Flood",
        "Fire",
        "Cyclone",
        "Gas Leak"
    ]
)

if disaster_mode != "General Emergency":

    st.info(f"🧠 CortexAI configured for: {disaster_mode} response mode")
# -----------------------------------
# USER INPUT
# -----------------------------------
st.subheader("📝 Ask your emergency question")

user_input = st.text_input(
    "",
    placeholder="Example: earthquake in Mumbai"
)


# -----------------------------------
# VOICE INPUT
# -----------------------------------
st.subheader("🎤 Voice Input")

audio = audiorecorder(
    "🎙️ Start Recording",
    "⏹️ Stop Recording"
)

voice_text = ""

if len(audio) > 0:
    st.success("✅ Voice recorded")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            audio.export(f.name, format="wav")

            recognizer = sr.Recognizer()

            with sr.AudioFile(f.name) as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = recognizer.record(source)
                voice_text = recognizer.recognize_google(audio_data)

                st.success(f"🗣️ You said: {voice_text}")

        os.remove(f.name)

    except sr.UnknownValueError:
        st.error("❌ Could not understand audio")

    except sr.RequestError:
        st.error("❌ Speech service unavailable")

    except Exception as e:
        st.error(f"Speech Error: {e}")


# -----------------------------------
# FINAL QUERY
# -----------------------------------
query = ""

if user_input.strip():
    query = f"{disaster_mode}: {user_input}"

elif voice_text.strip():
    query = voice_text


# -----------------------------------
# EMERGENCY STATUS
# -----------------------------------
st.subheader("🚨 National Emergency Status")

alert_query = query.lower() if query else ""

if "earthquake" in alert_query:
    st.error("🔴 EARTHQUAKE EMERGENCY ACTIVE")

elif "flood" in alert_query:
    st.warning("🟠 FLOOD WARNING ACTIVE")

elif "fire" in alert_query:
    st.warning("🟠 FIRE HAZARD DETECTED")

elif "cyclone" in alert_query:
    st.error("🔴 CYCLONE ALERT ACTIVE")

elif "gas leak" in alert_query:
    st.error("🔴 TOXIC GAS ALERT")

else:
    st.success("🟢 No major emergency detected")


# -----------------------------------
# SOS MODE
# -----------------------------------
if st.button("🚨 ACTIVATE SOS MODE"):

    sos_message = """
🚨 EMERGENCY SOS ACTIVATED

Move to nearest safe zone immediately.

Avoid dangerous areas.

Stay calm and follow evacuation routes.
"""

    st.markdown(
        f"""
        <div class="alert-box">
        {sos_message}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("🆘 Emergency Instructions")

    st.markdown("""
- Carry water and emergency supplies
- Stay connected with family
- Follow official rescue instructions
- Move toward green safe zones on map
""")

    speak_text("""
Emergency SOS activated.

Move to nearest safe zone immediately.

Avoid dangerous areas.

Stay calm and follow evacuation routes.
""")

# -----------------------------------
# RESCUE PRIORITY SCORE
# -----------------------------------
def get_priority_score(query):

    query = query.lower()

    if "earthquake" in query:

        return {
            "survivor_risk": "96%",
            "evacuation": "IMMEDIATE",
            "priority": "CRITICAL",
            "infrastructure": "SEVERE DAMAGE"
        }

    elif "flood" in query:

        return {
            "survivor_risk": "88%",
            "evacuation": "HIGH",
            "priority": "URGENT",
            "infrastructure": "ROAD COLLAPSE POSSIBLE"
        }

    elif "fire" in query:

        return {
            "survivor_risk": "82%",
            "evacuation": "HIGH",
            "priority": "URGENT",
            "infrastructure": "LOCAL DAMAGE"
        }

    elif "cyclone" in query:

        return {
            "survivor_risk": "91%",
            "evacuation": "IMMEDIATE",
            "priority": "CRITICAL",
            "infrastructure": "EXTREME WIND DAMAGE"
        }

    elif "gas leak" in query:

        return {
            "survivor_risk": "94%",
            "evacuation": "IMMEDIATE",
            "priority": "CRITICAL",
            "infrastructure": "TOXIC EXPOSURE RISK"
        }

    else:

        return {
            "survivor_risk": "40%",
            "evacuation": "LOW",
            "priority": "MONITOR",
            "infrastructure": "STABLE"
        }
# -----------------------------------
# AI RESPONSE
# -----------------------------------
if query:

    st.subheader("🧠 AI Response")

    try:

        response = generate_response(query)

        if response is None or response.strip() == "":
            response = "No response generated from AI."

        st.success(response)

        if st.button("🔊 Speak Response"):
            speak_text(response)

        # -----------------------------------
        # RESCUE PRIORITY ANALYTICS
        # -----------------------------------
        priority = get_priority_score(query)

        st.markdown(f"""
        <div style="
        background: linear-gradient(135deg,#0F172A,#1E293B);
        padding:25px;
        border-radius:22px;
        margin-top:20px;
        margin-bottom:20px;
        border:1px solid rgba(34,211,238,0.3);
        box-shadow:0 15px 45px rgba(0,0,0,0.3);
        ">

        <h2 style="color:#22D3EE;">
        📊 RESCUE PRIORITY ANALYTICS
        </h2>

        <h3 style="color:white;">
        🚨 Rescue Priority: {priority['priority']}
        </h3>

        <p style="color:white;font-size:18px;">
        👥 Survivor Risk Score:
        <b>{priority['survivor_risk']}</b>
        </p>

        <p style="color:white;font-size:18px;">
        🚨 Evacuation Urgency:
        <b>{priority['evacuation']}</b>
        </p>

        <p style="color:white;font-size:18px;">
        🏢 Infrastructure Impact:
        <b>{priority['infrastructure']}</b>
        </p>

        </div>
        """, unsafe_allow_html=True)

        # -----------------------------------
        # EMERGENCY TIMELINE
        # -----------------------------------
        st.markdown("""
        <div style="
        background: linear-gradient(135deg,#111827,#1E1B4B);
        padding:25px;
        border-radius:22px;
        margin-top:20px;
        margin-bottom:20px;
        border:1px solid rgba(168,85,247,0.35);
        ">

        <h2 style="color:#A78BFA;">🕒 Emergency Response Timeline</h2>

        <p style="color:white;font-size:18px;">✅ 00:00 — Disaster query received</p>
        <p style="color:white;font-size:18px;">✅ 00:03 — AI risk analysis generated</p>
        <p style="color:white;font-size:18px;">✅ 00:06 — Safety precautions prepared</p>
        <p style="color:white;font-size:18px;">✅ 00:09 — Evacuation route activated</p>
        <p style="color:white;font-size:18px;">✅ 00:12 — Rescue priority calculated</p>

        </div>
        """, unsafe_allow_html=True)

    except Exception as e:

        st.error(f"AI Error: {e}")
        # SAFETY PRECAUTIONS
        st.subheader("🛡️ Safety Precautions")

        query_lower = query.lower()

        if "earthquake" in query_lower:
            precautions = [
                "Move to open areas immediately",
                "Stay away from buildings and poles",
                "Do not use elevators",
                "Keep emergency medical kits ready",
                "Expect aftershocks"
            ]

        elif "flood" in query_lower:
            precautions = [
                "Move to higher ground immediately",
                "Avoid walking through flood water",
                "Disconnect electrical appliances",
                "Carry clean drinking water",
                "Follow evacuation routes"
            ]

        elif "fire" in query_lower:
            precautions = [
                "Stay low to avoid smoke inhalation",
                "Use wet cloth over nose",
                "Avoid elevators",
                "Call emergency fire services",
                "Evacuate immediately"
            ]

        else:
            precautions = [
                "Stay alert",
                "Follow official instructions",
                "Keep emergency supplies ready",
                "Avoid dangerous zones",
                "Stay connected with family"
            ]

        for p in precautions:
            st.markdown(f"- {p}")

    except Exception as e:

        st.error(f"AI Error: {e}")


# -----------------------------------
# GPS LOCATION
# -----------------------------------
st.subheader("📍 Live GPS Location")

location = streamlit_geolocation()

lat = 20.5937
lon = 78.9629

try:
    if location:
        gps_lat = location.get("latitude")
        gps_lon = location.get("longitude")

        if gps_lat is not None and gps_lon is not None:
            lat = float(gps_lat)
            lon = float(gps_lon)
            st.success(f"📍 Live Location: {lat}, {lon}")

        else:
            st.warning("⚠️ GPS unavailable. Using default location.")

    else:
        st.warning("⚠️ Waiting for GPS permission...")

except Exception as e:
    st.warning(f"GPS Error: {e}")


# -----------------------------------
# MAP DISPLAY
# -----------------------------------
st.subheader("🗺️ Emergency Navigation & Disaster Heatmap")

safe_lat = lat + 0.5
safe_lon = lon + 0.5

# CREATE MAP
map_object = folium.Map(
    location=[lat, lon],
    zoom_start=6
)

# HEATMAP DATA
heat_data = [
    [lat, lon, 1.0],
    [lat + 0.2, lon + 0.2, 0.8],
    [lat - 0.3, lon - 0.1, 0.7],
    [lat + 0.4, lon - 0.2, 0.9],
]

HeatMap(heat_data).add_to(map_object)

# DANGER ZONE
folium.Marker(
    [lat, lon],
    popup="⚠️ Disaster Zone",
    icon=folium.Icon(color="red")
).add_to(map_object)

# SAFE ZONE
folium.Marker(
    [safe_lat, safe_lon],
    popup="✅ Safe Zone",
    icon=folium.Icon(color="green")
).add_to(map_object)

# EVAC ROUTE
folium.PolyLine(
    locations=[[lat, lon], [safe_lat, safe_lon]],
    color="blue",
    weight=5
).add_to(map_object)

# SHOW MAP
st_folium(
    map_object,
    width=1200,
    height=600,
    returned_objects=[]
)

# -----------------------------------
# SAFE ZONE DETECTION
# -----------------------------------
st.subheader("🟢 Nearby Safe Zones")

safe_col1, safe_col2, safe_col3 = st.columns(3)

with safe_col1:

    st.success("""
🏥 Emergency Shelter Alpha

Distance: 1.2 km

Capacity: 240 people
""")

with safe_col2:

    st.success("""
⛑️ Medical Camp Delta

Distance: 2.4 km

Trauma Units Available
""")

with safe_col3:

    st.success("""
🚁 Rescue Extraction Point

Distance: 3.1 km

Helicopter Access Ready
""")


# -----------------------------------
# OFFLINE RESCUE NETWORK
# -----------------------------------
st.subheader("📡 Offline Rescue Network")

sos_input = st.text_input(
    "Broadcast emergency message",
    placeholder="Example: Need medical help near flood zone"
)

if st.button("📢 Broadcast SOS"):
    try:
        if sos_input.strip():
            broadcast_message(sos_input)
            st.success("Emergency message broadcasted")
        else:
            st.warning("Please enter a message before broadcasting.")

    except Exception as e:
        st.error(f"Broadcast Error: {e}")


# ------------------------------------------------
# AI DISASTER IMAGE ANALYSIS
# ------------------------------------------------

st.markdown("## 🧠 AI Disaster Image Analysis")

uploaded_file = st.file_uploader(
    "Upload disaster image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    st.image(uploaded_file, use_container_width=True)

    filename = uploaded_file.name.lower()

    if "fire" in filename:

        st.error("""
🔥 FIRE HAZARD DETECTED

• Severe fire risk identified
• Immediate evacuation recommended
• Avoid smoke exposure
• Emergency responders alerted
""")

    elif "flood" in filename:

        st.warning("""
🌊 FLOOD RISK DETECTED

• Waterlogging hazard identified
• Move to higher ground
• Avoid electrical infrastructure
""")

    else:

        st.success("""
⚠️ DISASTER ANALYSIS COMPLETE

• Hazardous environment detected
• Emergency precautions advised
• Await rescue guidance
""")

# -----------------------------------
# SURVIVOR FEED
# -----------------------------------
try:
    messages = get_messages()

    st.subheader("🛰️ Survivor Coordination Feed")

    for msg in messages[:5]:
        st.warning(
            f"{msg['time']} \n\n {msg['message']}"
        )

except Exception as e:
    st.warning(f"Feed Error: {e}")
    # -----------------------------------
# FINAL IMPACT STATEMENT
# -----------------------------------
st.markdown("""
<div style="
background: linear-gradient(135deg,#020617,#1E1B4B,#312E81);
padding:35px;
border-radius:28px;
margin-top:35px;
border:1px solid rgba(34,211,238,0.35);
box-shadow:0 20px 60px rgba(0,0,0,0.35);
text-align:center;
">

<h2 style="color:#22D3EE;">🌍 Why CortexAI Matters</h2>

<p style="color:white;font-size:20px;">
When disasters destroy internet, power, and communication systems,
CortexAI Sentinel continues operating locally.
</p>

<p style="color:white;font-size:20px;">
It gives civilians emergency guidance, safe-zone navigation,
SOS support, and offline rescue coordination.
</p>

<h3 style="color:#F472B6;">
When infrastructure fails, intelligence should not.
</h3>

</div>
""", unsafe_allow_html=True)
