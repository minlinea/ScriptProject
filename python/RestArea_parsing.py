import http.client
import folium
from xml.etree import ElementTree
import kakao_parsing

def Draw_folium(x,y, address):
    map_osm = folium.Map (location = [x, y],zoom_start=18)
    folium.Marker([x, y], popup=address).add_to(map_osm)
    map_osm.save('osm.html')

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
    Draw_folium((result[0][3]),float(result[0][2]),result[1][0][0])                # 주소 이미지와 주소 출력

def Parsing_PublicData_Find_representFoodServiceArea(Find_RestArea):              #원하는 휴게소 명(Find_RestArea)의 대표음식을 찾는다.
    server = "data.ex.co.kr"  # 서버
    key = "Gl2e5%2BDxQ9BFP7kv5O4uP7TaCRGsDYiJV8gsmoNWU18TBt4meJaLrC8K60czJZT%2FuOc95BaLWZb9uYunRM3okA%3D%3D"
    url = "/exopenapi/business/representFoodServiceArea?serviceKey=%s&type=xml&numOfRows=200&pageNo=1" %key
                                                    # 모든 정보르 받아와 버리자..
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
        if(item.find("serviceAreaName").text == Find_RestArea[0:len(Find_RestArea)-3]):     #찾고자 하는 휴게소의 이름을 받아 (이 공공데이터는 지리산휴게소인 경우 지리산만 출력함, 00휴게소인 경우 예외처리 필요
            addr.append(item.find("batchMenu"))             #대표음식
            result.append((addr[0].text))  # 휴게소의 대표 음식
            break
    print(result)

Parsing_PublicData_Find_representFoodServiceArea("지리산휴게소")