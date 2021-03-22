import os
from werkzeug.utils import secure_filename
from flask import Flask,flash,request,redirect,send_file,render_template
import shutil

UPLOAD_FOLDER = 'uploads/'
DOWNLOAD_FOLDER = 'downloads/'
AUDIO_FOLDER = './static/audio/'

#app = Flask(__name__)
app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER

#Home page
@app.route('/')
def index():
    return render_template('index.html')

# Upload API
@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    # Delete existing files from the upload folder
    for filename in os.listdir(UPLOAD_FOLDER) or filename in os.listdir(DOWNLOAD_FOLDER) or filename in os.listdir(AUDIO_FOLDER):
        file_path1 = os.path.join(UPLOAD_FOLDER, filename)
        file_path2 = os.path.join(DOWNLOAD_FOLDER, filename)
        file_path3 = os.path.join(AUDIO_FOLDER, filename)
        try:
            if filename!=".gitkeep":
                if os.path.isfile(file_path1) or os.path.islink(file_path1) or os.path.isfile(file_path2) or os.path.islink(file_path2) or os.path.isfile(file_path3) or os.path.islink(file_path3):
                    os.unlink(file_path1)
                    os.unlink(file_path2)
                    os.unlink(file_path3)
                elif os.path.isdir(file_path1) or os.path.isdir(file_path2) or os.path.isdir(file_path3):
                    shutil.rmtree(file_path1)
                    shutil.rmtree(file_path2)
                    shutil.rmtree(file_path3)

        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path1, e))
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            shutil.copy(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['DOWNLOAD_FOLDER'], filename))
            shutil.copy(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['AUDIO_FOLDER'], filename))
            print("saved file successfully")

      #send file name as parameter to downlad
            return redirect('/player/'+ filename)
    return render_template('upload_file.html')

# Player API
@app.route("/player/<filename>", methods = ['GET'])
def player(filename):
    if request.method == 'POST':
        return redirect('/downloadfile/'+ filename)
    return render_template('player.html', value=filename)

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