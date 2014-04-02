from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/ships/')
def ships():
	return render_template('ships.html')

@app.route('/ships/<name>/')
def ship(name):
	return render_template('ship.html', name=name)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
