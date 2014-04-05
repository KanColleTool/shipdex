#!/usr/bin/env python
# coding: utf-8
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
	data = load_data(u'data', path)
	data = translate(data['api_data'])
	save_data('cache', data, path)



def build_translation_cache():
	d = os.path.join(u'data', u'api_get_master')
	print "Building TL cache of %s..." % d
	for filename in os.listdir(os.path.join(ROOT_PATH, d)):
		if filename.endswith('.json'):
			translate_json_file(os.path.join(u'api_get_master', filename))

def build_ship_cache():
	ships = load_data(u'cache', u'api_get_master/ship.json')
	name_to_id = {}
	for item in ships:
		# There's a whole lot of placeholder ships just called just "なし".
		# I don't know why, and I don't think I want to, because the answer
		# would probably make me bang my head against my desk, and that'd
		# be an awful waste of a perfectly good desk.
		if item['api_name'] == u'なし':
			continue
		
		data = {
			"data": item
			# TODO: Versioning
		}
		name_to_id[item['api_name']] = item['api_id']
		save_data('cache', data, 'ships/{id}.json'.format(id=item['api_id']))
	
	save_data('cache', name_to_id, 'name_to_id.json')



if __name__ == '__main__':
	#build_translation_cache()
	build_ship_cache()
