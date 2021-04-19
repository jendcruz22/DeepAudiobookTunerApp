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

    dat.initialize(audiobook_path = audiobook_file_path)
    # dat.analyzeSentiments()
    dat.generateMusic()

    emotions = ["Happy", "Sad", "Angry", "Neutral"]
    clips = []
    for emotion in emotions:
        full_path = f"{dat.paths['music_clips_save_path']}/{emotion}.mp3"
        elements = full_path.split("\\")
        clips.append("temp/" + "/".join(elements[len(elements) - 2 :])) 

    file_path = UPLOAD_FOLDER + filename
    if request.method == 'POST':
        return send_file(file_path, as_attachment=True, attachment_filename='')
        return redirect('/final_product/'+ filename)

    return render_template('player.html', clips=clips)

@app.route('/play_audio/<filename>')
def play_audio(filename):
    file_path = UPLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')

# Final Audio API
@app.route("/final_product/<filename>", methods = ['GET', 'POST'])
def final_product(filename):
    return render_template('final_product.html', value=filename)

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