import os
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, send_file, render_template
import shutil
import sys
sys.path.append(os.path.abspath("../"))
import tensorflow as tf
from deepaudiobooktuner.deep_audiobook_tuner import *
from deepaudiobooktuner.utils.paths import path

from clean_folder import *

physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
   tf.config.experimental.set_memory_growth(physical_devices[0], True)

UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

dat = deepAudiobookTuner()

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Upload API
@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        # clean the existing files from the given folders
        clean_folder(UPLOAD_FOLDER)
        
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)

        else:
            filename = secure_filename(file.filename)
            # save the input audio in the uploads folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            print("saved file successfully")
            print(filename)

            # send file name as parameter to download
            return redirect('/player/'+ filename)
    return render_template('upload_file.html')

# Player API
@app.route("/player/<filename>", methods = ['GET', 'POST'])
def player(filename):
    
    audiobook_file_path = path(f'{UPLOAD_FOLDER}/{filename}')

    # Initialize the deepAudiobookTuner instance with the audiobook file path
    dat.initialize(audiobook_path = audiobook_file_path)

    # Analyze sentiments from the audiobook
    # dat.analyzeSentiments()

    # Generate muisc clips for the emotions
    dat.generateMusic()

    # Pruning the paths to the music clips
    emotions = ["Happy", "Sad", "Angry", "Neutral"]
    clips = []
    for emotion in emotions:
        full_path = f"{dat.paths['music_clips_save_path']}/{emotion}.mp3"
        elements = full_path.split("\\")
        clips.append("temp/" + "/".join(elements[len(elements) - 2 :])) 

    if request.method == 'POST':
        # Generate the final soundtrack and overlay it on the audiobook
        # dat.generateSoundtrack()

        # dat_audiobook_path = dat.final_audiobook
        # print(dat_audiobook_path)
    

        # file_path = UPLOAD_FOLDER + filename

        # return send_file(file_path, as_attachment=True, attachment_filename='')
        return redirect('/final_product/')

    return render_template('player.html', clips=clips)

# @app.route('/play_audio/<filename>')
# def regenerate_music(filename):
#     file_path = UPLOAD_FOLDER + filename
#     return send_file(file_path, as_attachment=True, attachment_filename='')


@app.route('/regenerate_music/', methods=['POST'])
def regenerate_music():
     emotion = None
     if request.method == "POST":
        emotion = [request.form.get("data")]
        print(emotion)
        dat.generateMusic(music_emotions=emotion)
        
        emotions = ["Happy", "Sad", "Angry", "Neutral"]
        clips = []
        for emotion in emotions:
            full_path = f"{dat.paths['music_clips_save_path']}/{emotion}.mp3"
            elements = full_path.split("\\")
            clips.append("temp/" + "/".join(elements[len(elements) - 2 :])) 

     return render_template('player.html', clips=clips)

# Final Audio API
@app.route("/final_product/", methods = ['GET', 'POST'])
def final_product():
    # Generate the final soundtrack and overlay it on the audiobook
    dat.generateSoundtrack()
    print(dat.paths["final_audiobook_save_path"])
    
    full_path = dat.paths["final_audiobook_save_path"]
    elements = full_path.split("\\")
    dat_audiobook_path = "temp/" + "/".join(elements[len(elements) - 2 :]) + f"/{dat.file_name}-dat.mp3"

    return render_template('final_product.html', dat_audiobook_path=dat_audiobook_path)

# Download API
@app.route("/downloadfile/<filename>", methods = ['GET', 'POST'])
def download_file(filename):
    return render_template('download.html', value=filename)

@app.route('/return-files/<filename>', methods = ['GET', 'POST'])
def return_files_tut(filename):
    file_path = DOWNLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')
    
if __name__ == "__main__":
    app.run(debug=True)