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

        def rename_section(self, old_name, new_name):
                if not self.has_section(old_name) or self.has_section(new_name):
                        return False
                for (name, value) in self.items(old_name):
                        self.set(new_name, name, value)
                self.remove_section(old_name)
                return True
