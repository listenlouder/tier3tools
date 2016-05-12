from Utilities import google_sheets as gs
from Utilities import zendesk_tools as z
# from Utilities import slack_tools as s

def update_tickets():
    updates = gs.Worksheet("ICCID Changes in NS (Responses)")
    needs_update = False
    update_list = updates.get_updates()

    for item in update_list:
        meid = item['meid']
        field = item['field']
        mac_sn = item['mac_sn']
        iccid = item['ICCID']
        ticket = item['ticket']
        update = item['update?']

        if mac_sn == '' and iccid != '':
            change = iccid
        elif iccid == '' and mac_sn != '':
            change = mac_sn
        elif iccid == '' and mac_sn == '':
            change = 'False'
        else:
            change = 'ERROR'
            print "Invalid change. Exiting..."
            exit()

        if update == 'Yes':
            needs_update = True
            z.update_comment(ticket, meid, field, change)
            print 'Updated %s' % ticket

    print 'Done!'
    if needs_update:
        pass
        # This will send a message to slack once we can get a stupid token
        # s.send_message('room_name', 'Tier 3', 'NetSuite updates are complete. Check your tickets for updates.')

update_tickets()
