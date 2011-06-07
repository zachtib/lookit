import gtk
import os
import sys

import liblookit
import lookitconfig
import uploader

CONNECTION_TYPES = uploader.PROTO_LIST

class PrefDialog:
    def __init__(self):
        try:
            builder = gtk.Builder()
            datadir = liblookit.get_data_dir()
            xmlfile = os.path.join(datadir, 'pref.xml')
            builder.add_from_file(xmlfile)
        except Exception as e:
            print e
            sys.exit(1)

        self.config = lookitconfig.LookitConfig()
        try:
            self.config.read(liblookit.CONFIG_FILE)
        except:
            print 'An error occurred reading the configuration file'
        self.config.set('General', 'version', liblookit.VERSION_STR)
        self.config.write(open(liblookit.CONFIG_FILE, 'w'))

        self.dialog = builder.get_object("pref_dialog")

        self.trash = builder.get_object("trash")
        self.shortenurl = builder.get_object("shortenurl")
        self.savedir = builder.get_object("savedir")
        self.autostart = builder.get_object("autostart")

        self.combobox = builder.get_object("combobox")
        connections = gtk.ListStore(str)
        for connection in CONNECTION_TYPES:
            connections.append([connection])
        self.combobox.set_model(connections)
        cell = gtk.CellRendererText()
        self.combobox.pack_start(cell)
        self.combobox.add_attribute(cell, 'text', 0)
        self.combobox.set_active(0)

        self.server = builder.get_object("server")
        self.port = builder.get_object("port")
        self.username = builder.get_object("username")
        self.password = builder.get_object("password")
        self.directory = builder.get_object("directory")
        self.url = builder.get_object("url")

        self.capturearea = builder.get_object("capturearea")
        self.capturescreen = builder.get_object("capturescreen")
        self.capturewindow = builder.get_object("capturewindow")

        builder.connect_signals(self)

    def run(self):
        self.combobox.set_active(CONNECTION_TYPES.index('None'))
        self.trash.set_active(self.config.getboolean('General', 'trash'))
        self.shortenurl.set_active(self.config.getboolean('General', 'shortenurl'))
        self.savedir.set_filename(self.config.get('General', 'savedir'))
        self.autostart.set_active(self.config.getboolean('General', 'autostart'))
        self.capturearea.set_text(self.config.get('Hotkeys', 'capturearea'))
        self.capturescreen.set_text(self.config.get('Hotkeys', 'capturescreen'))
        self.capturewindow.set_text(self.config.get('Hotkeys', 'capturewindow'))
        try:
            self.combobox.set_active(CONNECTION_TYPES.index( \
                self.config.get('Upload', 'type')))
        except:
            pass
        self.server.set_text(self.config.get('Upload', 'hostname'))
        self.port.get_adjustment().set_value(self.config.getint('Upload', 'port'))
        self.username.set_text(self.config.get('Upload', 'username'))
        self.password.set_text(self.config.get('Upload', 'password'))
        self.directory.set_text(self.config.get('Upload', 'directory'))
        self.url.set_text(self.config.get('Upload', 'url'))

        self.dialog.run()

    def on_proto_changed(self, widget, data=None):
        proto = widget.get_active_text()
        if proto in ['FTP', 'SSH']:
            self.server.set_sensitive(True)
            self.port.set_sensitive(True)
            self.username.set_sensitive(True)
            self.password.set_sensitive(True)
            self.directory.set_sensitive(True)
            self.url.set_sensitive(True)
        elif proto in ['CloudApp']:
            self.username.set_sensitive(True)
            self.password.set_sensitive(True)
            self.server.set_sensitive(False)
            self.port.set_sensitive(False)
            self.directory.set_sensitive(False)
            self.url.set_sensitive(False)
        else:
            self.server.set_sensitive(False)
            self.port.set_sensitive(False)
            self.username.set_sensitive(False)
            self.password.set_sensitive(False)
            self.directory.set_sensitive(False)
            self.url.set_sensitive(False)

        if proto == 'FTP':
            self.port.get_adjustment().set_value(21)
        elif proto == 'SSH':
            self.port.get_adjustment().set_value(22)

    def on_pref_dialog_response(self, widget, data=None):
        if data == 1:
            self.config.set('General', 'trash', self.trash.get_active())
            self.config.set('General', 'shortenurl', self.shortenurl.get_active())
            self.config.set('General', 'savedir', self.savedir.get_filename())
            self.config.set('General', 'autostart', self.autostart.get_active())
            self.config.set('Hotkeys', 'capturearea', self.capturearea.get_text())
            self.config.set('Hotkeys', 'capturescreen', self.capturescreen.get_text())
            self.config.set('Hotkeys', 'capturewindow', self.capturewindow.get_text())
            self.config.set('Upload', 'type', self.combobox.get_active_text())
            self.config.set('Upload', 'hostname', self.server.get_text())
            self.config.set('Upload', 'port', self.port.get_value_as_int())
            self.config.set('Upload', 'username', self.username.get_text())
            self.config.set('Upload', 'password', self.password.get_text())
            self.config.set('Upload', 'directory', self.directory.get_text())
            self.config.set('Upload', 'url', self.url.get_text())
            self.config.write(open(liblookit.CONFIG_FILE, 'w'))
        self.dialog.destroy()

if __name__=="__main__":
    p = PrefDialog() # For testing purposes only
    p.run()
