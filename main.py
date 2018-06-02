import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, flash
from glob import glob
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "wumpusthegrumpus"
def allowed_file(filename):
    return True

# Custom static data
@app.route('/upload/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return render_template("index.html", results=glob("./upload/*"))
            else:
	            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template("index.html", results=glob("./upload/*"))
@app.route("/uploaded_file")
def uploaded_file():
    filename = request.args.get("filename")
    link = os.path.join(UPLOAD_FOLDER, filename)
    return render_template("sure.html",link=link)
@app.route("/delete")
def delete():
    filetodel = request.args.get("file")
    os.remove(filetodel)
    print(filetodel)
    return redirect("/")


app.run()
