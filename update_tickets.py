from Utilities import google_sheets as gs
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
            change = iccid + "  You can now depro/repro the service line and inform the customer."
        elif iccid == '' and mac_sn != '':
            change = mac_sn
        elif iccid == '' and mac_sn == '':
            change = 'Please inform the customer.'
            # ^^^^  false changed to please inform the customer
        else:
            change = 'ERROR'
            print "Invalid change. Exiting..."
            exit()

        if update == 'Yes':
            z.update_comment(ticket, meid, field, change)
            print 'Updated %s' % ticket

    print 'Done!'


update_tickets()
