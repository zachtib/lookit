import os
import pynotify

XDG_CACHE_HOME = os.environ.get('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))

CONFIG_FILE = os.path.expanduser('~/.config/lookit.conf')
LOG_FILE = os.path.join(XDG_CACHE_HOME, 'lookit.log')
VERSION = (0, 5, 0)
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
