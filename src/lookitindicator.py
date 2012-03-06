try:
    import appindicator
    INDICATOR_SUPPORT = True
except ImportError:
    INDICATOR_SUPPORT = False

import gtk
import time
import webbrowser

import liblookit
import lookitconfig

from liblookit import enum
cmd = enum('CAPTURE_AREA', 'CAPTURE_ACTIVE_WINDOW', 'CAPTURE_SCREEN',
                'SHOW_PREFERENCES', 'SHOW_ABOUT', 'EXIT',
                'DELAY_0', 'DELAY_3', 'DELAY_5', 'DELAY_10', 'TOGGLE_UPLOAD')
MAX_IMAGE_COUNTS = 3

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

        delaymenu = gtk.Menu()
        self.add_menu_item('0 seconds', cmd.DELAY_0, delaymenu)
        self.add_menu_item('3 seconds', cmd.DELAY_3, delaymenu)
        self.add_menu_item('5 seconds', cmd.DELAY_5, delaymenu)
        self.add_menu_item('10 seconds', cmd.DELAY_10, delaymenu)
        sub = gtk.MenuItem('Set Delay:')
        sub.set_submenu(delaymenu)
        self.menu.append(sub)

        config = lookitconfig.LookitConfig()
        enableupload = config.getboolean('Upload', 'enableupload')
        self.add_check_menu_item('Upload to server', cmd.TOGGLE_UPLOAD, value=enableupload)

        self.add_menu_separator()
        self.add_menu_item('Preferences', cmd.SHOW_PREFERENCES)
        self.add_menu_item('About', cmd.SHOW_ABOUT)

        self.image_position = len(self.menu)
        self.image_list = []

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

    def add_check_menu_item(self, label, command, menu=None, value=True):
        item = gtk.CheckMenuItem(label)
        item.set_active(value)
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

    def set_upload(self, value):
        config = lookitconfig.LookitConfig()
        config.set('Upload', 'enableupload', value)
        config.save()

    def add_image(self, uri):
        """ Add image into menu and throw away an old image """
        if len(self.image_list) == 0:
            item = gtk.SeparatorMenuItem()
            item.show()
            self.menu.insert(item, self.image_position)
            self.image_position += 1

        if len(self.image_list) >= MAX_IMAGE_COUNTS:
            item = self.image_list.pop(0)
            self.menu.remove(item)

        label = time.strftime('%H:%M:%S')
        item = gtk.MenuItem(label)
        item.connect('activate', self.open_image, uri)
        item.show()
        position = self.image_position + len(self.image_list)
        self.menu.insert(item, position)
        self.image_list.append(item)

    def open_image(self, widget=None, uri=None):
        """ Open image and copy URI into clipboard """
        clipboard = gtk.clipboard_get()
        clipboard.set_text(uri)
        clipboard.store()

        webbrowser.open(uri)

    def handle_menu_item(self, widget=None, command=None):
        uri = None
        if command == cmd.CAPTURE_AREA:
            uri = liblookit.do_capture_area()
        elif command == cmd.CAPTURE_ACTIVE_WINDOW:
            uri = liblookit.do_capture_window()
        elif command == cmd.CAPTURE_SCREEN:
            uri = liblookit.do_capture_screen()
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
        elif command == cmd.TOGGLE_UPLOAD:
            self.set_upload(widget.get_active())
        else:
            print 'Error: reached end of handle_menu_item'

        if uri is not None:
            self.add_image(uri)

if __name__ == '__main__':
	i = LookitIndicator()
	gtk.main()
