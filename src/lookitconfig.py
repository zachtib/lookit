from ConfigParser import RawConfigParser
import keyring
import os
import subprocess

try:
        PICTURE_DIR = subprocess.Popen(['xdg-user-dir', 'PICTURES'], \
				stdout=subprocess.PIPE).communicate()[0] \
				.strip('\n')
except OSError:
        PICTURE_DIR = os.path.expanduser('~')

class LookitConfig(RawConfigParser):
        def __init__(self):
                RawConfigParser.__init__(self)
                self.load_defaults()

        def load_defaults(self):
                self.add_section('General')
                self.set('General', 'shortenurl', False)
                self.set('General', 'trash', False)
                self.set('General', 'savedir', PICTURE_DIR)
                
                self.add_section('Hotkeys')
                self.set('Hotkeys', 'caparea', '<Ctrl><Super>4')
                self.set('Hotkeys', 'capscreen', '<Ctrl><Super>3')
                
                self.add_section('Upload')
                self.set('Upload', 'type', 'None')
                self.set('Upload', 'server', '')
                self.set('Upload', 'port', 0)
                self.set('Upload', 'username', '')
                self.set('Upload', 'directory', '')
                self.set('Upload', 'url', 'http://')


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

if __name__ == '__main__':
        lc = LookitConfig()
        lc.load_defaults()

