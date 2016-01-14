import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials


class Worksheet(object):

    def __init__(self, sheet_name):
        self.sheet_name = sheet_name

    def get_sheet(self):
        json_key = json.load(open('Resources/google_sheets.json'))
        scope = ['https://spreadsheets.google.com/feeds']

        try:
            credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
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
            temp['meid'] = line[2]
            temp['field'] = line[3]
            temp['ICCID'] = line[4]
            temp['mac_sn'] = line[5]
            temp['ticket'] = line[10]
            temp['update?'] = line[12]

            output.append(temp)

        if output == []:
            return None
        else:
            return output
