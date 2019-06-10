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

key = 'sea100UMmw23Xycs33F1EQnumONR%2F9ElxBLzkilU9Yr1oT4TrCot8Y2p0jyuJP72x9rG9D8CN5yuEs6AS2sAiw%3D%3D'  # 변경 필요
TOKEN = '864658879:AAHnc3bUMwLTRs0s5MYxtY_OJ3XTk2eTGTo'
MAX_MSG_LENGTH = 300
baseurl = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?ServiceKey='+key  # 변경 필요
bot = telepot.Bot(TOKEN)

def getHighwayData(Find_route):
    res_list = []
    result = RestArea_parsing.Parsing_PublicData_Find_Find_route(Find_route)
    return res_list

def getRestareaData(Find_RestArea):              #원하는 휴게소 명(Find_RestArea)의 대표음식을 찾는다.
    import http.client
    import urllib
    from xml.etree import ElementTree
    flag = False
    Find_RestArea, x, y, Direction, flag = RestArea_parsing.exception_handling(Find_RestArea, 0, 0)
    if flag == False:
        Find_RestArea, Direction = RestArea_parsing.Separate_str(Find_RestArea)

    hangul_utf8 = urllib.parse.quote(Find_RestArea)
    server = "data.ex.co.kr"  # 서버
    key = "Gl2e5%2BDxQ9BFP7kv5O4uP7TaCRGsDYiJV8gsmoNWU18TBt4meJaLrC8K60czJZT%2FuOc95BaLWZb9uYunRM3okA%3D%3D"
    url = "/exopenapi/business/conveniServiceArea?serviceKey=%s&type=xml&serviceAreaName=%s&numOfRows=10&pageNo=1" %(key, hangul_utf8)
    conn = http.client.HTTPConnection(server)  # 서버 연결
    conn.request("GET", url)
    req = conn.getresponse()

    #data = req.rea()

    data = req.read()  # 데이터 저장
    tree = ElementTree.fromstring(data)  # ElementTree로 string화
    itemElements = tree.getiterator("list")  # documents 이터레이터 생성

    result = []
    for item in itemElements:
        if (item.find("direction").text == Direction):
            if (type(item.find("batchMenu"))) != type(None):
                result.append(item.find("batchMenu").text)  # 대표음식
            else:
                result.append('')
            if (type(item.find("brand"))) != type(None):
                result.append(item.find("brand").text)  # 입점브랜드
            else:
                result.append('')
            if (type(item.find("convenience"))) != type(None):
                result.append(item.find("convenience").text)  # 편의시설
            else:
                result.append('')
            if (type(item.find("telNo"))) != type(None):
                result.append(item.find("telNo").text)  # 전화번호
            else:
                result.append('')
            '''
               추가정보 (죽전휴게소 기준)
                <batchMenu>대나무잎영양맑은곰탕</batchMenu>
                <brand>할리스 외 2</brand>
                <convenience>수유실|내고장특산물|수면실|</convenience>
                <direction>서울</direction>
                <maintenanceYn>X</maintenanceYn>
                <serviceAreaCode>A00002</serviceAreaCode>
                <serviceAreaName>죽전</serviceAreaName>
                <telNo>031-262-3168</telNo>
                <truckSaYn>X</truckSaYn>    
            '''
            break
    return result

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run(date_param, param='11710'):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, date_param, param)
        res_list = getData( param, date_param )
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)
