import gtk
import os
import sys

import common

import uploader

CONNECTION_TYPES = uploader.PROTO_LIST

class PrefDlg:
	def __init__(self):
		self.prefs = None
		try:
			builder = gtk.Builder()
			datadir = common.get_data_dir()
			xmlfile = os.path.join(datadir, 'pref.xml')
			print xmlfile
			builder.add_from_file(xmlfile)
		except Exception as e:
			print e
			print "Error loading XML file"
			sys.exit(1)
		
		self.dialog = builder.get_object("pref_dialog")

		self.trash = builder.get_object("trash")
		self.shortenurl = builder.get_object("shortenurl")
		self.savedir = builder.get_object("savedir")
		
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

                self.caparea = builder.get_object("caparea")
                self.capscreen = builder.get_object("capscreen")

		builder.connect_signals(self)

	def run(self, config):
                self.config = config
                self.combobox.set_active(CONNECTION_TYPES.index('None'))
                self.trash.set_active( \
                        int(config.getboolean('General', 'trash')))
                self.shortenurl.set_active( \
                        int(config.getboolean('General', 'shortenurl')))
                self.savedir.set_filename( \
                        config.get('General', 'savedir'))
                self.caparea.set_text(config.get('Hotkeys', 'caparea'))
                self.capscreen.set_text(config.get('Hotkeys',
                                        'capscreen'))
                try:
                        self.combobox.set_active( \
                                CONNECTION_TYPES.index( \
                                config.get('Upload', 'type')))
                except:
                        pass
                self.server.set_text(config.get('Upload', 'hostname'))
                self.port.get_adjustment().set_value( \
                        config.getint('Upload', 'port'))
                self.username.set_text(config.get('Upload', 'username'))
                self.password.set_text(config.get('Upload', 'password'))
                self.directory.set_text( \
                        config.get('Upload', 'directory'))
                self.url.set_text(config.get('Upload', 'url'))
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
			self.prefs = dict()
                        self.config.set('General', 'trash',
                                self.trash.get_active())
                        self.config.set('General', 'shortenurl',
                                self.shortenurl.get_active())
                        self.config.set('General', 'savedir',
                                self.savedir.get_filename())
                        
                        self.config.set('Hotkeys', 'caparea',
                                self.caparea.get_text())
                        self.config.set('Hotkeys', 'capscreen',
                                self.capscreen.get_text())

			
                        self.config.set('Upload', 'type',
                                self.combobox.get_active_text())
			self.config.set('Upload', 'hostname',
                                self.server.get_text())
			self.config.set('Upload', 'port',
                                self.port.get_value_as_int())
			self.config.set('Upload', 'username',
                                self.username.get_text())
			self.config.set('Upload', 'password',
                                self.password.get_text())
			self.config.set('Upload', 'directory',
                                self.directory.get_text())
			self.config.set('Upload', 'url',
                                self.url.get_text())
		self.dialog.destroy()

	def on_pref_dialog_destroy(self, widget, data=None):
		if __name__=="__main__":
			gtk.main_quit() # Exit if this is being run directly
	
	def get_result(self):
		return self.config

if __name__=="__main__":
	p = PrefDlg() # For testing purposes only
	p.show()
	p.get_result()
