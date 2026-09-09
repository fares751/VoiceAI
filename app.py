import os
from flask import Flask, request, send_file, render_template
from gtts import gTTS
from io import BytesIO
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def text_to_audio_file(text):
    tts = gTTS(text)
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    return audio_file

@app.route('/')
def index():
    return render_template('index.html')
def ask_question(sentence: str) -> str:
    response= client.models.generate_content(
        model="gemini-2.5-flash",
        contents=sentence,
        config = types.GenerateContentConfig(
            system_instruction="Antworte die folgende Frage",
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        )
    )

    return response.text


@app.route('/speak', methods=['POST'])
def speak():
    sentence = request.form.get('sentence')

    if not sentence:
        return {"error": "Please provide a sentence"}, 400

    answer = ask_question(sentence)
    audio_file = text_to_audio_file(answer)
    return send_file(audio_file, mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(debug=True)
