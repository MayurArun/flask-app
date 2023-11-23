from flask import Flask, render_template, request, send_file
from PIL import Image
import pytesseract as tess
from gtts import gTTS
# import os

app = Flask(__name__)

# Set the path to the Tesseract executable
tess.pytesseract.tesseract_cmd = r'C:\Users\LENOVO\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
@app.route('/', methods=['GET', 'POST'])
def index():
    text = ''
    audio_link = None

    if request.method == 'POST':
        if 'file' in request.files:
            image = request.files['file']
            if image:
                img = Image.open(image)
                text = tess.image_to_string(img, lang='kan')

                # Convert recognized text to speech
                if text:
                    tts = gTTS(text, lang='kn')  # 'kn' is the language code for Kannada
                    audio_file = 'output.mp3'
                    tts.save(audio_file)
                    audio_link = audio_file

    return render_template('index.html', text=text, audio_link=audio_link)

@app.route('/download_audio')
def download_audio():
    return send_file('output.mp3', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)