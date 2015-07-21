class BaseConfig(object):
	DEBUG = False
	MAX_CONTENT_LENGTH = 16 * 1024 * 1024 * 1024
	ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])


class DevelopmentConfig(BaseConfig):
	DEBUG=True
