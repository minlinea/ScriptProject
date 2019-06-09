#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

import telegram_reply


def replyAptData(date_param, user, loc_param='11710'):

    print(user, date_param, loc_param)
    res_list = telegram_reply.getData( loc_param, date_param )
    msg = ''
    for r in res_list:
        print( str(datetime.now()).split('.')[0], r )
        if len(r+msg)+1 > telegram_reply.MAX_MSG_LENGTH:
            telegram_reply.sendMessage( user, msg )
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        telegram_reply.sendMessage( user, msg )
    else:
        telegram_reply.sendMessage( user, '%s 기간에 해당하는 데이터가 없습니다.'%date_param )


def save( user, loc_param ):

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES ("%s", "%s")' % (user, loc_param))
    except sqlite3.IntegrityError:
        telegram_reply.sendMessage( user, '이미 해당 정보가 저장되어 있습니다.' )
        return
    else:
        telegram_reply.sendMessage( user, '저장되었습니다.' )
        conn.commit()

def help(user, loc_param):
    pass

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        telegram_reply.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('고속도로') and len(args)>1:
        print('고속도로 검색:', args[1])
        replyAptData( '201705', chat_id, args[1] )
    elif text.startswith('휴게소')  and len(args)>1:
        print('휴게소 검색:', args[1])
        save( chat_id, args[1] )
    elif text.startswith('휴게소')  and len(args)>1:
        print('도움', args[1])
        help(chat_id, args[1])
    else:
        telegram_reply.sendMessage(chat_id, '모르는 명령어입니다.\n고속도로 [고속도로 이름], 휴게소 [휴게소 이름], 도움 중 하나의 명령을 입력하세요.')

def work_telegram():

    #today = date.today()
    #current_month = today.strftime('%Y%m')

    #print( '[',today,']received token :', telegram_reply.TOKEN )

    bot = telepot.Bot(telegram_reply.TOKEN)
    pprint( bot.getMe() )

    bot.message_loop(handle)

    print('텔레그램 작동완료')
