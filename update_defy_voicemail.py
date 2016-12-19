from Utilities import Defy_voicemail_sheet as gs
from Utilities import zendesk_tools as z


def update_tickets():
    updates = gs.Worksheet("Defy XT Voicemail Password Reset (Responses)")
    row = 1 #initializes the row variable
    update_list = updates.get_updates()
    for item in update_list:
        ticket = item['ticket_number']
        update = item['update?']
        row +=1

        if update == 'Test':
            z.update_public_comment(ticket)
            print 'Updated %s' % ticket
            updates.change_to_done(row)

    print 'Done!'


update_tickets()