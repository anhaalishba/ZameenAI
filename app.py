import streamlit as st
import requests
import os
import base64
import datetime
from openai import OpenAI
from google import genai
from PIL import Image


# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="ZameenAI Ultra",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_KEY = st.secrets["OPENWEATHER_API_KEY"]
gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# =============================
# GROQ CLIENT (ONLY 1 API)
# =============================
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# =============================
# SYSTEM PROMPT (FARMING ONLY)
# =============================
SYSTEM_PROMPT = """
You are ZameenAI, an expert agricultural assistant for Pakistan.
You ONLY answer questions related to:
-This app ZameenAI Ultra
- Farming
- Crops
- Soil
- Fertilizers
- Irrigation
- Weather for agriculture
- Pests & diseases
- Yield, harvesting, farm management
If the question is NOT related to farming,
reply exactly:
"I can only help with farming and agriculture-related questions."
"""

FARMING_KEYWORDS = [
    "crop","wheat","rice","maize","cotton","sugarcane",
    "fertilizer","soil","irrigation","pest","disease",
    "harvest","yield","farm","agriculture","weather"
]

def is_farming_question(text):
    return any(word in text.lower() for word in FARMING_KEYWORDS)

# =============================
# THEME / CUSTOM CSS
# =============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 15% 0%, rgba(37,99,235,0.18) 0%, transparent 45%),
        radial-gradient(circle at 85% 20%, rgba(59,130,246,0.10) 0%, transparent 40%),
        linear-gradient(180deg, #0b0d12 0%, #10131a 45%, #14181f 100%);
    color: #e7eaf0;
}

/* Hide default streamlit chrome a bit */
#MainMenu, footer {visibility: hidden;}

/* Make default streamlit text light on dark bg */
p, span, label, .stMarkdown, h1, h2, h3, h4, h5 {
    color: #e7eaf0;
}

