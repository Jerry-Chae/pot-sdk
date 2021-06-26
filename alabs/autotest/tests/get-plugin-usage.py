import os
import csv
import sys
import json
# import pprint
import requests
import logging
import urllib3
import subprocess
from bs4 import BeautifulSoup
from operator import itemgetter
from tempfile import NamedTemporaryFile
from alabs.ppm import _main


################################################################################
class PluginReport(object):
    DUMP_ALL = "https://pypi-official.argos-labs.com/data/plugin-static-files/dumpspec-def-all.json"
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # ==========================================================================
    def __init__(self, logger):
        self.logger = logger
        self.report = {}
        self.rows = []
        self.dumpall = None

    # ==========================================================================
    @staticmethod
    def ver_compare(a, b):
        a_eles = a.split('.')
        b_eles = b.split('.')
        max_len = max(len(a_eles), len(b_eles))
        for i in range(max_len):
            if i >= len(a_eles):  # a='1.2', b='1.2.3' 인 경우 a < b
                return -1
            elif i >= len(b_eles):  # a='1.2.3', b='1.2' 인 경우 a > b
                return 1
            if int(a_eles[i]) > int(b_eles[i]):
                return 1
            elif int(a_eles[i]) < int(b_eles[i]):
                return -1
        return 0

    # ==========================================================================
    def get_dump_all(self):
        # self.DUMP_ALL 에서 json 을 가져와서 처리하는데
        #   argoslabs.time.getts 와 같은 모듈이 안 보여서 alabs.ppm.main을 이용
        # r = requests.get(self.DUMP_ALL)
        # self.dumpall = json.loads(r.text)
        tf_name = None
        try:
            with NamedTemporaryFile(suffix='.json', prefix='dump-all-') as tf:
                tf_name = tf.name
            cmd = [
                #'alabs.ppm',
                '--plugin-index',
                'https://pypi-official.argos-labs.com/pypi',
                'plugin',
                'get',
                '--official-only',
                '--without-cache',
                '--outfile',
                tf_name
            ]
            r = _main(cmd)
            #po = subprocess.Popen(cmd)
            #po.wait()
            #r = po.returncode
            if r != 0:
                self.logger.error('Cannot get dump_all.json')
                return False
            with open(tf_name, encoding='utf-8') as ifp:
                self.dumpall = json.load(ifp)
            return bool(self.dumpall)
        except Exception as e:
            msg = f'get_dump_all Error: {str(e)}'
            self.logger.error(msg)
        finally:
            if tf_name and os.path.exists(tf_name):
                os.remove(tf_name)

    # ==========================================================================
    def get_display_name(self, m_name, ver):
        if m_name not in self.dumpall:
            return "UnKnown Plugin"
        disp_name = "UnKnown Plugin"
        for dspec in self.dumpall[m_name]:
            disp_name = dspec['display_name']
            if ver == dspec['version']:
                return disp_name
        return f'{disp_name} no version {ver}'

    # ==========================================================================
    def get_list_from_repository(self):
        self.get_dump_all()
        self.report = {}
        url = 'https://pypi-official.argos-labs.com/packages/'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        for x in soup.find_all('a'):
            modname = x.text
            if not modname.startswith('argoslabs.'):
                continue
            pi_name, pi_version, *rests = modname.split('-')
            if pi_name not in self.report:
                self.report[pi_name] = dict()
            if pi_version not in self.report[pi_name]:
                self.report[pi_name][pi_version] = {
                    'active_bot': 0,
                    'access_count': 0,
                }
        # pprint.pprint(self.report, width=200)

    # ==========================================================================
    def get_access_token(self):
        headers = {
            'Authorization': 'Basic YXJnb3MtYXBpOjc4Jiphcmdvcy1hcGkhQDEy',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'grant_type': 'client_credentials',
        }
        rp = requests.post('https://oauth-rpa.argos-labs.com/oauth/token',
                           headers=headers, data=data, verify=False)
        if rp.status_code // 10 != 20:
            msg = f'Cannot get access token, response code is {rp.status_code}: {rp.text}'
            self.logger.error(msg)
            raise IOError(msg)
        # print(rp.text)
        rj = json.loads(rp.text)
        self.logger.info('Getting access token was successful')
        return rj['access_token']

    # ==========================================================================
    def get_usage_report(self, access_token):
        # 호출한 시점에서 마지막 7일간의 통계정보를 가져
        headers = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'Authorization': f'Bearer {access_token}',
            'DNT': '1',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Origin': 'https://admin-rpa.argos-labs.com',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://admin-rpa.argos-labs.com/',
            'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
        }
        data = {
            "queryId": "of_plugin_weekly_by_version",
            "conditionMap": [],
        }
        rp = requests.post('https://api-rpa.argos-labs.com/report/v1/any_sql/query',
                           headers=headers, json=data, verify=False)
        if rp.status_code // 10 != 20:
            msg = f'Cannot get report, response code is {rp.status_code}: {rp.text}'
            self.logger.error(msg)
            raise IOError(msg)
        # print(rp.text)
        rj = json.loads(rp.text)
        # pprint.pprint(rj)
        return rj

    # ==========================================================================
    def get_report_from_rj(self, rj):
        self.get_list_from_repository()
        # report has this structure
        # {
        #     'argoslabs.data.binaryop': {
        #         '1.22.333': {
        #             'active_bot': 230,
        #             'access_count': 1687,
        #         },
        #         ...
        #     },
        #     ...
        # }
        for row in rj['data']:
            if row['plugin_name'] not in self.report:
                self.report[row['plugin_name']] = dict()
            vdict = self.report[row['plugin_name']]
            if row['plugin_version'] not in vdict:
                vdict[row['plugin_version']] = {
                    'active_bot': 0,
                    'access_count': 0,
                }
            adict = vdict[row['plugin_version']]
            adict['active_bot'] += row['active_bot']
            adict['access_count'] += row['access_count']
        # pprint.pprint(self.report, width=200)
        rows = list()
        #rows.append((
        #    'plugin_name', 'version', 'active_bot', 'access_count'
        #))
        for pi_name, pi_dict in self.report.items():
            for version, adict in pi_dict.items():
                rows.append([
                    pi_name,
                    version,
                    adict['active_bot'],
                    adict['access_count'],
                ])
        self.rows = rows
        # pprint.pprint(self.rows, width=200)

    # ==========================================================================
    def get_report(self, get_not_used=False, sort_index=2, _reversed=True):
        at = self.get_access_token()
        rj = self.get_usage_report(at)
        self.get_report_from_rj(rj)
        if not self.rows:
            return list()
        # fltering
        for i in range(len(self.rows)-1, -1, -1):
            not_used = False
            if self.rows[i][2] == 0 and self.rows[i][3] == 0:
                not_used = True
            if get_not_used and not not_used:
                del self.rows[i]
            #if not get_not_used and not_used:
            #    del self.rows[i]
        # sorting
        #if not isinstance(sort_index, (tuple, list)):
        #    sort_index = [sort_index]
        #for j in range(len(sort_index)-1, -1, -1):
        #    if not (0 <= j <= 3):
        #        continue
        #    #sorted(self.rows, key=itemgetter(j))
        #    self.rows.sort(key=itemgetter(j))
        self.rows.sort(key=itemgetter(sort_index))
        if _reversed:
            self.rows.reverse()
        cw = csv.writer(sys.stdout, lineterminator='\n')
        cw.writerow((
            'display_name', 'plugin_name', 'version', 'active_bot', 'access_count'
        ))
        for row in self.rows:
            d_name = self.get_display_name(row[0], row[1])
            row.insert(0, d_name)
            cw.writerow(row)


################################################################################
if __name__ == '__main__':
    logger = logging.getLogger('PluginReport')
    pr = PluginReport(logger=logger)

    #print(f'{"="*100}')
    #pr.get_report()

    #print(f'{"="*100}')
    #pr.get_report(sort_index=0, _reversed=False)

    print(f'{"="*100}')
    pr.get_report(
        #get_not_used=True,
        sort_index=3, _reversed=True
    )
