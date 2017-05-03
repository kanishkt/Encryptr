from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from encrypt import encrypt, decode

UPLOAD_FOLDER = 'static'
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def main_page():
    return render_template("base.html")


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    if request.method == 'POST':
        file = request.files['file']
        message = request.form['msg']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        copy = encrypt(UPLOAD_FOLDER+"/"+filename, message)
        copy.save(os.path.join(app.config['UPLOAD_FOLDER'], filename[:-4] + "_copy.png"))
        return redirect(url_for("view", filename=filename))
    # Check if the file is one of the allowed types/extensions
    else:
        return "File bad"


@app.route('/view/<filename>')
def view(filename):
    print filename
    return render_template("view.html", orig=filename, encoded=filename[:-4] + '_copy.png')


@app.route('/upload/<filename>/', methods=['POST'])
def uploaded_image(filename):
    message = decode(UPLOAD_FOLDER+"/"+filename,)
    print message
    return render_template("decode.html", message=message)


if __name__ == "__main__":
    app.run(debug=True)
