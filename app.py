import streamlit as st
import requests
import os
import base64
import datetime
from openai import OpenAI
from google import genai
from PIL import Image
from streamlit_mic_recorder import speech_to_text


# =============================
# CONFIG
# =============================
st.set_page_config(
    page_title="🌾 ZameenAI",
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
# THEME / CUSTOM CSS
# (black - grey - teal/blue-green theme)
# =============================
CUSTOM_CSS = """
<style>
    :root {
        --bg-main: #0e1117;
        --bg-panel: #161b22;
        --bg-panel-2: #1c2330;
        --border-color: #2a3140;
        --accent: #2dd4bf;      /* teal */
        --accent-2: #38bdf8;    /* sky blue */
        --accent-grad: linear-gradient(135deg, #2dd4bf 0%, #38bdf8 100%);
        --text-main: #e6e9ef;
        --text-muted: #9aa4b2;
    }

    /* App background */
    .stApp {
        background: radial-gradient(circle at 20% 0%, #131a24 0%, #0b0e13 55%, #08090c 100%);
        color: var(--text-main);
    }

    /* Hide default Streamlit chrome for a cleaner look */
    #MainMenu, footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: transparent;}

    /* Hero title block */
    .zameen-hero {
        padding: 1.6rem 1.8rem;
        border-radius: 18px;
        background: linear-gradient(120deg, rgba(45,212,191,0.12), rgba(56,189,248,0.08));
        border: 1px solid var(--border-color);
        margin-bottom: 1.2rem;
    }
    .zameen-hero h1 {
        font-size: 2.1rem;
        margin: 0;
        background: var(--accent-grad);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    .zameen-hero p {
        color: var(--text-muted);
        margin: 0.25rem 0 0 0;
        font-size: 0.95rem;
    }

    /* Radio menu styled as pill tabs */
    div[role="radiogroup"] {
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    div[role="radiogroup"] label {
        background: var(--bg-panel);
        border: 1px solid var(--border-color);
        padding: 0.5rem 1rem;
        border-radius: 999px;
        transition: all 0.15s ease-in-out;
        color: var(--text-muted) !important;
    }
    div[role="radiogroup"] label:hover {
        border-color: var(--accent);
        color: var(--text-main) !important;
    }
    div[role="radiogroup"] label[data-checked="true"] {
        background: var(--accent-grad);
        border-color: transparent;
        color: #06141a !important;
        font-weight: 700;
    }

    /* Generic content card wrapper — modern elevated card */
    .zameen-card {
        position: relative;
        background: linear-gradient(180deg, rgba(28,35,48,0.9), rgba(20,25,35,0.9));
        backdrop-filter: blur(6px);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 1.6rem 1.7rem 1.8rem 1.7rem;
        margin-bottom: 1.3rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.03);
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
        overflow: hidden;
    }
    .zameen-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: var(--accent-grad);
        opacity: 0.9;
    }
    .zameen-card:hover {
        transform: translateY(-3px);
        border-color: rgba(45,212,191,0.35);
        box-shadow: 0 16px 40px rgba(0,0,0,0.45), 0 0 0 1px rgba(45,212,191,0.08);
    }

    /* Card header row: icon badge + title + subtitle */
    .zameen-card-header {
        display: flex;
        align-items: center;
        gap: 0.9rem;
        margin-bottom: 1.1rem;
    }
    .zameen-icon-badge {
        flex-shrink: 0;
        width: 46px;
        height: 46px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        background: linear-gradient(135deg, rgba(45,212,191,0.18), rgba(56,189,248,0.18));
        border: 1px solid rgba(45,212,191,0.3);
        box-shadow: 0 4px 14px rgba(45,212,191,0.15);
    }
    .zameen-card-header .titles h3 {
        margin: 0;
        font-size: 1.15rem;
        color: var(--text-main) !important;
        font-weight: 700;
    }
    .zameen-card-header .titles p {
        margin: 0.1rem 0 0 0;
        font-size: 0.82rem;
        color: var(--text-muted);
    }

    /* Section subheader styling */
    h2, h3 {
        color: var(--text-main) !important;
    }

    /* Inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: var(--bg-panel-2) !important;
        border: 1px solid var(--border-color) !important;
        color: var(--text-main) !important;
        border-radius: 12px !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(45,212,191,0.15) !important;
    }

    /* Buttons */
    .stButton button, .stFormSubmitButton button {
        background: var(--accent-grad) !important;
        color: #06141a !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 0.6rem 1.5rem !important;
        transition: transform 0.12s ease-in-out, box-shadow 0.12s ease-in-out;
        box-shadow: 0 4px 14px rgba(45,212,191,0.2);
    }
    .stButton button:hover, .stFormSubmitButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 24px rgba(45, 212, 191, 0.3);
    }

    /* Success / info / warning / error boxes */
    div[data-testid="stAlert"] {
        border-radius: 14px;
        border: 1px solid var(--border-color);
    }

    /* Chat bubbles */
    div[data-testid="stChatMessage"] {
        background: var(--bg-panel);
        border: 1px solid var(--border-color);
        border-radius: 14px;
        padding: 0.4rem 0.6rem;
    }

    /* Metric-like KPI chips (used for weather etc.) */
    .zameen-metric-row { display: flex; gap: 0.8rem; flex-wrap: wrap; }
    .zameen-metric {
        flex: 1 1 160px;
        background: var(--bg-panel-2);
        border: 1px solid var(--border-color);
        border-radius: 14px;
        padding: 0.9rem 1rem;
        text-align: center;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .zameen-metric:hover {
        transform: translateY(-2px);
        border-color: rgba(45,212,191,0.4);
    }
    .zameen-metric .label { color: var(--text-muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.04em; }
    .zameen-metric .value { color: var(--accent); font-size: 1.5rem; font-weight: 800; margin-top: 0.2rem; }

    /* Result stat cards (calculators, recommendations) */
    .zameen-stat-row { display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 0.8rem; }
    .zameen-stat {
        flex: 1 1 200px;
        border-radius: 16px;
        padding: 1.1rem 1.3rem;
        border: 1px solid rgba(45,212,191,0.25);
        background: linear-gradient(135deg, rgba(45,212,191,0.10), rgba(56,189,248,0.06));
        position: relative;
        overflow: hidden;
    }
    .zameen-stat .stat-icon { font-size: 1.4rem; margin-bottom: 0.3rem; display: block; }
    .zameen-stat .stat-label { color: var(--text-muted); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; }
    .zameen-stat .stat-value { color: var(--text-main); font-size: 1.5rem; font-weight: 800; margin-top: 0.15rem; }
    .zameen-stat.positive .stat-value { color: #4ade80; }
    .zameen-stat.accent .stat-value {
        background: var(--accent-grad);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Simple note / tip banner used inside cards */
    .zameen-note {
        margin-top: 0.9rem;
        padding: 0.7rem 1rem;
        border-radius: 12px;
        background: rgba(56,189,248,0.08);
        border: 1px solid rgba(56,189,248,0.25);
        color: var(--text-muted);
        font-size: 0.85rem;
    }

    /* Divider */
    hr { border-color: var(--border-color) !important; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =============================
# SYSTEM PROMPT (FARMING ONLY)
# =============================
SYSTEM_PROMPT = """
You are ZameenAI, a friendly, professional, and intelligent AI farming assistant designed for farmers in Pakistan.

Your primary goal is to help farmers with accurate, practical, and easy-to-understand agricultural advice.

You can answer questions about:
• Farming and Agriculture
• Crops and Crop Management
• Soil Health
• Fertilizers and Nutrients
• Irrigation
• Agricultural Weather
• Plant Diseases and Pest Control
• Harvesting and Yield Improvement
• Farm Management
• This application (ZameenAI) and its features

Languages:
- English
- Urdu
- Sindhi

Rules:
1. Always reply in the same language used by the user unless they request another language.
2. Keep answers simple, practical, and farmer-friendly.
3. If the user greets you (e.g., "Hi", "Hello", "Assalam-o-Alaikum", "Thanks"), respond politely and naturally before continuing the conversation.
4. If the user asks something unrelated to farming or ZameenAI, politely reply:

"I'm ZameenAI, a farming assistant. I can only help with agriculture, crops, soil, fertilizers, irrigation, weather, plant diseases, pest management, and other farming-related topics. If you have any farming question, I'll be happy to help."

5. Never provide misleading information. If you are unsure, clearly say that you are not certain and suggest consulting a local agricultural expert.
6. Give practical recommendations suitable for Pakistan whenever possible.
7. Keep answers concise unless the user asks for a detailed explanation.
"""

FARMING_KEYWORDS = [
    "crop","wheat","rice","maize","cotton","sugarcane",
    "fertilizer","soil","irrigation","pest","disease",
    "harvest","yield","farm","agriculture","weather"
]

def is_farming_question(text):
    return any(word in text.lower() for word in FARMING_KEYWORDS)

# =============================
# HEADER
# =============================
st.markdown(
    """
    <div class="zameen-hero">
        <h1>🌾 ZameenAI</h1>
        <p>AI Powered Smart Farming Decision System</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =============================
# MENU
# =============================
menu = st.radio(
    "Navigation Menu", 
    ["🌦 Weather", "🦠 Disease Detection", "💬 Chatbot","🤖 Smart Advisory","🌾 Crop Estimator", "🧪 Fertilizer AI",  "📈 Market & Profit", "📅 Crop Calendar"],
    horizontal=True,
    label_visibility="collapsed"
)

st.write("")  # small spacer

# =============================
# WEATHER
# =============================

if menu == "🌦 Weather":

    st.markdown('<div class="zameen-card">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="zameen-card-header">
            <div class="zameen-icon-badge">🌦</div>
            <div class="titles">
                <h3>Live Weather</h3>
                <p>Real-time conditions for your area</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    city = st.text_input("Enter City Name")

    if st.button("Get Weather"):

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:

            temp = data["main"]["temp"]
            wind = data["wind"]["speed"]
            humidity = data["main"]["humidity"]
            description = data["weather"][0]["description"]

            st.markdown(
                f"""
                <div class="zameen-metric-row">
                    <div class="zameen-metric">
                        <div class="label">Temperature</div>
                        <div class="value">🌡 {temp}°C</div>
                    </div>
                    <div class="zameen-metric">
                        <div class="label">Wind Speed</div>
                        <div class="value">💨 {wind} m/s</div>
                    </div>
                    <div class="zameen-metric">
                        <div class="label">Humidity</div>
                        <div class="value">💧 {humidity}%</div>
                    </div>
                    <div class="zameen-metric">
                        <div class="label">Condition</div>
                        <div class="value" style="font-size:1.1rem;">🌥 {description}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            st.error("City not found")
    st.markdown('</div>', unsafe_allow_html=True)

# =============================
# CROP ESTIMATOR
# =============================
elif menu == "🌾 Crop Estimator":

    st.markdown('<div class="zameen-card">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="zameen-card-header">
            <div class="zameen-icon-badge">🌾</div>
            <div class="titles">
                <h3>Crop Cost & Yield Estimator</h3>
                <p>Estimate input cost and expected output per acre</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    crops = {
        "Wheat": {"cost": 50000, "yield": 30},
        "Rice": {"cost": 60000, "yield": 35},
        "Maize": {"cost": 45000, "yield": 28},
        "Sugarcane": {"cost": 80000, "yield": 60},
        "Cotton": {"cost": 70000, "yield": 25}
    }

    crop = st.selectbox("Select Crop", list(crops.keys()))
    area = st.number_input("Land Area (acres)", min_value=1)

    if st.button("Calculate"):
        total_cost = crops[crop]['cost'] * area
        total_yield = crops[crop]['yield'] * area
        st.markdown(
            f"""
            <div class="zameen-stat-row">
                <div class="zameen-stat">
                    <span class="stat-icon">💰</span>
                    <div class="stat-label">Estimated Cost</div>
                    <div class="stat-value">Rs {total_cost:,}</div>
                </div>
                <div class="zameen-stat accent">
                    <span class="stat-icon">🌾</span>
                    <div class="stat-label">Expected Yield</div>
                    <div class="stat-value">{total_yield:,} maunds</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

# =============================
# MARKET & PROFIT
# =============================
elif menu == "📈 Market & Profit":

    st.markdown('<div class="zameen-card">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="zameen-card-header">
            <div class="zameen-icon-badge">📈</div>
            <div class="titles">
                <h3>Profit Predictor</h3>
                <p>Quick revenue and profit projection by crop</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    prices = {
        "Wheat": 3900,
        "Rice": 4500,
        "Maize": 3500,
        "Sugarcane": 3000,
        "Cotton": 8500
    }

    crop = st.selectbox("Crop", list(prices.keys()))
    area = st.number_input("Land Area (acres)", min_value=1)

    if st.button("Predict"):
        revenue = prices[crop] * area * 30
        cost = 50000 * area
        profit = revenue - cost
        st.markdown(
            f"""
            <div class="zameen-stat-row">
                <div class="zameen-stat">
                    <span class="stat-icon">💰</span>
                    <div class="stat-label">Revenue</div>
                    <div class="stat-value">Rs {revenue:,}</div>
                </div>
                <div class="zameen-stat positive">
                    <span class="stat-icon">🏆</span>
                    <div class="stat-label">Profit</div>
                    <div class="stat-value">Rs {profit:,}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

# =============================
# FERTILIZER AI
# =============================
elif menu == "🧪 Fertilizer AI":

    st.markdown('<div class="zameen-card">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="zameen-card-header">
            <div class="zameen-icon-badge">🧪</div>
            <div class="titles">
                <h3>Fertilizer Recommendation</h3>
                <p>Get a quick dosage suggestion for your crop</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    crop = st.text_input("Crop Name")

    if st.button("Recommend"):
        if crop.lower() == "wheat":
            st.success("Use Urea + DAP in split doses")
        elif crop.lower() == "rice":
            st.success("Use NPK 20-20-20, maintain flooded field")
        else:
            st.info("Use balanced NPK with organic compost")
    st.markdown('</div>', unsafe_allow_html=True)

# =============================
# CROP CALENDAR
# =============================
# =============================
# CROP CALENDAR (WITH DROPDOWN)
# =============================
elif menu == "📅 Crop Calendar":
    st.markdown('<div class="zameen-card">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="zameen-card-header">
            <div class="zameen-icon-badge">📅</div>
            <div class="titles">
                <h3>Pakistan Crop Calendar</h3>
                <p>Select a month to see recommended agricultural activities</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # List of months for the dropdown
    months_list = [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ]
    
    # Get current month to set as default index
    current_month_str = datetime.datetime.now().strftime("%B")
    default_index = months_list.index(current_month_str)
    
    # Expanded Calendar Data
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

    # Month Selection Dropdown
    selected_month = st.selectbox("Select Month:", months_list, index=default_index)

    # Displaying the Result
    st.markdown(f"---")
    st.markdown(f"#### 🗓️ Agricultural Activities for **{selected_month}**")
    st.success(calendar_data.get(selected_month))
    
    # Highlight if it's the current month
    if selected_month == current_month_str:
        st.markdown(
            '<div class="zameen-note">✨ <strong>Note:</strong> This is the current month. Prioritize these tasks for your farm.</div>',
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

# =============================
# SMART ADVISORY (AI)
# =============================
elif menu == "🤖 Smart Advisory":

    st.markdown('<div class="zameen-card">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="zameen-card-header">
            <div class="zameen-icon-badge">🤖</div>
            <div class="titles">
                <h3>AI Farming Advisory</h3>
                <p>Personalized advice based on your crop, soil and season</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    crop = st.text_input("Crop")
    soil = st.selectbox("Soil Type", ["Sandy", "Clay", "Loamy"])
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
        st.write(response.output_text)
    st.markdown('</div>', unsafe_allow_html=True)

# =============================
# CHATBOT (TEXT + VOICE)
# =============================
elif menu == "💬 Chatbot":

    st.markdown('<div class="zameen-card">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="zameen-card-header">
            <div class="zameen-icon-badge">💬</div>
            <div class="titles">
                <h3>Farming Assistant</h3>
                <p>Ask anything about crops, soil, pests and more</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show previous chat
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    st.markdown("##### 🎤 Speak or Type Your Question")

    # Voice Input
    voice_input = speech_to_text(
        language="ur-PK",   # or "en-US"
        use_container_width=True,
        just_once=True,
        key="voice"
    )

    # Text Input
    typed_input = st.chat_input("Ask a farming question...")

    # Use whichever input is available
    user_input = typed_input if typed_input else voice_input

    if user_input:

        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        st.chat_message("user").write(user_input)

        with st.spinner("Thinking..."):
            response = client.responses.create(
                model="openai/gpt-oss-20b",
                input=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                max_output_tokens=1000
            )

        reply = response.output_text

        st.session_state.messages.append(
            {"role": "assistant", "content": reply}
        )

        st.chat_message("assistant").write(reply)
    st.markdown('</div>', unsafe_allow_html=True)

# =============================
# DISEASE DETECTION (BYPASS 403)
# =============================
elif menu == "🦠 Disease Detection":
    st.markdown('<div class="zameen-card">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="zameen-card-header">
            <div class="zameen-icon-badge">🦠</div>
            <div class="titles">
                <h3>Crop Disease Detection</h3>
                <p>Take or upload a photo of the leaf for instant analysis</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Form use karne se Axios error bypass ho jata hai
    with st.form("disease_form", clear_on_submit=True):
        # Option 1: Mobile Camera (Best for farmers)
        cam_image = st.camera_input("Take a photo of the leaf")
        
        # Option 2: File Upload (If camera not available)
        file_image = st.file_uploader("Select File", type=["jpg", "jpeg", "png"])
        
        submit_button = st.form_submit_button("Check Disease")

    # Image processing logic
    target_image = cam_image if cam_image is not None else file_image

    if target_image is not None and submit_button:
        try:
            # Step 1: Image ko open aur compress karein
            img = Image.open(target_image)
            
            # AI ke liye 1024px kafi hai, is se Axios crash nahi hota
            img.thumbnail((1024, 1024))
            
            # st.image(img, caption="Processing Image...", width=300)

            with st.spinner("Checking..."):
                # prompt
                prompt = """
                    You are an expert plant pathologist for Pakistan's crops. 
                    Analyze this image of a  plant. 
                    1. Name the disease.
                    2. Give a brief explanation of why it happened.
                    3. Suggest organic (desi) and chemical remedies.
                    4.Answer briefly in 200 words max.
                    If the plant is healthy, congratulate the farmer.
                    """
                
                # Gemini Client Call
                response = gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[prompt, img]
                )
                
                st.success("✅ Analysis Result:")
                st.markdown(response.text)

        except Exception as e:
            st.error(f"Error: {e}")
            st.warning("Agar Axios 403 aaye, toh photo ka size kam karein ya camera input use karein.")
    st.markdown('</div>', unsafe_allow_html=True)
