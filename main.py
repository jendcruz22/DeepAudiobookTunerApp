import os
from werkzeug.utils import secure_filename
from flask import Flask,flash,request,redirect,send_file,render_template

UPLOAD_FOLDER = 'uploads/'
DOWNLOAD_FOLDER = 'download/'

#app = Flask(__name__)
app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

#Home page
@app.route('/')
def index():
    return render_template('index.html')

# Upload API
@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    # Delete existing files from the upload folder
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    
    # Delete existing files from the download folder
    for filename in os.listdir(DOWNLOAD_FOLDER):
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

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
            file.save(os.path.join(app.config['DOWNLOAD_FOLDER'], filename))
            print("saved file successfully")

      #send file name as parameter to downlad
            return redirect('/downloadfile/'+ filename)
    return render_template('upload_file.html')

# Player API
# @app.route("/player/<filename>", methods = ['GET'])
# def player(filename):
#     return render_template('player.html', value=filename)

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