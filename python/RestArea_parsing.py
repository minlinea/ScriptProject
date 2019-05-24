import http.client
import urllib
from xml.etree import ElementTree
import kakao_parsing



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

Parsing_PublicData_Find_RestArea("기흥휴게소(부산)", "0010")
