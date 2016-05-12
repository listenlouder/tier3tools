import csv
import getpass
import requests
import json
from sys import argv


def get_csv(file_name):
    with open('/Users/%s/Downloads/%s' % (getpass.getuser(), file_name), 'rU') as data:
        reader = csv.reader(data)
        asn_list = list(reader)

    return asn_list


def build_meids(asn_list):
    meids = ''
    for line in asn_list:
        if line[0] != '':
            meids += line[0] + ','

    return meids[:-1]


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
        else:
            print 'MEID %s not found in NS' % data[0]


def run():
    _, filename = argv
    asn_list = get_csv(filename)
    print 'Asking Lord Stratus nicely for %s device records...' % len(asn_list)
    stratus_list = get_device_inventory_record(build_meids(asn_list))

    compare_items(asn_list, stratus_list)
    print 'Script finished.'


run()
