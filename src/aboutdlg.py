import gtk
import sys
import os

import common

class AboutDlg:
    def __init__(self):
        try:
            builder = gtk.Builder()
            datadir = common.get_data_dir()
            xmlfile = os.path.join(datadir, 'about.xml')
            builder.add_from_file(xmlfile)
        except:
            print "Error loading XML file"
            sys.exit(1)

        self.dialog = builder.get_object("about_dialog")

        self.dialog.connect("response", self.on_about_dialog_close)

        builder.connect_signals(self)

        self.dialog.set_version(common.VERSION_STR)

    def run(self):
        self.dialog.run()

    def on_about_dialog_response(self, widget, data=None):
        print "Response"
        self.dialog.destroy()

    def on_about_dialog_close(self, widget, data=None):
        self.dialog.destroy()

    def on_about_dialog_destroy(self, widget, data=None):
        if __name__=="__main__":
            gtk.main_quit()

if __name__=="__main__":
    AboutDlg().run() # For testing purposes only
    gtk.main()
