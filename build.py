from flask_frozen import Freezer
from shipdex import app

# Make sure relative paths resolve correctly!
app.config['FREEZER_BASE_URL'] = 'http://kancolletool.github.io/shipdex/'

freezer = Freezer(app)

if __name__ == '__main__':
	freezer.freeze()
