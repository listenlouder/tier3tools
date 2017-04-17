import csv
import requests
import getpass
import json


def get_sluuids(file_name):
    with open(file_name, 'rU') as f:
        reader = csv.reader(f)
        csv_list = list(reader)

    sluuids = []

    for line in csv_list:
        if line[0] != 'SLUUID':
            sluuids.append(line[0])

    return sluuids


def get_sluuid_info(sluuid, output):
    print 'Getting info for sluuid %s' % sluuid
    rsp = requests.get("<url>/v3/service_lines/%s" % sluuid,
                       headers=dict({'<auth_headers>': '<more_headers'}))

    assert rsp.status_code == 200, 'Request failed: %s' % rsp.status_code
    blah = rsp.json()

    output.append({'service_line': sluuid, 'iccid': get_iccid(blah), 'msisdn': get_msisdn(blah),
                   'imei': blah['current_device']['device_id']})


def get_iccid(service_line):
    if service_line.get('iccid'):
        return service_line['iccid']
    else:
        return service_line['sims'][0]['iccid']


def get_msisdn(service_line):
    if service_line.get('mdn'):
        return service_line['mdn']
    else:
        for sim in service_line['sims']:
            if sim['status'] in ['Provisioned', 'PendingActivation']:
                return sim['mdn']
            else:
                return None


sluuids = get_sluuids('/Users/%s/Downloads/tmo_import.csv' % getpass.getuser())

output_list = []

for sluuid in sluuids:
    get_sluuid_info(sluuid, output_list)

with open('for_tier_3.json', 'w') as fp:
    json.dump(output_list, fp)