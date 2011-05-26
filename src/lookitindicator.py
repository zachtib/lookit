import appindicator
import gtk

from common import enum
cmd = enum('CAPTURE_AREA', 'CAPTURE_SCREEN', 'SHOW_PREFERENCES',
                'SHOW_ABOUT', 'EXIT')

class LookitIndicator:

    def __init__(self):
        self.indicator = appindicator.Indicator(
            "lookit-indicator",
            "lookit",
            appindicator.CATEGORY_APPLICATION_STATUS)
        self.indicator.set_status(appindicator.STATUS_ACTIVE)

        try:
            # Check for special Ubuntu themes.
            # This is an ugly, ugly hack
            theme = gtk.gdk.screen_get_default().get_setting(
                            'gtk-icon-theme-name')
            if theme == 'ubuntu-mono-dark':
                self.indicator.set_icon('lookit-dark')
            elif theme == 'ubuntu-mono-light':
                self.indicator.set_icon('lookit-light')
            # Oh god, it hurt to even type that, I need to find
            # a better solution, but it won't see the icons if I
            # install them manually whhhaaarrgggbbbbllll
        except ValueError:
            # Couldn't find the setting, probably not running gnome
            print "Warning: Couldn't detect gtk theme"

        self.menu = gtk.Menu()
        self.add_menu_item('Capture Area', cmd.CAPTURE_AREA)
        self.add_menu_item('Capture Entire Screen', cmd.CAPTURE_SCREEN)
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
            pass
        elif command == cmd.CAPTURE_SCREEN:
            pass
        elif command == cmd.SHOW_PREFERENCES:
            pass
        elif command == cmd.SHOW_ABOUT:
            pass
        elif command == cmd.EXIT:
            gtk.main_quit()
        else:
            print 'Error: reached end of handle_menu_item'

if __name__ == '__main__':
	i = LookitIndicator()
	gtk.main()
