from operator import itemgetter
from flask import Flask, render_template, redirect, url_for, g
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
	filtered_ships = {}
	
	# Order the display dictionary by ID, numerically
	# JSON doesn't let you use numbers as keys, so this is necessary
	for sid, ship in ships.iteritems():
		# Filter out Abyssal ships for now, until I have a
		# way to present them separately from allied ships
		if ship['api_getmes'] == '':
			continue
		
		filtered_ships[sid] = ship
	
	# Filter out anything referenced by an api_aftershipid, as
	# remodels should go on the same page as their base forms
	for ship in ships.itervalues():
		afterid = ship['api_aftershipid']
		if afterid != '0' and afterid in filtered_ships:
			del filtered_ships[afterid]
	
	shiplist = sorted(filtered_ships.values(), key=itemgetter('api_name'))
	return render_template('index.html', ships=shiplist)

@app.route('/s/')
def ships():
	return redirect(url_for('index'))

@app.route('/s/<name>/')
def ship(name):
	ship = load_data('cache', u'ships/{name}.json'.format(name=normalize_name(name)))
	return render_template('ship.html', ship=ship)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
