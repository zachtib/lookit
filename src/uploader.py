import os
import sys
import ftplib

PROTO_LIST = ['None']

try:
	import ftplib
	PROTO_LIST.append('FTP')
except ImportError:
	print 'FTP support not found'

try:
	import paramiko
	PROTO_LIST.append('SSH')
except ImportError:
	print 'SFTP support not found'

try:
	import ubuntuone
	import ubuntuone.storageprotocol
	# PROTO_LIST.append('Ubuntu One') # Not yet supported
except ImportError:
	print 'Ubuntu One support not found'

try:
	import pycurl
	import xml.parsers.expat
	PROTO_LIST.append('Imgur')
except ImportError:
	print 'Imgur support not available'

IMGUR_ALLOWED = ['JPEG', 'GIF', 'PNG', 'APNG', 'TIFF', 'BMP', 'PDF', 'XCF']

class ImgurUploader:
	def __init__(self):
		self.response = ''
		self.current_key = None
		self.mapping = {}
	
	def xml_ele_start(self, name, attrs):
		self.current_key = str(name)
	
	def xml_ele_end(self, name):
		self.current_key = None
	
	def xml_ele_data(self, data):
		if self.current_key is not None:
			self.mapping[self.current_key] = str(data)
	
	def curl_response(self, buf):
		self.response = self.response + buf

	def upload(self, image):
		c = pycurl.Curl()
		# Note: This key is specific for Lookit. If you want to use
		# the Imgur API in your application, please apply for an 
		# API key at: http://imgur.com/register/api/
		values = [	('key', 'e5acb0d99a09b654a2c7e833c7f2dbe1'),
				('image', (c.FORM_FILE, image))]
		
		c.setopt(c.URL, 'http://imgur.com/api/upload.xml')
		c.setopt(c.HTTPPOST, values)
		c.setopt(c.WRITEFUNCTION, self.curl_response)
	
		c.perform()
		c.close()
		
		p = xml.parsers.expat.ParserCreate()
	
		p.StartElementHandler = self.xml_ele_start
		p.EndElementHandler = self.xml_ele_end
		p.CharacterDataHandler = self.xml_ele_data
	
		p.Parse(self.response)
	
def get_proto_list():
	return PROTO_LIST

def upload_file_ftp(f, hostname, port, username, password, directory, url):
	i = open(f, 'r')

	try:
		ftp = ftplib.FTP()
		ftp.connect(hostname, port)
		ftp.login(username, password)
		ftp.cwd(directory)
		ftp.storbinary('STOR ' + f, i)
		ftp.quit()
	except Exception as error:
		return False, 'Error occured during FTP upload'
	
	i.close()

	return True, None

def upload_file_sftp(f, hostname, port, username, password, directory, url):
	t = paramiko.Transport((hostname, port))
	t.connect(username=username, password=password)
	sftp = paramiko.SFTPClient.from_transport(t)
	try:
		sftp.chdir(directory)
	except IOError:
		return False, 'Destination directory does not exist'
	
	sftp.put(f, f)

	return True, None

def upload_file_imgur(f):
	if not 'Imgur' in PROTO_LIST:
		print 'Error: Imgur not supported'
	i = ImgurUploader()
	i.upload(f)
	return True, i.mapping

def upload_file_ubuntuone(f):
	pass
