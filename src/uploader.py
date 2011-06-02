import os
import sys
import gtk
import ftplib
import pynotify
import shutil
import tempfile
import time
import urllib
import urlparse

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
    
try:
	import pycurl
	import re
	PROTO_LIST.append('Omploader')
except ImportError:
	print 'Omploader support not available'

import common
import lookitconfig

IMGUR_ALLOWED = ['JPEG', 'GIF', 'PNG', 'APNG', 'TIFF', 'BMP', 'PDF', 'XCF']

class OmploaderUploader:
	def __init__(self):
		self.response = ''
		self.mapping = {}
		
	def curl_response(self, buf):
		self.response = self.response + buf

	def upload(self, image):
		c = pycurl.Curl()
		values = [	('file1', (c.FORM_FILE, image))]
		c.setopt(c.URL, 'http://ompldr.org/upload')
		c.setopt(c.HTTPPOST, values)
		c.setopt(c.WRITEFUNCTION, self.curl_response)

		c.perform()
		c.close()
        
		m = re.findall("v\w+", self.response)
		self.mapping['original_image'] = "http://ompldr.org/%s" % m[2]
        

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
	i = open(f, 'rb')

	try:
		ftp = ftplib.FTP()
		ftp.connect(hostname, port)
		ftp.login(username, password)
		ftp.cwd(directory)
		ftp.storbinary('STOR ' + os.path.basename(f), i)
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

	sftp.put(f, os.path.basename(f))

	return True, None

def upload_file_omploader(f):
	if not 'Omploader' in PROTO_LIST:
		print 'Error: Omploader not supported'
	i = OmploaderUploader()
	i.upload(f)
	if not 'error_msg' in i.mapping:
		return True, i.mapping
	else:
		return False, i.mapping.get('error_msg')

def upload_file_imgur(f):
	if not 'Imgur' in PROTO_LIST:
		print 'Error: Imgur not supported'
	i = ImgurUploader()
	i.upload(f)
	if not 'error_msg' in i.mapping:
		return True, i.mapping
	else:
		return False, i.mapping.get('error_msg')

def upload_pixbuf(pb):
    if pb is not None:
        ftmp = tempfile.NamedTemporaryFile(suffix='.png', prefix='', delete=False)
        pb.save_to_callback(ftmp.write, 'png')
        ftmp.flush()
        ftmp.close()
        upload_file(ftmp.name)

def upload_file(image, existing_file=False):
    config = lookitconfig.LookitConfig()
    try:
        config.read(common.CONFIG_FILE)
    except:
        print 'An error occurred reading the configuration file'

    proto = config.get('Upload', 'type')

    if proto == 'SSH':
        common.show_notification('Lookit', 'Uploading image to {0}...'.format(config.get('Upload', 'hostname')))
        success, data = upload_file_sftp(image,
                    config.get('Upload', 'hostname'),
                    int(config.get('Upload', 'port')),
                    config.get('Upload', 'username'),
                    config.get('Upload', 'password'),
                    config.get('Upload', 'directory'),
                    config.get('Upload', 'url'),
                    )
    elif proto == 'FTP':
        common.show_notification('Lookit', 'Uploading image to {0}...'.format(config.get('Upload', 'hostname')))
        success, data = upload_file_ftp(image,
                    config.get('Upload', 'hostname'),
                    int(config.get('Upload', 'port')),
                    config.get('Upload', 'username'),
                    config.get('Upload', 'password'),
                    config.get('Upload', 'directory'),
                    config.get('Upload', 'url'),
                    )
    elif proto == 'Omploader':
        common.show_notification('Lookit', 'Uploading image to Omploader')
        success, data = upload_file_omploader(image)
        try:
            f = open(common.LOG_FILE, 'ab')
            f.write(time.ctime() + ' Uploaded screenshot to Omploader: ' + data['original_image'] + '\n')
        except IOError, e:
            pass
        finally:
            f.close()
    elif proto == 'Imgur':
        common.show_notification('Lookit', 'Uploading image to Imgur...')
        success, data = upload_file_imgur(image)
        try:
            f = open(common.LOG_FILE, 'ab')
            f.write(time.ctime() + ' Uploaded screenshot to Imgur: ' + data['original_image'] + '\n')
            f.write('Delete url: ' + data['delete_page'] + '\n')
        except IOError, e:
            pass
        finally:
            f.close()
    elif proto == 'None':
        success = True
        data = False
    else:
        success = False
        data = "Error: no such protocol: {0}".format(proto)

    if not success:
        common.show_notification('Lookit', 'Error: ' + data)
        return

    if data:
        url = data['original_image']
    else:
        url = urlparse.urljoin(config.get('Upload', 'url'),
            os.path.basename(image))

    if config.getboolean('General', 'shortenurl') and proto != None:
        url = urllib.urlopen('http://is.gd/api.php?longurl={0}'
                        .format(url)).readline()
        print "URL Shortened:", url
    if not existing_file:
        if config.getboolean('General', 'trash'):
            os.remove(os.path.abspath(image))
        else:
            try:
                timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
                filename = timestamp + '.png'
                destination = os.path.join(config.get('General', 'savedir'), filename)
                i = 0
                while os.path.exists(destination):
                    filename = timestamp + '_' + str(i) + '.png'
                    destination = os.path.join(config.get('General', 'savedir'), filename)
                    i += 1
                shutil.move(image, destination)
                image = destination
            except IOError:
                print 'Error moving file'

    clipboard = gtk.clipboard_get()
    clipboard.set_text(url)
    clipboard.store()

    if proto == 'None':
        if config.getboolean('General', 'trash'):
            common.show_notification('Lookit', 'Error: No upload type selected')
        else:
            common.show_notification('Lookit', 'Image saved: ' + image)
    else:
        common.show_notification('Lookit', 'Upload complete: ' + url)

