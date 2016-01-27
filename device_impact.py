from Utilities import zendesk_tools as z
from sys import argv

try:
    script, ticket = argv
except ValueError:
    print 'Include ticket when calling.'
    exit()

device_table = z.calculate_device_impact(ticket)
print device_table
