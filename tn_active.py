# tn_active.py - checks IRIS for numbers on a CSV and returns those that are active

import requests
from sys import argv
import csv

# using argv, take in user csv for input data
try:
    _, csv = argv
except ValueError:
    print """
    Please include CSV file when executing!
    Format: (python) (script name) (csv name/location)
    Example: python tn_active.py dash_tns\ - \ Sheet1.csv (forward slash necessary for spaces in terminal)
    """
    exit()

# function for ripping TNs from provided CSV
def pull_tns_from_csv(csv):

    # reads from the input csv and strips the leading '1' from the tn
    # stores it in an empty list for conversion
    with open(csv) as csvfile:
        temp_store = []

        for tn in csvfile:
            temp_store.append(tn[1:11])

    # print temp_store
    return temp_store

# function for requesting TN data from IRIS
def request_tn_data_from_iris(temp_store):
    print "Querying IRIS API...Please wait."

    for tn in temp_store:
        rsp = requests.get("https://api.inetwork.com/v1.0/tns/%s" % tn,
                           headers=dict({
                               'Accept': 'application/xml',
                               'Content-Type': 'application/xml',
                               'Authorization': 'Basic cmVwdWJsaWN3aXJlbGVzczpwb25HUzcyU3AhY2E='}))

        if rsp.status_code == 200:
            print tn + " is either still in-service with Republic or in aging status."

        # used for debugging the response content from IRIS
        # print rsp.content
    print "\nRequest complete!"


def main():
    request_tn_data_from_iris(pull_tns_from_csv(csv))

main()