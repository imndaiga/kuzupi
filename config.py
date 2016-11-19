import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	CONF_PATH = os.path.join(basedir, "kuzupiconf.ini")

	@staticmethod
	def init_app(app):
		pass

config = {
	'default' : Config()
}