from app import db
from flask.ext.sqlalchemy import SQLAlchemy


class ImageTable(db.Model):
    __tablename__ = 'imagetable'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    imagelink = db.Column(db.String, nullable=False)

    #deleted  heading, priority,
    def __init__(self, name, imagelink):
        self.name = name
        self.imagelink = imagelink

    def __repr__(self):
        return '<Name is %s>' % self.name