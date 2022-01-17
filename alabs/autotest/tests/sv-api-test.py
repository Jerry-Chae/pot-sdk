"""
— Plugin 조회
curl --location --request GET 'https://admin-license-rpa.argos-labs.com/openapi/get_plugin_usage_stat?startDate=2021-09-25&endDate=2021-09-25'

— Plugin 수정
curl --location --request POST 'https://admin-license-rpa.argos-labs.com/openapi/set_plugin_usage_stat?pluginName=argoslabs.aaa.ldap&pluginVersion=1.1124.2100&status=pass'
"""


import requests
from pprint import pprint

params = (
    ('startDate', '2021-09-29'),
    ('endDate', '2021-09-29'),
)

rp = requests.get('https://admin-license-rpa.argos-labs.com/openapi/get_plugin_usage_stat', params=params)
print(rp)
rj = rp.json()
pprint(rj)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://admin-license-rpa.argos-labs.com/openapi/get_plugin_usage_stat?startDate=2021-09-25&endDate=2021-09-25')



import requests

params = (
    ('pluginName', 'argoslabs.aaa.ldap'),
    ('pluginVersion', '1.1124.2100'),
    ('status', 'pass'),
)

rp = requests.post('https://admin-license-rpa.argos-labs.com/openapi/set_plugin_usage_stat', params=params)
print(rp)
rj = rp.json()
pprint(rj)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('https://admin-license-rpa.argos-labs.com/openapi/set_plugin_usage_stat?pluginName=argoslabs.aaa.ldap&pluginVersion=1.1124.2100&status=pass')