from flask import Flask, render_template, request, redirect, flash, url_for, session
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = set(['mp3', 'm4a', 'pdf', 'jpg'])

app = Flask(__name__)
app.secret_key = b'S\xe8(\xcc\x0f\xa47\x07\xe0\xac\xe9U\xab\xbe\xb9\x11'
app.config['UPLOAD_FOLDER'] = "./audio-files"


@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/output")
def output():
    file_path = session['filepath']
    text = run_ASR(file_path)
    return render_template("output.html", text=text)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'audio' in request.files:
            f = request.files['audio']
            if f.filename != '' and allowed_file(f.filename):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
                f.save(file_path)
                session["filepath"] = file_path
                return redirect(url_for('output'))
    return render_template("index.html")



import vosk
import os
import sys
import getopt
from traceback import print_exc
from subprocess import Popen, PIPE
import shlex
import json
from vosk import Model, KaldiRecognizer, SetLogLevel


def run_ASR(filename):

    model_path = "./model"
    audio_filename = filename


    if not os.path.exists(model_path):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        raise Exception("Model Cannot Found")

    
    SetLogLevel(-1)
    sample_rate=16000
    model = Model(model_path)
    rec = KaldiRecognizer(model, sample_rate)


    process = Popen(['ffmpeg', '-loglevel', 'quiet', '-i',
                                audio_filename,
                                '-ar', str(sample_rate) , '-ac', '1', '-f', 's16le', '-'],
                                stdout=PIPE)


    result = ""
    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            data = json.loads(rec.Result())
            result += data['text']

    #print(result) 
    data = json.loads(rec.FinalResult())
    result += data['text']
    return result



if __name__ == "__main__":
    app.run(debug=True)