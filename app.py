from flask import Flask, request, send_from_directory, render_template
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PASSWORD = os.getenv("APP_PASSWORD", "changeme")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')  # Optional UI

@app.route('/login', methods=['POST'])
def login():
    if request.form.get('password') == PASSWORD:
        return "Authenticated", 200
    return "Forbidden", 403

@app.route('/upload', methods=['POST'])
def upload():
    if request.form.get('password') != PASSWORD:
        return "Forbidden", 403
    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, secure_filename(file.filename)))
    return "Uploaded", 200

@app.route('/download/<filename>')
def download(filename):
    if request.args.get('password') != PASSWORD:
        return "Forbidden", 403
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/list')
def list_files():
    if request.args.get('password') != PASSWORD:
        return "Forbidden", 403
    return {'files': os.listdir(UPLOAD_FOLDER)}

# ✅ Only used for local testing
if __name__ == "__main__":
    app.run(debug=True)
