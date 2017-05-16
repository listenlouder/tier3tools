# tn_active.py - checks IRIS for numbers on a CSV and returns those that are active

import requests
from sys import argv
import csv

# using argv, take in user csv for input data
try:
    _, csv = argv
except ValueError:
    print 'Please include CSV file when executing!'
    exit()

# function for submitting request to IRIS
def pull_tns_from_csv(csv):

    # reads from the input csv and strips the leading '1' from the tn
    # stores it in an empty list for conversion
    with open(csv) as csvfile:
        temp_store = []

        for tn in csvfile:
            temp_store.append(tn[1:])

    # print temp_store
    return temp_store

def request_tn_data_from_iris(temp_store):

    for tn in temp_store:
        print tn
        rsp = requests.get("https://api.inetwork.com/v1.0/tns/%s" % tn,
                           headers=dict({
                               'Accept': 'application/xml',
                               'Content-Type': 'application/xml',
                               'Authorization': 'Basic cmVwdWJsaWN3aXJlbGVzczpwb25HUzcyU3AhY2E='}))

        if rsp.status_code != 200:
            print'Request failed: %s' % rsp.status_code


def main():
    request_tn_data_from_iris(pull_tns_from_csv(csv))

main()