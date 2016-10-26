import requests
import json
import csv
import time
from copy import deepcopy

json_info = json.load(open('Resources/zendesk.json'))

zd_url = json_info['url']
auth_info = (json_info['email'], json_info['token'])


def get_emails_from_csv(file_name):
    with open(file_name, 'rU') as f:
        reader = csv.reader(f)
        csv_list = list(reader)

    emails = []

    for line in csv_list:
        emails.append(line[2])

    return emails

def get_all_users(url, auth_info):
    all_users = []

    while url is not None:
        rsp = requests.get(url, auth = auth_info)

        if rsp.status_code == 429:
            time_to_sleep = rsp.headers['Retry-After']
            time.sleep(time_to_sleep)

        elif rsp.status_code != 200:
            print 'Problem with the request. Exiting'
            print rsp
            exit()

        users = rsp.json()
        all_users.extend(users['users'])

        url = users.get('next_page')

    return all_users


def parse_users(emails, users):
    cool_users = []
    for user in users:
        if user['email'] in emails:
            user['user_fields']['soak_member'] = 'churn_xp_1'
            cool_users.append(user)

    return cool_users


def update_handler(users, url, auth_info):
    copy_users = deepcopy(users)
    start_pos = 0
    while start_pos <= len(users):
        if start_pos + 100  > len(users):
            end_pos = len(users)
        else:
            end_pos = start_pos + 100
        update_users = json.dump(copy_users[start_pos: end_pos])
        copy_users = copy_users[end_pos:]

        success = post_updates(url, auth_info, update_users)

        if success:
            start_pos += 100
        else:
            print 'Request unsuccessful'


def post_updates(url, auth_info, users):
    success = False

    while not success:
        rsp = requests.put(url, auth = auth_info, data = users)

        if rsp.status_code == 429:
            time_to_sleep = rsp.headers['Retry-After']
            time.sleep(time_to_sleep)

        elif rsp.status_code != 200:
            print 'Problem with the request. Exiting'
            print rsp
            exit()

        else:
            success = True

    return success


def run():
    list_of_emails = get_emails_from_csv('file.csv')
    all_users = get_all_users('%s/users.json' % zd_url, auth_info)
    cool_users = parse_users(list_of_emails, all_users)
    update_handler(cool_users, '%s/users/update_many.json' % zd_url, auth_info)
