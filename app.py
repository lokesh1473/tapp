from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from PyPDF2 import PdfReader
import speech_recognition as sr
import os

app = Flask(__name__)
translator = Translator()

# Translate text input
def translate_text(input_text, target_lang):
    translation = translator.translate(input_text, dest=target_lang)
    return translation.text

# Translate PDF input
def translate_pdf(pdf_file, target_lang):
    pdf_reader = PdfReader(pdf_file)
    pdf_text = ""
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:  # Check if text is extracted
            pdf_text += text + "\n"
    return translate_text(pdf_text, target_lang)

# Translate speech input
def translate_speech(audio_file, target_lang):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            input_text = recognizer.recognize_google(audio_data)
            return translate_text(input_text, target_lang)
        except Exception as e:
            return f"Could not process the audio. Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    input_type = request.form.get('inputType')
    target_lang = request.form.get('targetLang')

    if input_type == 'text':
        input_text = request.form.get('inputText')
        translation = translate_text(input_text, target_lang)
        return jsonify({'translation': translation})

    elif input_type == 'pdf':
        pdf_file = request.files['pdfFile']
        translation = translate_pdf(pdf_file, target_lang)
        return jsonify({'translation': translation})

    elif input_type == 'audio':
        audio_file = request.files['audioFile']
        translation = translate_speech(audio_file, target_lang)
        return jsonify({'translation': translation})

if __name__ == '__main__':
    app.run(debug=True)
