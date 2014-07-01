#!/usr/bin/env python
# coding: utf-8
import sys, os
import json
import ctypes
import re
from util import *

def build_ship_cache():
	print "Compiling ship data..."
	
	# Exclude なし (placeholder) ships, alternate forms and old event ships
	# Note that these are regex patterns, not string literals
	excluded_name = [ur'なし', ur'S-Naka']
	excluded_yomi = [ur'アル(.*)', ur'mist(.*)']
	
	# Compile them
	excluded_name = [re.compile(pattern) for pattern in excluded_name]
	excluded_yomi = [re.compile(pattern) for pattern in excluded_yomi]
	
	raw_ships = load_data(u'data', u'api_start2.json')['api_data']['api_mst_ship']
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
		afterid = int(ship['api_aftershipid'])
		if afterid != 0 and afterid in baseships:
			del baseships[afterid]
	
	# Collect all ships of the same 'evolutionary line' together
	for ship in baseships.itervalues():
		line = []
		current_item = ship
		while True:
			line.append(current_item)
			afterid = int(current_item['api_aftershipid'])
			if afterid != 0:
				current_item = ships[afterid]
			else:
				break
		save_data(u'cache', line, u'ships/{name}.json'.format(name=normalize_name(translate(ship['api_name']))))
	
	save_data(u'cache', ships, u'ships.json')

def build_equipment_cache():
	print "Compiling equipment data..."
	
	raw_equips = load_data(u'data', u'api_start2.json')['api_data']['api_mst_slotitem']
	equips = {}
	
	for item in raw_equips:
		# Items with no description are enemy-only
		if item['api_info'] == '':
			continue
		
		equips[item['api_id']] = item
		save_data(u'cache', item, u'equips/{name}.json'.format(name=normalize_name(translate(item['api_name']))))
	
	save_data(u'cache', equips, u'equips.json')



if __name__ == '__main__':
	build_ship_cache()
	build_equipment_cache()
