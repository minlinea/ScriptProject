import http.client
from xml.etree import ElementTree


def Parsing_PublicData():
    server = "data.ex.co.kr"  # 서버
    #key = "Gl2e5%2BDxQ9BFP7kv5O4uP7TaCRGsDYiJV8gsmoNWU18TBt4meJaLrC8K60czJZT%2FuOc95BaLWZb9uYunRM3okA%3D%3D"
    url = "/exopenapi/locationinfo/locationinfoRest?serviceKey=Gl2e5%2BDxQ9BFP7kv5O4uP7TaCRGsDYiJV8gsmoNWU18TBt4meJaLrC8K60czJZT%2FuOc95BaLWZb9uYunRM3okA%3D%3D&type=xml&routeNo=0100&numOfRows=10&pageNo=1"
    conn = http.client.HTTPSConnection(server)  # 서버 연결
    conn.request("GET", url)
    req = conn.getresponse()
    print(req.status, req.reason)
    data = req.read()
    print(data.decode('utf-8'))

    data = req.read()  # 데이터 저장
    tree = ElementTree.fromstring(data)  # ElementTree로 string화
    itemElements = tree.getiterator("list")  # documents 이터레이터 생성

    result = []
    for item in itemElements:
        addr = []
        addr.append(item.find("unitName"))
        addr.append(item.find("routeName"))
        addr.append(item.find("xValue"))
        addr.append(item.find("yValue"))
        result.append((addr[0].text, addr[1].text,addr[2].text, addr[3].text))
    return result


Parsing_PublicData()

