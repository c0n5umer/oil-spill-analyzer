import os
from detector import analysis
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/var/www/html/api/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
REDIRECT_URL = 'http://example.ru/api/oil/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/analyze', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        files = request.files.getlist('file')

        for file in files:
            if file.filename == '':
                return redirect(request.url)

            if file and allowed_file(file.filename):

                if request.form['paint'] == "yes":
                    draw = 1
                else:
                    draw = 0

                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                analysis(os.path.join(app.config['UPLOAD_FOLDER'], filename), 0.063, 0.003, draw, filename)

        return redirect(REDIRECT_URL)
    return '''
    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8">
        <link href="https://fonts.googleapis.com/css?family=Montserrat:400,500,800" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
        <style type="text/css">
        .main {
            text-align: center;
            font-family: 'Montserrat';
        }
        
        .btn {
            margin-top: 10px;
        }
        </style>
    </head>
    <body>
    <title>Детектор</title>
    <div class="main">
    <h1>Детектор нефтяных разливов</h1>
    <form method=post enctype=multipart/form-data>
        <input type=file class="form-control" name=file multiple><br>
        <input type="radio" class="form-check-input" name="paint" value="yes" checked> Помечать разливы </input><br>
        <input type="radio" class="form-check-input" name="paint" value="no"> Не помечать разливы </input><br>
        <input type=submit class="btn btn-success" value=Загрузить>
    </form>
    </div>
    </body>
    </html>
    '''
if __name__ == '__main__':
    app.secret_key = 'HPZgXfBaavUle3AovC1U'
    app.run(host="0.0.0.0", port=8000, debug=True)