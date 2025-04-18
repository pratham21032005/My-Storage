from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Define the upload folder and make sure it exists
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file extensions (you can customize it if needed)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Password authentication route
@app.route('/')
def index():
    return render_template('login_page.html')  # Serve the login page

# Route for password verification
@app.route('/login', methods=['POST'])
def login():
    password = request.form.get('password')
    if password == 'Pratham':
        return redirect(url_for('upload_form'))  # Redirect to upload page after successful login
    else:
        return jsonify({"message": "Invalid Password"}), 401

# Upload file page
@app.route('/upload_form')
def upload_form():
    # Get the list of available files in the 'uploads' folder
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('upload_form.html', files=files)  # Pass the list of files to the template

# Upload file route
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['file']

    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"message": "File type not allowed"}), 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('upload_form'))  # Redirect to the upload form after successful upload

# Download file route
@app.route('/download/<filename>')
def download(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        return jsonify({"message": "File not found"}), 404

# Fetch all files route
@app.route('/files', methods=['GET'])
def files_list():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({"files": files})

if __name__ == '__main__':
    # Change the port to 8000 (or any other port you prefer)
    app.run(debug=True, port=8000)
