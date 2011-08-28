import gtk
import sys
import os

from . import liblookit

class AboutDialog:
    def __init__(self):
        try:
            builder = gtk.Builder()
            datadir = liblookit.get_data_dir()
            xmlfile = os.path.join(datadir, 'about.xml')
            builder.add_from_file(xmlfile)
        except:
            print("Error loading XML file")
            sys.exit(1)

        self.dialog = builder.get_object("about_dialog")
        self.dialog.connect("response", self.on_about_dialog_close)
        builder.connect_signals(self)
        self.dialog.set_version(liblookit.VERSION_STR)

    def run(self):
        self.dialog.run()

    def on_about_dialog_response(self, widget, data=None):
        self.dialog.destroy()

    def on_about_dialog_close(self, widget, data=None):
        self.dialog.destroy()

if __name__=="__main__":
    AboutDialog().run() # For testing purposes only
