#!/usr/bin/python
from flask import Flask, send_from_directory,render_template, url_for, redirect, request
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from PIL import Image
import PIL

import os

UPLOAD_FOLDER = './Uploads'

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

db = SQLAlchemy(app)

#Importing models only after db is created since db is imported to models
from models import *

#So the user is prevented from uploading files with names like ../../../../myimage.jpg
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS


@app.route('/add', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		file = request.files['file']
		dimensions = app.config['DIMENSIONS']
		selectedBg = request.form['background']
		heading = request.form['heading']
		priority = request.form['priority']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			f = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(f)
			with Image.open(f) as img:
				origHeight = img.size[1]
				origWidth = img.size[0]
				#Resize main image
				newHeight = int((float(origHeight)*float(dimensions/float(origWidth))))
				img = img.resize((dimensions, newHeight), PIL.Image.ANTIALIAS)
				if selectedBg != "none":
					if selectedBg == "white":
						bg = Image.new(img.mode, (dimensions, dimensions),  (255, 255, 255, 255))
					else:
						bg = Image.new(img.mode, (dimensions, dimensions), (0,0,0,0))
					heightPosition = float(dimensions - newHeight) * 0.5
					bg.paste(img,(0,int(heightPosition)))
					newf = os.path.join(app.config['UPLOAD_FOLDER'], filename)
					bg.save(newf)
				else:
					newf = os.path.join(app.config['UPLOAD_FOLDER'], filename)
					img.save(newf)
				print newf
				qry = ImageTable(file.name, heading, priority, newf)
				db.session.add(qry)
				db.session.commit()
			return redirect(url_for('uploaded_file', filename=filename))
	return render_template('imageform.html')


@app.route('/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
	app.run()
