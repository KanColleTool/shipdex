import os
import json
import zlib

ROOT_PATH = unicode(os.path.dirname(os.path.abspath(__file__)))

tldata = None

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

def load_translation_data():
	global tldata
	with open(os.path.join(ROOT_PATH, u'data', u'translation.json')) as f:
		tldata = json.loads(f.read())

def strip_prefix(prefix, s):
	return s if not s.startswith(prefix) else s[len(prefix):]

def normalize_name(name):
	replacements = {
		'#': '_n',
		'.': '',
		'/': '',
		' ': '_'
	}
	name = name.lower()
	for before, after in replacements.iteritems():
		name = name.replace(before, after)
	return name

def save_data(basedir, data, filename, pretty=True):
	outpath = os.path.join(ROOT_PATH, basedir, filename)
	outdir = os.path.dirname(outpath)
	if not os.path.exists(outdir):
		os.makedirs(outdir)
	
	dumpsparams = {}
	if pretty:
		dumpsparams['indent'] = 4
		dumpsparams['separators'] = (',', ': ')
	
	with open(outpath, 'w') as f:
		f.write(json.dumps(data, ensure_ascii=False, **dumpsparams).encode('utf-8'))

def load_data(basedir, filename):
	with open(os.path.join(unicode(ROOT_PATH), unicode(basedir), unicode(filename))) as f:
		return json.loads(strip_prefix("svdata=", f.read()))
