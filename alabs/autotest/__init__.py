"""
====================================
 :mod:alabs.autotest
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
automatic testing for plugins
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2020/04/23]
#     - _do_cmd 에서 stdout 결과를 가져오는데
#       cp949' codec can't encode character '\u5b66' in position 9: illegal multibyte sequence
#     - set PYTHONIOENCODING=UTF-8
#  * [2020/04/21]
#     - 통계 확인 및 OP-AUTOTEST 에 매일 0시 적용
#  * [2020/03/12]
#     - stat email
#  * [2020/03/05]
#     - Delete APScheduler
#     - crontab 또는 윈도우 스케줄러를 이용하도록 함
#  * [2020/01/24]
#     - change Scheduler => APScheduler
#  * [2020/01/04]
#     - demploy to alabs.autotest
#  * [2020/12/14]
#     - Starting

################################################################################
import os
import sys
import csv
import yaml
import json
# import time
import shutil
# import argparse
import pathlib
# import logging
# import urllib3
import requests
import datetime
import traceback
import subprocess
from bs4 import BeautifulSoup
from operator import itemgetter
from tempfile import NamedTemporaryFile
from io import StringIO
from tempfile import gettempdir, TemporaryFile
from alabs.common.util.vvlogger import get_logger
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
#from apscheduler.schedulers.gbackground import BlockingScheduler
from alabs.ppm import _main as ppm_main
from requests.packages.urllib3.exceptions import InsecureRequestWarning


################################################################################
class PluginReport(object):
    DUMP_ALL = "https://pypi-official.argos-labs.com/data/plugin-static-files/dumpspec-def-all.json"
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    # ==========================================================================
    def __init__(self, statdir, logger):
        self.statdir = statdir
        self.logger = logger
        self.report = {}
        # for result filenames
        self.stat_ver_f = None
        self.stat_gbn_f = None
        self.stat_gnu_f = None
        # 결과 rows
        self.rows = []
        self.gbn_rows = []
        self.gnu_rows = []
        # for getting display_name
        self.dumpall = None
        # for report
        self.contents = []

    # ==========================================================================
    def _error(self, msg):
        msg = msg.strip()
        sys.stderr.write('[ERROR]:' + msg + '\n')
        self.logger.error(msg)
        self.contents.append(f'[{datetime.datetime.now().strftime("%Y%m%d %H%M%S")}] ERROR: {msg}')

    # ==========================================================================
    def _info(self, msg):
        sys.stdout.write('[INFO]:' + msg + '\n')
        self.logger.info(msg.strip())
        self.contents.append(f'[{datetime.datetime.now().strftime("%Y%m%d %H%M%S")}] INFO: {msg}')

    # ==========================================================================
    def _debug(self, msg):
        msg = msg.strip()
        sys.stdout.write('[DEBUG]:' + msg + '\n')
        self.logger.debug(msg)
        self.contents.append(f'[{datetime.datetime.now().strftime("%Y%m%d %H%M%S")}] DEBUG: {msg}')

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
            r = ppm_main(cmd)
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
    def get_display_name(self, m_name, ver=None):
        if m_name not in self.dumpall:
            return "UnKnown Plugin"
        disp_name = "UnKnown Plugin"
        for dspec in self.dumpall[m_name]:
            disp_name = dspec['display_name']
            if ver is None:  # 만약 버전을 지정하지 않으면 무조건 첫번째 disp_name
                return disp_name
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
            self._error(msg)
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
    def get_report(self, s_ts):
        try:
            self._info('Starting Usage Statistics...')

            stat_fn = f'alabs-plugins-usage-ver-{s_ts.strftime("%Y%m%d-%H%M")}.csv'
            self.stat_ver_f = os.path.join(self.statdir, stat_fn)
            stat_fn = f'alabs-plugins-usage-gbn-{s_ts.strftime("%Y%m%d-%H%M")}.csv'
            self.stat_gbn_f = os.path.join(self.statdir, stat_fn)
            stat_fn = f'alabs-plugins-usage-gnu-{s_ts.strftime("%Y%m%d-%H%M")}.csv'
            self.stat_gnu_f = os.path.join(self.statdir, stat_fn)

            # get_not_used = False
            # sort_index = 2
            _reversed = True
            # group_by_name=False
            at = self.get_access_token()
            rj = self.get_usage_report(at)
            self.get_report_from_rj(rj)
            if not self.rows:
                return list()
            # get not used
            from copy import deepcopy
            self.gnu_rows = deepcopy(self.rows)
            for i in range(len(self.gnu_rows)-1, -1, -1):
                not_used = False
                if self.gnu_rows[i][2] == 0 and self.gnu_rows[i][3] == 0:
                    not_used = True
                if not not_used:
                    del self.gnu_rows[i]
            # sorting
            #if not isinstance(sort_index, (tuple, list)):
            #    sort_index = [sort_index]
            #for j in range(len(sort_index)-1, -1, -1):
            #    if not (0 <= j <= 3):
            #        continue
            #    #sorted(self.rows, key=itemgetter(j))
            #    self.rows.sort(key=itemgetter(j))

            # for group_by_name
            gbn = {}
            for row in self.rows:
                if row[0] not in gbn:
                    gbn[row[0]] = (0, 0)
                gbn[row[0]] = (gbn[row[0]][0] + int(row[2]), gbn[row[0]][1] + int(row[3]))
            gbn_rows = list()
            for pn, cnt_t in gbn.items():
                gbn_rows.append([pn, cnt_t[0], cnt_t[1]])
            self.gbn_rows = gbn_rows
            self.gbn_rows.sort(key=itemgetter(2))
            self.gbn_rows.reverse()

            for row in self.rows:
                row[2] = int(row[2])
                row[3] = int(row[3])

            self.rows.sort(key=itemgetter(3))
            self.rows.reverse()

            # 1) 버전별 사용 카운트 저장
            with open(self.stat_ver_f, 'w', encoding='utf-8') as ofp:
                cw = csv.writer(ofp, lineterminator='\n')
                cw.writerow((
                    'display_name', 'plugin_name', 'version', 'active_bot', 'access_count'
                ))
                for row in self.rows:
                    d_name = self.get_display_name(row[0], row[1])
                    row.insert(0, d_name)
                    cw.writerow(row)
            self._info(f'Statistics for version by version usage: {os.path.basename(self.stat_ver_f)}')

            # 2) 그룹별 카운트 저장
            with open(self.stat_gbn_f, 'w', encoding='utf-8') as ofp:
                cw = csv.writer(ofp, lineterminator='\n')
                cw.writerow((
                    'display_name', 'plugin_name', 'active_bot', 'access_count'
                ))
                for row in self.gbn_rows:
                    d_name = self.get_display_name(row[0])
                    row.insert(0, d_name)
                    cw.writerow(row)
            self._info(f'Statistics for group by name usage: {os.path.basename(self.stat_gbn_f)}')

            # 3) 사용되지 않은 카운트 저장
            with open(self.stat_gnu_f, 'w', encoding='utf-8') as ofp:
                cw = csv.writer(ofp, lineterminator='\n')
                cw.writerow((
                    'display_name', 'plugin_name', 'version', 'active_bot', 'access_count'
                ))
                for row in self.gnu_rows:
                    d_name = self.get_display_name(row[0], row[1])
                    row.insert(0, d_name)
                    cw.writerow(row)
            self._info(f'Statistics for Not used plugins: {os.path.basename(self.stat_gnu_f)}')
        except Exception as e:
            exc_info = sys.exc_info()
            out = traceback.format_exception(*exc_info)
            del exc_info
            msg = '%s\n' % ''.join(out)
            self._error(msg)
            msg = 'get_report Error: %s' % str(e)
            self._error(msg)


################################################################################
class AutoTest(object):
    # ==========================================================================
    @staticmethod
    def conf_substitute(conf_s):
        conf_s = conf_s.replace('{{gettempdir}}', gettempdir())
        conf_s = conf_s.replace('{{home}}', str(pathlib.Path.home()))
        return conf_s

    # ==========================================================================
    def __init__(self, args):
        self.args = args
        conf_f = args.conf
        _filter = args.filter
        if not _filter:
            _filter = list()
        if getattr(sys, 'frozen', False):
            g_dir = os.path.abspath(sys._MEIPASS)
            c_dir = os.path.abspath(os.path.dirname(sys.executable))
            # print('pdir=%s, cdir=%s' % (g_dir, c_dir))
        else:
            g_dir = c_dir = os.path.abspath(os.path.dirname(__file__))
        self.g_dir = g_dir
        if not conf_f:
            conf_f = 'autotest.yaml'
        if not os.path.exists(conf_f):
            raise IOError(f'Cannot read conf file "{conf_f}"')
        with open(conf_f, encoding='utf-8') as ifp:
            conf_s = ifp.read()
        conf_s = self.conf_substitute(conf_s)
        conf_sio = StringIO(conf_s)
        self.conf = yaml.load(conf_sio, yaml.FullLoader)
        self.filter = _filter
        # for internal
        self.logger = get_logger(self.conf['environment']['log'])
        self.logger.info('Starting AutoTest object...')
        self.report = None
        self._init_report()

    # ==========================================================================
    def _init_report(self):
        if self.args.stat:
            subject = 'Getting statistics for Plugin usage'
        else:
            subject = 'Automatic Plugin Test'
        self.report = {
            'subject': subject,
            'contents': [],
            'summary': [],
        }

    # ==========================================================================
    def _summary(self, msg):
        msg = msg.strip()
        self.report['summary'].append(f'{msg}')

    # ==========================================================================
    def _error(self, msg):
        msg = msg.strip()
        sys.stderr.write('[ERROR]:' + msg + '\n')
        self.logger.error(msg)
        self.report['contents'].append(f'[{datetime.datetime.now().strftime("%Y%m%d %H%M%S")}] ERROR: {msg}')

    # ==========================================================================
    def _info(self, msg):
        sys.stdout.write('[INFO]:' + msg + '\n')
        self.logger.info(msg.strip())
        self.report['contents'].append(f'[{datetime.datetime.now().strftime("%Y%m%d %H%M%S")}] INFO: {msg}')

    # ==========================================================================
    def _debug(self, msg):
        msg = msg.strip()
        sys.stdout.write('[DEBUG]:' + msg + '\n')
        self.logger.debug(msg)
        self.report['contents'].append(f'[{datetime.datetime.now().strftime("%Y%m%d %H%M%S")}] DEBUG: {msg}')

    # ==========================================================================
    def _do_cmd(self, cmd):
        f_out = TemporaryFile()
        f_err = TemporaryFile()
        try:
            # print(os.environ.get('_OLD_VIRTUAL_PATH'))
            # print(os.environ.get('VIRTUAL_ENV'))
            # del os.environ['_OLD_VIRTUAL_PATH']
            # del os.environ['VIRTUAL_ENV']
            po = subprocess.Popen(cmd, stdout=f_out, stderr=f_err, env=os.environ)
            po.wait()
            rc = po.returncode
            f_out.seek(0)
            f_err.seek(0)
            s_out = f_out.read().decode('utf-8')
            s_err = f_err.read().decode('utf-8')
            if rc != 0:
                raise RuntimeError(f'Cmd="{" ".join(cmd)}" returns {rc}\n'
                                   f'stdout="{s_out}"\nstderr="{s_err}"')
            self._info(f'Cmd="{" ".join(cmd)}" returns {rc}\n'
                       f'stdout="{s_out}"\nstderr="{s_err}"')
            return s_out
        finally:
            f_out.close()
            f_err.close()

    # ==========================================================================
    def make_venv(self):
        # Error: Command '['C:\\Users\\mcchae\\autotest.venv\\Scripts\\python.exe',
        #   '-Im', 'ensurepip', '--upgrade', '--default-pip']' returned non-zero exit status 1
        # so use without-pip
        cmd = [
            self.conf['environment']['virtualenv']['py3'],
            '-m', 'venv',
            self.conf['environment']['virtualenv']['dir'],
            '--without-pip',
        ]
        self._do_cmd(cmd)

        venv_py = os.path.join(self.conf['environment']['virtualenv']['dir'],
                               'Scripts', 'python.exe')
        get_pip = os.path.join(self.g_dir, 'get-pip.py')
        cmd = [
            venv_py,
            get_pip
        ]
        self._do_cmd(cmd)

    # ==========================================================================
    def pip_install_plugin(self, plugin, version=None):
        venv_pip = os.path.join(self.conf['environment']['virtualenv']['dir'],
                                'Scripts', 'pip.exe')
        cmd = [
            venv_pip,
            'install',
            '-i', 'https://pypi-official.argos-labs.com/simple',
            plugin,
        ]
        if version:
            cmd.append(f'=={version}')
        self._do_cmd(cmd)

    # ==========================================================================
    def prepare_venv(self, is_clear=False):
        venv_dir = self.conf['environment']['virtualenv']['dir']
        self._info(f'\n[venv]{"=" * 80}\nvenv dir="{venv_dir}"')
        if is_clear and os.path.exists(venv_dir):
            self._info(f'removing venv dir="{venv_dir}"')
            shutil.rmtree(venv_dir)
        # venv_py_f = os.path.join(venv_dir, 'Scripts', 'python.exe')
        if not os.path.exists(venv_dir):
            # making venv
            self._info(f'making venv dir="{venv_dir}"')
            self.make_venv()
        self._info(f'\n[install reporting module]{"=" * 80}')
        self.pip_install_plugin(self.conf['report']['email']['plugin'])

    # ==========================================================================
    def do_test(self, ndx, test):
        ver_str = test["version"] if test["version"] else 'latest'
        s_title = f'[{test["plugin"]}:{ver_str}] "{test["name"]}"'
        s_ts = datetime.datetime.now()
        try:
            self._info(f'\n\n[{ndx+1}th]{"="*80}\nTesting "{test["name"]}", '
                       f'plugin="{test["plugin"]}", version="{ver_str}"')
            self.pip_install_plugin(test['plugin'], test['version'])
            cmd = test['cmd']
            cmd[0] = os.path.join(self.conf['environment']['virtualenv']['dir'],
                                  'Scripts', cmd[0])
            stdout = self._do_cmd(cmd)
            stdout_json = test.get('stdout_json', False)
            if stdout_json:
                js = json.loads(stdout)
            br = eval(test['assert_true'], globals(), locals())
            if br:
                self._info(f'Checking for result "{test["assert_true"]}" is OK')
                self._summary(f'{s_title} passed')
            else:
                self._info(f'Checking for result "{test["assert_true"]}" is NOK!')
                self._summary(f'{s_title} NOT passed')
            return br
        except Exception as err:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self._error('implicitly_wait Error: %s\n' % str(err))
            self._error('%s\n' % ''.join(_out))
            self._summary(f'{s_title} got Exception!')
            return False
        finally:
            e_ts = datetime.datetime.now()
            self._info(f'\nTesting ended and it takes {e_ts - s_ts}')

    # ==========================================================================
    def email_report_tests(self, s_ts, e_ts, succ_cnt, fail_cnt):
        total_cnt = succ_cnt + fail_cnt
        email_f = os.path.join(gettempdir(), 'autotest.report.txt')
        with open(email_f, 'w', encoding='utf-8') as ofp:
            ofp.write(f'This testing started at {s_ts} and ended at {e_ts},\n'
                      f'it took {e_ts - s_ts}\n\n')
            ofp.write(f'Total {total_cnt} plugins and falied {fail_cnt}\n\n\n')
            for i, s in enumerate(self.report['summary']):
                ofp.write(f'[{i+1}/{total_cnt}] {s}\n')
            ofp.write(f'\n\n\n{"*" * 100}\n')
            ofp.write('\n'.join(self.report['contents']))
        cmd = [
            os.path.join(self.conf['environment']['virtualenv']['dir'],
                         'Scripts', self.conf['report']['email']['plugin']),
            self.conf['report']['email']['server'],
            self.conf['report']['email']['user'],
            self.conf['report']['email']['passwd'],
            f'[{s_ts.strftime("%Y%m%d %H%M%S")}~{e_ts.strftime("%Y%m%d %H%M%S")}]'
            f' {self.report["subject"]} {fail_cnt} fails out of {total_cnt}',
            '--body-file', email_f,
        ]
        for i, to in enumerate(self.conf['report']['email']['to']):
            if i < 1:
                cmd.extend(['--to', to])
            # else:
            #     cmd.extend(['--cc', to])
        self._do_cmd(cmd)

    # ==========================================================================
    def do_tests(self):
        s_ts = datetime.datetime.now()
        self._init_report()
        self.prepare_venv(is_clear=self.args.clear_venv)
        succ_cnt = fail_cnt = 0
        if self.filter:
            tests = list()
            for t in self.conf.get('tests', []):
                b_found = False
                for f in self.filter:
                    if t['name'].find(f) >= 0:
                        b_found = True
                        break
                if b_found:
                    tests.append(t)
        else:
            tests = self.conf.get('tests', [])
        for i, test in enumerate(tests):
            br = self.do_test(i, test)
            if br:
                succ_cnt += 1
            else:
                fail_cnt += 1
        e_ts = datetime.datetime.now()
        self.email_report_tests(s_ts, e_ts, succ_cnt, fail_cnt)

    # ==========================================================================
    def email_report_stats(self, s_ts, e_ts, pr):
        self.report['contents'].extend(pr.contents)
        email_f = os.path.join(gettempdir(), 'autotest.report.txt')
        with open(email_f, 'w', encoding='utf-8') as ofp:
            ofp.write(f'This testing started at {s_ts} and ended at {e_ts},\n'
                      f'it took {e_ts - s_ts}\n\n')
            ofp.write(f'{"*" * 100}\n')
            ofp.write('\n'.join(self.report['contents']))
        cmd = [
            os.path.join(self.conf['environment']['virtualenv']['dir'],
                         'Scripts', self.conf['report']['email']['plugin']),
            self.conf['report']['email']['server'],
            self.conf['report']['email']['user'],
            self.conf['report']['email']['passwd'],
            f'[{s_ts.strftime("%Y%m%d %H%M%S")}~{e_ts.strftime("%Y%m%d %H%M%S")}]'
            f' {self.report["subject"]} for {s_ts.strftime("%Y%m%d-%H%M")}',
            '--body-file', email_f,
        ]
        for i, to in enumerate(self.conf['report']['email']['to']):
            cmd.extend(['--to', to])
        cmd.extend(['--attachments', pr.stat_ver_f])
        cmd.extend(['--attachments', pr.stat_gbn_f])
        cmd.extend(['--attachments', pr.stat_gnu_f])
        self._do_cmd(cmd)

    # ==========================================================================
    def do_stats(self):
        s_ts = datetime.datetime.now()
        self._init_report()
        self.prepare_venv(is_clear=self.args.clear_venv)

        statdir = self.conf['environment']['statdir']
        if not os.path.exists(statdir):
            os.makedirs(statdir)

        pr = PluginReport(statdir, logger=self.logger)
        pr.get_report(s_ts)

        e_ts = datetime.datetime.now()
        self.email_report_stats(s_ts, e_ts, pr)

    # ==========================================================================
    def do(self):
        if self.args.stat:
            return self.do_stats()
        return self.do_tests()


################################################################################
def _main(*args):
    with ModuleContext(
        owner='ARGOS-LABS',
        group='alabs',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Argos Icon',
        icon_path=get_icon_path(__file__),
        description='alabs.autotest util for automatic plugin testing',
    ) as mcxt:
        mcxt.add_argument('--conf', '-c',
                          help='set config file, default is "autotest.yaml"')
        mcxt.add_argument('--filter', '-f', action='append',
                          help='Only matching contains this string for the name')
        mcxt.add_argument('--clear-venv', action='store_true',
                          help='If this flag is set clear VirtualEnv before testing')
        mcxt.add_argument('--stat', '-s', action='store_true',
                          help='If this flag is set getting the statistics of plugin usage count')
        argspec = mcxt.parse_args(args)

        os.environ['PYTHONIOENCODING'] = 'UTF-8'
        at = AutoTest(argspec)
        at.do()
        return 0


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass

