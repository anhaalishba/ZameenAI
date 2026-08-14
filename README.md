# 🌾 ZameenAI

> **AI-Powered Smart Farming Decision System for Pakistan 🇵🇰**

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-GPT--OSS--20B-orange)
![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-4285F4?logo=google&logoColor=white)
![OpenWeather](https://img.shields.io/badge/OpenWeather-API-FFB300)
![Whisper](https://img.shields.io/badge/Whisper-Large%20V3-8A2BE2)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

---

## 🌱 About ZameenAI

**ZameenAI** is a multimodal AI-powered smart farming system designed especially for farmers in Pakistan.

It brings multiple agricultural tools into a single, simple and farmer-friendly platform.

From **crop disease detection** and **AI farming advice** to **live weather**, **voice interaction**, **profit estimation**, and a **Pakistan crop calendar**, ZameenAI helps farmers make smarter agricultural decisions.

> 🌾 **Our vision is simple:**
> Make modern agricultural knowledge more accessible to every farmer.

---

# ✨ Features

### 🌦️ Live Weather

Get real-time weather information for any city.

**Provides:**

- 🌡️ Temperature
- 💧 Humidity
- 💨 Wind Speed
- 🌥️ Weather Condition
- 📅 5-Day Forecast

Powered by **OpenWeather API**.

---

### 🦠 AI Crop Disease Detection

Farmers can either capture a crop leaf using the camera or upload an image.

The AI analyzes the image and provides:

- 🔍 Possible disease identification
- 📖 Explanation of the possible cause
- 🌿 Organic remedies
- 🧪 Chemical treatment suggestions
- ❤️ Healthy plant feedback

Powered by **Google Gemini 2.5 Flash**.

> ⚠️ Disease detection is AI-assisted and should be verified by a qualified agricultural expert for critical decisions.

---

### 💬 AI Farming Chatbot

Ask farming questions naturally and get AI-powered answers.

Example:

> *"When should I irrigate wheat?"*

The chatbot focuses specifically on:

- 🌾 Crops
- 🌱 Soil
- 💧 Irrigation
- 🧪 Fertilizers
- 🐛 Pests
- 🦠 Plant Diseases
- 🌦️ Agricultural Weather
- 🚜 Farm Management

Powered by **GPT-OSS-20B through Groq**.

---

### 🎙️ Voice Farming Assistant

Farmers don't always need to type.

ZameenAI supports voice-based questions:

```text
🎙️ Farmer speaks
       ↓
📝 Whisper Large V3
       ↓
💬 Text Question
       ↓
🤖 GPT-OSS-20B
       ↓
🌾 Farming Advice
````

Powered by **Whisper Large V3**.

---

### 🔊 Read Aloud

AI responses can also be spoken aloud using the browser's built-in **Speech Synthesis** capability.

This makes the application more accessible for users who prefer listening instead of reading.

---

### 🤖 Smart Farming Advisory

Get personalized farming advice based on:

* 🌾 Crop
* 🌱 Soil Type
* 🌤️ Season

Example:

```text
Crop: Wheat
Soil: Loamy
Season: Winter
```

The AI generates short, practical and farmer-friendly recommendations.

---

### 📈 Market & Profit Predictor

Estimate the financial outcome of a crop based on:

* 🌾 Crop
* 📐 Land Area
* 💰 Estimated Revenue
* 💸 Estimated Cost
* 🏆 Estimated Profit

The current prototype uses predefined crop prices and basic calculations.

> 🚀 Future versions can integrate real-time agricultural market prices.

---

### 📅 Pakistan Crop Calendar

Get month-wise agricultural activities for Pakistan.

Includes guidance related to crops such as:

* 🌾 Wheat
* 🍚 Rice
* 🌽 Maize
* 🎋 Sugarcane
* 🧵 Cotton
* 🥔 Potato
* 🌻 Sunflower
* 🌱 Pulses
* 🥬 Vegetables
* 🌿 Oilseeds

The calendar helps farmers understand what agricultural activities are important during each month.

---

# 🧠 AI Capabilities

ZameenAI combines multiple AI technologies:

| AI Technology                           | Purpose                          |
| --------------------------------------- | -------------------------------- |
| 🤖 **LLM**                              | Farming chatbot & smart advisory |
| 👁️ **Computer Vision / Multimodal AI** | Crop disease analysis            |
| 🎙️ **Speech Recognition**              | Voice-to-text farming questions  |
| 🔊 **Speech Synthesis**                 | Read AI responses aloud          |
| 🌦️ **External APIs**                   | Real-time weather information    |
| 📅 **Rule-Based Logic**                 | Crop calendar                    |
| 📊 **Calculations**                     | Revenue & profit estimation      |

---

# 🛠️ Tech Stack

| Technology               | Usage                      |
| ------------------------ | -------------------------- |
| 🐍 **Python**            | Main programming language  |
| 🎨 **Streamlit**         | Web application & UI       |
| 🤖 **GPT-OSS-20B**       | Farming chatbot & advisory |
| ⚡ **Groq API**           | Fast LLM inference         |
| 👁️ **Gemini 2.5 Flash** | Crop image analysis        |
| 🎙️ **Whisper Large V3** | Speech-to-text             |
| 🌦️ **OpenWeather API**  | Live weather & forecast    |
| 🖼️ **Pillow**           | Image processing           |
| 🌐 **Requests**          | API communication          |
| 🔊 **Web Speech API**    | Read Aloud                 |

---

# 🏗️ System Architecture

```text
                         👨‍🌾 FARMER
                             │
                             ▼
                    ┌─────────────────┐
                    │    ZameenAI     │
                    │    Streamlit    │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
      🌦 Weather          💬 Chatbot        🦠 Disease
          │                  │                  │
          ▼                  ▼                  ▼
    OpenWeather          Groq API           Gemini
                            │
                            ▼
                       GPT-OSS-20B

          ┌──────────────────┼──────────────────┐
          │                  │
          ▼                  ▼
      🎙️ Voice          📅 Calendar
          │                  │
          ▼                  ▼
       Whisper          Rule-Based
```

---

# 📂 Project Structure

```text
ZameenAI/
│
├── app.py
├── requirements.txt
├── README.md
│
├── .streamlit/
   └── secrets.toml
```

---

# 🚀 Getting Started

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/anhaalishba/ZameenAI.git
cd ZameenAI
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 API Configuration

Create:

```text
.streamlit/secrets.toml
```

Add your OpenWeather API key:

```toml
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"
```

Set the following environment variables:

```text
GROQ_API_KEY=YOUR_GROQ_API_KEY
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

> 🔒 Never commit API keys or secrets to GitHub.

---

# ▶️ Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 🌍 Supported Languages

ZameenAI is designed to support:

🇬🇧 **English**

🇵🇰 **Urdu**

🌾 **Sindhi**

The system is especially designed to make agricultural information easier to understand for Pakistani farmers.


---

# 💡 Why ZameenAI?

Traditional farming often requires farmers to search through different sources for different problems.

ZameenAI brings several tools together:

```text
🌦️ Weather
      +
🦠 Disease Detection
      +
🤖 AI Advisory
      +
💬 Farming Chatbot
      +
🎙️ Voice Assistant
      +
📈 Profit Estimation
      +
📅 Crop Calendar
      ↓
🌾 ZameenAI
```

One platform.
Multiple farming tools.
Designed for Pakistan.

---

# 🚀 Future Roadmap

### 🔮 Coming Next

* 📚 RAG-based agricultural knowledge base
* 🔗 LangChain AI workflows
* 🛰️ Satellite crop monitoring
* 🌱 Soil analysis
* 📡 IoT soil-moisture monitoring
* 🐛 AI pest prediction
* 📈 Real-time market prices
* 📍 Location-based farming recommendations
* 📱 Mobile application
* 🔊 Advanced voice interaction
* 🗄️ Farmer history & profiles
* 🌾 More crop disease classes
* 📊 Advanced yield prediction
* 🏛️ Government agriculture information

---

# ⚠️ Limitations

ZameenAI is currently a prototype and has some limitations:

* Disease detection may not always be accurate.
* Market prices are currently predefined.
* Crop calendar information is predefined.
* AI features require internet access.
* Weather depends on the external OpenWeather API.
* AI recommendations should be verified for critical agricultural decisions.

---

# 🌾 Project Vision

> **"Empowering farmers with intelligent technology and accessible agricultural knowledge."**

ZameenAI aims to bridge the gap between **modern AI technology and everyday farming**.

Our vision is to build a future where every farmer can access useful agricultural assistance simply through a phone, image, or voice.

---

# 👨‍💻 Team

### 🌾 ZameenAI Team

* **Anha Alishba**
* **Sayed Asad Murtiza**

---

# 🙏 Acknowledgements

Special thanks to:

* 🤖 Google Gemini
* ⚡ Groq
* 🌦️ OpenWeather
* 🎨 Streamlit
* 🎙️ Whisper
* 🐍 Python
* 🌾 Agricultural knowledge & farming communities

---

# 📜 License

This project is licensed under the **MIT License**.

---

<div align="center">

## 🌾 ZameenAI

### **Smart Technology. Smarter Farming. 🇵🇰**

⭐ **If you find this project useful, consider giving it a star!**

</div>
```
