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
    long_url = zd_url + 'tickets/%s.json' % ticket
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


def get_ticket_info(ticket):
    long_url = zd_url + 'tickets/%s.json' % ticket
    auth = (zd_email, zd_token)
    response = requests.get(long_url, auth=auth)

    if response.status_code != 200:
        print 'Problem with the request. Exiting.'
        exit()
    else:
        print 'Success!'

    return response.content


def get_device_info(content):
    info = content['custom_fields']

    device_info = {
        'TN': info['22016047'],
        'Serial Number': info['28873987'],
        'RW App Version': info['28864868'],
        'MEID': info['28864878'],
        'Model': info['29283457'],
        'WiFi MAC': info['28873877'],
        'Storage': info['28873887'],
        'Build': info['28873907'],
        'ICCID': info['28864958'],
        'MDN': info['28864968'],
        'Plan': info['28865258']
    }

    return device_info


def pull_view(view):
    next_page = view
    login = ('wbradford@bandwidth.com/token', 'r3JY0ireK2G2d0yvbxZfBLLIZcAk8TbkTE1xqInI')
    ticket_numbers = {}
    tally = 1
    print 'Querying Zendesk...'

    while next_page is not None:
        ticket_view = requests.get(next_page, auth=login)
        if ticket_view.status_code != 200:
            print('Status:', ticket_view.status_code, 'Problem with the request. Exiting.')
            exit()
        json_data = json.loads(ticket_view.text)
        tickets_temp = json_data.get("tickets")
        total = json.loads(ticket_view.text).get("count")

        for thing in tickets_temp:
            for key, value in thing.items():
                if key == "id":
                    ticket_numbers[value] = thing.get('updated_at'), thing.get('status'), thing.get('custom_fields')
        next_page = json.loads(ticket_view.text).get('next_page')

        print 'Finished page %d of %d' % (tally, total/100 + 1)
        tally += 1

    print 'Done!'
    return ticket_numbers


def get_device_type_tickets(device_type, ticket):
    incidents = pull_view('https://help.republicwireless.com/api/v2/tickets/%s/incidents.json' % ticket)
    device_type_tickets = []

    for key, value in incidents.items():
        if str(value[2][2].values()[1]) == device_type:
            device_type_tickets.append(key)

    return device_type_tickets


def get_affected_devices(ticket):
    incidents = pull_view('https://help.republicwireless.com/api/v2/tickets/%s/incidents.json' % ticket)
    device_types = []

    for key, value in incidents.items():
        device_types.append(str(value[2][2].values()[1]))

    return device_types


def calculate_device_impact(ticket):
    device_info = get_affected_devices(ticket)
    device_table = {}

    for item in device_info:
        if item not in device_table:
            device_table[item] = 1
        else:
            device_table[item] += 1

    return device_table
