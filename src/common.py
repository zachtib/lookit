import os

VERSION = (0, 3, 1)
VERSION_STR = '.'.join(str(num) for num in VERSION)

def get_data_dir():
	p = os.path.abspath(__file__)
	p = os.path.dirname(p)
	p = os.path.join(p, 'data')
	return p
