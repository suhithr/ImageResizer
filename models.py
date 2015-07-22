from app import db

from flask.ext.sqlalchemy import SQLAlchemy


class ImageTable(db.Model):
    __tablename__ = 'imagetable'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    heading = db.Column(db.Integer, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    imagelink = db.Column(db.String, nullable=False)

    def __init__(self, name, heading, priority, imagelink):
        self.name = name
        self.heading = heading
        self.priority = priority
        self.imagelink = imagelink

    def __repr__(self):
        return '<Name is %s>' % self.name
