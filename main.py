import requests
import json
from worker import Worker

from datetime import datetime
from pytz import timezone

from flask import Flask, request

import os, codecs, ast
import sys
import dbController
import MBot

from collections import OrderedDict

server = Flask(__name__)

def help():
    print('')
    print('/exit                - завершить приложение.')
    print('/pause               - приостановить бота.')
    print('/updatedata          - принудительно обновить данные о группах/каналах.')
    print('/getmessage          - вывести текст сообщения.')
    print('/setmessage          - изменить текст сообщения. Заготовленный текст перенесите в консоль (ПКМ по консоли или CTRL+V).')
    print('/getchats            - вывод списка групп/каналов в которых состоит бот.')
    print('/settoken            - добавить бота по токену.')
    print('/getbots             - вывод списка ботов.')
    print('/activatebot id      - выбрать бота по его id который будет слать сообщения (активировать).')
    print('/activatebot token   - выбрать бота по его токену который будет слать сообщения (активировать).')
    print('/sendall             - выполнить принудительную рассылку сообщений по всем группам/каналам.')
    print('/settime             - установить время для рассылки (06:45, 13:00), по МСК.')
    print('/gettimes            - вывести все временные точки.')
    print('/deltime             - удалить временную точку.')
    print('')
#--------------------------------------------------------------
def about_programm():
    print('')
    print('Привет! Я бот спамер для телеграмма.')
    print('Нужна справка по коммандам! Введите -> /help')


def index():
    print('Hello')

#@server.route("/")
def main():
    about_programm()

    global message

    worker = Worker()

    MBot.get_message()
    MBot.select_bot()
    MBot.upd_chats()
    worker.update_times()
    worker.start()

    while True:
        command = input('>>').lower()

        if(command == '/exit'):
            worker.stop()
            sys.exit()
        elif(command == '/pause'):
            worker.pause()
            print(worker.paused())
        elif(command == '/help'):
            help()
        elif(command == '/updatedata'):
            MBot.upd_chats()
        elif(command == '/getmessage'):
            print(MBot.get_message())
        elif(command == '/getchats'):
            MBot.get_chats()
        elif(command == '/setmessage'):
            message = input('m: ')
            dbController.set_message(message)
            MBot.message = message
        elif(command == '/settoken'):
            token = input('token: ')
            dbController.set_token(token)
            MBot.get_bot_info(token)
        elif(command == '/getbots'):
            dbController.get_bots()
        elif(command == '/activatebot id'):
            id = input('id: ')
            dbController.set_status_bot(str(id), '-1')
            MBot.select_bot()
        elif(command == '/activatebot token'):
            token = input('token: ')
            dbController.set_status_bot('-1', str(token))
            MBot.select_bot()
        elif(command == '/sendall'):
            MBot.send_message_for_all_group()
        elif(command == '/get_token'):
            print('-_- А вот хуй тебе -_-')
        elif(command == '/settime'):
            t = input('HH:MM - Moscow: ')
            dbController.set_time(t)
            worker.update_times()
        elif(command == '/gettimes'):
            dbController.get_times()
            worker.update_times()
        elif(command == '/deltime'):
            id = input('id: ')
            dbController.del_time(id)
            worker.update_times()
        elif(command == '/getrealtime'):
            print( datetime.now(timezone('Europe/Moscow')).strftime('%H:%M'))
        else:
            print('Комманда "' + command + '" не существует')
#--------------------------------------------------------------
if __name__ == "__main__":
    main()
    #server.run( port=os.environ.get('PORT', 5000))

server = Flask(__name__)
'''
if __name__ == "__main__":
    main()
'''
