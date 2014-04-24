#!/usr/bin/env python
# coding: utf-8
import sys, os
import json
import zlib
import ctypes
import re
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
	data = load_data(u'data', path)
	data = translate(data['api_data'])
	save_data('cache', data, path)
	print "-> Translated %s" % path



def build_translation_cache():
	print "Translating data files..."
	d = os.path.join(u'data', u'api_get_master')
	for filename in os.listdir(os.path.join(ROOT_PATH, d)):
		if filename.endswith('.json'):
			translate_json_file(os.path.join(u'api_get_master', filename))

def build_ship_cache():
	print "Compiling ship data..."
	
	# Exclude なし (placeholder) ships, alternate forms and old event ships
	# Note that these are regex patterns, not string literals
	excluded_name = [ur'なし', ur'S-Naka']
	excluded_yomi = [ur'アル(.*)', ur'mist(.*)']
	
	# Compile them
	excluded_name = [re.compile(pattern) for pattern in excluded_name]
	excluded_yomi = [re.compile(pattern) for pattern in excluded_yomi]
	
	raw_ships = load_data(u'cache', u'api_get_master/ship.json')
	ships = {}
	for item in raw_ships:
		skip = False
		
		# Apply filters
		for pattern in excluded_name:
			if pattern.search(item['api_name']):
				skip = True
		
		for pattern in excluded_yomi:
			if pattern.search(item['api_yomi']):
				skip = True
		
		if skip:
			continue
		
		# TODO: Versioning
		
		# Store any items that pass
		ships[item['api_id']] = item
	
	# Collect all 'base' ships, eg. un-remodeled models
	baseships = ships.copy()
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
		save_data(u'cache', line, u'ships/{name}.json'.format(name=normalize_name(ship['api_name'])))
	
	save_data(u'cache', ships, u'ships.json')

def build_equipment_cache():
	print "Compiling equipment data..."
	
	raw_equips = load_data(u'cache', u'api_get_master/slotitem.json')
	equips = {}
	
	for item in raw_equips:
		equips[item['api_id']] = item
		save_data(u'cache', item, u'equips/{name}.json'.format(name=normalize_name(item['api_name'])))
	
	save_data(u'cache', equips, u'equips.json')



if __name__ == '__main__':
	build_translation_cache()
	build_ship_cache()
	build_equipment_cache()
