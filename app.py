import os
from io import BytesIO

from flask import Flask, request, send_file, render_template
from gtts import gTTS
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
app = Flask(__name__)

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

def text_to_audio_file(text):
    tts = gTTS(text=text, lang="en")
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    return audio_file


@app.route("/")
def index():
    return render_template("index.html")

def ask_question(sentence: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=sentence
    )

    return response.output_text

@app.route("/speak", methods=["POST"])
def speak():
    sentence = (request.form.get("sentence") or "").strip()

    if not sentence:
        return {"error": "Please provide a sentence"}, 400


    answer = ask_question(sentence)

    audio_file = text_to_audio_file(answer)
    return send_file(audio_file, mimetype="audio/mpeg")


if __name__ == "__main__":
    app.run(debug=True)
