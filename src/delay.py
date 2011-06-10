import gtk
import sys
import time
import os

import liblookit

class DelayDialog:
    def __init__(self):
        try:
            self.builder = gtk.Builder()
            datadir = liblookit.get_data_dir()
            xmlfile = os.path.join(datadir, 'delay.xml')
            self.builder.add_from_file(xmlfile)
        except Exception as e:
            print 'Error loading XML file', e.message
            sys.exit(1)

        self.dialog = self.builder.get_object('dialog')
        self.dialog.connect('response', self.on_response)

    def run(self):
        self.dialog.run()

    def on_response(self, widget, data=None):
        self.dialog.hide_all()
        if data != 0:
            return
        delay_value = self.builder.get_object('spinbutton').get_value()
        time.sleep(delay_value)
        if self.builder.get_object('radiobutton_area').get_active():
            liblookit.do_capture_area()
        elif self.builder.get_object('radiobutton_screen').get_active():
            liblookit.do_capture_screen()
        elif self.builder.get_object('radiobutton_window').get_active():
            liblookit.do_capture_window()

if __name__ == '__main__':
    DelayDialog().run()
