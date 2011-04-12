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
        self.set('General', 'autostart', True)

        self.add_section('Hotkeys')
        self.set('Hotkeys', 'caparea', '<Ctrl><Super>4')
        self.set('Hotkeys', 'capscreen', '<Ctrl><Super>3')

        self.add_section('Upload')
        self.set('Upload', 'type', 'None')
        self.set('Upload', 'hostname', '')
        self.set('Upload', 'port', 0)
        self.set('Upload', 'username', '')
        self.set('Upload', 'directory', '')
        self.set('Upload', 'url', 'http://')


    def get(self, section, option):
        if option == 'password':
            password = keyring.get_password('lookit', 'lookit')
            if password is None:
                return ''
            else:
                return password
        else:
            return RawConfigParser.get(self, section, option)

    def set(self, section, option, value):
        if option == 'autostart':
            try:
                if value:
                    os.symlink('/usr/share/applications/lookit.desktop',\
                        os.path.expanduser('~/.config/autostart/lookit.desktop'))
                else:
                    os.unlink(os.path.expanduser('~/.config/autostart/lookit.desktop'))
            except OSError:
                pass
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

    def getboolean(self, section, option):
        try:
            return RawConfigParser.getboolean(self, section, option)
        except AttributeError:
            # XXX:
            # For some reason, getboolean likes to die sometimes.
            # Until I figure it out, this will act as a band-aid
            # to prevent the error from causing Lookit to not work
            value = self.get(section, option)
            return value == "True"

if __name__ == '__main__':
        lc = LookitConfig()
        lc.load_defaults()

