import appindicator
import gtk

import liblookit

from liblookit import enum
cmd = enum('CAPTURE_AREA', 'CAPTURE_ACTIVE_WINDOW', 'CAPTURE_SCREEN',
                'SHOW_PREFERENCES', 'SHOW_ABOUT', 'EXIT')

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
        self.add_menu_separator()
        self.add_menu_item('Preferences', cmd.SHOW_PREFERENCES)
        self.add_menu_item('About', cmd.SHOW_ABOUT)
        self.add_menu_separator()
        self.add_menu_item('Exit', cmd.EXIT)

        self.indicator.set_menu(self.menu)

    def add_menu_item(self, label, command):
        item = gtk.MenuItem(label)
        item.connect('activate', self.handle_menu_item, command)
        item.show()
        self.menu.append(item)

    def add_menu_separator(self):
        item = gtk.SeparatorMenuItem()
        item.show()
        self.menu.append(item)

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
        else:
            print 'Error: reached end of handle_menu_item'

if __name__ == '__main__':
	i = LookitIndicator()
	gtk.main()
