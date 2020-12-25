#REQUIREMENTS
# ffmpeg
# vosk
##
"""
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


if __name__ == '__main__':
    run_ASR()
"""