import gtk
import sys
import time
import os

import liblookit
import lookitconfig

class DelayDialog:
    def __init__(self):
        self.config = lookitconfig.LookitConfig()
        try:
            self.config.read(liblookit.CONFIG_FILE)
        except:
            pass

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

        self.builder.get_object('hscale').set_value(self.config.getint('General', 'delay'))

    def run(self):
        self.dialog.run()

    def on_response(self, widget, data=None):
        self.dialog.hide_all()
        if data != 0:
            return
        delay_value = int(self.builder.get_object('hscale').get_value())
        print delay_value
        self.config.set('General', 'delay', delay_value)
        self.config.write(open(liblookit.CONFIG_FILE, 'w'))

if __name__ == '__main__':
    DelayDialog().run()
