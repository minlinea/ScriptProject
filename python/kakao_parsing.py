import http.client
from xml.etree import ElementTree

headers = {'Authorization': 'KakaoAK cdb3b880191792500cb20af4a46a8edc'}
server = "dapi.kakao.com"
conn = http.client.HTTPSConnection(server)
conn.request("GET", "/v2/local/geo/coord2regioncode.xml?x=127.1086228&y=37.4012191", None, headers)
req = conn.getresponse()
print(req.status, req.reason)

data = req.read()
tree = ElementTree.fromstring(data)
itemElements = tree.getiterator("documents")
for item in itemElements:
	addr = item.find("address_name")
	print(addr.text)