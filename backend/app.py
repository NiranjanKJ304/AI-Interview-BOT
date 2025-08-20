import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from utils.asr_utils import transcribe_speech
from utils.tts_utils import speak_text_to_file
from utils.body_language_utils import BodyLanguageProcessor

# Load environment variables
load_dotenv()

# Configure API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in .env file")
genai.configure(api_key=api_key)

# Use Gemini 1.5 Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

# Generate interview question
def generate_question(domain, interview_type, difficulty):
    prompt = (
        f"Generate a {difficulty.lower()} level {interview_type.lower()} interview question "
        f"for the {domain.lower()} domain."
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating question: {e}")
        return "Error: Could not generate question."

# Evaluate the candidate's answer
def evaluate_answer(question, answer):
    prompt = (
        f"Question: {question}\n"
        f"Candidate's Answer: {answer}\n\n"
        f"Evaluate the candidate's answer. Provide:\n"
        f"1. A short constructive feedback (1-2 lines).\n"
        f"2. A score between 0 and 1, where 1 is perfect and 0 is incorrect.\n\n"
        f"Respond in the format:\n"
        f"Feedback: <your feedback>\n"
        f"Score: <score between 0 and 1>"
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error evaluating answer: {e}")
        return "Error: Could not evaluate answer."

# Get correct answer to a question
def get_answer(question):
    prompt = f"You are an expert interviewer. Provide a correct and concise answer to the following question:\n\nQ: {question}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error getting answer: {e}")
        return "Error: Could not get answer."

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for testing

@app.route("/analyze_pose", methods=["POST"])
def analyze_pose_route():
    if 'image' not in request.files:
        return jsonify({"result": "No image uploaded"}), 400
    image = request.files['image'].read()
    processor = BodyLanguageProcessor()
    result = processor.analyze_image_bytes(image)
    return jsonify({"result": result})

@app.route("/generate_question", methods=["POST"])
def generate():
    data = request.json
    domain = data.get("domain")
    interview_type = data.get("interview_type")
    difficulty = data.get("difficulty")
    if not all([domain, interview_type, difficulty]):
        return jsonify({"error": "Missing required fields"}), 400
    question = generate_question(domain, interview_type, difficulty)
    return jsonify({"question": question})

@app.route("/get_answer", methods=["POST"])
def model_answer():
    question = request.json.get("question")
    if not question:
        return jsonify({"error": "Question is required"}), 400
    answer = get_answer(question)
    return jsonify({"answer": answer})

@app.route("/transcribe", methods=["POST"])
def transcribe():
    try:
        result = transcribe_speech()
        return jsonify({"transcription": result})
    except Exception as e:
        print(f"Error transcribing speech: {e}")
        return jsonify({"error": "Transcription failed"}), 500

@app.route("/evaluate", methods=["POST"])
def evaluate():
    data = request.json
    question = data.get("question")
    answer = data.get("answer")
    if not all([question, answer]):
        return jsonify({"error": "Question and answer are required"}), 400
    feedback = evaluate_answer(question, answer)
    return jsonify({"feedback": feedback})

@app.route("/speak", methods=["POST"])
def speak():
    text = request.json.get("text", "")
    if not text:
        return jsonify({"error": "Text is required"}), 400
    try:
        audio_path = speak_text_to_file(text)
        return send_file(audio_path, mimetype="audio/mpeg", as_attachment=False)
    except Exception as e:
        print(f"Error generating audio: {e}")
        return jsonify({"error": "Audio generation failed"}), 500

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True, port=5000)