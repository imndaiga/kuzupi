from . import Settings
from configparser import ConfigParser

Config = ConfigParser()
Config.read(Settings().CONF_PATH)

def ConfigSection(section):
	dict1 = {}
	options = Config.options(section)
	for option in options:
		try:
			dict1[option] = Config.get(section, option)
			if dict1[option] == '<please_input>':
				DebugPrint("skip: {}".format(option))
		except:
			print("exception on {}".format(option))
			dict1[option] = None
	return dict1