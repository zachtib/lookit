from ConfigParser import RawConfigParser
import keyring

class LookitConfig(RawConfigParser):
	def get(self, section, option):
		if option == 'password':
			return keyring.get_password('lookit', 'lookit')
		else:
			return RawConfigParser.get(self, section, option)

	def set(self, section, option, value):
		if option == 'password':
			keyring.set_password('lookit', 'lookit', value)
		else:
			RawConfigParser.set(self, section, option, value)
