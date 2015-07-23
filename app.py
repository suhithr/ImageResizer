#!/usr/bin/python
from flask import Flask, jsonify, send_from_directory,render_template, url_for, redirect, request
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from PIL import Image
import PIL

import os

UPLOAD_FOLDER = './static/img'

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
def add():
	if request.method == 'POST':
		file = request.files['file']
		dimensions = app.config['DIMENSIONS']
		selectedBg = request.form['background']
		heading = request.form['heading']
		priority = request.form['priority']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			f = os.path.join(app.static_folder, 'img/' + filename)
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
					newf = os.path.join(app.static_folder, 'img/' + filename)
					bg.save(newf)
				else:
					newf = os.path.join(app.static_folder, 'img/' + filename)
					img.save(newf)
				qry = ImageTable(file.filename, heading, priority, newf)
				db.session.add(qry)
				db.session.commit()
			return redirect(url_for('uploaded_file', filename=filename))
	headings = HPTable.query.all()
	print headings
	return render_template('imageform.html', headings=headings)


@app.route('/new', methods=['GET', 'POST'])
def new():
	print "Here"
	if request.method == 'POST':
		receivedHeading = request.json["heading"]
		print receivedHeading
		receivedPriority = request.json["priority"]
		print receivedPriority
		db.session.add(HPTable(str(receivedHeading), int(receivedPriority)))
		db.session.commit()
		return jsonify(heading=receivedHeading, priority=receivedPriority)



@app.route('/')
def home():
	levels = []
	levels = ImageTable.query.order_by(ImageTable.heading.desc(),ImageTable.priority.desc()).all()
	for i in xrange(len(levels)):
		levels[i].imagelink = '/' +levels[i].name

	return render_template("view.html", levels=levels)


@app.route('/<filename>')
def uploaded_file(filename):
	return send_from_directory(os.path.join(app.static_folder, 'img/'), filename)

if __name__ == '__main__':
	app.run()
