import os
import json

ROOT_PATH = unicode(os.path.dirname(os.path.abspath(__file__)))

def strip_prefix(prefix, s):
	return s if not s.startswith(prefix) else s[len(prefix):]

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
