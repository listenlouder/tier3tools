import gspread
from oauth2client.service_account import ServiceAccountCredentials


class Worksheet(object):

    def __init__(self, sheet_name):
        self.sheet_name = sheet_name

    def get_sheet(self):
        scope = ['https://spreadsheets.google.com/feeds']

        try:
            credentials = ServiceAccountCredentials.from_json_keyfile_name('Resources/google_sheets.json', scope)
            gc = gspread.authorize(credentials)
            wks = gc.open(self.sheet_name).sheet1
            return wks
        except KeyError:
            print "Google login info not found. Check help.txt for more info."
            exit()


    def get_updates(self):
        mac_sn = Worksheet(self.sheet_name).get_sheet()
        data = mac_sn.get_all_values()
        data = data[1::]
        output = []

        for line in data:
            temp = {}
            temp['ticket_number'] = line[4]
            temp['update?'] = line[7]

            output.append(temp)

        if output == []:
            return None
        else:
            return output

    def change_to_done(self,row): #changes 'Yes' to 'Done' in the Worksheet
    	mac_sn = Worksheet(self.sheet_name).get_sheet()
    	output = mac_sn.update_cell(row,7,'Done')