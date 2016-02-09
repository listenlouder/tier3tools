from Utilities import zendesk_tools as z
from sys import argv

try:
    _, device_type, ticket = argv
except ValueError:
    print 'Include "device type (based on zendesk tag) ticket" when calling.'
    exit()

z.get_device_type_tickets(device_type, ticket)
