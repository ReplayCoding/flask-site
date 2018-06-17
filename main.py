import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, flash
from glob import glob
import urllib
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "wumpusthegrumpus"
def allowed_file(filename):
	return True

# Custom static data
@app.route('/upload', methods=['GET','POST'])
def upload():
	filename = request.args.get("file", default="upload")
	if os.path.isdir(filename):
		all_files=glob(os.path.join(filename,"*"))
		name=[os.path.split(i)[1] for i in all_files]
		return render_template("index.html", results=zip(all_files,name), folder=filename)
	f = os.path.split(filename)
	return send_from_directory(f[0], f[1])

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	folder = request.values.get("folder", default="upload")
	if request.method == 'POST':
		print(request.files)
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
			if not os.path.exists(os.path.join(folder, filename)):
				file.save(os.path.join(folder, filename))
				return redirect(url_for("upload", file=folder))
			else:
				return redirect(url_for('uploaded_file',
									filename=filename))
	return redirect("/upload")
@app.route("/uploaded_file")
def uploaded_file():
	filename = request.args.get("filename")
	link = os.path.join(UPLOAD_FOLDER, filename)
	return render_template("sure.html",link=link)
@app.route("/delete")
def delete():
	filetodel = request.args.get("file")
	os.remove(os.path.abspath(filetodel))
	print(filetodel)
	return redirect("/?folder=" + urllib.quote(request.args.get("folder")))


if not os.path.isdir("./upload/"):
	os.mkdir("./upload/")
app.run(use_reloader=True)
