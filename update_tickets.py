from Utilities import google_sheets as gs
from Utilities import hipchat_tools as hc
from Utilities import zendesk_tools as z


def update_tickets():
    updates = gs.Worksheet("ICCID Changes in NS (Responses)")

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
            z.update_comment(ticket, meid, field, change)
            print 'Updated %s' % ticket

    print 'Done!'
    hc.send_message('276421', 'Tier 3', 'NetSuite updates are complete. Check your tickets for updates.')

update_tickets()
