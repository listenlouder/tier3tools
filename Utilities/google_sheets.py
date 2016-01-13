import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials


class Worksheet(object):

    def __init__(self, sheet_name):
        self.sheet_name = sheet_name

    def get_sheet(self):
        json_key = json.load(open('Resources/google_sheets.json'))
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
        gc = gspread.authorize(credentials)
        wks = gc.open(self.sheet_name).sheet1
        return wks

    def get_updates(self):
        mac_sn = Worksheet(self.sheet_name).get_sheet()
        data = mac_sn.get_all_values()
        data = data[1::]
        output = []

        for line in data:
            temp = []
            if line[5] != '':
                temp.extend([line[2], line[3], line[5], line[10], line[12]])
            if temp != []:
                output.append(temp)

        if output == []:
            return None
        else:
            return output
