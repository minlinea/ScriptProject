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
    Find_RestArea, X, Y, Direction, flag = exception_handling(Find_RestArea, X, Y)
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
    return result, X,Y, flag

def exception_handling(name, x, y):

    #case 01 경부선
    if name == '만남의광장':
        return '서울만남', x, y, '부산', True
    if name == '죽전휴게소':
        return '죽전', x, y, '서울', True
    if name == '천안(삼)휴게소(서울)':
        return '천안', x, y, '서울', True
    if name == '김천휴게소(서울)':
        return '김천', 128.16356784172586, 36.13086818383473, '서울', True
    if name == '김천휴게소(부산)':
        return '김천', 128.16528919111644, 36.12901166672491, '부산', True
    if name == '통도사휴게소(부산)':
        return '통도사', 129.0909495939539, 35.48878366183761, '부산', True
    if name == '양산휴게소(서울)':
        return '양산', 129.06982849805124, 35.43678924199853, '서울', True
    if name == '함안휴게소(부산)':
        return '함안', 128.34383617340958, 35.29380041362239, '부산', True
    if name == '함안휴게소(순천)':
        return '함안', 128.34383617340958, 35.29380041362239, '순천', True
    if name == '진주휴게소(부산)':
        return '진주', 128.1235874208442, 35.16032726841969, '부산', True
    if name == '보성녹차휴게소(광양)':
        return '보성녹차', 127.1821137477721, 34.80790132772698, '광양', True
    if name == '보성녹차휴게소(무안)':
        return '보성녹차', 127.12767529194748, 34.81371440785017, '무안', True
    if name == '지리산휴게소(고서)':
        return '지리산', x, y, '담양', True
    if name == '거창휴게소(고서)':
        return '거창', x, y, '광주', True
    if name == '논공휴게소(고서)':
        return '논공', x, y, '광주', True
    if name == '논공휴게소(대구)':
        return '논공', 128.40276310711798, 35.76457178676094, '대구', True
    if name == '강천산휴게소(대구)':
        return '강천산', 127.10464157688027, 35.364379524058705, '대구', True
    if name == '강천산휴게소(광주)':
        return '강천산', 127.10572115096238, 35.36533759805025, '광주', True
    if name == '서산휴게소(목포)':
        return '서산', x, y, '무안', True
    if name == '함평휴게소(목포)':
        return '함평', x, y, '무안', True
    if name == '홍성휴게소(무안)':
        return '홍성', x, y, '목포', True
    if name == '고창고인돌휴게소(목포)':
        return '고창', x, y, '목포', True
    if name == '고창고인돌휴게소(서울)':
        return '고창', x, y, '서울', True
    if name == '행담도휴게소(목포)':
        return '행담도', x, y, '서울', True
    if name == '목감휴게소(서울)':
        return '목감', 126.86997404835101, 37.3903279980462, '서울', True
    if name == '매송휴게소(서울)':
        return '매송', 126.89244245681190, 37.26619557598881, '시흥', True
    if name == '매송휴게소(목포)':
        return '매송', 126.8883363822355, 37.264750108105327, '목포', True
    if name == '청통휴게소':
        return '청통', x, y, '대구', True
    if name == '와촌휴게소':
        return '와촌', x, y, '포항', True
    if name == '마이산휴게소(장수)':
        return '진안', x, y, '장수', True
    if name == '마이산휴게소(익산)':
        return '진안', x, y, '익산', True
    if name == '이서휴게소(순천)':
        return '이서', 127.02385321748493, 35.80412162128559, '순천', True
    if name == '이서휴게소(천안)':
        return '이서', 127.02579083249078, 35.80184643246116, '천안', True
    if name == '오수휴게소(완주)':
        return '오수', 127.31161305880694, 35.540243924351614, '전주', True
    if name == '오수휴게소(순천)':
        return '오수', 127.3093928973747, 35.54100673136881, '광양', True
    if name == '황전휴게소(완주)':
        return '황전', 127.45464176791653, 35.15331693978817, '전주', True
    if name == '황전휴게소(순천)':
        return '황전', 127.4541691064677, 35.14883719358269, '광양', True
    if name == '화서휴게소':
        return '화서', x, y, '상주', True
    if name == '속리산휴게소':
        return '속리산', x, y, '청원', True
    if name == '의성휴게소(청주)':
        return '의성', 128.44455233634204, 36.410927715964746, '상주', True
    if name == '의성휴게소(영덕)':
        return '의성', 128.44694602248086, 36.40967685806674, '영덕', True
    if name == '청송휴게소(청주)':
        return '청송', 129.0120145568761, 36.45683094719459, '상주', True
    if name == '청송휴게소(영덕)':
        return '청송', 129.01329192690858, 36.45550475159024, '영덕', True
    if name == '만남의광장(남이)':
        return '하남만남', 127.20610091272289, 37.53033424558787, '통영', True
    if name == '마장휴게소(남이)':
        return '마장', 127.40848361003513, 37.26274653264699, '복합', True
    if name == '마장휴게소(통영)':
        return '마장복합', 127.40848361003513, 37.26274653264699, '통영', True
    if name == '안성맞춤휴게소(안성)':
        return '안성맞춤', x, y, '평택', True
    if name == '안성맞춤휴게소(음성)':
        return '안성맞춤', x, y, '충주', True
    if name == '천등산휴게소(제천)':
        return '천등산', 127.93969902749748, 37.06131985944529, '제천', True
    if name == '천등산휴게소(평택)':
        return '천등산', 127.98937127019306, 37.0769255343566, '평택', True
    if name == '금왕휴게소(평택)':
        return '금왕', 127.5895753420414, 36.97051826793606, '평택', True
    if name == '금왕휴게소(제천)':
        return '금왕', 127.5907134109884, 36.968980786026, '충주', True
    if name == '용인휴게소(인천)':
        return '용인', x, y, '서창', True
    if name == '여주휴게소(인천)':
        return '여주', x, y, '서창', True
    if name == '문막휴게소(인천)':
        return '문막', x, y, '서창', True
    if name == '횡성휴게소(인천)':
        return '횡성', x, y, '서창', True
    if name == '평창휴게소(인천)':
        return '평창', x, y, '서창', True
    if name == '강릉휴게소(인천)':
        return '강릉', x, y, '서창', True
    if name == '덕평휴게소(강릉)':
        return '덕평', 127.38980831645587, 37.241321530161926, '강릉', True
    if name == '홍천강휴게소':
        return '홍천강', x, y, '춘천', True
    else:
        return name, x, y, '', False