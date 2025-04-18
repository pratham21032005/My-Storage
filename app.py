from flask import Flask, request, send_from_directory, redirect, render_template
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PASSWORD = os.getenv("APP_PASSWORD", "defaultpass")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')  # optional UI

@app.route('/login', methods=['POST'])
def login():
    password = request.form.get('password')
    if password == PASSWORD:
        return "Authenticated", 200
    return "Forbidden", 403

@app.route('/upload', methods=['POST'])
def upload():
    if request.form.get('password') != PASSWORD:
        return "Forbidden", 403
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return "Uploaded", 200

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    if request.args.get('password') != PASSWORD:
        return "Forbidden", 403
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/list', methods=['GET'])
def list_files():
    if request.args.get('password') != PASSWORD:
        return "Forbidden", 403
    files = os.listdir(UPLOAD_FOLDER)
    return {'files': files}
