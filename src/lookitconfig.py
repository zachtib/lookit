from ConfigParser import RawConfigParser
import gconf
import keyring
import os
import subprocess

import liblookit

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

class LookitConfig(RawConfigParser):
    def __init__(self):
        RawConfigParser.__init__(self)
        self.load_defaults()

    def load_defaults(self):
        self.ignore_updates = True
        self.add_section('General')
        self.set('General', 'shortenurl', False)
        self.set('General', 'trash', False)
        self.set('General', 'savedir', PICTURE_DIR)
        self.set('General', 'autostart', True)
        self.set('General', 'delay', 0)

        self.add_section('Hotkeys')
        self.set('Hotkeys', 'capturearea', '<Control><Alt>4')
        self.set('Hotkeys', 'capturescreen', '<Control><Alt>5')
        self.set('Hotkeys', 'capturewindow', '<Control><Alt>6')

        self.add_section('Upload')
        self.set('Upload', 'type', 'None')
        self.set('Upload', 'hostname', '')
        self.set('Upload', 'port', 0)
        self.set('Upload', 'username', '')
        self.set('Upload', 'directory', '')
        self.set('Upload', 'url', 'http://')
        self.ignore_updates = False

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
        if section == 'Hotkeys' and not self.ignore_updates:
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

def quickget(section, option):
    c = LookitConfig()
    c.read(liblookit.CONFIG_FILE)
    return c.get(section, option)

if __name__ == '__main__':
    lc = LookitConfig()
    lc.load_defaults()

