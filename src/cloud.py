"""
Cloud is a CloudApp API Wrapper, obviously written in Python.

The code is under GNU GPL V3.0.
The complete license text should have been shipped with this file. If this is
not the case you can find it under http://www.gnu.org/licenses/gpl-3.0.txt.

In order to have this fully functional you need:
    - poster
        This is needed as Python does not (yet) support
        multipart/form-data-requests out of the box.
    - Python 2.7 or ordereddict
        Necessary because Amazon's S3 expects the file to be the last
        value in the upload request.

The following values are available:
    - *cloud.__version_info__*
        a 3-tuple containing the version number.
        Format: '(major, minor, maintenance)'
    - *cloud.__version__*
        a string generated from __version_info__.
        Format: 'major.minor.maintenance'
    - *cloud.PROTOCOL*
        a string specifying the protocol to be used.
        Default: '\'http://\''
    - *cloud.URI*
        a string containing the URL used by non-authed requests.
        Default: '\'cl.ly\''
    - *cloud.AUTH_URI*
        a string containg the URL used by authed requests.
        Default: '\'my.cl.ly\''
    - *cloud.FILE_TYPES*
        a tuple filled with available filetypes.

The following classes are available:
    - CloudException
        An exception thrown on errors with Cloud.
    - DeleteRequest
        A HTTP DELETE request.
    - Cloud
        The pythonic CloudApp API Wrapper.

"""

import urllib2
import urllib
import json
import os

__version_info__ = (0, 7, 0)
__version__ = '.'.join([str(x) for x in __version_info__])


# Python does not support multipart/form-data encoding out of the box
try:
    import poster
    POSTER = True
except ImportError:
    POSTER = False

# We need ordereddicts as Amazon S3 expects 'file' to be the last param
# in the request's body when uploading.
ORDERED_DICT = True
try:
    from collections import OrderedDict
except ImportError:
    try:
        from ordereddict import OrderedDict
    except ImportError:
        ORDERED_DICT = False

PROTOCOL = 'http://'
    
URI = 'cl.ly'
AUTH_URI = 'my.cl.ly'
USER_AGENT = 'Cloud API Python Wrapper/%s' % __version__

FILE_TYPES = ('image', 'bookmark', 'test', 'archive', 'audio', 'video', 'unknown')


class CloudException(Exception):
    """An exception thrown on errors with cloud."""
    pass

class DeleteRequest(urllib2.Request):
    """
    A HTTP DELETE request.

    Public methods:
        - get_method
            Sets the HTTP method to DELETE.

    """
    def get_method(self):
        """Sets the HTTP method to DELETE."""
        return 'DELETE'

class Cloud(object):
    """
    The pythonic CloudApp API Wrapper.

    Public methods:
        - auth(username, password)
            Authenticates a user.
        - item_info(url)
            Get metadata about a cl.ly URL.
        - list_items(page=False, per_page=False, file_type=False, deleted=False)
            List the authenticated user's items.
        - create_bookmark(name, url)
            Creates a bookmark with the given name and url.
        - upload_file(path)
            Upload a file.
            
    """
    def __init__(self):
        """
        Init.

        *opener* is for functions that do not need authentication.
        
        """
        self.opener = urllib2.build_opener()
        self.opener.addheaders = [('User-Agent', USER_AGENT),
                                  ('Accept', 'application/json'),]
        self.auth_success = 0

    def auth(self, username, password):
        """
        Authenticate the given username with the given password.

        If poster is installed, build an upload handler.

        """
        if self.auth_success == 1:
            return True
        
        passwordmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passwordmgr.add_password(None, AUTH_URI, username, password)
        auth = urllib2.HTTPDigestAuthHandler(passwordmgr)

        self.auth_opener = urllib2.build_opener(auth)
        self.auth_opener.addheaders = [('User-Agent', USER_AGENT),
                                       ('Accept', 'application/json'),]

        if POSTER:
            self.upload_auth_opener = poster.streaminghttp.register_openers()
            self.upload_auth_opener.add_handler(auth)
            self.upload_auth_opener.addheaders = [('User-Agent', USER_AGENT),
                                                  ('Accept', 'application/json'),]

        if self.auth_success == 0:
            self._test_auth()

    def _test_auth(self):
        """Test authentication."""
        query = urllib.urlencode({'page': 1, 'per_page': 1})
        page = self.auth_opener.open('%s%s/items?%s' % (PROTOCOL, AUTH_URI, query))
        if page.code == 200:
            self.auth_success = 1
            return True
        return False

    def item_info(self, uri):
        """Get metadata about a cl.ly URL."""
        validator = '%s%s' % (PROTOCOL, URI)
        if validator in uri:
            return json.load(self.opener.open(uri))
        raise CloudException('URI not valid')

    def list_items(self, page=False, per_page=False, file_type=False, deleted=False):
        """
        List the authenticated user's items.

        Optional arguments:
            - *page*
                an integer representing the page number.
            - *per_page*
                an integer representing number of items per page.
            - *type*
                Filter items by types found in FILTER_TYPES
            - *deleted*
                a boolean. Show trashed items.
        
        """
        if self.auth_success == 0:
            raise CloudException('Not authed')
        
        params = {}
        if page:
            params['page'] = int(page)
        if per_page:
            params['per_page'] = int(per_page)
        if file_type:
            if isinstance(file_type, basestring) and \
               file_type.lower() in FILE_TYPES:
                params['type'] = file_type
        if deleted:
            params['deleted'] = bool(deleted)

        query = urllib.urlencode(params)
        return json.load(self.auth_opener.open('%s%s/items?%s' % (PROTOCOL, AUTH_URI, query)),
                         encoding='utf-8')

    def create_bookmark(self, name, bookmark_uri):
        """Creates a bookmark with the given name and url."""
        if self.auth_success == 0:
            raise CloudException('Not authed')

        values = {'item': {'name': name, 'redirect_url': bookmark_uri}}
        data = json.dumps(values, encoding='utf-8')
        request = urllib2.Request('%s%s/items' % (PROTOCOL, AUTH_URI), data)
        request.add_header('Content-Type', 'application/json')

        return json.load(self.auth_opener.open(request))

    def upload_file(self, path):
        """
        Upload a file.

        This function requires you to be authenticated.
        
        Furthermore you need to have poster installed as well as python 2.7 or
        ordereddict.
        
        """
        if not POSTER:
            raise CloudException('Poster is not installed')
        if not ORDERED_DICT:
            raise CloudException('Python 2.7 or ordereddict are not installed')
        
        if self.auth_success == 0:
            raise CloudException('Not authed')

        if not os.path.exists(path):
            raise CloudException('File does not exist')
        if not os.path.isfile(path):
            raise CloudException('The given path does not point to a file')

        directives = json.load(self.auth_opener.open('%s%s/items/new' % (PROTOCOL, AUTH_URI)))
        directives['params']['key'] = directives['params']['key'] \
                                      .replace('${filename}',
                                               os.path.split(path)[-1])
        upload_values = OrderedDict(sorted(directives['params'].items(), key=lambda t: t[0]))
        upload_values['file'] = open(path, 'rb').read()
        datagen, headers = poster.encode.multipart_encode(upload_values)
        request = urllib2.Request(directives['url'], datagen, headers)

        return json.load(self.upload_auth_opener.open(request))

    def delete_file(self, href):
        """Delete a file with the given href."""
        if self.auth_success == 0:
            raise CloudException('Not authed')
        result = self.auth_opener.open(DeleteRequest(href))
        if result.code == 200:
            return True
        raise CloudException('Deletion failed')
