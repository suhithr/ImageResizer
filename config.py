class BaseConfig(object):
	DEBUG = False
	MAX_CONTENT_LENGTH = 16 * 1024 * 1024 * 1024
	#Its pointing to the database imageresizer belonging to the user postgres
	SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
	# SQLALCHEMY_DATABASE_URI = 'sqlite://///home/suhith/Coding/ImageResizer/test.db'
	ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
	DIMENSIONS = 500

class DevelopmentConfig(BaseConfig):
	DEBUG=True
