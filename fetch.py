import sys, os
import json
import requests
from util import *

try:
	from keys import *
except Exception, e:
	print "To use this, you first have to create a file called 'keys.py' in the"
	print "application directory. Then look at your API Link:"
	print ""
	print "    http://[server_ip]/kcs/mainD2.swf?api_token=[api_token]&api_starttime=..."
	print ""
	print "Once you're done looking at it, paste the following into keys.py,"
	print "replacing [server_ip] and [api_token] with your own values:"
	print ""
	print "--------------------------------------------------------------------"
	print ""
	print "KANCOLLE_API_SERVER = '[server_ip]'"
	print "KANCOLLE_API_TOKEN = '[api_token]'"
	print ""
	print "--------------------------------------------------------------------"
	print ""
	print "WARNING: Your API Token will let anyone bypass the login and access"
	print "         your account. Don't let anyone you don't trust see it, or"
	print "         you just might wake up one day to find all your boatgirls"
	print "         missing and your deck full of nothing but NAKA-CHAN DAYO."
	sys.exit()



# 
# Global Variables
# 
s = requests.Session()
s.headers.update({'Referer': 'http://%s/kcs/mainD2.swf?api_token=%s' % (KANCOLLE_API_SERVER, KANCOLLE_API_TOKEN)})



# 
# Fetching stuff
# 
def fetch_translation():
	r = requests.get('http://api.comeonandsl.am/translation/en/')
	data = r.json()
	save_data('data', data['translation'], 'translation.json')

def fetch_endpoint(endpoint, save=True):
	r = s.post('http://%s/kcsapi/%s' % (KANCOLLE_API_SERVER, endpoint), data={'api_token': KANCOLLE_API_TOKEN, 'api_verno': 1});
	data = json.loads(strip_prefix('svdata=', r.text).decode('unicode-escape'))
	
	if save:
		save_data('data', data, endpoint + '.json')



if __name__ == '__main__':
	fetch_translation()
	fetch_endpoint('api_get_master/ship')
