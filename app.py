#!/usr/bin/python
from flask import Flask, send_from_directory,render_template, url_for, redirect, request
from werkzeug import secure_filename
from PIL import Image
import PIL

import os

UPLOAD_FOLDER = './Uploads'

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
	form  = UploadForm()
	if request.method == 'POST':
		file = request.files['file']
		selectedBg = request.form['background']
		print selectedBg
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			f = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(f)
			with Image.open(f) as img:
				print img
				origHeight = img.size[1]
				origWidth = img.size[0]
				newHeight = int((float(origHeight)*float(500/float(origWidth))))
				img = img.resize((500, newHeight), PIL.Image.ANTIALIAS)
				#Resized
				if selectedBg != "none":
					if selectedBg == "white":
						bg = Image.new(img.mode, (500,500),  (255, 255, 255, 255))
					else:
						bg = Image.new(img.mode, (500,500), (0,0,0,0))
					bg.paste(img,(0,0))
					newf = os.path.join(app.config['UPLOAD_FOLDER'], filename)
					bg.save(newf)
				else:
					newf = os.path.join(app.config['UPLOAD_FOLDER'], filename)
					img.save(newf)				
			return redirect(url_for('uploaded_file', filename=filename))
	return render_template('imageform.html')


@app.route('/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],
								filename)

if __name__ == '__main__':
	app.run()