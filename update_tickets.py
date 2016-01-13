from Utilities import google_sheets as gs
from Utilities import hipchat_tools as hc
from Utilities import zendesk_tools as z


def update_tickets():
    updates = gs.Worksheet("ICCID Changes in NS (Responses)")

    update_list = updates.get_updates()
    for line in update_list:
        meid = line[0]
        field = line[1]
        change = line[2]
        ticket = line[3]
        update = line[4]

        if update == 'Yes':
            z.update_comment(ticket, meid, field, change)
            print 'Updated %s' % ticket

    print 'Done!'
    hc.send_message('276421', 'Tier 3', 'NetSuite updates are complete. Check your tickets for updates.')
    print 'Hipchat notification sent.'

update_tickets()
