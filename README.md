```markdown
# 🌾 ZameenAI Ultra: AI-Powered Smart Farming System

**ZameenAI Ultra** is a comprehensive precision agriculture ecosystem designed to empower farmers in Pakistan. By leveraging state-of-the-art Artificial Intelligence, it provides real-time solutions for disease detection, crop management, and market predictability.

---

## 🚀 Key Features

* **🦠 AI Disease Detection:** Powered by **Google Gemini 2.5 Flash Vision**. Farmers can upload or take a photo of a crop leaf to receive an instant diagnosis and treatment plan (Organic & Chemical).
* **🤖 Smart Advisory & Chatbot:** A multilingual agricultural assistant powered by **Groq** to answer queries regarding soil health, fertilizers, and pest control.
* **📅 Dynamic Crop Calendar:** A month-by-month guide for Rabi and Kharif crops, automatically synchronized with the current date.
* **🌦 Live Weather Integration:** Real-time weather updates to help farmers plan irrigation and harvest schedules.
* **📈 Market & Profit Predictor:** Tools to estimate crop yield and calculate potential revenue based on land area.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **Vision AI:** [Google Gemini 2.5 Flash](https://ai.google.dev/) (Generative AI SDK)
* **Language Model:** [openai/gpt-oss-120b](https://groq.com/) (via Groq Cloud)
* **Image Processing:** PIL (Pillow)
* **Language:** Python 3.10+

---

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/anhaalishba/ZameenAI.git](https://github.com/anhaalishba/ZameenAI.git)
   cd zameenai-ultra

```

2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Set up Environment Variables:**
Create a `.env` file or export your API keys:
```env
GEMINI_API_KEY=your_google_gemini_key
GROQ_API_KEY=your_groq_api_key

```


4. **Run the App:**
```bash
streamlit run streamlit_app.py

```



---

## 📂 Project Structure

```text
├── .streamlit/          # Streamlit configuration
├──  streamlit_app.py # Main application code
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation


```

---

## 🌟 Why ZameenAI?

Traditional farming in Pakistan suffers from an "Information Gap." **ZameenAI Ultra** bridges this gap by providing:

1. **Speed:** Gemini 2.5 Flash ensures sub-second response times for image analysis disease detection.
2. **Accuracy:** High-resolution vision models for early pest detection.
3. **Accessibility:** A simple, mobile-first interface designed for rural users.

---

## 🤝 Contributing

Contributions are welcome! If you have suggestions for new features or crop data, feel free to open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License.

```

---

### 💡 Quick Tips for your GitHub:
1.  **Add a Screenshot:** Inside the `assets/` folder, put a screenshot of your app's main page and name it `screenshot.png`. Then add `![App Screenshot](assets/screenshot.png)` at the top of the README.
2.  **Add Tags:** On the right side of your GitHub repo, add tags like `#agriculture`, `#python`, `#gemini-2.5`, and `#streamlit` to help people find your project.
3.  **Deployment Link:** Make sure to put your Streamlit Cloud link in the **"About"** section of the repository.

**Would you like me to generate a "License" file for you as well? (MIT License is standard for projects like this).**

```
