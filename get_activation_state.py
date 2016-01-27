import requests
from sys import argv
import json

json_info = json.load(open('Resources/republic.json'))

try:
    rw_url = json_info['url']
except KeyError:
    print 'Republic auth not found. Check help.txt for more info.'
    exit()


def get_activation_state(meid, msn, mac):
    response = requests.get(rw_url + 'device_state?'
                            'meid=%s&msn=%s&mac_address=%s' % (meid, msn, mac))
    print response.content

try:
    script, meid, msn, mac = argv
except ValueError:
    print "Include MEID, MSN, and MAC when calling."
    exit()

get_activation_state(meid, msn, mac)
