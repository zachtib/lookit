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
		try:
			self.combobox.set_active(CONNECTION_TYPES.index('None'))
			self.trash.set_active( \
				int(config.getboolean('General', 'trash')))
			self.shortenurl.set_active( \
				int(config.getboolean('General', 'shortenurl')))
			self.savedir.set_filename( \
				config.get('General', 'savedir'))
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
		except:
			print 'There was an error loading preferences'
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
			self.prefs['trash'] = self.trash.get_active()
			self.prefs['shortenurl'] = self.shortenurl.get_active()
			self.prefs['proto'] = self.combobox.get_active_text()
			self.prefs['hostname'] = self.server.get_text()
			self.prefs['port'] = self.port.get_value_as_int()
			self.prefs['username'] = self.username.get_text()
			self.prefs['password'] = self.password.get_text()
			self.prefs['directory'] = self.directory.get_text()
			self.prefs['url'] = self.url.get_text()
			self.prefs['savedir'] = self.savedir.get_filename()
		self.dialog.destroy()

	def on_pref_dialog_destroy(self, widget, data=None):
		if __name__=="__main__":
			gtk.main_quit() # Exit if this is being run directly
	
	def get_result(self, config):
		if self.prefs is None:
			return config
		config.set('General', 'savedir', self.prefs['savedir'])
		config.set('General', 'trash', self.prefs['trash'])
		config.set('General', 'shortenurl', self.prefs['shortenurl'])
		config.set('Upload', 'type', self.prefs['proto'])
		config.set('Upload', 'hostname', self.prefs['hostname'])
		config.set('Upload', 'port', self.prefs['port'])
		config.set('Upload', 'username', self.prefs['username'])
		config.set('Upload', 'password', self.prefs['password'])
		config.set('Upload', 'directory', self.prefs['directory'])
		config.set('Upload', 'url', self.prefs['url'])
		return config

if __name__=="__main__":
	p = PrefDlg() # For testing purposes only
	p.show()
	p.get_result()
