from app import db
from models import *

db.create_all()
db.session.add(HPTable('amateur', '1'))
db.session.add(HPTable('novice', '2'))
db.session.add(HPTable('advanced', '3'))
db.session.add(HPTable('expert', '4'))
db.session.commit()
