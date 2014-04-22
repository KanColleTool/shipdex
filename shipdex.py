from collections import OrderedDict
from flask import Flask, render_template, url_for, g
from util import *
from tplhelpers import *

app = Flask(__name__)
app.config.from_object('config')

@app.context_processor
def expose_functions():
	return {
		'normalize_name': normalize_name,
		'sum': sum,
		'speed_string': speed_string,
		'range_string': range_string
	}

@app.route('/')
def index():
	ships = load_data('cache', 'ships.json')
	displayships = OrderedDict()
	
	# Order the display dictionary by ID, numerically
	# JSON doesn't let you use numbers as keys, so this is necessary
	for sid in sorted([int(sid_) for sid_ in ships.keys()]):
		ship = ships[str(sid)]
		
		# Filter out Abyssal ships for now, until I have a
		# way to present them separately from allied ships
		if ship['api_getmes'] == '':
			continue
		
		displayships[sid] = ship
	
	# Filter out anything with an api_aftershipid, as remodels
	# should go on the same page as their base forms
	for sid, ship in ships.iteritems():
		
		afterid = int(ship['api_aftershipid'])
		if afterid != 0 and afterid in displayships:
			del displayships[afterid]
	
	return render_template('index.html', ships=displayships, breadcrumb=['Home'])

@app.route('/s/<name>/')
def ship(name):
	ship = load_data('cache', u'ships/{name}.json'.format(name=normalize_name(name)))
	return render_template('ship.html', ship=ship, breadcrumb=[(url_for('index'), 'Home'), ship[0]['api_name']])

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
