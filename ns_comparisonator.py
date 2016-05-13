import csv
import getpass
import requests
import json
import re
from sys import argv

# Gets list of asn values to check from a csv
def get_csv(file_name):
    with open('/Users/%s/Downloads/%s' % (getpass.getuser(), file_name), 'rU') as data:
        reader = csv.reader(data)
        asn_list = list(reader)
    # regex to filter out headers at the top of the csv
    if re.match(r'9{2}0{3}.{9}|A0{5}.{8}', asn_list[0][0]) is None:
        asn_list = asn_list[1:]
    # removes any blank lines in the
    for pos, line in enumerate(asn_list):
        if line[0] == '':
            asn_list.pop(pos)

    return asn_list

# Builds a string of MEIDs to send in the request url
def build_meids(asn_list):
    meids = ''
    for line in asn_list:
        if line[0] != '':
            meids += line[0] + ','

    return meids[:-1]

# Requests device inventory records for specified string of MEIDs
def get_device_inventory_record(meids):
    json_info = json.load(open('Resources/republic.json'))
    base_url = json_info['url2']
    auth_headers = {}
    auth_headers.update({json_info['auth1']: json_info['auth1.5']})
    auth_headers.update({json_info['auth2']: json_info['auth2.5']})

    response = requests.get('%s/device_inventory_records?meid=%s' % (base_url, meids),
                            headers = dict({'accept': 'application/json'},
                                          **auth_headers))

    if response.status_code != 200:
        print 'Problem with the request. Error %s. Exiting...' % response.status_code
        exit()

    return response.json()

# Checks for duplicate MEIDs in the modus list
def find_duplicates(asn_list):
    meids = []
    for item in asn_list:
        meids.append(item[0])

    for item in meids:
        if meids.count(item) > 1:
            print 'Duplicate MEID found: %s. Please resolve before continuing.' % item
            exit()
    print 'No duplicates found'

# Compares response and known list and filters out any missing MEIDs with notification
def remove_missing_meids(asn_list, stratus_list):
    for pos, data in enumerate(asn_list):
        found = False
        for more_data in stratus_list['members']:
            if more_data['meid'] == data[0]:
                found = True
                continue

        if not found:
            print 'MEID %s not found in NS' % data[0]
            asn_list.pop(pos)

    return asn_list

# Cleans asn list then compares it to the stratus list
def compare_items(asn_list, stratus_list):
    clean_asn_list = remove_missing_meids(asn_list, stratus_list)

    for position, data in enumerate(clean_asn_list):
        asn_item = stratus_list['members'][position]
        if asn_item['meid'] == data[0]:
            if data[1] != asn_item['iccid']:
                print 'ICCID mismatch found for device %s. Expected %s Modus gave %s' % \
                      (asn_item['meid'], asn_item['iccid'], data[1])

            if data[2].upper() != asn_item['mac_address']:
                print 'WiFi MAC mismatch found for device %s. Expected %s Modus gave %s' % \
                      (asn_item['meid'], asn_item['mac_address'], data[2].upper())


def run():
    _, filename = argv
    asn_list = get_csv(filename)
    find_duplicates(asn_list)
    print 'Asking Lord Stratus nicely for %s device records...' % len(asn_list)
    stratus_list = get_device_inventory_record(build_meids(asn_list))
    # TODO: Add in a validator for iccid/mac to ensure the values we're given are valid
    compare_items(asn_list, stratus_list)
    print 'Script finished.'


run()
