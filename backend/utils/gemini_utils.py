import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use Gemini 2.0 Flash model
model = genai.GenerativeModel("gemini-2.0-flash")

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
        print("Error generating question:", e)
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
        print("Error evaluating answer:", e)
        return "Error: Could not evaluate answer."

# Get correct answer to a question
def get_answer(question):
    prompt = f"You are an expert interviewer. Provide a correct and concise answer to the following question:\n\nQ: {question}"
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Error getting answer:", e)
        return "Error: Could not get answer."
