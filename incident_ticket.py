# incident_ticket.py ---------

from Utilities import zendesk_tools as z
from sys import argv

try:
    _, ticket = argv
except ValueError:
    print 'Please include ticket number when executing!'
    exit()

z.pull_view(ticket)

# Customer ticket
# multiple member-generated tickets that are attached as incidents to the zendesk master. Contain query items
# such as:
#            * device type
#            * tags
#            * assignee
#            * last updated
#            * ticket ID
#            * group assigned
#            * affected phone #
#            * triage bucket
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

