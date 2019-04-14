import requests
import json

from datetime import datetime
from pytz import timezone

import os, codecs, ast
import sys
import dbController

from collections import OrderedDict

global URL
global message
global token

URL = 'https://api.telegram.org/bot'
token = '.'
message = '.'

#--------------------------------------------------------------
def upd_chats():
    json = get_updates()
    #write_json(json)
    global result
    result = ''
    try:
        result = json['result']
    except KeyError:
        pass

    for arr in result:
        try:
            if arr['message']['chat']['type'] == 'group':
                dbController.update_groups(arr['message']['chat']['id'], arr['message']['chat']['title'], arr['message']['chat']['type'])
        except KeyError:
            pass
        try:
            if arr['channel_post']['chat']['type'] == 'channel':
                dbController.update_groups(arr['channel_post']['chat']['id'], arr['channel_post']['chat']['title'], arr['channel_post']['chat']['type'])
        except KeyError:
            pass

#--------------------------------------------------------------
def send_message_for_all_group():
    chats = dbController.get_groups()
    for row in chats:
        send_message(row[1], message)

#--------------------------------------------------------------
def send_message(chat_id, text):
    url = URL + token + '/sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=answer)
#--------------------------------------------------------------
def write_json(json):
    with codecs.open("answer.json", "w", encoding="utf-8") as file:
        file.write(str(json))

#--------------------------------------------------------------
def get_chats():
    chats = dbController.get_groups()
    for row in chats:
        print('chat_id: ' + str(row[1]) + ' name: ' + str(row[2]) + ' type: ' + str(row[3]))
#--------------------------------------------------------------
def get_updates():
    url = URL + token + '/getupdates'
    resp = requests.get(url)
    return resp.json()
#--------------------------------------------------------------
#--------------------------------------------------------------
def get_message():
    global message
    messages = dbController.get_message()
    for row in messages:
        message = row[0]
        break
    return message

#--------------------------------------------------------------
def get_bot_info(token):
    url = URL + token + '/getMe'
    resp = requests.get(url)
    json = resp.json()
    if str(json['ok']) == 'True':
        dbController.upd_info_bot(token, json['result']['id'], json['result']['first_name'], json['result']['username'])

#--------------------------------------------------------------
def select_bot():
    global token
    bots = dbController.get_bots_()
    for row in bots:
        if(str(row[4]) == 'True'):
            token = str(row[3])
            break
#--------------------------------------------------------------
