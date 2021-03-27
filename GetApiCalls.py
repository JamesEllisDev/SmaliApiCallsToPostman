import io
import re
import json

fp = open('ApiCalls.Smali')
inMethod = False
data = {}
# data['info'] = {}
data['info'] = {
    '_postman_id': 'ce5e504d-7a79-40b0-aca1-1221947dc435',
    'name': fp.name,
    'schema': 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'
}
data['item'] = []

datatoadd = {}

request = {}

for x in fp:
    if x.strip() not in ['\n', '\r\n', '', '\r', '\t']:
        if 'return' in x:
            data['item'].append(datatoadd)
            if inMethod == True:
                datatoadd = {}
            inMethod = False
        pass
        if 'public static' in x:
            inMethod = True
            datatoadd['name'] = re.findall('[^\s]+(?=\()', x)[0]
            datatoadd['protocolProfileBehavior'] = {
                'disableBodyPruning': True
            }
            datatoadd['request'] = {
                'method': 'GET',
                "header": [],
                "body": [],
                "url": {
                    'protocol': "http",
                    'path': [],
                    'query': [],
                    'host': []
                }
            }
            datatoadd['response'] = []
        pass
        if inMethod == True:
            if 'const-string' in x:
                string = re.findall('"(.*?)"', x)[0]
                if "/" not in x:
                    datatoadd['request']['url']['query'].append({
                        "key": string,
                        "value": ""
                    })
                pass
                if "/" in x:
                    if "https" in string:
                        datatoadd['request']['url']['protocol'] = 'https'
                        pass
                    elif "http" in string:
                        datatoadd['request']['url']['protocol'] = 'http'
                        pass
                    stringWithoutHttps = string.replace(
                        "http://", "").replace("https://", "")
                    spliiter = stringWithoutHttps.split('/')
                    for item in spliiter:
                        if "." in item:
                            hosts = item.split('.')
                            for item in hosts:
                                datatoadd['request']['url']['host'].append(item)
                        elif "." not in item:
                            datatoadd['request']['url']['path'].append(item)
                        pass
                pass
        pass
    pass

# datatoadd['request']['url']['raw']

with open('output.json', 'w') as outfile:
    json.dump(data, outfile)
