import gtk
import os
import sys

import liblookit
import lookitconfig

from uploader import PROTO_LIST as CONNECTION_TYPES

WIDGETS = ( (bool, 'trash', 'General', 'trash'),
            (bool, 'shortenurl', 'General', 'shortenurl'),
            (bool, 'autostart', 'General', 'autostart'),
            (bool, 'force_fallback', 'General', 'force_fallback'),
            (int, 'delayscale', 'General', 'delay'),
            (file, 'savedir', 'General', 'savedir'),
            (str, 'capturearea', 'Hotkeys', 'capturearea'),
            (str, 'capturescreen', 'Hotkeys', 'capturescreen'),
            (str, 'capturewindow', 'Hotkeys', 'capturewindow'),
            (str, 'server', 'Upload', 'hostname'),
            (str, 'username', 'Upload', 'username'),
            (str, 'password', 'Upload', 'password'),
            (int, 'port', 'Upload', 'port'),
            (str, 'directory', 'Upload', 'directory'),
            (str, 'url', 'Upload', 'url'),
            (None, 'combobox', 'Upload', 'type'),
)

class PreferencesDialog:
    def __init__(self):
        try:
            self.builder = gtk.Builder()
            datadir = liblookit.get_data_dir()
            xmlfile = os.path.join(datadir, 'preferences.xml')
            self.builder.add_from_file(xmlfile)
        except Exception as e:
            print e
            sys.exit(1)

        connections = gtk.ListStore(str)
        for connection in CONNECTION_TYPES:
            connections.append([connection])
        cell = gtk.CellRendererText()
        combobox = self.builder.get_object('combobox')
        combobox.set_model(connections)
        combobox.pack_start(cell)
        combobox.add_attribute(cell, 'text', 0)
        combobox.set_active(0)

        self.config = lookitconfig.LookitConfig()
        self.builder.connect_signals(self)

    def run(self):
        for (kind, name, section, option) in WIDGETS:
            widget = self.builder.get_object(name)
            if kind == bool:
                value = self.config.getboolean(section, option)
                widget.set_active(value)
            elif kind == int:
                value = self.config.getint(section, option)
                widget.set_value(value)
            elif kind == str:
                value = self.config.get(section, option)
                widget.set_text(value)
            elif kind == file:
                value = self.config.get(section, option)
                widget.set_filename(value)
            elif kind == None:
                value = self.config.get(section, option)
                widget.set_active(CONNECTION_TYPES.index(value))

        self.builder.get_object('dialog').run()

    def on_proto_changed(self, widget, data=None):
        proto = widget.get_active_text()

        user_pass = ('username', 'password')
        server_port_dir_url = ('server', 'port', 'directory', 'url')
        all_fields = user_pass + server_port_dir_url

        if proto in ['FTP', 'SSH']:
            for field in all_fields:
                self.builder.get_object(field).set_sensitive(True)
        elif proto in ['CloudApp']:
            for field in user_pass:
                self.builder.get_object(field).set_sensitive(True)
            for field in server_port_dir_url:
                self.builder.get_object(field).set_sensitive(False)
        else:
            for field in all_fields:
                self.builder.get_object(field).set_sensitive(False)

        if proto == 'FTP':
            self.builder.get_object('port').set_value(21)
        elif proto == 'SSH':
            self.builder.get_object('port').set_value(22)

    def on_dialog_response(self, widget, data=None):
        if data != 1:
            widget.destroy()
            return
        for (kind, name, section, option) in WIDGETS:
            field = self.builder.get_object(name)
            if kind == bool:
                value = field.get_active()
            elif kind == int:
                value = int(field.get_value())
            elif kind == str:
                value = field.get_text()
            elif kind == file:
                value = field.get_filename()
            elif kind == None:
                value = field.get_active_text()
            self.config.set(section, option, value)
        self.config.save()
        widget.destroy()

if __name__ == '__main__':
    dialog = PreferencesDialog()
    dialog.run()
