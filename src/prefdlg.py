import gtk
import os
import sys

import common

import uploader

CONNECTION_TYPES = uploader.PROTO_LIST

class PrefDlg:
	def __init__(self):	
		self.prefs = dict()
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

		builder.connect_signals(self)

	def run(self, prefs=None):
		try:
			self.trash.set_active(prefs['trash'])
			self.shortenurl.set_active(prefs['shortenurl'])
			try:
				self.combobox.set_active(
					CONNECTION_TYPES.index(prefs['proto']))
			except:
				pass
			self.server.set_text(prefs['hostname'])
			self.port.get_adjustment().set_value(prefs['port'])
			self.username.set_text(prefs['username'])
			self.password.set_text(prefs['password'])
			self.directory.set_text(prefs['directory'])
			self.url.set_text(prefs['url'])
		except KeyError:
			self.combobox.set_active(CONNECTION_TYPES.index('None'))
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
			self.prefs['trash'] = self.trash.get_active()
			self.prefs['shortenurl'] = self.shortenurl.get_active()
			self.prefs['proto'] = self.combobox.get_active_text()
			self.prefs['hostname'] = self.server.get_text()
			self.prefs['port'] = int(self.port.get_text())
			self.prefs['username'] = self.username.get_text()
			self.prefs['password'] = self.password.get_text()
			self.prefs['directory'] = self.directory.get_text()
			self.prefs['url'] = self.url.get_text()
		else:
			self.prefs = dict()
		self.dialog.destroy()

	def on_pref_dialog_destroy(self, widget, data=None):
		if __name__=="__main__":
			gtk.main_quit() # Exit if this is being run directly
	
	def get_result(self):
		return self.prefs

if __name__=="__main__":
	p = PrefDlg() # For testing purposes only
	p.show()
	p.get_result()
