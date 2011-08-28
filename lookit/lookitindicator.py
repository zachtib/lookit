import appindicator
import gtk

from . import liblookit
from . import lookitconfig

from .liblookit import enum
cmd = enum('CAPTURE_AREA', 'CAPTURE_ACTIVE_WINDOW', 'CAPTURE_SCREEN',
                'SHOW_PREFERENCES', 'SHOW_ABOUT', 'EXIT',
                'DELAY_0', 'DELAY_3', 'DELAY_5', 'DELAY_10')

class LookitIndicator:

    def __init__(self):
        self.indicator = appindicator.Indicator(
            "Lookit",
            "lookit-panel",
            appindicator.CATEGORY_APPLICATION_STATUS)
        self.indicator.set_status(appindicator.STATUS_ACTIVE)

        self.menu = gtk.Menu()
        self.add_menu_item('Capture Area', cmd.CAPTURE_AREA)
        self.add_menu_item('Capture Entire Screen', cmd.CAPTURE_SCREEN)
        self.add_menu_item('Capture Active Window', cmd.CAPTURE_ACTIVE_WINDOW)

        delaymenu = gtk.Menu()
        self.add_menu_item('0 seconds', cmd.DELAY_0, delaymenu)
        self.add_menu_item('3 seconds', cmd.DELAY_3, delaymenu)
        self.add_menu_item('5 seconds', cmd.DELAY_5, delaymenu)
        self.add_menu_item('10 seconds', cmd.DELAY_10, delaymenu)
        sub = gtk.MenuItem('Set Delay:')
        sub.set_submenu(delaymenu)
        self.menu.append(sub)

        self.add_menu_separator()
        self.add_menu_item('Preferences', cmd.SHOW_PREFERENCES)
        self.add_menu_item('About', cmd.SHOW_ABOUT)
        self.add_menu_separator()
        self.add_menu_item('Exit', cmd.EXIT)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

    def add_menu_item(self, label, command, menu=None):
        item = gtk.MenuItem(label)
        item.connect('activate', self.handle_menu_item, command)
        if menu is None:
            menu = self.menu
        menu.append(item)

    def add_menu_separator(self):
        item = gtk.SeparatorMenuItem()
        item.show()
        self.menu.append(item)

    def set_delay(self, value):
        config = lookitconfig.LookitConfig()
        config.set('General', 'delay', value)
        config.save()

    def handle_menu_item(self, widget=None, command=None):
        if command == cmd.CAPTURE_AREA:
            liblookit.do_capture_area()
        elif command == cmd.CAPTURE_ACTIVE_WINDOW:
            liblookit.do_capture_window()
        elif command == cmd.CAPTURE_SCREEN:
            liblookit.do_capture_screen()
        elif command == cmd.SHOW_PREFERENCES:
            liblookit.do_preferences()
        elif command == cmd.SHOW_ABOUT:
            liblookit.do_about()
        elif command == cmd.EXIT:
            gtk.main_quit()
        elif command == cmd.DELAY_0:
            self.set_delay(0)
        elif command == cmd.DELAY_3:
            self.set_delay(3)
        elif command == cmd.DELAY_5:
            self.set_delay(5)
        elif command == cmd.DELAY_10:
            self.set_delay(10)
        else:
            print('Error: reached end of handle_menu_item')

if __name__ == '__main__':
	i = LookitIndicator()
	gtk.main()
