import http.client
import urllib
from xml.etree import ElementTree
import kakao_parsing

RESTAREA = {
    "0010" : "경부선", "0100" : "남해선", "0101" : "남해선(영암-순천)", "0120" : "88올림픽선",
    "0121" : "무안광주선", "0140" : "고창담양선", "0150" : "서해안선" , "0153" : "평택시흥선",
    "0160" : "울산선", "0170" : "평택화성선", "0200" : "대구포항선", "0201" : "익산장수선",
    "0251" : "호남선", "0252" : "천안논산선", "0270" : "순천완주선", "0300" : "청원상주선" ,
    "0301" : "당진대전선", "0351" : "중부선(대전통영)", "0352" : "중부선", "0370" : "제2중부선",
    "0400" : "평택제천선", "0500" : "중부내륙선", "0550" : "영동선"
}

def Parsing_PublicData_Find_RestArea(Find_RestArea, Find_route):              #기타 입력을 통해 어떤 고속도로(Find_route)를 받고 거기서 원하는 휴게소 명(Find_RestArea)을 찾는다.
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
        if(item.find("unitName").text == Find_RestArea):     #찾고자 하는 휴게소를 인자로 받아
            addr.append(item.find("unitName"))              #휴게소 이름
            addr.append(item.find("routeName"))             #고속도로 명
            addr.append(item.find("xValue"))                #x값
            addr.append(item.find("yValue"))                #y값
            result.append((addr[0].text, addr[1].text,addr[2].text, addr[3].text))  #(휴게소 이름, 고속도로명, x, y)
            result.append(kakao_parsing.Parsing_KAKAOMAP_XY(addr[2].text, addr[3].text))
            break
    print(result)






def Parsing_PublicData_Find_Facilities(Find_RestArea):              #원하는 휴게소 명(Find_RestArea)의 대표음식을 찾는다.

    hangul_utf8 = urllib.parse.quote(Find_RestArea[0:len(Find_RestArea)-3])
    server = "data.ex.co.kr"  # 서버
    key = "Gl2e5%2BDxQ9BFP7kv5O4uP7TaCRGsDYiJV8gsmoNWU18TBt4meJaLrC8K60czJZT%2FuOc95BaLWZb9uYunRM3okA%3D%3D"
    url = "/exopenapi/business/conveniServiceArea?serviceKey=%s&type=xml&serviceAreaName=%s&numOfRows=10&pageNo=1" %(key, hangul_utf8)
    conn = http.client.HTTPConnection(server)  # 서버 연결
    conn.request("GET", url)
    req = conn.getresponse()
    #print(req.status, req.reason)      연결 확인

    #data = req.rea()
    #print(data.decode('utf-8'))        #데이터 확인

    data = req.read()  # 데이터 저장
    tree = ElementTree.fromstring(data)  # ElementTree로 string화
    itemElements = tree.getiterator("list")  # documents 이터레이터 생성

    result = []
    for item in itemElements:
        addr = []
        if(item.find("serviceAreaName").text == Find_RestArea[0:len(Find_RestArea)-3]):     #찾고자 하는 휴게소의 이름을 받아 (이 공공데이터는 지리산휴게소인 경우 지리산만 출력함, 00휴게소인 경우 예외처리 필요
            addr.append(item.find("batchMenu").text)             #대표음식
            addr.append(item.find("telNo").text)
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
            result.append(addr)  # 휴게소의 대표 음식
            break
    print(result)

Parsing_PublicData_Find_RestArea("죽전휴게소", "0010")
