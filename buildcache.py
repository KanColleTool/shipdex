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
	for filename in os.listdir(os.path.join(ROOT_PATH, d)):
		if filename.endswith('.json'):
			translate_json_file(os.path.join(u'api_get_master', filename))

def build_ship_cache():
	raw_ships = load_data(u'cache', u'api_get_master/ship.json')
	ships = {}
	for item in raw_ships:
		# There's a whole lot of placeholder ships just called just "なし".
		# I don't know why, and I don't think I want to, because the answer
		# would probably make me bang my head against my desk, and that'd
		# be an awful waste of a perfectly good desk.
		if item['api_name'] == u'なし':
			continue
		
		# Also skip Mist ships
		if item['api_yomi'][:4] == 'mist':
			continue
		
		# TODO: Versioning
		
		ships[item['api_id']] = item
	
	# Collect all 'base' ships, eg. un-remodeled models
	baseships = {k:v for k,v in ships.iteritems()}
	for ship in ships.itervalues():
		if ship['api_aftershipid'] != '0' and ship['api_aftershipid'] in baseships:
			del baseships[ship['api_aftershipid']]
	
	# Collect all ships of the same 'evolutionary line' together
	for ship in baseships.itervalues():
		line = []
		current_item = ship
		while True:
			line.append(current_item)
			if current_item['api_aftershipid'] != '0':
				current_item = ships[int(current_item['api_aftershipid'])]
			else:
				break
		save_data('cache', line, u'ships/{name}.json'.format(name=normalize_name(ship['api_name'])))
	
	save_data('cache', ships, 'ships.json', False)	# Make sure to minify this!



if __name__ == '__main__':
	build_translation_cache()
	build_ship_cache()
