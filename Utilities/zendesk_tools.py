from zdesk import Zendesk
import json

json_info = json.load(open('Resources/zendesk.json'))

zd_url = json_info['url']
zd_email = json_info['email']
zd_token = json_info['token']

zd = Zendesk(zd_url, zd_email, zd_token, zdesk_token=True)


def update_comment(ticket, meid, field, change):
    data = json.dumps({
        'ticket': {
            'status': 'open',
            'comment': {
                'public': False,
                'body': 'MEID: %s updated with %s: %s' % (meid, field, change)
            }
        }
    })
    zd.ticket_update(ticket, data)
    print 'Success!'
