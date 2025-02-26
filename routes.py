from flask import Flask, request, redirect, url_for, render_template
import cloudinary.uploader

app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        file_to_upload = request.files['file']
        if file_to_upload:
            upload_result = cloudinary.uploader.upload(file_to_upload)
            return render_template('upload.html', upload_result=upload_result)
    return render_template('upload.html')

