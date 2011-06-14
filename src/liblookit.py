import os
import pynotify
import time

import about
import lookitconfig
import preferences
import screencapper
import selector
import uploader

from xdg import BaseDirectory

XDG_CACHE_HOME = os.environ.get('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))

CONFIG_DIR = BaseDirectory.save_config_path('lookit')
LOG_FILE = os.path.join(CONFIG_DIR, 'log')

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

def migrate_from_1_0():
    old_config = os.path.expanduser('~/.config/lookit.conf')
    if os.path.isfile(old_config):
        config = lookitconfig.LookitConfig(old_config)
        config.filename = lookitconfig.CONFIG_FILE
        config.save()
        os.remove(old_config)

def upload_file(filename, existing_file=False):
    uploader.upload_file(filename, existing_file)

def handle_delay():
    delay_value = lookitconfig.LookitConfig().getint('General', 'delay')
    time.sleep(delay_value)

def do_capture_area():
    handle_delay()
    ffb = lookitconfig.LookitConfig().getboolean('General', 'force_fallback')
    selection = selector.Selector().get_selection(ffb)
    if selection is None:
        show_notification('Lookit', 'Selection cancelled')
        return
    pb = screencapper.capture_selection(selection)
    uploader.upload_pixbuf(pb)

def do_capture_window():
    handle_delay()
    pb = screencapper.capture_active_window()
    uploader.upload_pixbuf(pb)

def do_capture_screen():
    handle_delay()
    pb = screencapper.capture_screen()
    uploader.upload_pixbuf(pb)

def do_preferences():
    preferences.PrefDialog().run()

def do_about():
    about.AboutDialog().run()
