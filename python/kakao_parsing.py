import http.client
from xml.etree import ElementTree
import urllib
def Parsing_KAKAOMAP_XY(x, y):
    # 카카오 요청, 다른 예시는 https://developers.kakao.com/docs/restapi/local 참고
    server = "dapi.kakao.com"  # 서버
    headers = {'Authorization': 'KakaoAK cdb3b880191792500cb20af4a46a8edc'}  # 인증 키
    url = "/v2/local/geo/coord2address.xml?x=%s&y=%s" % (x, y)  # 좌표값 url str화
    conn = http.client.HTTPSConnection(server)  # 서버 연결
    conn.request("GET", url, None, headers)
    req = conn.getresponse()
    data = req.read()  # 데이터 저장
    tree = ElementTree.fromstring(data)  # ElementTree로 string화
    w = tree.getiterator()  # documents 이터레이터 생성

    result = ''
    for i in w:
        addr = []
        if(i.tag == "address_name"):
            return i.text

    return result

'''
    # 카카오 요청, 다른 예시는 https://developers.kakao.com/docs/restapi/local 참고
server = "dapi.kakao.com"                                                              #서버
headers = {'Authorization': 'KakaoAK cdb3b880191792500cb20af4a46a8edc'}         #인증 키
url = "/v2/local/geo/coord2regioncode.xml?x=%s&y=%s" %(x,y)                       #좌표값 url str화
conn = http.client.HTTPSConnection(server)                                                #서버 연결
conn.request("GET", url, None, headers)
req = conn.getresponse()

#print(req.status, req.reason)   #요청 확인



#데이터 출력
data = req.read()       #데이터 저장
tree = ElementTree.fromstring(data)     #ElementTree로 string화
itemElements = tree.getiterator("documents")        #documents 이터레이터 생성
'''
'''
conn.request("GET", "/v2/local/geo/coord2regioncode.xml?x=127.1086228&y=37.4012191", None, headers)
예제 기준 항목
document<region_type, code, region_1depth_name, region_2depth_name,
region_3depth_name, region_4depth_name, x, y>


for item in itemElements:
	addr = item.find("address_name")
	print(addr.text)
'''

def Parsing_KAKAOMAP_Address(search_address):
    # 카카오 요청, 다른 예시는 https://developers.kakao.com/docs/restapi/local 참고
    server = "dapi.kakao.com"  # 서버
    headers = {'Authorization': 'KakaoAK cdb3b880191792500cb20af4a46a8edc'}  # 인증 키
    hangul_utf = urllib.parse.quote(search_address)
    url = "/v2/local/search/address.xml?query=%s" %hangul_utf # 좌표값 url str화
    conn = http.client.HTTPSConnection(server)  # 서버 연결
    conn.request("GET", url, None, headers)
    req = conn.getresponse()
    data = req.read()  # 데이터 저장
    tree = ElementTree.fromstring(data)  # ElementTree로 string화
    itemElements = tree.getiterator("documents")  # documents 이터레이터 생성

    result = []
    for item in itemElements:
        addr = []
        addr.append(item.find("y"))
        addr.append(item.find("x"))
        result.append((addr[0].text, addr[1].text))
    return result
