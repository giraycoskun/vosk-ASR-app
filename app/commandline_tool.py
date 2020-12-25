#REQUIREMENTS
# ffmpeg
# vosk
# youtube-dl
##

import vosk
import os
import sys
import getopt
from traceback import print_exc
from subprocess import Popen, PIPE
import shlex
import json
from vosk import Model, KaldiRecognizer, SetLogLevel


def main(*argv):

    try:
        #argv = argv[0]
        argv = sys.argv[1:] 
        model_path = "./model"
        audio_filename = ""
        youtube_link = ""
        
        try:
            
            opts, _ = getopt.getopt(argv, "l:f:m:",  
                                        ["link =","file_name =", 
                                        "model_path ="]) 

            #print(opts)
            #print(args)
            
        except Exception as err: 
            print(repr(err))
            raise Exception("Option Error")

        for opt, arg in opts: 
            if opt in ['-f', '--audio_filename']: 
                audio_filename = arg 
            elif opt in ['-m', '--model_path']: 
                model_path = arg
            elif opt in ['-l', '--youtube_Link']:
                youtube_link = arg
        


        if not os.path.exists(model_path):
            print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
            raise Exception("Model Cannot Found")
        


        if(youtube_link != ""):
            audio_filename = get_youtube_audio(youtube_link)


        #TODO
        assert(youtube_link != "" or audio_filename != "") ("Input Error")
        print( "LINK:",youtube_link,"FILE: ", audio_filename, " MODEL: ",model_path)

        
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
        print("\n")
        print(result)
    
    except Exception as error:
        print("ERROR: {}".format(error))
        print_exc()


def get_youtube_audio(link):
    extension = ".m4a"
    filename = ""
    try:

        command = "youtube-dl --get-filename  -o '%(title)s by %(uploader)s on %(upload_date)s.%(ext)s' " + link
        args = shlex.split(command)
        with Popen(args, stdout=PIPE, stderr=PIPE) as process:
            process.wait()
            for line in process.stdout.readlines():
                temp = line.decode().strip()
                filename = temp[:temp.index('.')]
                filename = filename + extension
                print(filename)

        command = "youtube-dl -x --audio-format m4a " + link + " -o '%(title)s by %(uploader)s on %(upload_date)s.%(ext)s'"
        args = shlex.split(command)
        with Popen(args, stdout=PIPE, stderr=PIPE) as process:
            
            process.wait()
            error_check = True
            for line in process.stdout.readlines():
                print(line.decode().strip())
                
            for line in process.stdout.readlines():
                error_check = False
                print(line)

            assert(error_check)
            assert(process.returncode == 0)
            return filename
        
    except:
        raise Exception("youtube-dl error")

    return filename


if __name__ == '__main__':
    #args = ['-l', 'https://www.youtube.com/watch?v=gt027PfguDQ']
    main()