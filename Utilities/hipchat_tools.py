import hipchat
import json

json_info = json.load(open('Resources/hipchat.json'))
try:
    token = json_info['token']
    hc = hipchat.HipChat(token=token)
except KeyError:
    print "Hipchat auth not found. Check help.txt for more info."
    exit()


def send_message(room_id, from_name, message):
    message_color = 'gray'
    hc.message_room(room_id, from_name, message, color=message_color)
    print 'Hipchat notification sent.'
