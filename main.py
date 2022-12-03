from flask import Flask, request, render_template
from google.cloud import texttospeech
import os


app = Flask(__name__)

@app.route("/")
def index_page():
    return render_template("main.html")

@app.route("/speak")
def speak():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.path.realpath(os.path.dirname(__file__)),'astrodev-googleapi-key.json')
    text_input = request.args.get("target")
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text_input)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open("static/output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
    return render_template("main.html", sound = "output.mp3")

if __name__ == '__main__':
    app.run(debug=True)