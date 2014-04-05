import sys, os
import json
import zlib
import ctypes
from util import *

tldata = None

def load_translation_data():
	global tldata
	with open(os.path.join(ROOT_PATH, u'data', u'translation.json')) as f:
		tldata = json.loads(f.read())

def translate(thing):
	global tldata
	if tldata is None:
		load_translation_data()
	
	if isinstance(thing, dict):
		for key, value in thing.iteritems():
			thing[key] = translate(value)
	elif isinstance(thing, list):
		return [translate(item) for item in thing]
	elif isinstance(thing, str) or isinstance(thing, unicode):
		crc = str(zlib.crc32(thing.encode('utf-8')) & 0xFFFFFFFF)
		if crc in tldata:
			return tldata[crc] or thing
	return thing

def translate_json_file(path):
	print "-> Translating %s..." % path
	data = {}
	with open(path) as f:
		data = json.loads(f.read())
	
	data = translate(data['api_data'])
	save_data('cache', data, path)



def build_translation_cache():
	d = os.path.join(u'data', u'api_get_master')
	print "Building TL cache of %s..." % d
	for filename in os.listdir(os.path.join(ROOT_PATH, d)):
		if filename.endswith('.json'):
			translate_json_file(os.path.join(d, filename))

if __name__ == '__main__':
	build_translation_cache()