/* Hero header */
.hero {
    background: linear-gradient(135deg, #131722 0%, #171c28 55%, #1b2233 100%);
    padding: 34px 40px;
    border-radius: 20px;
    margin-bottom: 22px;
    border: 1px solid #262e3d;
    box-shadow: 0 14px 34px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.03);
}
.hero h1 {
    color: #ffffff;
    font-size: 34px;
    font-weight: 700;
    margin: 0;
    background: linear-gradient(90deg, #5eb1ff, #7c8cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p {
    color: #93a0b5;
    font-size: 15px;
    margin-top: 6px;
    margin-bottom: 0;
}

/* ===================================== */
/* MODERN SEGMENTED NAV                  */
/* ===================================== */
div[data-testid="stRadio"] {
    background: linear-gradient(180deg, #12151d 0%, #0f1218 100%);
    border: 1px solid #232a38;
    border-radius: 16px;
    padding: 10px;
    box-shadow: inset 0 1px 4px rgba(0,0,0,0.4);
    margin-bottom: 8px;
}
div[role="radiogroup"] {
    gap: 8px;
    flex-wrap: wrap;
}
div[role="radiogroup"] label {
    background: transparent;
    border: 1px solid #262e3d;
    padding: 10px 20px;
    border-radius: 12px;
    transition: all 0.18s ease-in-out;
    color: #9aa5b6 !important;
    font-weight: 500;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
}
/* restyle the little radio circle instead of hiding it */
div[role="radiogroup"] label [data-baseweb="radio"] > div {
    background-color: transparent !important;
    border-color: #3b4252 !important;
}
div[role="radiogroup"] label:hover {
    border-color: #3b82f6;
    color: #cfe0ff !important;
    background: rgba(59,130,246,0.08);
}
div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    border-color: #3b82f6;
    color: #ffffff !important;
    box-shadow: 0 6px 18px rgba(37,99,235,0.45);
}
div[role="radiogroup"] label:has(input:checked) p {
    color: #ffffff !important;
    font-weight: 600;
}
div[role="radiogroup"] label:has(input:checked) [data-baseweb="radio"] > div {
    border-color: #ffffff !important;
}

/* Section card wrapper */
.section-card {
    background: linear-gradient(180deg, #161a22 0%, #12151c 100%);
    border-radius: 18px;
    padding: 26px 28px;
    box-shadow: 0 8px 26px rgba(0,0,0,0.45);
    border: 1px solid #232a38;
    margin-bottom: 20px;
}

.section-title {
    font-size: 22px;
    font-weight: 600;
    color: #f2f4f8;
    margin-bottom: 4px;
}
.section-sub {
    color: #8994a6;
    font-size: 14px;
    margin-bottom: 18px;
}

/* Result / info cards */
.result-card {
    border-radius: 14px;
    padding: 18px 20px;
    margin-top: 12px;
    font-size: 15px;
    line-height: 1.6;
    border: 1px solid transparent;
}
.result-green {
    background: rgba(34,197,94,0.10);
    border-left: 4px solid #22c55e;
    border-color: rgba(34,197,94,0.2);
    color: #c9f5d8;
}
.result-blue {
    background: rgba(59,130,246,0.10);
    border-left: 4px solid #3b82f6;
    border-color: rgba(59,130,246,0.2);
    color: #cfe0ff;
}
.result-amber {
    background: rgba(224,165,44,0.10);
    border-left: 4px solid #e0a52c;
    border-color: rgba(224,165,44,0.2);
    color: #f5e2bd;
}

/* Metric-style tiles */
.tile-row {
    display: flex;
    gap: 14px;
    flex-wrap: wrap;
}
.tile {
    flex: 1;
    min-width: 140px;
    background: linear-gradient(180deg, #181d27 0%, #12151c 100%);
    border-radius: 14px;
    padding: 16px 18px;
    border: 1px solid #232a38;
    text-align: center;
    transition: transform 0.15s ease, border-color 0.15s ease;
}
.tile:hover {
    transform: translateY(-2px);
    border-color: #3b82f6;
}
.tile .label {
    font-size: 12px;
    color: #8994a6;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.tile .value {
    font-size: 24px;
    font-weight: 700;
    background: linear-gradient(90deg, #5eb1ff, #7c8cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 4px;
}

/* Inputs */
.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
    background-color: #161a22 !important;
    color: #e7eaf0 !important;
    border: 1px solid #232a38 !important;
    border-radius: 10px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.25) !important;
}

/* Buttons */
.stButton>button, .stFormSubmitButton>button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 10px 22px;
    font-weight: 600;
    box-shadow: 0 4px 16px rgba(37,99,235,0.35);
}
.stButton>button:hover, .stFormSubmitButton>button:hover {
    background: linear-gradient(135deg, #1d4ed8, #1e40af);
    color: #ffffff;
}

/* Chat bubbles look a little softer */
[data-testid="stChatMessage"] {
    border-radius: 14px;
    background: #161a22;
    border: 1px solid #232a38;
}
</style>
""", unsafe_allow_html=True)


def result_card(text, style="green"):
    st.markdown(f'<div class="result-card result-{style}">{text}</div>', unsafe_allow_html=True)


# =============================
# HERO HEADER
# =============================
st.markdown("""
<div class="hero">
    <h1>🌾 ZameenAI Ultra</h1>
    <p>AI-Powered Smart Farming Decision System — weather, disease detection, market insights & advisory, all in one place.</p>
</div>
""", unsafe_allow_html=True)

# =============================
# MENU
# =============================
menu = st.radio(
    "Navigation Menu",
    ["🌦 Weather", "🦠 Disease Detection", "💬 Chatbot", "🤖 Smart Advisory",
     "🌾 Crop Estimator", "🧪 Fertilizer AI", "📈 Market & Profit", "📅 Crop Calendar"],
    horizontal=True,
    label_visibility="collapsed"
)

st.write("")

# =============================
# WEATHER
# =============================
if menu == "🌦 Weather":

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🌦 Live Weather</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Check current conditions for your farm location.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        city = st.text_input("Enter City Name", label_visibility="collapsed", placeholder="Enter city name e.g. Multan")
    with col2:
        get_weather = st.button("Get Weather", use_container_width=True)

    if get_weather:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            temp = data["main"]["temp"]
            wind = data["wind"]["speed"]
            humidity = data["main"]["humidity"]
            description = data["weather"][0]["description"]

            st.markdown(f"""
            <div class="tile-row">
                <div class="tile"><div class="label">Temperature</div><div class="value">{temp}°C</div></div>
                <div class="tile"><div class="label">Wind Speed</div><div class="value">{wind} m/s</div></div>
                <div class="tile"><div class="label">Humidity</div><div class="value">{humidity}%</div></div>
                <div class="tile"><div class="label">Condition</div><div class="value" style="font-size:16px; text-transform:capitalize;">{description}</div></div>
            </div>
            """, unsafe_allow_html=True)
        else:
            result_card("❌ City not found", "amber")

    st.markdown('</div>', unsafe_allow_html=True)

# =============================
# CROP ESTIMATOR
# =============================
elif menu == "🌾 Crop Estimator":

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🌾 Crop Cost & Yield Estimator</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Estimate cost and yield based on land area.</div>', unsafe_allow_html=True)

    crops = {
        "Wheat": {"cost": 50000, "yield": 30},
        "Rice": {"cost": 60000, "yield": 35},
        "Maize": {"cost": 45000, "yield": 28},
        "Sugarcane": {"cost": 80000, "yield": 60},
        "Cotton": {"cost": 70000, "yield": 25}
    }

    col1, col2 = st.columns(2)
    with col1:
        crop = st.selectbox("Select Crop", list(crops.keys()))
    with col2:
        area = st.number_input("Land Area (acres)", min_value=1)

    if st.button("Calculate"):
        st.markdown(f"""
        <div class="tile-row">
            <div class="tile"><div class="label">Estimated Cost</div><div class="value">Rs {crops[crop]['cost'] * area:,}</div></div>
            <div class="tile"><div class="label">Estimated Yield</div><div class="value">{crops[crop]['yield'] * area} maunds</div></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =============================
# MARKET & PROFIT
# =============================
elif menu == "📈 Market & Profit":

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Profit Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Predict revenue and profit for your crop and land size.</div>', unsafe_allow_html=True)

    prices = {
        "Wheat": 3900,
        "Rice": 4500,
        "Maize": 3500,
        "Sugarcane": 3000,
        "Cotton": 8500
    }

    col1, col2 = st.columns(2)
    with col1:
        crop = st.selectbox("Crop", list(prices.keys()))
    with col2:
        area = st.number_input("Land Area (acres)", min_value=1)

    if st.button("Predict"):
        revenue = prices[crop] * area * 30
        cost = 50000 * area
        profit = revenue - cost
        profit_style = "green" if profit >= 0 else "amber"

        st.markdown(f"""
        <div class="tile-row">
            <div class="tile"><div class="label">Revenue</div><div class="value">Rs {revenue:,}</div></div>
            <div class="tile"><div class="label">Estimated Cost</div><div class="value">Rs {cost:,}</div></div>
        </div>
        """, unsafe_allow_html=True)
        result_card(f"🏆 <b>Profit: Rs {profit:,}</b>", profit_style)

    st.markdown('</div>', unsafe_allow_html=True)

# =============================
# FERTILIZER AI
# =============================
elif menu == "🧪 Fertilizer AI":

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧪 Fertilizer Recommendation</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Get a quick fertilizer suggestion for your crop.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col1:
        crop = st.text_input("Crop Name", label_visibility="collapsed", placeholder="e.g. Wheat, Rice, Cotton")
    with col2:
        recommend = st.button("Recommend", use_container_width=True)

    if recommend:
        if crop.lower() == "wheat":
            result_card("✅ Use Urea + DAP in split doses", "green")
        elif crop.lower() == "rice":
            result_card("✅ Use NPK 20-20-20, maintain flooded field", "green")
        else:
            result_card("ℹ️ Use balanced NPK with organic compost", "blue")

    st.markdown('</div>', unsafe_allow_html=True)

# =============================
# CROP CALENDAR (WITH DROPDOWN)
# =============================
elif menu == "📅 Crop Calendar":

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📅 Pakistan Crop Calendar</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Select a month to see the recommended agricultural activities.</div>', unsafe_allow_html=True)

    months_list = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    current_month_str = datetime.datetime.now().strftime("%B")
    default_index = months_list.index(current_month_str)

    calendar_data = {
        "January": "🌾 **Wheat:** Apply second irrigation and urea. Prepare land for spring vegetables like gourds.",
        "February": "🥔 **Potato:** Harvesting begins. **Sugarcane:** Ideal time for spring planting.",
        "March": "☁️ **Cotton:** Start land preparation. **Sunflower:** Sowing should be completed this month.",
        "April": "🌾 **Rice:** Prepare nurseries for Basmati. **Wheat:** Harvesting starts in Sindh and Southern Punjab.",
        "May": "🎋 **Sugarcane:** Focus on irrigation and hoeing. **Cotton:** Peak sowing time in Punjab.",
        "June": "🌱 **Rice:** Transplantation to main fields. **Maize:** Sowing for the autumn crop begins.",
        "July": "🌽 **Monsoon Crops:** Maintenance of Maize and Sugarcane. Ensure proper drainage for rain.",
        "August": "🐛 **Cotton:** Critical month for pest scouting (Whitefly/Bollworms). **Pulses:** Sowing of Mung and Mash beans.",
        "September": "🌾 **Rice:** Early varieties (like KS-282) are ready for harvest. **Mustard:** Start sowing Toria.",
        "October": "🚜 **Wheat Prep:** Land preparation is key. **Oilseeds:** Best time for sowing Mustard and Canola.",
        "November": "🌾 **Wheat:** Peak sowing time for maximum yield. **Sugarcane:** Harvesting and crushing season begins.",
        "December": "🥦 **Vegetables:** Care for winter crops (Cabbage, Radish). **Wheat:** Apply first irrigation (Kor) 20-25 days after sowing."
    }

    selected_month = st.selectbox("Select Month:", months_list, index=default_index)

    st.markdown(f"#### 🗓️ Agricultural Activities for **{selected_month}**")
    result_card(calendar_data.get(selected_month), "green")

    if selected_month == current_month_str:
        result_card("✨ <b>Note:</b> This is the current month. Prioritize these tasks for your farm.", "blue")

    st.markdown('</div>', unsafe_allow_html=True)

# =============================
# SMART ADVISORY (AI)
# =============================
elif menu == "🤖 Smart Advisory":

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🤖 AI Farming Advisory</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Get a tailored recommendation based on your crop, soil, and season.</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        crop = st.text_input("Crop")
    with col2:
        soil = st.selectbox("Soil Type", ["Sandy", "Clay", "Loamy"])
    with col3:
        season = st.selectbox("Season", ["Summer", "Winter", "Monsoon", "Spring"])

    if st.button("Generate Advisory"):
        prompt = f"""
        Crop: {crop}
        Soil: {soil}
        Season: {season}
        Give farming advice.
        """
        with st.spinner("Generating advisory..."):
            response = client.responses.create(
                model="openai/gpt-oss-20b",
                input=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_output_tokens=1000
            )
        result_card(response.output_text.replace("\n", "<br>"), "green")

    st.markdown('</div>', unsafe_allow_html=True)

# =============================
# CHATBOT (FARMING ONLY)
# =============================
elif menu == "💬 Chatbot":

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💬 Farming Assistant Chatbot</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Ask anything about crops, soil, pests, or irrigation.</div>', unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_box = st.container(height=420)
    with chat_box:
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

    if user_input := st.chat_input("Ask farming question..."):
        st.session_state.messages.append({"role": "user", "content": user_input})

        if not is_farming_question(user_input):
            reply = "🌾 I can only help with farming and agriculture-related questions."
        else:
            response = client.responses.create(
                model="openai/gpt-oss-20b",
                input=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ],
                max_output_tokens=1000
            )
            reply = response.output_text

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =============================
# DISEASE DETECTION (BYPASS 403)
# =============================
elif menu == "🦠 Disease Detection":

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🦠 Crop Disease Detection</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Take a picture of the crop leaf or upload one for instant AI analysis.</div>', unsafe_allow_html=True)

    # Form use karne se Axios error bypass ho jata hai
    with st.form("disease_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            cam_image = st.camera_input("Take a photo of the leaf")
        with col2:
            file_image = st.file_uploader("Select File", type=["jpg", "jpeg", "png"])

        submit_button = st.form_submit_button("Check Disease", use_container_width=True)

    target_image = cam_image if cam_image is not None else file_image

    if target_image is not None and submit_button:
        try:
            img = Image.open(target_image)
            img.thumbnail((1024, 1024))

            with st.spinner("Checking..."):
                prompt = """
                    You are an expert plant pathologist for Pakistan's crops.
                    Analyze this image of a  plant.
                    1. Name the disease.
                    2. Give a brief explanation of why it happened.
                    3. Suggest organic (desi) and chemical remedies.
                    4.Answer briefly in 200 words max.
                    If the plant is healthy, congratulate the farmer.
                    """

                response = gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[prompt, img]
                )

                st.markdown('<div class="section-sub" style="color:#5eb1ff; font-weight:600;">✅ Analysis Result</div>', unsafe_allow_html=True)
                result_card(response.text.replace("\n", "<br>"), "green")

        except Exception as e:
            result_card(f"❌ Error: {e}", "amber")
            result_card("⚠️ Agar Axios 403 aaye, toh photo ka size kam karein ya camera input use karein.", "amber")

    st.markdown('</div>', unsafe_allow_html=True)
