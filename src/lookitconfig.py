from ConfigParser import RawConfigParser, NoSectionError, NoOptionError
import gconf
import keyring
import os
import subprocess

from xdg import BaseDirectory

CONFIG_DIR = BaseDirectory.save_config_path('lookit')
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config')

try:
    PICTURE_DIR = subprocess.Popen(['xdg-user-dir', 'PICTURES'], \
                stdout=subprocess.PIPE).communicate()[0] \
                .strip('\n')
except OSError:
    PICTURE_DIR = os.path.expanduser('~')

HOTKEY_NAMES = {'capturearea': 'Lookit: Capture Area',
                'capturescreen': 'Lookit: Capture Screen',
                'capturewindow': 'Lookit: Capture Window'}
HOTKEY_IDENTS = {'capturearea': 'lookit_capture_area',
                'capturescreen': 'lookit_capture_screen',
                'capturewindow': 'lookit_capture_window'}
HOTKEY_ACTIONS = {'capturearea': 'lookit --capture-area',
                'capturescreen': 'lookit --capture-screen',
                'capturewindow': 'lookit --capture-window'}

KEYBINDING_DIR = '/desktop/gnome/keybindings/'

DEFAULTS = {'General': {'shortenurl': False,
                        'trash': False,
                        'savedir': PICTURE_DIR,
                        'autostart': False,
                        'delay': 0,
                        'force_fallback': False},
            'Hotkeys': {'capturearea': '<Control><Alt>4',
                        'capturescreen': '<Control><Alt>5',
                        'capturewindow': '<Control><Alt>6'},
            'Upload':  {'type': 'None',
                        'hostname': '',
                        'port': 0,
                        'username': '',
                        'ssh_key_file': '',
                        'directory': '',
                        'url': 'http://'}
}

class LookitConfig(RawConfigParser):
    def __init__(self, filename=CONFIG_FILE):
        RawConfigParser.__init__(self)
        self.filename = filename
        self.load()

    def get(self, section, option):
        if option == 'password':
            password = keyring.get_password('lookit', 'lookit')
            if password is None:
                return ''
            else:
                return password
        else:
            try:
                return RawConfigParser.get(self, section, option)
            except (NoSectionError, NoOptionError):
                return DEFAULTS[section][option]

    def set(self, section, option, value):
        if not section in self.sections():
            self.add_section(section)
        if section == 'Hotkeys':
            client = gconf.client_get_default()
            key = HOTKEY_IDENTS[option]
            client.set_string(KEYBINDING_DIR + key + '/name', HOTKEY_NAMES[option])
            client.set_string(KEYBINDING_DIR + key + '/action', HOTKEY_ACTIONS[option])
            client.set_string(KEYBINDING_DIR + key + '/binding', value)
        if option == 'autostart':
            try:
                if value:
                    os.symlink('/usr/share/applications/lookit.desktop', \
                        os.path.expanduser( \
                        '~/.config/autostart/lookit.desktop'))
                else:
                    os.unlink(os.path.expanduser( \
                        '~/.config/autostart/lookit.desktop'))
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
            if type(value) == bool:
                return value
            elif type(value) == str:
                return value == 'True'
            else:
                return bool(value)

    def load(self):
        self.read(self.filename)

    def save(self):
        f = open(self.filename, 'w')
        self.write(f)
        f.flush()
        f.close()

if __name__ == '__main__':
    lc = LookitConfig()

