

# 🤖 AI Interview System

This project is an **AI-powered Interview Preparation System** that simulates real-time technical and HR interviews.  
It generates domain-specific questions, listens to answers via microphone, evaluates responses with AI, and provides instant feedback along with **body language monitoring** using the webcam.

---

## Project Structure
AI-Interview-BOT/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── .env.example
│   └── utils/
│       ├── gemini_utils.py
│       ├── tts_utils.py
│       ├── asr_utils.py
│       └── body_language_utils.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
└── README.md

## 🚀 Features
- AI-generated **interview questions** using Gemini API.
- **Speech-to-Text (ASR)** for capturing candidate responses.
- **AI-based evaluation** with feedback & scoring.
- **Text-to-Speech (TTS)** for reading questions aloud.
- **Body language detection** using MediaPipe (eye contact, posture).

---

## 🛠️ Tech Stack
- **Frontend**: HTML, CSS, JavaScript  
- **Backend**: Python (Flask)  
- **AI & ML**: Google Gemini API, MediaPipe, Whisper/Vosk  
- **Other Tools**: TTS API, CORS, dotenv  

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

git clone https://github.com/NiranjanKJ304/AI-Interview-BOT.git
cd AI-Interview-BOT

## Backend run
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt

Create a .env file inside backend/:
GEMINI_API_KEY="re-place your Gemeni-API"

Run backend:
python app.py

## Frontend run
Open frontend/index.html in your browser

