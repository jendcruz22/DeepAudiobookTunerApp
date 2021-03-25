import os
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, send_file, render_template
import shutil

UPLOAD_FOLDER = 'uploads/'
DOWNLOAD_FOLDER = 'downloads/'
EMOTIONS_FOLDER = './static/emotions/'
FINAL_AUDIO_FOLDER = './static/final_audio/'

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['EMOTIONS_FOLDER'] = EMOTIONS_FOLDER
app.config['FINAL_AUDIO_FOLDER'] = FINAL_AUDIO_FOLDER

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Upload API
@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():

    # Delete existing files from the upload, download, and audio folders before processing the next/new input audio
    for filename in os.listdir(UPLOAD_FOLDER) or filename in os.listdir(DOWNLOAD_FOLDER) or filename in os.listdir(EMOTIONS_FOLDER) or filename in os.listdir(FINAL_AUDIO_FOLDER):
        file_path1 = os.path.join(UPLOAD_FOLDER, filename)
        file_path2 = os.path.join(DOWNLOAD_FOLDER, filename)
        file_path3 = os.path.join(EMOTIONS_FOLDER, filename)
        file_path4 = os.path.join(FINAL_AUDIO_FOLDER, filename)
        try:
            if filename!=".gitkeep":
                if os.path.isfile(file_path1) or os.path.islink(file_path1) or os.path.isfile(file_path2) or os.path.islink(file_path2) or os.path.isfile(file_path3) or os.path.islink(file_path3) or os.path.isfile(file_path4) or os.path.islink(file_path4):
                    os.unlink(file_path1)
                    os.unlink(file_path2)
                    os.unlink(file_path3)
                    os.unlink(file_path4)

                elif os.path.isdir(file_path1) or os.path.isdir(file_path2) or os.path.isdir(file_path3) or os.path.isdir(file_path4):
                    shutil.rmtree(file_path1)
                    shutil.rmtree(file_path2)
                    shutil.rmtree(file_path3)
                    shutil.rmtree(file_path4)

        except Exception as e:
            print('Failed to delete. Reason: %s' % (e))
    
    if request.method == 'POST':

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

            # file.save only works once like a queue and is also called file buffer.
            # Since the audio has been parsed now, if we use the above line of code to save the above audio file, it will get saved empty. 
            # Therefore we use the audio saved once in the uploads folder and make copies of it as shown below
            shutil.copy(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['DOWNLOAD_FOLDER'], filename))
            shutil.copy(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['EMOTIONS_FOLDER'], filename))
            print("saved file successfully")

            # send file name as parameter to download
            return redirect('/player/'+ filename)
    return render_template('upload_file.html')

# Player API
@app.route("/player/<filename>", methods = ['GET'])
def player(filename):
    file_path = EMOTIONS_FOLDER + filename
    if request.method == 'POST':
        return send_file(file_path, as_attachment=True, attachment_filename='')
    return render_template('player.html', value=filename)

@app.route('/play_audio/<filename>')
def play_audio(filename):
    file_path = EMOTIONS_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')


# Final Audio API
# @app.route("/final_product/<filename>", methods = ['GET'])
# def final_product(filename):
#     return render_template('final_product.html', value=filename)

# Download API
@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    return render_template('download.html', value=filename)

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = DOWNLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')

if __name__ == "__main__":
    app.run(debug=True)