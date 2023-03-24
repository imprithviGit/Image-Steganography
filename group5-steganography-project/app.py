import os

from flask import Flask, render_template, request
from main import create_image, decode_image
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = os.path.join('static/images')
ALLOWED_EXTENSIONS = {'png','txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if os.path.exists(app.config['UPLOAD_FOLDER']) is False:
    os.mkdir(app.config['UPLOAD_FOLDER'])


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/encode', methods=['GET', 'POST'])
def encode():
    if request.method == 'POST':

        # LOADING AND SAVING IMAGE
        if 'image' not in request.files:
            return 'there is no image in form!'
        image = request.files['image']
        path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)

        # delete cached file
        if os.path.isfile(path):
            os.remove(path)

        image.save(path)

        if 'file' not in request.files:
            return 'there is no file in form!'
        file = request.files['file']
        if file.filename == '':
            return 'no file selected'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # STEGANOGRAPHY
            #with open(file_path, 'r') as f:
              #  secret_message = f.read()
            with open(file_path, 'r', encoding='utf-8') as f:
                 secret_message = f.read()


        base_image_path = path
        msg = create_image(secret_message, base_image_path)
        if msg is None:
            return render_template('result_encode.html', img_path=base_image_path, msg="ok")

        return render_template('result_encode.html', img_path=base_image_path, msg=msg)

    return render_template('encode.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'txt'


@app.route('/decode', methods=['GET', 'POST'])
def decode():

    if request.method == 'POST':

        # LOADING AND SAVING IMAGE
        if 'image' not in request.files:
            return 'there is no image in form!'
        image = request.files['image']
        path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(path)

        # STEGANOGRAPHY

        secret = decode_image(path)
        return render_template('result_decode.html', secret=secret)

    return render_template('decode.html')


if __name__ == '__main__':
    app.run()
