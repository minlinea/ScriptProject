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
import RestArea_parsing
import telegram_reply


RESTAREA = {
    "0010" : "경부선", "0100" : "남해선", "0101" : "남해선(영암-순천)", "0120" : "88올림픽선",
    "0121" : "무안광주선", "0140" : "고창담양선", "0150" : "서해안선" , "0153" : "평택시흥선",
    "0160" : "울산선", "0170" : "평택화성선", "0200" : "대구포항선", "0201" : "익산장수선",
    "0251" : "호남선", "0252" : "천안논산선", "0270" : "순천완주선", "0300" : "청원상주선" ,
    "0301" : "당진대전선", "0351" : "중부선(대전통영)", "0352" : "중부선", "0370" : "제2중부선",
    "0400" : "평택제천선", "0500" : "중부내륙선", "0550" : "영동선"
}

def Search_Highway(data, user):
    res_list = []
    print(user, data)
    for route_num, route_name in RESTAREA.items():
        if(route_name == data):
            result = RestArea_parsing.Parsing_PublicData_Find_Find_route(route_num)
            for i in range(len(result)):
                res_list.append(result[i][0])
            if (route_name == RESTAREA["0120"]):
                res_list.pop(0)
                res_list.pop(4)
                res_list.pop(5)
            elif (route_name == RESTAREA["0201"]):
                res_list.pop(2)
                res_list.pop(2)
            elif (route_name == RESTAREA["0252"]):
                res_list.pop(0)
                res_list.pop(0)
                res_list.pop(0)
                res_list.pop(0)
            elif (route_name == RESTAREA["0270"]):
                res_list.pop(0)
                res_list.pop(0)
            elif (route_name == RESTAREA["0301"]):
                res_list.pop(0)
                res_list.pop(2)
                res_list.pop(2)
            elif (route_name == RESTAREA["0352"]):
                res_list.pop(7)
                res_list.pop(7)
            elif (route_name == RESTAREA["0400"]):
                res_list.pop(3)
                res_list.append("천등산휴게소(평택)")
            elif (route_name == RESTAREA["0500"]):
                res_list.pop(12)
                res_list.pop(12)

    msg = ''
    for r in res_list:
        #print( str(datetime.now()).split('.')[0], r )
        if len(r+msg)+1 > telegram_reply.MAX_MSG_LENGTH:
            telegram_reply.sendMessage( user, msg )
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        telegram_reply.sendMessage( user, msg )
    else:
        telegram_reply.sendMessage( user, '%s에 해당하는 데이터가 없습니다.'%data )


def Search_Restarea( user, data  ):

    res_list = []
    print(user, data)
    res_list = telegram_reply.getRestareaData(data)
    if(len(res_list) == 0):
        telegram_reply.sendMessage(user, '%s에 해당하는 데이터가 없습니다.' % data)
    else:
        new_text = '특색 메뉴 : {0}\n입점 브랜드 : {1}\n편의시설 : {2}\n전화번호 : {3}'.format(res_list[0], res_list[1], res_list[2],
                                                                                        res_list[3])
        if new_text:
            telegram_reply.sendMessage(user, new_text)
        else:
            telegram_reply.sendMessage(user, '%s에 해당하는 데이터가 없습니다.' % data)

def help(user, data):
    if(data == '고속도로'):
        msg = "다음과 같이 입력합니다.\n고속도로 [고속도로명]\nex)고속도로 경부선\n"
        for i in RESTAREA.values():
            msg += i + ' '
    elif (data == '휴게소'):
        msg = "다음과 같이 입력합니다.\n휴게소 [휴게소명]\nex)고속도로 기흥휴게소(부산)\n고속도로에서 검색한 내용과 일치한 이름으로 검색해야 합니다."
    else:
        msg = '도움이 필요하신가요?\n도움 고속도로\n도움 휴게소'
    telegram_reply.sendMessage(user, msg)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        telegram_reply.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('고속도로') and len(args)>1:
        print('고속도로 검색:', args[1])
        Search_Highway( args[1], chat_id)
    elif text.startswith('휴게소')  and len(args)>1:
        print('휴게소 검색:', args[1])
        Search_Restarea( chat_id, args[1] )
    elif text.startswith('도움')  and len(args)>1:
        print('도움', args[1])
        help(chat_id, args[1])
    else:
        telegram_reply.sendMessage(chat_id, '모르는 명령어입니다.\n고속도로 [고속도로 이름], 휴게소 [휴게소 이름], 도움 중 하나의 명령을 입력하세요.')

def work_telegram():

    bot = telepot.Bot(telegram_reply.TOKEN)
    pprint( bot.getMe() )

    bot.message_loop(handle)

    print('텔레그램 작동완료')
