import http.client

headers = {'Authorization': 'KakaoAK cdb3b880191792500cb20af4a46a8edc'}
server = "dapi.kakao.com"
conn = http.client.HTTPSConnection(server)
conn.request("GET", "/v2/local/geo/coord2regioncode.xml?x=127.1086228&y=37.4012191", None, headers)
req = conn.getresponse()
print(req.status, req.reason)
data = req.read()
print(data.decode('utf-8'))