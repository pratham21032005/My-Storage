from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'  # Needed for session management

# Upload config
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Helpers
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def index():
    return render_template('login_page.html')

@app.route('/login', methods=['POST'])
def login():
    password = request.form.get('password')
    if password == 'Pratham':
        session['role'] = 'admin'
        return redirect(url_for('upload_form'))
    elif password == '1234':
        session['role'] = 'user'
        return redirect(url_for('upload_form'))
    else:
        return jsonify({"message": "Invalid Password"}), 401

@app.route('/upload_form')
def upload_form():
    if 'role' not in session:
        return redirect(url_for('index'))  # Not logged in
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('upload_form.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    if 'role' not in session:
        return jsonify({"message": "Unauthorized"}), 401
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    if not allowed_file(file.filename):
        return jsonify({"message": "File type not allowed"}), 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('upload_form'))

@app.route('/files', methods=['GET'])
def files_list():
    if 'role' not in session:
        return jsonify({"message": "Unauthorized"}), 401
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({"files": files})

@app.route('/download/<filename>')
def download(filename):
    if 'role' not in session:
        return jsonify({"message": "Unauthorized"}), 401
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        return jsonify({"message": "File not found"}), 404

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    if 'role' not in session or session['role'] != 'admin':
        return jsonify({"message": "Unauthorized or insufficient privileges"}), 403

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return redirect(url_for('upload_form'))
    else:
        return jsonify({"message": "File not found"}), 404

@app.route('/logout')
def logout():
    session.pop('role', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
