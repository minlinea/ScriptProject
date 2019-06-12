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

TOKEN = '864658879:AAHnc3bUMwLTRs0s5MYxtY_OJ3XTk2eTGTo'
MAX_MSG_LENGTH = 300
bot = telepot.Bot(TOKEN)

def getHighwayData(Find_route):
    res_list = []
    result = Parsing_PublicData_Find_Find_route(Find_route)
    return res_list

def Parsing_PublicData_Find_Find_route(Find_route):              #기타 입력을 통해 어떤 고속도로(Find_route)를 받고 거기서 원하는 휴게소 명(Find_RestArea)을 찾는다.


    server = "data.ex.co.kr"  # 서버
    key = "Gl2e5%2BDxQ9BFP7kv5O4uP7TaCRGsDYiJV8gsmoNWU18TBt4meJaLrC8K60czJZT%2FuOc95BaLWZb9uYunRM3okA%3D%3D"
    url = "/exopenapi/locationinfo/locationinfoRest?serviceKey=%s&type=xml&routeNo=%s&numOfRows=50&pageNo=1" %(key, Find_route)
                                                    # 기본적으로 구역으로 검색이 나오기 때문에 Find_route를 인자형태로 넘겨준다.
    conn = http.client.HTTPConnection(server)  # 서버 연결
    conn.request("GET", url)
    req = conn.getresponse()
    #print(req.status, req.reason)      연결 확인
    # print(data.decode('utf-8'))        데이터 확인

    data = req.read()  # 데이터 저장
    tree = ElementTree.fromstring(data)  # ElementTree로 string화
    itemElements = tree.getiterator("list")  # documents 이터레이터 생성

    result = []
    for item in itemElements:
        addr = []
        addr.append(item.find("unitName"))              #휴게소 이름
        if(type(item.find("xValue")) != type(None)):
            addr.append(item.find("xValue"))
            addr.append(item.find("yValue"))
            result.append((addr[0].text, addr[1].text, addr[2].text))
        else:
            addr.append("0")
            addr.append("0")
            result.append((addr[0].text, addr[1], addr[2]))

    return result

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
            break
    return result

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)
