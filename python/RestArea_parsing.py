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

def Separate_str(Find_RestArea):
    n=0
    ns = len(Find_RestArea) -1
    AreaName = ''
    Direction = ''
    while(Find_RestArea[n] != '휴'):
        n += 1
        if(len(Find_RestArea) == n):
            break
    if(Find_RestArea[ns] == ')'):
        Direction = Find_RestArea[ns-2:ns]
    AreaName = Find_RestArea[0:n]           #OO휴게소에서 OO 추출
    return AreaName,Direction



def Parsing_PublicData_Find_Facilities(Find_RestArea, X, Y):              #원하는 휴게소 명(Find_RestArea)의 대표음식을 찾는다.

    flag = False
    Find_RestArea, X, Y, Direction, flag = exception_handling(Find_RestArea,X,Y)
    if flag == False:
        Find_RestArea, Direction = Separate_str(Find_RestArea)

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
        if(item.find("direction").text == Direction):
            if(type(item.find("batchMenu"))) != type(None):
                result.append(item.find("batchMenu").text)             #대표음식
            else:
                result.append('')
            if (type(item.find("brand"))) != type(None):
                result.append(item.find("brand").text)                    #입점브랜드
            else:
                result.append('')
            if (type(item.find("convenience"))) != type(None):
                result.append(item.find("convenience").text)          #편의시설
            else:
                result.append('')
            if (type(item.find("telNo"))) != type(None):
                result.append(item.find("telNo").text)                #전화번호
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
    result.append(kakao_parsing.Parsing_KAKAOMAP_XY(X,Y))
    return result

def exception_handling(name, x, y):

    #case 01 경부선
    if name == '만남의광장':
        return '서울만남', x, y, '부산', True

    else:
        return name, x, y, '', False
'''
안나오는 것
경부선
만남의광장 : 정보
죽전휴게소 : 정보
천안(삼)휴게소 : 정보
금강휴게소 : 정보
김천휴게소(서울,부산) : 지도, 주소, 좌표?
통도사휴게소(부산) : 지도, 주소, 좌표?
양산휴게소(서울) : 지도, 주소, 좌표?

남해선
함안휴게소(부산) : 지도, 주소, 좌표?
함안휴게소(순천) : 지도, 주소, 좌표?
진주휴게소(부산) : 지도, 주소, 좌표?

남해선(영암-순천)
보성녹차휴게소(무안) : 정보, 지도, 주소, 좌표?
보성녹차휴게소(광양) : 지도, 주소, 좌표

88올림픽선
남원휴게소(대구) : 정보
지리산휴게소(고서) : 정보
거창휴게소(고서) : 정보
함양산삼골휴게소(고서) : 정보
함양산삼골휴게소(대구) : 정보, 지도, 주소, 좌표?
논공휴게소(고서) : 정보
논공휴게소(고서) : 지도, 주소, 좌표?
강천산휴게소(대구) : 지도, 주소, 좌표?
강천산휴게소(광주) : 지도, 주소, 좌표?

무안광주선 X

고창담양선 X

서해안선
서산휴게소(목포) : 정보
함평휴게소(목포) : 정보
홍성휴게소(무안) : 정보
고창고인돌휴게소(서울) : 정보
고창고인돌휴게소(목포) : 정보
목감휴게소(서울) : 지도, 주소, 좌표?
매송휴게소(서울) : 정보, 지도, 주소, 좌표?
매송휴게소(목포) : 지도, 주소, 좌표?

평택시흥선 X

울산선 X

평택화성선 X 

대구포항선
청통휴게소 : 정보
와촌휴게소 : 정보

익산장수선
마이산휴게소(장수) : 정보
마이산휴게소(익산) : 정보
진안휴게소(익산) : 지도, 주소, 좌표?
진안휴게소(장수) : 지도, 주소, 좌표?
'''