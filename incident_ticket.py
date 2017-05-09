# incident_ticket.py ---------
import json
from sys import argv
import requests

# Shamelessly ripped from zendesk_tools.py - Reads Zendesk creds stored in
# json zendesk resource file and assigns elements to local variables for
# the requests module to use.
json_info = json.load(open('Resources/zendesk.json'))

try:
    zd_url = json_info['url']
    # print zd_url - used this to test variable assignment
    zd_email = json_info['email']
    zd_token = json_info['token']
except KeyError:
    print 'Zendesk auth not found. Check help.txt for more info.'
    exit()

# sets credentials obtained from json resource file to Global auth variable
Auth = (zd_email, zd_token)

# Use argv to take in the Zendesk master ticket ID for script use (bug ticket # follows script call).
try:
    _, ticket = argv
except ValueError:
    print 'Please include bug ticket number when executing!'
    exit()

# function for submitting request to Zendesk api to request JSON payload
def get_incident_ticket_info(ticket):
    start_url = zd_url + 'tickets/%s/incidents.json' % ticket
    print 'Querying Zendesk API...'

    # loads each page of JSON data from the zendesk api - stringed by the value pulled
    # by the 'next_page' key.
    while start_url is not None:
        next_url = requests.get(start_url, auth=Auth)
        if next_url.status_code != 200:
            print('Status:', next_url.status_code, 'Problem with the request. Exiting.')
            exit()
        json_data = json.loads(next_url.text)
        tickets_temp = json_data.get('tickets')

        start_url = json.loads(next_url.text).get('next_page')

    print json.dumps(tickets_temp, indent=4)
    return tickets_temp

get_incident_ticket_info(ticket)



# Customer ticket
# multiple member-generated tickets that are attached as incidents to the zendesk master. Contain query items
# such as:
#            * device type - "id": 21108369
#            * tags - will come back to this one, looks a little tricky
#            * assignee - "id": 21638441 (may not be as useful now with current TAC policies)
#            * last updated -
#            * ticket ID
#            * group assigned - (request group) "id": 21638431
#            * affected phone # - "id": 22016047
#            * triage bucket - "id": 22858340
#            * etc... as needed

# zendesk user
# the member who created the ticket. Contains info that we would likely want associated with the query
#  such as:
#            * primary email
#            * user-tags
#            * time zone
#            * community username

# Query functionality
# ability to take a search term against the tickets attached to the zendesk master. Every session of the
#  script should begin as a query for information.
#
#    Zendesk master
#        - The primary zendesk bug or outage ticket (problem ticket) that the customer tickets are attached to. This will
#        - be what is asked for from the initiating user.

# -(additional ability) sort - zendesk search api allows for sorting on (updated_at, created_at, priority, status
#                                                                       or ticket_type)
# -(additional ability) sort order - one of asc or desc (defaults to desc)

# print functionality
# - after collecting the information, need to be able to print it out for the human users.

