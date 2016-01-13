import hipchat
import json

json_info = json.load(open('Resources/hipchat.json'))

token = json_info['token']

hc = hipchat.HipChat(token=token)


def send_message(room_id, from_name, message):
    message_color = 'gray'
    hc.message_room(room_id, from_name, message, color=message_color)
    print 'Hipchat notification sent'
