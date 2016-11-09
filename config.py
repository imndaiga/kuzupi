import os

basedir = os.path.abspath(os.path.dirname(__file__))

class ConfigSetting:
	CONF_PATH = os.path.join(basedir, "kuzupiconf.ini")