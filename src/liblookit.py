import os
import pynotify

import about
import preferences
import screencapper
import selector
import uploader

XDG_CACHE_HOME = os.environ.get('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))

CONFIG_FILE = os.path.expanduser('~/.config/lookit.conf')
LOG_FILE = os.path.join(XDG_CACHE_HOME, 'lookit.log')
VERSION = (1, 1, 0)
VERSION_STR = '.'.join(str(num) for num in VERSION)

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

def str_to_tuple(s):
    return tuple(int(x) for x in s.split('.'))

def get_data_dir():
    p = os.path.abspath(__file__)
    p = os.path.dirname(p)
    p = os.path.join(p, 'data')
    return p

def show_notification(title, message):
    pynotify.init('Lookit')
    n = pynotify.Notification(title, message, 'lookit')
    n.set_hint_string('append', '')
    n.show()

def do_capture_area():
    selection = selector.Selector().get_selection()
    if selection is None:
        show_notification('Lookit', 'Selection cancelled')
        return
    pb = screencapper.ScreenCapper().capture_selection(selection)
    uploader.upload_pixbuf(pb)

def do_capture_window():
    pb = screencapper.ScreenCapper().capture_active_window()
    uploader.upload_pixbuf(pb)

def do_capture_screen():
    pb = screencapper.ScreenCapper().capture_screen()
    uploader.upload_pixbuf(pb)

def do_preferences():
    preferences.PrefDialog().run()

def do_about():
    about.AboutDialog().run()
