# Turkish Simple ASR with VOSK API and model
by giraycoskun@sabanciuniv.edu

Designed as a command line tool to convert audio files or youtube files to text.
It is a simple approach and not suitable for professional usage.

**Deployment:** To **Heroku** with https://asr-vosk-app.herokuapp.com

---

## Requirements

- vosk: pip install vosk

- ffmpeg: brew install vosk(for MACOS)

- youtube-dl:(if you want to use youtube links) brew install youtube-dl(MACOS)

- A Vosk Model from: https://alphacephei.com/vosk/models

---

## Commadline Options

- -m -- model_path: directory path to the model(deafult: ./model)

- -f --audio_filename:file name path to the audio file; there is no default

- -l --youtube_link: yotube link to download audio which is converted to m4a

---

## Example Commands and Notes

- python3 main.py -f ./test.mp3

- python3 main.py -f ./test.mp3 -m ./dummy/model

- python3 main.py -l 'https://www.youtube.com/watch?v=VUKPVG2_5Lc'

- python3 main.py -l 'https://www.youtube.com/watch?v=VUKPVG2_5Lc' -m ./dummy/model

- -l -f options cannot be used together if such audio_filename will be discarded

- youtube-dl will downlaod audio file to same directory of python script with template name:%(title)s by %(uploader)s on %(upload_date)s.%(ext)s

- Turkish Recognition is provided by the model if you use any other model provided by vosk; recognition languauge will be changed 

---

## References:

- https://github.com/alphacep/vosk-api
- https://ffmpeg.org
- https://youtube-dl.org
- https://dev.to/techparida/how-to-deploy-a-flask-app-on-heroku-heb
- https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/
- https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world-legacy,
- https://getbootstrap.com/docs/5.0/getting-started/introduction/
- https://www.youtube.com/watch?v=4nzI4RKwb5I
