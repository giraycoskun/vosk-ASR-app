from flask import Flask, render_template, request, redirect, flash, url_for, session
from werkzeug.utils import secure_filename
from model import run_ASR
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





if __name__ == "__main__":
    app.run(debug=True)