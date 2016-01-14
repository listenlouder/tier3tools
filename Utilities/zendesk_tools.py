import requests
import json

json_info = json.load(open('Resources/zendesk.json'))

try:
    zd_url = json_info['url']
    zd_email = json_info['email']
    zd_token = json_info['token']
except KeyError:
    print 'Zendesk auth not found. Check help.txt for more info.'
    exit()


def update_comment(ticket, meid, field, change):
    long_url = zd_url + '/tickets/%s.json' % ticket
    auth = (zd_email, zd_token)
    data = json.dumps({
        'ticket': {
            'status': 'open',
            'comment': {
                'public': False,
                'body': 'MEID: %s updated with %s: %s' % (meid, field, change)
            }
        }
    })
    headers = {'Content-Type': 'application/json'}

    response = requests.put(long_url, data=data, auth=auth, headers=headers)

    if response.status_code != 200 and response.status_code != 422:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')
        exit()
    elif response.status_code == 422:
        print 'Ticket %s could not be updated. Is it closed?' % ticket

    print 'Success!'
