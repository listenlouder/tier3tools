from Utilities import zendesk_tools as z
from sys import argv

try:
    script, ticket = argv
except ValueError:
    print 'Include ticket when calling.'
    exit()

z.get_ticket_info(ticket)
