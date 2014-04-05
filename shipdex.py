from flask import Flask, render_template, url_for
from util import *

app = Flask(__name__)

@app.context_processor
def expose_functions():
	return {
		'normalize_name': normalize_name,
		'sum': sum
	}

@app.route('/')
def index():
	ships = load_data('cache', 'ships.json')
	return render_template('index.html', ships=ships, breadcrumb=['Home'])

@app.route('/<name>/')
def ship(name):
	ship = load_data('cache', 'ships/{name}.json'.format(name=normalize_name(name)))
	return render_template('ship.html', ship=ship, breadcrumb=[(url_for('index'), 'Home'), ship['api_name']])

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
