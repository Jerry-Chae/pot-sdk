"""
====================================
 :mod:alabs.ppm ARGOS-LABS Plugin Module Manager
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: VIVANS
"""

# 관련 작업자
# ===========
#
# 본 모듈은 다음과 같은 사람들이 관여했습니다:
#  * 채문창
#
# 작업일지
# --------
#
# 다음과 같은 작업 사항이 있었습니다:
#  * [2021/05/27]
#   - 암호로 다운로드하는 private repository 에 대한 pip 처리
#  * [2021/02/06]
#   - setup.py 에서 PipSession 의 경우 20 이상 되는 것 체크하는 코드 추가
#   - setup.py 에서 req, requirement attr 문제 코드 넣음
#  * [2021/02/06]
#   - for Linux porting
#  * [2021/01/25]
#   - idna==2.7 install
#     ERROR: Could not find a version that satisfies the requirement idna<3,>=2.5 (from requests->alabs.ppm) (from versions: 3.1)
#     ERROR: No matching distribution found for idna<3,>=2.5 (from requests->alabs.ppm)
#  * [2020/10/21]
#   - tests 폴더가 없으면 __main__.py 생성하는 체크 코드 추가
#   - setup.yaml 파일을 디폴트로 wheel 파일에 포함
#  * [2020/09/07]
#   - plugin venv-clean 명령 추가
#   - _append_indices 로 PPM에서 Invalid 한 플러그인 저장소는 제외하도록 함
#  * [2020/08/10]
#   - pandas2 플러그인을 설치하는데 오류가 발생하는데 모든 open 시 utf-8 옵션 추가
#  * [2020/07/08]
#   - setup.yaml 에 install_requires 항목이 있으면 이를 추가하도록 함
#   - argoslabs.check.env 에서 screeninfo 모듈을 소스째 가져오다 보니 필요
#  * [2020/06/20~]
#   - selftest 기능 추가
#  * [2020/06/16]
#   - on_premise 인 경우에만 --index 그 외에는 --extra-index-url 를 하도록 함
#  * [2020/04/06]
#   - plugin unique 명령 추가
#  * [2020/03/21]
#   - YAML_PATH 파일이 없을 경우 upload 에서 오류 수정 (default 설정 저장)
#   - upload 에서 서버 암호 잘못 입력한 경우 체크 오류 수정
#  * [2020/03/18]
#   - requests.get 등에서 verity=False 로 가져오도록 함 (NCSoft On-Premise 문제)
#  * [2020/02/26]
#   - get version 명령을 주면 setup.yaml 에 있는 버전 가져오도록 설정
#  * [2020/02/25]
#   - plugin 명령에 --without-cache 옵션을 추가하여 서버에서 캐쉬 없이 결과를
#     가져오도록 함 (work woth 조성은)
#   - 조팀 요청에 따라 --plugin-index 추가
#  * [2020/02/21]
#   - %homepath%\.argos-rpa-config.yaml 설정파일 이용
#   - 기존 %homepath%\.argos-rpa.conf 는 이용하지 않도록 함
#   - 기존 ppm.config 는 임시 사용으로만 사용
#   - submit / upload 해야함
#  * [2020/02/19]
#   - STU 시작 시 속도개선 시작
#  * [2019/12/12]
#   - 아래의 --on-premise 인 경우 pypi.org 를 접속하려고 시도
#  * [2019/12/12]
#   - --on-premise 별도 옵션 추가 (for HCL only)
#     - STU 에서 호출
#       - --on-premise --self-upgrade plugin dumpspec --official-only --last-only --user {0} --user-auth \"Bearer {1}\""
#       - --on-premise --self-upgrade plugin dumpspec --private-only --last-only --user {0} --user-auth \"Bearer {1}\""
#  * [2019/12/11]
#   - on-premise에서 인터넷 연결 시 문제 수정
#  * [2019/12/06]
#   - on-premise에 적응하도록 수정 (도메인의 호스트 명에 -hcl 붙인 것들 확인)
#   - 정확히 일치하는 버전의 플러그인 없으면 최신 버전을 설치하도록 수정
#  * [2019/12/04]
#   - offline 저장소를 만들려다 보니 argoslabs.* 만 플러그인으로 가져오도록 함 _list_modules
#  * [2019/09/03]
#   - argos-pbtail.exe 상태 표시창 추가 (win32)
#  * [2019/08/28]
#   - STU & PAM에서 사용할 기본 상태파일 마련 : HOME/.argos-rpa.sta
#  * [2019/08/26]
#   - ppm exe로 만들어 테스트 하기: for STU & PAM
#  * [2019/08/08]
#   - argoslabs.time.workanlendar 같은 경우 ephem 모듈은 C컴파일러가 필요하므로
#     prebuilt 버전이 필요함. 이에 따라 로컬에 가져온 다음 필요에 따라
#     requirements.txt를 미리 설치하도록 함
#  * [2019/08/06]
#   - PAM 이 맥주소를 넘길 수 있도록 --pam-id 추가
#  * [2019/07/29]
#   - upload 시 user 및 암호 받아오기
#  * [2019/07/27]
#   - --self-upgrade 체크 속도 개선
#  * [2019/07/25]
#   - POT 속도개선 작업
#  * [2019/06/25]
#   - venv의 Popen 결과를 Thread, Queue로 해결
#  * [2019/06/20]
#   - venv의 Popen 결과를 line by line 으로 가져와서 처리
#  * [2019/05/28]
#   - ppm self upgrade on startup (--self-upgrade option)
#   - dumppi 명령 추가 (--dumppi-folder 옵션)
#  * [2019/05/27]
#   - submit 별도 구축 및 테스트
#   - 설정에 버전 넣고 지정
#   - plugin versions 명령은 해당 플러그인 들만 가져오도록 수정해야함
#   - pypiuploader를 이용하여 https용 pypiserver에 업로드
#  * [2019/05/17]
#   - python 3.6.3 에서 setuptools 를 최신 것으로 update 해야하는 상황 발생
#  * [2019/05/2?]
#   - python 3.6.3 에서 setuptools 를 최신 것으로 update 해야하는 상황 발생
#  * [2019/05/04]
#   - 특정 plugin의 버전목록 구하기 기능 추가
#  * [2019/05/01]
#   - 사용자 별 dumpspec 기능 추가
#  * [2019/04/29]
#   - plugin venv command 추가
#   - plugin command 에서 버전 목록을 가장 최신 버전부터 소팅
#  * [2019/04/24]
#   - plugin commands 추가
#  * [2019/04/22]
#   - dumpspec.json 을 alabs.ppm build 에서 wheel을 만들기 전에 포함되도록
#   - 이후 해당 dumpspec을 가져오는 것은
#     pip download argoslabs.terminal.sshexp --index http://pypi.argos-labs.com:8080 --trusted-host=pypi.argos-labs.com --dest=C:\tmp\pkg --no-deps
#     pip download argoslabs.demo.helloworld==1.327.1731 --index http://pypi.argos-labs.com:8080 --trusted-host=pypi.argos-labs.com --dest=C:\tmp\pkg --no-deps
#     위의 명령어로 해당 패키지만 다운받아 unzip 하여 dumpspec.json 을 추출하여 특정 dumpspec.json 뽑도록
#  * [2019/04/03]
#   - check empty 'private-repositories'
#  * [2019/03/27]
#   - search 에서는 --extra-index-url 등이 지원 안되는 문제
#  * [2019/03/22~2019/03/26]
#   - PPM.do 에서 return 값을 실제 프로세스 returncode를 리턴 0-정상
#   - submit 에서 upload 서버로 올림
#  * [2019/03/20]
#   - .argos-rpa.conf 애 private-repositories 목록 추가
#   - 기존 register => submit 변경
#  * [2019/03/06]
#   - dumpspec 추가
#  * [2019/03/05]
#   - add package_data
#  * [2018/11/28]
#   - Linux 테스트 OK
#  * [2018/11/27]
#   - 윈도우 테스트 OK
#  * [2018/10/31]
#   - 본 모듈 작업 시작
################################################################################
import os
import sys
import ssl
# noinspection PyPackageRequirements
import yaml
import glob
import copy
import json
import time
# noinspection PyUnresolvedReferences
import venv       # for making venv in pyinstaller
import shutil
import hashlib
# noinspection PyPackageRequirements
import chardet
import logging
import zipfile
# noinspection PyPackageRequirements
import requests
import argparse
import datetime
import tempfile
import traceback
import subprocess
import requirements
import pkg_resources
# noinspection PyPackageRequirements
import urllib3
import urllib.request
import urllib.parse
# noinspection PyUnresolvedReferences
import setuptools
# noinspection PyUnresolvedReferences,PyPackageRequirements,PyProtectedMember
# from pip._internal import main as pipmain
# from random import randint
from threading import Thread
from queue import Queue, Empty
# noinspection PyPackageRequirements
from bs4 import BeautifulSoup
from alabs.common.util.vvjson import get_xpath
from alabs.common.util.vvlogger import get_logger
from alabs.common.util.vvupdown import SimpleDownUpload
from alabs.common.util.vvnet import is_svc_opeded
from alabs.ppm.pypiuploader.commands import main as pu_main
from functools import cmp_to_key
from getpass import getpass
from pathlib import Path
from contextlib import closing

import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# noinspection PyProtectedMember,PyUnresolvedReferences
from email.utils import formatdate, COMMASPACE
from alabs.common.util.vvencoding import get_file_encoding

from tempfile import gettempdir
if '%s.%s' % (sys.version_info.major, sys.version_info.minor) < '3.3':
    raise EnvironmentError('Python Version must greater then "3.3" '
                           'which support venv')
else:
    from urllib.parse import urlparse, quote
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


################################################################################
class EMailSend(object):
    # ==========================================================================
    def __init__(self, server, user, passwd,
                 to, subject,
                 cc=None, bcc=None,
                 body_text=None, body_file=None, body_type=None,
                 attachments=None,
                 port=0, use_ssl=True, use_tls=False,
                 logger=None):
        self.server = server
        self.user = user
        self.passwd = passwd
        self.to = to if to else []
        self.subject = subject
        self.cc = cc if cc else []
        self.bcc = bcc if bcc else []
        self.body_text = body_text
        self.body_file = body_file
        self.body_type = body_type
        self.attachments = attachments if attachments else []
        self.port = port
        self.use_ssl = use_ssl
        self.use_tls = use_tls
        self.logger = logger
        # for internal
        self.sm = None
        self.open()

    # ==========================================================================
    def __del__(self):
        self.close()

    # ==========================================================================
    def __enter__(self):
        return self

    # ==========================================================================
    # noinspection PyShadowingBuiltins
    def __exit__(self, *args):
        self.close()

    # ==========================================================================
    def open(self):
        if self.use_ssl:
            if not self.port:
                self.port = 465
            self.sm = smtplib.SMTP_SSL(self.server, self.port)
        else:
            if self.use_tls:
                if not self.port:
                    self.port = 587
                self.sm = smtplib.SMTP(self.server, self.port)
                self.sm.starttls()
            else:
                if not self.port:
                    self.port = 25
                self.sm = smtplib.SMTP(self.server, self.port)
        self.sm.login(self.user, self.passwd)

    # ==========================================================================
    def close(self):
        if self.sm is not None:
            self.sm.close()
            # self.sm.quit()
            self.sm = None

    # ==========================================================================
    def check_valid(self):
        if not self.to:
            raise RuntimeError('One or more recepient needed with --to option!')
        if self.body_type not in ('text', 'html'):
            raise RuntimeError('Invalid type of Email body "%s"' % self.body_type)
        if not self.logger:
            raise RuntimeError('Invalid logger')

    # ==========================================================================
    def send(self):
        self.check_valid()
        # necessary mimey stuff
        msg = MIMEMultipart()
        msg.preamble = 'This is a multi-part message in MIME format.\n'
        msg.epilogue = ''
        msg['From'] = self.user
        msg['To'] = COMMASPACE.join(self.to)
        msg['Cc'] = COMMASPACE.join(self.cc)
        msg['Bcc'] = COMMASPACE.join(self.bcc)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = self.subject
        msg_body = MIMEMultipart('alternative')
        body_type = 'html' if self.body_type == 'html' else 'plain'
        body = self.body_text
        if body:
            msg_body.attach(MIMEText(body, body_type))
        if self.body_file:
            if not os.path.exists(self.body_file):
                raise RuntimeError('Cannot find --body-file "%s"' % self.body_file)
            encoding = get_file_encoding(self.body_file)
            with open(self.body_file, encoding=encoding) as ifp:
                body = ifp.read()
        if not body:
            raise RuntimeError('Invalid body, please set --body-text or --body-file')
        msg_body.attach(MIMEText(body, body_type))
        msg.attach(msg_body)
        receiver = self.to + self.cc + self.bcc
        for f in self.attachments:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=os.path.basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
            msg.attach(part)
        # self.sm.set_debuglevel(1)
        r = self.sm.sendmail(self.user, receiver, msg.as_string())
        if r:
            self.logger.error('Email send error: %s' % r)
        else:
            print('OK')
        return not bool(r)


################################################################################
def send_email(**kwargs):
    # kwargs = {
    #     'server': args.server,
    #     'user': args.user,
    #     'passwd': args.passwd,
    #     'to': args.to,
    #     'cc': args.cc,
    #     'bcc': args.bcc,
    #     'subject': args.subject,
    #     'body_text': args.body_text,
    #     'body_file': args.body_file,
    #     'body_type': args.body_type,
    #     'attachments': args.attachments,
    #     'port': args.port,
    #     'use_ssl': not args.no_use_ssl,
    #     'use_tls': args.use_tls,
    #     'logger': mcxt.logger,
    # }
    with EMailSend(**kwargs) as sm:
        r = sm.send()
    return 0 if r else 1


################################################################################
YAML_NAME = '.argos-rpa-config.yaml'
YAML_PATH = os.path.join(str(Path.home()), YAML_NAME)
YAML_CONFIG = """# Default Service config
- WebServiceHost: https://manager-rpa.argos-labs.com
  FileServiceHost: https://manager-rpa.argos-labs.com
  ImageServiceHost: api.rpa.argos-labs.com:8080
  OnDemandResultWebServer: rpa.argos-labs.com
  LoginPageHost: https://rpa.argos-labs.com/clear.html
  UpdateUrl: http://patch-rpa.argos-labs.com/Patch/SSUpdateNew/SS.yaml
  HostAlias: RPA
  alabsPpmHost: https://pypi-official.argos-labs.com/pypi"""
LOG_NAME = '.argos-rpa.log'
LOG_PATH = os.path.join(str(Path.home()), LOG_NAME)
OUT_NAME = '.argos-rpa.out'
OUT_PATH = os.path.join(str(Path.home()), OUT_NAME)
ERR_NAME = '.argos-rpa.err'
ERR_PATH = os.path.join(str(Path.home()), ERR_NAME)
pbtail_po = None


################################################################################
__all__ = ['main']

# _conf_version_list = [
#     '1.1'
# ]
# _conf_last_version = _conf_version_list[-1]
# _conf_contents_dict = {
#     _conf_last_version: """
# ---
# version: "{last_version}"
#
# repository:
#   url: https://pypi-official.argos-labs.com/pypi
#   req: https://pypi-req.argos-labs.com
# private-repositories:
# """.format(last_version=_conf_last_version)
#     # - name: pypi-test
#     #  url: https://pypi-test.argos-labs.com/simple
#     #  username: user
#     #  password: pass
# }
# _conf_last_contents = _conf_contents_dict[_conf_last_version]

g_path = os.environ['PATH']


################################################################################
class DownloadInstallError(Exception):
    pass


################################################################################
class PythonError(Exception):
    pass


################################################################################
class StatLogger(object):
    # ==========================================================================
    STA_NAME = '.argos-rpa.sta'
    STA_PATH = os.path.join(str(Path.home()), STA_NAME)
    ERR_NAME = '.argos-rpa.err'
    ERR_PATH = os.path.join(str(Path.home()), ERR_NAME)
    # ==========================================================================
    LT_1 = 1
    LT_2 = 2
    LT_3 = 3

    # ==========================================================================
    def clear(self):
        for f in glob.glob(self.STA_PATH):
            os.remove(f)
        for f in glob.glob('%s.*' % self.STA_PATH):
            os.remove(f)
        if os.path.exists(self.ERR_PATH):
            os.remove(self.ERR_PATH)

    # ==========================================================================
    def __init__(self, is_clear=False):
        if is_clear:
            self.clear()

    # ==========================================================================
    def __add__(self, other):
        self.log(*other)

    # ==========================================================================
    def log(self, level, msg, is_append=True):
        for _ in range(3):
            # noinspection PyBroadException
            try:
                with open(self.STA_PATH, 'a', encoding='utf-8') as ofp:
                    ofp.write('[%s:%s] %s\n' %
                              (datetime.datetime.now().strftime('%Y%m%d %H%M%S'), level, msg))
                    ofp.flush()
                break
            except Exception:
                time.sleep(0.1)
        om = 'a' if is_append else 'w'
        if level <= 0:
            level = 1
        elif level > 3:
            level = 3
        for _ in range(3):
            # noinspection PyBroadException
            try:
                with open('%s.%s' % (self.STA_PATH, level), om, encoding='utf-8') as ofp:
                    ofp.write('%s\n' % msg)
                    ofp.flush()
                break
            except Exception:
                time.sleep(0.1)

    # ==========================================================================
    def error(self, msg):
        with open(self.STA_PATH, 'a', encoding='utf-8') as ofp:
            ofp.write('[%s:E] %s\n' %
                      (datetime.datetime.now().strftime('%Y%m%d %H%M%S'), msg))
            ofp.flush()
        with open(self.ERR_PATH, 'a', encoding='utf-8') as ofp:
            ofp.write('[%s] %s\n' %
                      (datetime.datetime.now().strftime('%Y%m%d %H%M%S'), msg))
            ofp.flush()


################################################################################
def ver_compare(a, b):
    a_eles = a.split('.')
    b_eles = b.split('.')
    max_len = max(len(a_eles), len(b_eles))
    for i in range(max_len):
        if i >= len(a_eles):    # a='1.2', b='1.2.3' 인 경우 a < b
            return -1
        elif i >= len(b_eles):  # a='1.2.3', b='1.2' 인 경우 a > b
            return 1
        if int(a_eles[i]) > int(b_eles[i]):
            return 1
        elif int(a_eles[i]) < int(b_eles[i]):
            return -1
    return 0


################################################################################
def version_compare(a, b):
    return ver_compare(a['version'], b['version'])


################################################################################
def plugin_version_compare(a, b):
    return ver_compare(a['plugin_version'], b['plugin_version'])


################################################################################
class ArgumentParser(argparse.ArgumentParser):
    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, sys.stderr)
            raise RuntimeWarning('ArgumentParser Exit: %s', message)
        # else:
        #     raise RuntimeWarning('ArgumentParser Exit')


################################################################################
def set_venv(g_dir):
    os.environ['VIRTUAL_ENV'] = g_dir
    os.environ['PATH'] = os.path.join(g_dir, r'Scripts') + ';' + g_path
    # sys.stderr.write('setuptools.__file__=%s\n' % setuptools.__file__)
    # sys.stderr.write('sys.path=%s\n' % sys.path)
    # sys.stderr.write('os.environ["PATH"]=%s\n' % os.environ['PATH'])
    os.environ['PYTHONPATH'] = g_dir + r'\Lib\site-packages'
    pw = os.path.join(g_dir, r'Scripts\python.exe')
    sys.executable = pw
    sys.path = [
        g_dir,
        g_dir + '\\lib\\site-packages',
        g_dir + '\\lib\\site-packages\\win32',
        g_dir + '\\lib\\site-packages\\win32\\lib',
        g_dir + '\\lib\\site-packages\\Pythonwin',
    ]
    return True


################################################################################
# noinspection PyProtectedMember
class VEnv(object):
    # ==========================================================================
    def __init__(self, args, root='py.%s' % sys.platform, logger=None):
        self.args = args
        # home 폴더 아래에 py.win32, py.darwin, py.linux 처럼 만듦
        if os.path.basename(root) == root:  # basename만 왔을 경우 ~/ HOME 아래에
            self.root = os.path.join(str(Path.home()), root)
        else:
            self.root = root
        self.use = args.venv
        if logger is None:
            logger = get_logger(LOG_PATH)
        self.logger = logger
        # for internal
        self.py = None
        self.check_environments()
        self.sta = StatLogger()

    # ==========================================================================
    def check_python(self):
        pyver = '%s.%s' % (sys.version_info.major, sys.version_info.minor)
        if pyver < '3.3':
            msg = 'Python Version must greater then "3.3" but "%s"' % pyver
            self.logger.error(msg)
            raise EnvironmentError(msg)
        self.logger.debug('VEnv.check_python: python version is "%s"' % pyver)
        return 0

    # ==========================================================================
    def check_environments(self):
        self.check_python()

    # ==========================================================================
    def clear(self):
        if os.path.isdir(self.root):
            shutil.rmtree(self.root)
        self.logger.debug('VEnv.clear: "%s" is removed' % self.root)
        return 0

    # ==========================================================================
    def _upgrade(self, ndx_param=None, is_common=True, is_ppm=True):
        if not any((is_common, is_ppm)):
            return 9
        rl = list()
        rl.append(self.venv_pip('install', '--upgrade', 'pip'))
        rl.append(self.venv_pip('install', '--upgrade', 'setuptools'))
        if not ndx_param:
            ndx_param = list()
        if is_common:
            rl.append(self.venv_pip('install', '--upgrade', 'alabs.common', *ndx_param))
        if is_ppm:
            rl.append(self.venv_pip('install', '--upgrade', 'alabs.ppm', *ndx_param))
        return 1 if any(rl) else 0

    # ==========================================================================
    # noinspection PyUnresolvedReferences
    def make_venv(self, isdelete=True):
        if not self.use:
            return 9
        if os.path.isdir(self.root) and isdelete:
            shutil.rmtree(self.root)

        self.logger.info("Now making venv %s ..." % self.root)
        if getattr(sys, 'frozen', False):
            shutil.copytree(os.path.join(os.path.abspath(sys._MEIPASS), 'venv'), self.root)
            set_venv(self.root)
            return 0
        cmd = [
            '"%s"' % os.path.abspath(sys.executable),
            '-m',
            'venv',
            '"%s"' % self.root  # 아래의 shell=True 때문에 ""를 주었음
        ]
        self.logger.info("venv: cmd='%s'" % ' '.join(cmd))
        # python -m venv ... 명령은 shell 에서 해야 정상 동작함
        with open(OUT_PATH, 'w', encoding='utf-8') as out_fp, \
                open(ERR_PATH, 'w', encoding='utf-8') as err_fp:
            po = subprocess.Popen(' '.join(cmd), shell=True,
                                  stdout=out_fp, stderr=err_fp)
            po.wait()

        if po.returncode != 0:
            msg = 'VEnv.make_venv: making venv %s: error %s' % \
                  (' '.join(cmd), po.returncode)
            self.logger.error(msg)
            raise RuntimeError(msg)
        self.logger.info("making venv %s success!" % self.root)
        return 0

    # ==========================================================================
    def check_venv(self):
        if not self.use:
            py = os.path.abspath(sys.executable)
            self.py = py
            self.logger.debug('VEnv.check_venv: use=%s, py=%s' % (self.use, self.py))
            return py

        if not os.path.isdir(self.root):
            self.make_venv()
        if sys.platform == 'win32':
            py = os.path.abspath(os.path.join(self.root, 'Scripts', 'python.exe'))
        else:
            py = os.path.abspath(os.path.join(self.root, 'bin', 'python'))
        if not os.path.exists(py):
            msg = 'VEnv.check_venv: Cannot find python "%s"' % py
            self.logger.error(msg)
            raise RuntimeError(msg)
        self.py = py
        self.logger.debug(
            'VEnv.check_venv: use=%s, py=%s' % (self.use, self.py))
        return py

    # ==========================================================================
    def get_venv(self):
        return self.check_venv()

    # ==========================================================================
    @staticmethod
    def enqueue_stdout(out, queue):
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()

    # ==========================================================================
    @staticmethod
    def enqueue_stderr(err, queue):
        for line in iter(err.readline, b''):
            queue.put(line)
        err.close()

    # ==========================================================================
    def get_line_str(self, line):
        try:
            if not line:
                return ""
            line = line.decode("utf-8").rstrip()
        except UnicodeDecodeError:
            cd = chardet.detect(line)
            if not (cd and 'encoding' in cd):
                return ""
            line = line.decode(cd['encoding']).rstrip()
        except Exception as err:
            self.logger.error('get_line_str: Error: %s' % str(err))
            raise
        return line

    # ==========================================================================
    def do_stdout(self, line, kwargs, out_fp):
        if not line:
            return
        line = self.get_line_str(line)
        if kwargs['getstdout']:
            print(line)
        out_fp.write('%s\n' % line)
        self.logger.debug('VEnv.venv_py: %s' % line)
        if self.sta is None:
            self.sta = StatLogger()
        self.sta.log(StatLogger.LT_3, line)

    # ==========================================================================
    def do_stderr(self, line, kwargs, err_fp):
        if not line:
            return
        line = self.get_line_str(line)
        if kwargs['getstdout']:
            sys.stderr.write('%s\n' % line)
        err_fp.write('%s\n' % line)
        if line.startswith('You are using pip version') or line.startswith('You should consider upgrading via the'):
            self.logger.debug('VEnv.venv_py: %s' % line)
        else:
            self.logger.error('VEnv.venv_py: %s' % line)

    # ==========================================================================
    def venv_py(self, *args, **kwargs):
        tmpdir = None
        stdin_ifp = None
        try:
            if 'raise_error' not in kwargs:
                kwargs['raise_error'] = False
            if 'getstdout' not in kwargs:
                kwargs['getstdout'] = False
            if 'outfile' not in kwargs:
                kwargs['outfile'] = None
            cmd = [
                self.get_venv(),
            ]
            cmd += args
            # 다음과 같이 따옴표를 붙였는데 안되는 PC 있어서 위에 줄로 원복
            # for arg in args:
            #     if arg.lower().startswith('c:\\'):
            #         arg = '"%s"' % arg
            #     cmd.append(arg)
            self.logger.debug('VEnv.venv_py: cmd="%s"' % ' '.join(cmd))
            # Windows의 python.exe -m 등의 명령어가 shell 모드에서 정상 동작함

            tmpdir = tempfile.mkdtemp(prefix='venv_py_')
            out_path = os.path.join(tmpdir, 'stdout.txt')
            err_path = os.path.join(tmpdir, 'stderr.txt')
            self.logger.debug('VEnv.venv_py: cmd="%s"' % ' '.join(cmd))
            with open(out_path, 'w', encoding='utf-8') as out_fp, \
                    open(err_path, 'w', encoding='utf-8') as err_fp:
                # po = subprocess.Popen(' '.join(cmd), shell=True,
                #                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # private repository 저장소 구현을 위하여 잘못된 user 암호를 넣은 경우
                # User for ...? 라고 물어보는 것을 그냥 지나기 위하여 stdin 을 처리
                if 'pip' in args:
                    stdin_f = os.path.join(gettempdir(), 'alabs_ppm_pip_stdin.txt')
                    with open(stdin_f, 'w') as ofp:
                        ofp.write('\n')
                    stdin_ifp = open(stdin_f)
                    po = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                          stdin=stdin_ifp)
                else:
                    po = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                q_out, q_err = Queue(), Queue()
                t_out = Thread(target=self.enqueue_stdout, args=(po.stdout, q_out))
                t_out.daemon = True  # thread dies with the program
                t_out.start()
                t_err = Thread(target=self.enqueue_stderr, args=(po.stderr, q_err))
                t_err.daemon = True  # thread dies with the program
                t_err.start()

                # while po.poll() is None:
                while po.poll() is None:
                    try:
                        line = q_out.get_nowait()
                        self.do_stdout(line, kwargs, out_fp)
                    except Empty:
                        pass
                    try:
                        line = q_err.get_nowait()  # or q.get(timeout=.1)
                        self.do_stderr(line, kwargs, err_fp)
                    except Empty:
                        pass
                    time.sleep(0.1)

                while not q_out.empty():
                    line = q_out.get()
                    self.do_stdout(line, kwargs, out_fp)
                while not q_err.empty():
                    line = q_err.get()  # or q.get(timeout=.1)
                    self.do_stderr(line, kwargs, err_fp)

                t_out.join()
                t_err.join()

            if kwargs['outfile']:
                shutil.copy2(out_path, kwargs['outfile'])
            if po.returncode != 0 and kwargs['raise_error']:
                msg = 'VEnv.venv_py: venv command "%s": error %s' % (' '.join(cmd), po.returncode)
                self.logger.error(msg)
                raise PythonError(msg)
            self.logger.debug('VEnv.venv_py: returncode="%s"' % po.returncode)
            return po.returncode
        finally:
            if tmpdir and os.path.exists(tmpdir):
                shutil.rmtree(tmpdir)
            if stdin_ifp is not None:
                stdin_ifp.close()

    # ==========================================================================
    def venv_pip(self, *args, **kwargs):
        # self.logger.debug('venv_pip: self.py="%s"' % self.py)
        # self.logger.debug('venv_pip: sys.executable="%s"' % sys.executable)
        # self.logger.debug('venv_pip: sys.path=%s' % sys.path)
        # self.logger.debug('venv_pip: environ[PATH]="%s"' % os.environ['PATH'])
        # self.logger.debug('venv_pip: environ[PYTHONPATH]="%s"' % os.environ['PYTHONPATH'])

        # r = pipmain(list(args))
        msg_l = list(args[:2])
        if msg_l[-1].startswith('-') and len(args) > 2:
            msg_l.append(args[2])
        if len(msg_l) >= 2 and msg_l[-1].startswith(str(Path.home())):
            # noinspection PyBroadException
            try:
                msg_l[-1] = os.path.basename(msg_l[-1])
            except Exception:
                pass
        if msg_l[0] == 'freeze':
            msg_l[0] = 'finishing...'
        if self.sta is None:
            self.sta = StatLogger()
        self.sta.log(StatLogger.LT_2, ' '.join(msg_l))
        r = self.venv_py('-m', 'pip', *args, **kwargs)
        self.logger.debug('venv_pip: "%s" returns %s' % (' '.join(args), r))
        return r


################################################################################
# noinspection PyShadowingBuiltins,PyUnresolvedReferences,PyBroadException,PyPep8Naming
class PPM(object):
    # ==========================================================================
    BUILD_PKGS = [
        'wheel',
    ]
    UPLOAD_PKGS = [
        'twine',
    ]
    # PLUGIN_PKGS = [
    #     # 'pip2pi',
    #     # 'twine',    # for gTTS
    #     # 'zip',  # for dumppi
    #     # 'pbr',  # for dumppi
    # ]
    DUMPPI_PKGS = [
        'alabs.ppm',
        'twine',
        # 'zip',
        'pbr',
    ]
    CLASSIFIERS = [
        'Topic :: RPA',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        # for build date
        'Build :: Method :: alabs.ppm',
        'Build :: Date :: %s' %
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    ]
    DUMPSPEC_JSON = 'dumpspec.json'
    EXCLUDE_PKGS = ('alabs.ppm', 'alabs.common', 'alabs.icon')
    # ==========================================================================
    URL_OFFPI = [   # official plugin
        'https://pypi-official.argos-labs.com/pypi',
    ]
    URL_OAUTH = [
        'https://api-rpa.argos-labs.com/oauth2',
        'https://oauth-rpa.argos-labs.com',     # OLD
        # 'https://oauth-rpa-hcl.argos-labs.com',
    ]
    URL_API_CHIEF = [
        'https://api-rpa.argos-labs.com/api/chief',
        'https://api-chief.argos-labs.com',     # OLD
        # 'https://api-chief-hcl.argos-labs.com',
    ]
    URL_PLUGIN = [
        'https://pypi-official.argos-labs.com/data/plugin-static-files',
        'https://s3-us-west-2.amazonaws.com/rpa-file.argos-labs.com/plugins',  # OLD
    ]
    URL_DEF_DUMPSPEC = '%s/dumpspec-def-all.json'
    URL_MOD_VER = '%s/mod-ver-list.json'
    URL_DUMPSPEC = '%s/{plugin_name}-{version}-dumpspec.json'
    # ==========================================================================
    SELFTEST_ROOT = os.path.join(str(Path.home()), '.argos-rpa.test')

    # ==========================================================================
    @staticmethod
    def _is_url_valid(url):
        up = urlparse(url)
        nl = up.netloc
        if nl.find(':') > 0:
            host = urlparse(url).netloc.split(':')[0]
            port = urlparse(url).netloc.split(':')[1]
        else:
            host = nl
            port = 443 if up.scheme == 'https' else 80
        for _ in range(3):
            r = is_svc_opeded(host, int(port))
            if r:
                return r
            time.sleep(0.2)
        return False

    # ==========================================================================
    @staticmethod
    def _get_valid_url(urls):
        for url in urls:
            if PPM._is_url_valid(url):
                return url
        return None

    # ==========================================================================
    def _get_URL_OFFPI(self):
        if self.args.plugin_index:
            if self.args.plugin_index not in self.URL_OFFPI:
                self.URL_OFFPI.insert(0, self.args.plugin_index)
        if self.url_config and 'alabsPpmHost' in self.url_config and \
                self.url_config['alabsPpmHost'] and \
                self.url_config['alabsPpmHost'] not in self.URL_OFFPI:
            url = self.url_config['alabsPpmHost']
            self.URL_OFFPI.insert(0, url)
            self.logger.debug('Insert "%s" in self.URL_OFFPI %s' % (url, self.URL_OFFPI))
        r = self._get_valid_url(self.URL_OFFPI)
        if not r:
            raise RuntimeError('Cannot find valid URL for Official Plugin')
        return r

    # ==========================================================================
    def _get_URL_OAUTH(self):
        if self.url_config and 'oauthHost' in self.url_config and \
                self.url_config['oauthHost'] and \
                self.url_config['oauthHost'] not in self.URL_OAUTH:
            url = self.url_config['oauthHost']
            self.URL_OAUTH.insert(0, url)
            self.logger.debug('Insert "%s" in self.URL_OAUTH %s' % (url, self.URL_OAUTH))
        r = self._get_valid_url(self.URL_OAUTH)
        if not r:
            raise RuntimeError('Cannot find valid URL for OAUTH')
        return r

    # ==========================================================================
    def _get_URL_API_CHIEF(self):
        if self.url_config and 'oauthHost' in self.url_config and \
                self.url_config['oauthHost']:
            # 'https://api-rpa.argos-labs.com/oauth2' ==>
            # 'https://api-rpa.argos-labs.com/api/chief'  # by 조성은
            s = self.url_config['oauthHost']
            api_chief = '/'.join(s.split('/')[:-1]) + '/api/chief'
            if api_chief not in self.URL_API_CHIEF:
                url = api_chief
                self.URL_API_CHIEF.insert(0, url)
                self.logger.debug('Insert "%s" in self.URL_API_CHIEF %s' % (url, self.URL_API_CHIEF))
        r = self._get_valid_url(self.URL_API_CHIEF)
        if not r:
            raise RuntimeError("Cannot find valid URL for Supersivor's API")
        return r

    # ==========================================================================
    def _get_URL_PLUGIN(self):
        if self.args.plugin_index:
            if self.args.plugin_index not in self.URL_OFFPI:
                self.URL_OFFPI.insert(0, self.args.plugin_index)
        if self.url_config and 'alabsPpmHost' in self.url_config and \
                self.url_config['alabsPpmHost']:
            # 'https://pypi-official.argos-labs.com/pypi' ==>
            # 'https://pypi-official.argos-labs.com/data/plugin-static-files'
            s = self.url_config['alabsPpmHost']
            plugin_data = '/'.join(s.split('/')[:-1]) + '/data/plugin-static-files'
            if plugin_data not in self.URL_PLUGIN:
                url = plugin_data
                self.URL_PLUGIN.insert(0, url)
                self.logger.debug('Insert "%s" in self.URL_PLUGIN %s' % (url, self.URL_PLUGIN))
        r = self._get_valid_url(self.URL_PLUGIN)
        if not r:
            raise RuntimeError("Cannot find valid plugin data URL")
        return r

    # ==========================================================================
    def _is_on_premise(self):
        return self.args.on_premise
        # # 인터넷 연결과 상관없이 on-premise 인가 조사
        # r1 = self._get_valid_url(self.URL_OAUTH[1:])
        # r2 = self._get_valid_url(self.URL_API_CHIEF[1:])
        # return r1 and r2

    # ==========================================================================
    def __init__(self, _venv, args, logger=None, sta=None):
        self.venv = _venv
        self.args = args
        self.url_config = {}    # %homepath%\.argos-rpa-config.yaml (yaml)
        if not os.path.exists(YAML_PATH):
            with open(YAML_PATH, 'w', encoding='utf-8') as ofp:
                ofp.write(YAML_CONFIG)
        if os.path.exists(YAML_PATH):
            with open(YAML_PATH, encoding='utf-8') as ifp:
                if yaml.__version__ >= '5.1':
                    # noinspection PyUnresolvedReferences
                    yd = yaml.load(ifp, Loader=yaml.FullLoader)
                else:
                    yd = yaml.load(ifp)
                if yd and isinstance(yd, list):
                    self.url_config = yd[0]
        self.config = {}
        if logger is None:
            logger = get_logger(LOG_PATH)
        self.logger = logger
        if sta is None:
            sta = StatLogger()
        self.sta = sta
        # for internal
        self.pkgname = None
        self.pkgpath = None
        self.basepath = None
        self.setup_config = None
        self.indices = []
        self.ndx_param = []
        # Next are for POT speed-up
        self.mod_ver_list = None
        self.def_dumpspec = None
        self.ds_hash = None

    # ==========================================================================
    def _get_pkgname(self):
        # alabs.demo.helloworld 패키지를 설치하려고 하면, 해당 helloworld 폴더에
        # 들어가서 ppm 을 돌림
        if not os.path.exists('__init__.py'):
            # --venv 가 없는 경우도 있으므로 그냥 '.' 을 리턴
            # raise RuntimeError('Cannot find __init__.py file. Please run '
            #                    'ppm in python package folder')
            return '.'
        pkglist = []
        abspath = os.path.abspath('.')
        abs_list = abspath.split(os.path.sep)
        while True:
            if len(abs_list) <= 1:
                raise RuntimeError('PPM._get_pkgname: Cannot find package (__init__.py)')
            pkglist.append(abs_list[-1])
            abs_list = abs_list[0:-1]
            ppath = os.path.sep.join(abs_list)
            if not os.path.exists(os.path.join(ppath, '__init__.py')):
                self.basepath = ppath
                if self.args.venv:
                    os.chdir(ppath)
                break
        pkglist.reverse()
        return '.'.join(pkglist)

    # ==========================================================================
    def _check_pkg(self):
        self.pkgname = self._get_pkgname()
        self.pkgpath = self.pkgname.replace('.', os.path.sep)

        if self.args.venv and not os.path.exists(self.pkgpath):
            raise RuntimeError('PPM._check_pkg: Cannot find package path for "%s"' % self.pkgpath)
        if self.args.new_py:
            self.venv.make_venv()
        else:
            self.venv.check_venv()

    # ==========================================================================
    @staticmethod
    def _check_subargs(subargs):
        sa = subargs
        # subparser에서 REMAINER를 이용하면 첫번째 "-V" 과 같은 옵션이
        # 상위 옵션으로 먹히기 때문에 옵션부터 이용할 경우 pass 라고 줌
        if sa and sa[0] == 'pass':
            return sa[1:]
        return sa

    # ==========================================================================
    def _clear(self):
        c_cnt = 0
        f = '%s.%s' % (self.pkgname, 'egg-info')
        if os.path.exists(f):
            shutil.rmtree(f)
            c_cnt += 1
        f = 'build'
        if os.path.exists(f):
            shutil.rmtree(f)
            c_cnt += 1
        f = 'dist'
        if os.path.exists(f):
            shutil.rmtree(f)
            c_cnt += 1
        dl = [d for d in glob.glob('**/__pycache__', recursive=True) if
              not d.startswith('py.')]
        for d in dl:
            shutil.rmtree(d)
            c_cnt += 1
        gfl = ('setup.py', 'setup.py.log', 'setup.cfg')
        for gf in gfl:
            if os.path.exists(gf):
                os.unlink(gf)
                c_cnt += 1
        return 0 if c_cnt > 0 else 1

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _clear_py(self):
        return self.venv.clear()

    # ==========================================================================
    def _get_setup_config(self):
        yamlpath = os.path.join(self.pkgpath, 'setup.yaml')
        if not os.path.exists(yamlpath):
            raise IOError('PPM._get_setup_config: Cannot find "%s" for setup' % yamlpath)
        with open(yamlpath, encoding='utf-8') as ifp:
            if yaml.__version__ >= '5.1':
                # noinspection PyUnresolvedReferences
                yaml_config = yaml.load(ifp, Loader=yaml.FullLoader)
            else:
                yaml_config = yaml.load(ifp)
            if 'setup' not in yaml_config:
                raise RuntimeError('PPM._get_setup_config: "setup" attribute must be exists in setup.yaml')
            self.setup_config = yaml_config['setup']

    # ==========================================================================
    def _set_private_repositories(self, _prlist):
        prconfig = list()
        prlist = sorted(_prlist, key=lambda d: d['view_priority'])
        for prd in prlist:
            if not prd['is_activate']:
                continue
            prconfig.append({
                'name': prd['repo_name'],
                'url': prd['repo_url'],
                'username': prd['repo_user'],
                'password': prd['repo_pw'],
            })
        self.config['private-repositories'] = prconfig

    # ==========================================================================
    def _get_private_repositories(self):
        # /chief/repositories 로 사용하는 API를 /repositories 로 수정 요청 (조성은)
        # 아직은 서비스와 On-Premise 에 일치 문제 때문에 두 개 모두 테스트
        urls = (
                '%s/repositories' % self._get_URL_API_CHIEF(),
                '%s/chief/repositories' % self._get_URL_API_CHIEF(),
        )
        try:
            for url in urls:
                headers = {
                    'Accept': 'application/json',
                }
                if not self.args.pam_id:
                    headers['authorization'] = self.args.user_auth
                    r = requests.get(url, headers=headers, verify=False)
                    r_msg = f'_get_private_repositories:url="{url}", ' \
                            f'headers={headers} ' \
                            f'status_code={r.status_code}'
                else:
                    params = (
                        ('user_id', self.args.user),
                        ('pam_auth_key', self.args.user_auth),
                        ('pam_mac_address', self.args.pam_id),
                    )
                    # noinspection PyTypeChecker
                    r = requests.get(url, headers=headers, params=params, verify=False)
                    r_msg = f'_get_private_repositories:url="{url}", ' \
                            f'headers={headers}, params={params}, ' \
                            f'status_code={r.status_code}'
                self.logger.info(r_msg)
                if r.status_code // 10 == 20:
                    self._set_private_repositories(json.loads(r.text))
                    return True
            # noinspection PyUnboundLocalVariable
            msg = 'Get private plugin for user "%s" Error: API result is %s' \
                  % (self.args.user, r.status_code)
            sys.stderr.write('%s\n' % msg)
            self.logger.error(msg)
            return False
        except Exception as err:
            self.sta.log(StatLogger.LT_2, 'Error: to connect %s' % ' or '.join(urls))
            msg = '_get_private_repositories Error to connect "%s": \n%s\n' \
                  % (' or '.join(urls), str(err))
            sys.stderr.write(msg)
            self.logger.error(msg)
            return False

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _append_indices(self, url):
        o = urlparse(url)
        host = None
        port = None
        if o.netloc.find(':') >= 0:
            host, port = o.netloc.split(':', maxsplit=1)
        else:
            host = o.netloc
            if o.scheme.lower() == 'https':
                port = 443
            elif o.scheme.lower() == 'http':
                port = 80
            else:
                return False
        if is_svc_opeded(host, int(port)):
            self.indices.append(url)
            return True
        return False

    # ==========================================================================
    def _add_private_url(self, rep):
        url = rep.get('url')
        username = rep.get('username')
        password = rep.get('password')
        if not (username and password):
            self.ndx_param.append(url)
        else:
            up = urlparse(url)
            up_url = f'{up.scheme}://{quote(username)}:{quote(password)}@{up.netloc}{up.path}'
            self.ndx_param.append(up_url)

    # ==========================================================================
    def _get_indices(self):
        self.indices = []
        self.ndx_param = []

        self.sta.log(StatLogger.LT_2, 'Starting to get list of plugin repositories')
        url = self._get_URL_OFFPI()
        if not url:
            raise RuntimeError('PPM._get_indices: Invalid repository.url from %s' % YAML_NAME)
        self._append_indices(url)
        if self._is_on_premise():  # 2020
            self.ndx_param.append('--index')
        else:
            self.ndx_param.append('--extra-index-url')
        self.ndx_param.append(url)
        self.ndx_param.append('--trusted-host')
        self.ndx_param.append(self._get_host_from_index(url))
        pr = None
        # 2019.7.27 POT private plugin 정보를 API로 가져오도록 함
        is_pr = False
        if self.args.user and self.args.user_auth:
            is_pr = self._get_private_repositories()
        if not is_pr:
            return self.indices
        # 2019.12.06 : 만약 on-premise 처럼 API에서 못 가져오면 config에서
        # 가져오도록 아래를 타도록 위에 두 줄을 막음

        if 'private-repositories' in self.config:
            pr = self.config.get('private-repositories', [])
        if not pr:
            pr = []
        for rep in pr:
            url = rep.get('url')
            if not url:
                continue
            # 만약 위에 on premise 인 경우에는 indices가 비어 있으므로
            # 첫 번째를 --index 로 기술해 주어야 함 (2020.1.21)
            if not self._append_indices(url):
                continue
            if self._is_on_premise() and len(self.indices) == 1:
                self.ndx_param.append('--index-url')
            else:
                self.ndx_param.append('--extra-index-url')
            #  * [2021/05/27]
            #   - 암호로 다운로드하는 private repository 에 대한 pip 처리
            # self.ndx_param.append(url)
            self._add_private_url(rep)

            self.ndx_param.append('--trusted-host')
            self.ndx_param.append(self._get_host_from_index(url))
        self.logger.debug('PPM._get_indices: indices=%s, ndx_param=%s' %
                          (self.indices, self.ndx_param))
        self.sta.log(StatLogger.LT_3, 'Done to get list of plugin repositories')
        return self.indices

    # ==========================================================================
    @staticmethod
    def _get_host_from_index(url):
        return urlparse(url).netloc.split(':')[0]

    # ==========================================================================
    def _dumpspec(self):
        _ = self._install_requirements()
        dumpspec_file = os.path.join(self.pkgpath, self.DUMPSPEC_JSON)
        self.venv.venv_py('-m',
                          self.pkgname, '--dumpspec',
                          '--outfile', dumpspec_file,
                          getstdout=True)

    # ==========================================================================
    def _list_modules(self, startswith='argoslabs.',
                      official_only=False, private_only=False):
        # last_only 인 경우 마지막 버전 목록만 주도록 함
        modlist = list()
        moddict = {}
        for i, url in enumerate(self.indices):
            if i == 0 and private_only:
                continue
            if official_only and i > 0:
                break
            o = urlparse(url)
            web_url = '{scheme}://{netloc}/packages/'.format(scheme=o.scheme,
                                                             netloc=o.netloc)
            # noinspection PyProtectedMember
            context = ssl._create_unverified_context()
            with urllib.request.urlopen(web_url, context=context) as response:
                html = response.read()
                soup = BeautifulSoup(html, 'html.parser')
            for x in soup.find_all('a'):
                # pprint(x.text)
                # offline 저장소를 만들려다 보니 argoslabs.* 만 플러그인으로 가져오도록 함
                modname = x.text
                if not modname.startswith('argoslabs.'):
                    continue
                if startswith and not modname.startswith(startswith):
                    continue
                is_exclude = False
                for exc_pkg in self.EXCLUDE_PKGS:
                    if modname.startswith(exc_pkg):
                        is_exclude = True
                        break
                if is_exclude:
                    continue
                if modname not in modlist:
                    modlist.append(modname)
                if self.args.last_only:
                    dlist = modname.split('-')
                    if dlist[0] not in moddict:
                        moddict[dlist[0]] = modname
                    else:
                        plist = moddict[dlist[0]].split('-')
                        # 가장 최신 버전이면 덮어씀
                        if ver_compare(plist[1], dlist[1]) < 0:
                            moddict[dlist[0]] = modname
        if self.args.last_only:
            modlist = list(moddict.values())
        modlist.sort()
        return modlist

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _dumpspec_json_clear_cache(self):
        glob_filter = '%s%sdumpspec-*.json' % (tempfile.gettempdir(), os.path.sep)
        for f in glob.glob(glob_filter):
            os.remove(f)

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _dumpspec_json_save(self, modname, version, jd):
        jsfile = '%s%sdumpspec-%s-%s.json' % (tempfile.gettempdir(), os.path.sep, modname, version)
        if os.path.exists(jsfile):
            return False
        with open(jsfile, 'w', encoding='utf-8') as ofp:
            json.dump(jd, ofp)
        self.logger.debug('PPM._dumpspec_json_save: save dumpspec cache "%s"' % jsfile)
        return True

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _dumpspec_json_load(self, modname, version):
        jsfile = '%s%sdumpspec-%s-%s.json' % (tempfile.gettempdir(), os.path.sep, modname, version)
        if not os.path.exists(jsfile):
            return None
        with open(jsfile, encoding='utf-8') as ifp:
            r = json.load(ifp)
        self.logger.debug('PPM._dumpspec_json_load: load dumpspec from "%s"' % jsfile)
        return r

    # ==========================================================================
    def _get_dumpspec_hash(self):
        url_def_dumpspec = self.URL_DEF_DUMPSPEC % self._get_URL_PLUGIN()
        ds_hash_url = url_def_dumpspec[:-4] + 'hash'
        self.sta.log(StatLogger.LT_3, 'Get hash specification "%s"' %
                     ds_hash_url.split('/')[-1])
        # 우선 해쉬를 가져와서 해당 파일이 로컬에 저장되었나 확인
        r = requests.get(ds_hash_url, verify=False)
        if r.status_code // 10 == 20:
            self.ds_hash = r.content.decode()

    # ==========================================================================
    def _def_dumpspec_from_plugin(self):
        url_def_dumpspec = self.URL_DEF_DUMPSPEC % self._get_URL_PLUGIN()
        self.sta.log(StatLogger.LT_3, "Get dump specification from %s" %
                     url_def_dumpspec.split('/')[-1])
        if self.ds_hash:
            ds_file = '%s%sdumpspec-all-%s.json' % \
                      (tempfile.gettempdir(), os.path.sep, self.ds_hash)
            if os.path.exists(ds_file):
                with open(ds_file, encoding='utf-8') as ifp:
                    return json.load(ifp)
        # 캐쉬가 없으면 실제 json을 다운로드 하고
        r = requests.get(url_def_dumpspec, verify=False)
        if r.status_code // 10 != 20:
            self.sta.error("download %s error!" % url_def_dumpspec)
            raise RuntimeError('Cannot get "%s"' % url_def_dumpspec)
        self.sta.log(StatLogger.LT_3, "download %s" % url_def_dumpspec.split('/')[-1])
        rj = json.loads(r.content)
        # 캐쉬로 저장
        enc = hashlib.sha256()
        enc.update(r.content)
        self.ds_hash = ds_hash2 = enc.hexdigest()
        ds_file = '%s%sdumpspec-all-%s.json' % \
                  (tempfile.gettempdir(), os.path.sep, ds_hash2)
        with open(ds_file, 'w', encoding='utf-8') as ofp:
            json.dump(rj, ofp)
        return rj

    # ==========================================================================
    def _dumpspec_from_plugin(self, modname, version):
        if modname in self.def_dumpspec:
            for ds in self.def_dumpspec[modname]:
                if ds['plugin_version'] == version:
                    return ds
            self.logger.error('Found "%s" module but not version "%s" in self.def_dumpspec' % (modname, version))
        url_dumpspec = self.URL_DUMPSPEC % self._get_URL_PLUGIN()
        url = url_dumpspec.format(plugin_name=modname, version=version)
        r = requests.get(url, verify=False)
        if r.status_code // 10 != 20:
            self.sta.error("download %s error!" % url)
            raise RuntimeError('Cannot get "%s"' % url)
        self.sta.log(StatLogger.LT_3, "download %s" % url.split('/')[-1])
        return json.loads(r.content)

    # ==========================================================================
    def _mod_ver_list_from_plugin(self):
        try:
            if self.ds_hash:
                # 로컬 해쉬 값이 있으면 해당 값을 가져옴
                ds_file = '%s%smod-ver-list-%s.json' % \
                          (tempfile.gettempdir(), os.path.sep, self.ds_hash)
                if os.path.exists(ds_file):
                    with open(ds_file, encoding='utf-8') as ifp:
                        return json.load(ifp)
            url_mod_ver = self.URL_MOD_VER % self._get_URL_PLUGIN()
            self.sta.log(StatLogger.LT_2, "Downloading %s" % url_mod_ver.split('/')[-1])
            r = requests.get(url_mod_ver, verify=False)
            if r.status_code // 10 != 20:
                self.sta.error("download %s error!" % url_mod_ver)
                raise RuntimeError('Cannot get "%s"' % url_mod_ver)
            self.sta.log(StatLogger.LT_3, "Downloaded %s" % url_mod_ver.split('/')[-1])
            rj = json.loads(r.content)
            mvl = {}
            for md in rj['mod-ver-list']:
                mvl[md['name']] = md['versions']
            if self.ds_hash:
                # 로컬 해쉬 값으로 저장
                ds_file = '%s%smod-ver-list-%s.json' % \
                          (tempfile.gettempdir(), os.path.sep, self.ds_hash)
                with open(ds_file, 'w', encoding='utf-8') as ofp:
                    json.dump(mvl, ofp)
            return mvl
        except Exception:
            return {}

    # ==========================================================================
    def _find_last_version_from_mod_ver_list(self, modname):
        if not self.mod_ver_list:
            return None
        if modname not in self.mod_ver_list:
            return None
        return self.mod_ver_list[modname][0]   # descending order

    # ==========================================================================
    def _dumpspec_json(self, modname, version=None):
        # pip download argoslabs.demo.helloworld==1.327.1731
        # --index http://pypi.argos-labs.com:8080 --trusted-host=pypi.argos-labs.com
        # --dest=C:\tmp\pkg --no-deps
        if not version:
            log_msg = "Getting specifications for plugin %s" % modname
        else:
            log_msg = "Getting specifications for plugin %s with version %s" % (modname, version)
        self.sta.log(StatLogger.LT_3, log_msg)
        mname = modname
        if not version:
            version = self._find_last_version_from_mod_ver_list(modname)
        if version:
            # noinspection PyBroadException
            try:
                jd = self._dumpspec_json_load(modname, version)
                if jd is None:
                    jd = self._dumpspec_from_plugin(modname, version)
                    self._dumpspec_json_save(modname, version, jd)
                return jd
            except Exception:
                err_msg = 'Cannot get dumpspec for ("%s", "%s")' % (modname, version)
                self.sta.error(err_msg)
                self.logger.debug(err_msg)
            mname = '%s==%s' % (modname, version)
            jd = self._dumpspec_json_load(modname, version)
            if jd:
                return jd

        glob_filter = '%s%s%s-*.whl' % (tempfile.gettempdir(), os.path.sep, modname)
        for f in glob.glob(glob_filter):
            os.remove(f)
        self.venv.venv_pip('download', mname,
                           '--dest', tempfile.gettempdir(),
                           '--no-deps',
                           *self.ndx_param)
        mfilename = None
        for f in glob.glob(glob_filter):
            mfilename = f
            break
        if not mfilename:
            err_msg = 'PPM._dumpspec_json: Cannot get plugin wheel file "%s"' % mfilename
            self.sta.error(err_msg)
            raise RuntimeError(err_msg)
        eles = os.path.basename(mfilename).split('-')
        jd = self._dumpspec_json_load(eles[0], eles[1])
        if jd:
            return jd
        with zipfile.ZipFile(mfilename) as zf:
            dsj = modname.replace('.', '/') + '%s%s' % ('/', self.DUMPSPEC_JSON)
            with zf.open(dsj) as jfp:
                jd = json.load(jfp)
                self.logger.debug('PPM._dumpspec_json: get dumpspec.json from "%s"' % mfilename)
                self._dumpspec_json_save(eles[0], eles[1], jd)
                return jd

    # ==========================================================================
    def _dumpspec_user(self, tmpdir):
        # curl -X GET --header 'Accept: application/json'
        #   --header 'authorization: Bearer 312df8e2-b143-4d5e-8d77-f4c15fe2b911'
        #   'https://api-chief.argos-labs.com/plugin/api/v1.0/users/fjoker%40naver.com/plugins'
        # GET /plugin/api/v1.0/users/{user_id}/plugins
        # curl -X GET --header 'Accept: application/json' 'https://api-chief.argos-labs.com/plugin/api/v1.0/users/seonme%40vivans.net/plugins'
        msg = 'Try to dump plugin spec for user "%s"' % self.args.user
        sys.stdout.write('%s\n' % msg)
        self.logger.info(msg)
        url = '%s/plugin/api/v1.0/users/%s/plugins' \
              % (self._get_URL_API_CHIEF(),
                 quote(self.args.user))
        if not self.args.user_auth:
            raise RuntimeError('_dumpspec_user: --user-auth option must have a valid key')
        headers = {
            # 'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json',
            'authorization': self.args.user_auth,
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3',
        }
        r = requests.get(url, headers=headers, verify=False)
        if r.status_code // 10 != 20:
            msg = 'Dump plugin spec for user "%s" Error: API result is %s' % (self.args.user, r.status_code)
            sys.stderr.write('%s\n' % msg)
            self.logger.error(msg)
            self.sta.error('Error to get user dependent information. Please logout STU and login again.')
            raise RuntimeError('PPM._dumpspec_user: API Error!')
            # mdlist = [
            #     {'user_id': 'seonme@vivans.net', 'plugin_id': 'argoslabs.google.tts', 'plugin_version': '1.330.1500'},
            #     # {'user_id': 'seonme@vivans.net', 'plugin_id': 'argoslabs.api.rest', 'plugin_version': '1.315.1054'},
            #     {'user_id': 'seonme@vivans.net', 'plugin_id': 'argoslabs.api.rossum', 'plugin_version': '1.327.1355'},
            #     # {'user_id': 'seonme@vivans.net', 'plugin_id': 'argoslabs.data.excel', 'plugin_version': '1.425.1322'},
            #     {'user_id': 'seonme@vivans.net', 'plugin_id': 'argoslabs.data.json', 'plugin_version': '1.418.1631'},
            #     # {'user_id': 'seonme@vivans.net', 'plugin_id': 'argoslabs.data.rdb', 'plugin_version': '1.313.1857'},
            #     # {'user_id': 'seonme@vivans.net', 'plugin_id': 'argoslabs.filesystem.monitor', 'plugin_version': '1.424.1142'},
            #     {'user_id': 'seonme@vivans.net', 'plugin_id': 'argoslabs.filesystem.op', 'plugin_version': '1.418.1812'},
            #     # {'user_id': 'seonme@vivans.net', 'plugin_id': 'argoslabs.filesystem.op', 'plugin_version': '1.430.1418'},
            #     # {'user_id': 'seonme@vivans.net', 'plugin_id': 'argoslabs.terminal.sshexp', 'plugin_version': '1.415.1930'},
            # ]
        else:
            mdlist = json.loads(r.text)
            self.sta.log(StatLogger.LT_3, 'Getting %d plugins for the user' % len(mdlist))
        # print(md)
        if not self.args.private_only:
            req_txt = os.path.join(tmpdir, 'requirements.txt')
            with open(req_txt, 'w', encoding='utf-8') as ofp:
                for md in mdlist:
                    if 'plugin_name' in md:
                        if 'plugin_version' in md:
                            ofp.write('%s==%s\n' % (md['plugin_name'], md['plugin_version']))
                        else:
                            ofp.write('%s\n' % md['plugin_name'])
                    else:
                        self.logger.error('Chief API result for user plugin "%s" must have "plugin_name" key')
            self.args.requirements_txt = req_txt
            # self.args.user = None
        return True

    # ==========================================================================
    def _pre_requirements_install(self, new_venv, _tmpdir, whlfile, modname,
                                  prefix='argoslabs.'):
        self.logger.debug('_pre_requirements_install: new_venv="%s", _tmpdir="%s", whlfile="%s", modname="%s", prefix="%s"'
                          % (new_venv.root,  _tmpdir, whlfile, modname, prefix))
        with closing(zipfile.ZipFile(whlfile)) as zf:
            rqt = modname.replace('.', os.path.sep) + '%s%s' % (os.path.sep, 'requirements.txt')
            rqt_f = '%s%srequirements.txt' % (_tmpdir, os.path.sep)
            # 만약 whl 안에 requirements.txt 가 있다면 이를 먼저 설치
            # noinspection PyBroadException
            try:
                with zf.open(rqt) as ifp:
                    with open(rqt_f, 'w', encoding='utf-8') as ofp:
                        ofp.write(ifp.read().decode('utf-8'))
                r = new_venv.venv_pip('install', '-r', rqt_f, *self.ndx_param)
                if r != 0:
                    self.logger.error('_pre_requirements_install: '
                                      'install "%s" error!' % rqt_f)
            except Exception as err:
                # _exc_info = sys.exc_info()
                # _out = traceback.format_exception(*_exc_info)
                # del _exc_info
                # sys.stderr.write('_pre_requirements_install: %s\n' % ''.join(_out))
                self.logger.debug('_pre_requirements_install: '
                                  'install "%s" error: %s' % (rqt_f, str(err)))
            # 만약 whl 안에 whl 이 있다면 이를 직접 설치
            for info in zf.infolist():
                if info.filename.lower().endswith('.whl'):
                    zf.extract(info, _tmpdir)
                    wh_t = os.path.join(_tmpdir, info.filename)
                    if not os.path.exists(wh_t):
                        wh_t = os.path.join(_tmpdir, os.path.basename(info.filename))
                    if not os.path.exists(wh_t):
                        self.logger.error('_pre_requirements_install: '
                                          'extract "%s" from whl but fail to access' % info.filename)
                        r = 1
                    else:
                        r = new_venv.venv_pip('install', wh_t)
                    if r != 0:
                        self.logger.error('_pre_requirements_install: '
                                          'install "%s" error!' % wh_t)

        r = new_venv.venv_pip('install', whlfile, *self.ndx_param)
        return r

    # ==========================================================================
    def _download_module(self, new_venv, modname, op, version, _tmpdir):
        _cachedir = tempfile.gettempdir()
        if not (op and version):
            if modname in self.mod_ver_list:
                op = '=='
                version = self.mod_ver_list[modname][0]
        else:
            # todo: op가 > < 등 일 때 목록에서 체크
            ...
        b_found = False
        gl = glob.glob('%s/%s-%s-*.whl' % (_cachedir, modname, version))
        for f in gl:
            shutil.copy(f, _tmpdir)
            b_found = True
            break
        if not b_found:
            modspec = modname
            if op and version:
                modspec += '%s%s' % (op, version)
            _args = [
                'download', modspec,
                '--dest', _tmpdir,
                '--no-deps',
                *self.ndx_param
            ]
            r = new_venv.venv_pip(*_args)
            if r != 0:
                _msg = '_check_cache_download_and_install: Cannot pip download: cmd=%s' % ' '.join(_args)
                self.logger.error(_msg)
                raise RuntimeError(_msg)

    # ==========================================================================
    def _check_cache_download_and_install(self, new_venv, modname, op, version):
        self.logger.debug('_check_cache_download_and_install: new_venv="%s", modname="%s", op="%s", version="%s"'
                          % (new_venv.root, modname, op, version))
        _cachedir = tempfile.gettempdir()
        _tmpdir = tempfile.mkdtemp(prefix='down_install_')
        try:
            self._download_module(new_venv, modname, op, version, _tmpdir)
            gl = glob.glob('%s/%s-*.whl' % (_tmpdir, modname))
            gls = [f for f in gl]
            if gls:
                for f in gls:
                    r = self._pre_requirements_install(new_venv, _tmpdir, f, modname)
                    if r != 0:
                        self.logger.error('_check_cache_download_and_install: '
                                          'install "%s" error!' % f)
                    # noinspection PyBroadException
                    try:
                        bn = os.path.basename(f)
                        if not os.path.exists(os.path.join(_cachedir, bn)):
                            shutil.move(f, _cachedir)
                    except Exception:
                        self.logger.error('"%s" is exists in "%s"'
                                          % (os.path.basename(f), _cachedir))
                    return r
            # whl이 아닌 경우 그대로 설치하려고 노력 : 2019.12.12
            _args = [
                'install', modspec,
                *self.ndx_param
            ]
            r = new_venv.venv_pip(*_args)
            return r
        finally:
            if os.path.exists(_tmpdir):
                shutil.rmtree(_tmpdir)

    # ==========================================================================
    def _download_and_install(self, new_venv, requirements_txt):
        self.logger.debug('_download_and_install: new_venv="%s", requirements_txt="%s"'
                          % (new_venv.root, requirements_txt))
        r = -1
        _modspec = {}
        with open(requirements_txt, encoding='utf-8') as ifp:
            for req in requirements.parse(ifp):
                _modspec[req.name] = req.specs
        for modname, speclist in _modspec.items():
            if speclist:
                for op, ver in speclist:
                    r = self._check_cache_download_and_install(new_venv, modname, op, ver)
                    break
            else:
                # noinspection PyTypeChecker
                r = self._check_cache_download_and_install(new_venv, modname, None, None)
        return r

    # ==========================================================================
    def _get_venv(self, new_d):
        _tmpdir = None
        try:
            self.args.venv = True
            new_venv = VEnv(self.args, root=new_d, logger=self.logger)
            new_venv.check_venv()
            if self.args.requirements_txt:
                requirements_txt = self.args.requirements_txt
            else:
                _tmpdir = tempfile.mkdtemp(prefix='get_venv_')
                requirements_txt = os.path.join(_tmpdir, 'requirements.txt')
                with open(requirements_txt, 'w', encoding='utf-8') as ofp:
                    ofp.write('# pip dependent packages\n')
                    for pm in self.args.plugin_module:
                        ofp.write('%s\n' % pm)
            # r = new_venv.venv_pip('install', '-r', requirements_txt,
            #                       *self.ndx_param, getstdout=True)
            r = self._download_and_install(new_venv, requirements_txt)
            if r == 0:
                outfile = os.path.join(new_d, 'freeze.txt')
                new_venv.venv_pip('freeze', outfile=outfile, getstdout=True)
                freeze_d = {}
                with open(outfile, encoding='utf-8') as ifp:
                    for line in ifp:
                        eles = line.rstrip().split('==')
                        if len(eles) != 2:
                            raise RuntimeError('PPM._get_venv: freeze must module==version but "%s"' % line.rstrip())
                        freeze_d[eles[0].strip().lower()] = eles[1].strip()
                if os.path.exists(outfile):
                    os.remove(outfile)
                freeze_f = os.path.join(new_d, 'freeze.json')
                with open(freeze_f, 'w', encoding='utf-8') as ofp:
                    json.dump(freeze_d, ofp)
            else:
                raise DownloadInstallError('PPM._get_venv: r=%s, new_venv="%s", '
                                           'requirements_txt="%s" error'
                                           % (r, new_venv.root, requirements_txt))
            return r
        finally:
            if _tmpdir and os.path.exists(_tmpdir):
                shutil.rmtree(_tmpdir)

    # ==========================================================================
    def _get_modspec(self, tmpdir):
        """
docopt == 0.6.1             # Version Matching. Must be version 0.6.1
keyring >= 4.1.1            # Minimum version 4.1.1
coverage != 3.5             # Version Exclusion. Anything except version 3.5
Mopidy-Dirble ~= 1.1        # Compatible release. Same as >= 1.1, == 1.*
SomeProject
SomeProject == 1.3
SomeProject >=1.2,<2.0
SomeProject[foo, foo]
SomeProject~=1.4.2

Django [('>=', '1.11'), ('<', '1.12')]
six [('==', '1.10.0')]
        """
        requirements_txt = None
        try:
            modspec = {}
            requirements_txt = os.path.join(tmpdir, 'modspec.txt')
            if self.args.requirements_txt and os.path.exists(self.args.requirements_txt):
                shutil.copy(self.args.requirements_txt, requirements_txt)
            if self.args.plugin_module:
                with open(requirements_txt, 'a', encoding='utf-8') as ofp:
                    ofp.write('# plugin_module parameters\n')
                    for pm in self.args.plugin_module:
                        ofp.write('%s\n' % pm)
            if not os.path.exists(requirements_txt):
                return modspec
            with open(requirements_txt, encoding='utf-8') as ifp:
                for req in requirements.parse(ifp):
                    modspec[req.name.lower()] = req.specs
            return modspec
        finally:
            if requirements_txt and os.path.exists(requirements_txt):
                os.remove(requirements_txt)

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _is_conflict(self, freeze_d, modspec):
        for modname, speclist in modspec.items():
            if modname not in freeze_d:
                continue
            for op, ver in speclist:
                cmp = ver_compare(freeze_d[modname], ver)
                if op == '==':
                    if cmp != 0:
                        return True
                elif op == '>':
                    if cmp <= 0:
                        return True
                elif op == '>=':
                    if cmp < 0:
                        return True
                elif op == '<':
                    if cmp >= 0:
                        return True
                elif op == '<=':
                    if cmp > 0:
                        return True
                elif op == '~=':  # '>=' and '=='
                    f_v = '.'.join(freeze_d[modname].split('.')[:-1])
                    s_v = '.'.join(ver.split('.')[:-1])
                    cmp = ver_compare(f_v, s_v)
                    if cmp < 0:
                        return True
        return False

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _count_satisfy(self, freeze_d, modspec):
        match_cnt = 0
        for modname, speclist in modspec.items():
            if modname not in freeze_d:
                continue
            if not speclist:
                # 만약 모듈이름만 나왔다면 무조건 하나 매칭된다고 가정하자
                match_cnt += 1
            for op, ver in speclist:
                cmp = ver_compare(freeze_d[modname], ver)
                if op == '==':
                    if cmp == 0:
                        match_cnt += 1
                elif op == '>':
                    if cmp > 0:
                        match_cnt += 1
                elif op == '>=':
                    if cmp >= 0:
                        match_cnt += 1
                elif op == '<':
                    if cmp < 0:
                        match_cnt += 1
                elif op == '<=':
                    if cmp <= 0:
                        match_cnt += 1
                elif op == '~=':  # '>=' and '=='
                    f_v = '.'.join(freeze_d[modname].split('.')[:-1])
                    s_v = '.'.join(ver.split('.')[:-1])
                    cmp = ver_compare(f_v, s_v)
                    if cmp >= 0:
                        match_cnt += 1
        return match_cnt

    # ==========================================================================
    # def _cmd_modspec(self, moddict, modspec, version_attr='version'):  # 2020.02.20
    def _cmd_modspec(self, moddict, modspec, version_attr='plugin_version'):
        rd = {}
        if not modspec:  # all
            if self.args.last_only:
                for modname in moddict.keys():
                    rd[modname] = moddict[modname][0]  # 마지막 버전
                return rd
            return moddict
        for modname, speclist in modspec.items():
            if modname not in moddict:
                self.logger.error('plugin get command module "%s" does not exists in plugin list' % modname)
                continue
            if not speclist:
                # 만약 모듈이름만 나왔다면 무조건 최신 모듈
                rd[modname] = moddict[modname][0]  # 마지막 버전
                continue
            b_found = False
            for vdict in moddict[modname]:
                for op, ver in speclist:
                    if version_attr in vdict:
                        vdver = vdict[version_attr]
                    else:
                        vdver = vdict['version']
                    cmp = ver_compare(vdver, ver)
                    if op == '==':
                        if cmp == 0:
                            b_found = True
                    elif op == '>':
                        if cmp > 0:
                            b_found = True
                    elif op == '>=':
                        if cmp >= 0:
                            b_found = True
                    elif op == '<':
                        if cmp < 0:
                            b_found = True
                    elif op == '<=':
                        if cmp <= 0:
                            b_found = True
                    elif op == '~=':  # '>=' and '=='
                        f_v = '.'.join(vdict[version_attr].split('.')[:-1])
                        s_v = '.'.join(ver.split('.')[:-1])
                        cmp = ver_compare(f_v, s_v)
                        if cmp >= 0:
                            b_found = True
                    if b_found:
                        rd[modname] = vdict
                        break
                if b_found:
                    break
            if not b_found:
                self.logger.error('plugin get command module "%s" failed to find '
                                  'version spec %s' % (modname, str(speclist)))
        return rd

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _get_with_dumpspec(self, mod, d, modds):
        if mod not in modds:
            raise RuntimeError('Cannot get "%s" dumpspec from modds in _get_with_dumpspec' % mod)
        for ds in modds[mod]:
            if d['version'] == ds['plugin_version']:
                d['dumpspec'] = ds
                return True
        raise RuntimeError('Cannot find "%s" dumpspec from modds in _get_with_dumpspec' % mod)

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _get_saved_dumpspec(self, modlist):
        enc = hashlib.sha256()
        enc.update(str(modlist).encode('utf-8'))
        hexd = enc.hexdigest()
        modd_file = '%s%sdumpspec-%s.modd' % (tempfile.gettempdir(), os.path.sep, hexd)
        if not os.path.exists(modd_file):
            return {}, {}
        modds_file = '%s%sdumpspec-%s.modds' % (tempfile.gettempdir(), os.path.sep, hexd)
        if not os.path.exists(modds_file):
            return {}, {}
        with open(modd_file, encoding='utf-8') as ifp:
            modd = json.load(ifp)
        with open(modds_file, encoding='utf-8') as ifp:
            modds = json.load(ifp)
        return modd, modds

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _set_saved_dumpspec(self, modlist, modd, modds):
        enc = hashlib.sha256()
        enc.update(str(modlist).encode('utf-8'))
        hexd = enc.hexdigest()
        modd_file = '%s%sdumpspec-%s.modd' % (tempfile.gettempdir(), os.path.sep, hexd)
        with open(modd_file, 'w', encoding='utf-8') as ofp:
            json.dump(modd, ofp)
        modds_file = '%s%sdumpspec-%s.modds' % (tempfile.gettempdir(), os.path.sep, hexd)
        with open(modds_file, 'w', encoding='utf-8') as ofp:
            json.dump(modds, ofp)

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _clear_log(self):
        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
        for f in glob.glob(os.path.join(str(Path.home()), '.argos-rpa.log*')):
            os.remove(f)

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _zip_log(self, pkgname):
        nowstr = datetime.datetime.now().strftime('%Y%m%d_%H%M')
        zf_name = f'{pkgname}_{nowstr}.zip'
        zf_path = os.path.join(self.SELFTEST_ROOT, zf_name)
        with zipfile.ZipFile(zf_path, 'w') as zf:
            for f in glob.glob(os.path.join(str(Path.home()), '.argos-rpa.log*')):
                zf.write(f, compress_type=zipfile.ZIP_DEFLATED)
        return zf_path

    # ==========================================================================
    def _selftest_one(self, st_or, version=None, venv_dir=None):
        pkgname = st_or['pkgname']
        print(f'>>>"{st_or["display_name"]}({st_or["pkgname"]} {st_or["plugin_version"]})" testing... ')
        if not venv_dir:
            venv_dir = os.path.join(self.SELFTEST_ROOT, pkgname)
            # 만약 해당 폴더가 있다면 모두 지우고 시작
            if os.path.isdir(venv_dir):
                shutil.rmtree(venv_dir)
        try:
            self._clear_log()
            st_or['start_ts'] = datetime.datetime.now()
            self.args.plugin_module = [pkgname]
            # if not self.args.venv:
            #     # 새로운 가상환경을 만들기 위하여
            #     self.args.venv = True
            self._get_venv(venv_dir)
            st_or['install'] = 'passed'  # install test passed
            st_venv = VEnv(self.args, root=venv_dir, logger=self.logger)
            r = st_venv.venv_py('-m', f'{pkgname}.tests', raise_error=True)
            if r == 0:
                st_or['unittest'] = 'passed'  # unittest passed
            else:
                st_or['unittest'] = 'failed'  # install test failed
        except DownloadInstallError:
            st_or['install'] = 'failed'  # install test failed
        except PythonError:
            st_or['unittest'] = 'failed'  # install test failed
        except Exception as e:
            raise RuntimeError('Unexpected selftest error!')
        finally:
            if st_or['install'] == 'failed' or st_or['unittest'] == 'failed':
                st_or['zipped_log'] = self._zip_log(pkgname)
            st_or['end_ts'] = datetime.datetime.now()
            print(f'<<<install {st_or["install"]}, unittest {st_or["unittest"]} '
                  f'takes {st_or["end_ts"] - st_or["start_ts"]}')

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _get_public_ip_address(self):
        # noinspection PyBroadException
        rs = 'N/A'
        try:
            rp = requests.get('https://api.ipify.org')
            if rp.status_code // 10 == 20:
                rs = f'[{rp.text}]'
            else:
                rs = '[Invalid IP Address]'
        except Exception:
            rs = '[No Internet connecton]'
        finally:
            return rs

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def _report_selftest(self, st_r):
        pub_ip = self._get_public_ip_address()
        lines = [f'Self test from {pub_ip}', '']
        dnames = []
        attachments = []
        ceyaml = os.path.join(str(Path.home()), '.argos-rpa.test', '.check_env.yaml')
        if os.path.exists(ceyaml):
            attachments.append(ceyaml)
        for st_or in st_r:
            # if st_or["install"] == 'passed' and st_or["unittest"] == 'passed':
            #     continue
            dnames.append(f'"{st_or["display_name"]}"')
            lines.append(f'"{st_or["display_name"]}({st_or["pkgname"]} {st_or["plugin_version"]})" testing... '
                         f'install {st_or["install"]}, unittest {st_or["unittest"]} '
                         f'takes {st_or["end_ts"] - st_or["start_ts"]}')
            if st_or['zipped_log']:
                attachments.append(st_or['zipped_log'])
        to = ['plugin<plugin@argos-labs.com>']
        if self.args.selftest_email:
            to.append(self.args.selftest_email)
        dns = ','.join(dnames[:3])
        if len(dnames) > 3:
            dns += '...'
        subject = f'SelfTest {dns} from {pub_ip}'
        send_email(
            server='imap.gmail.com',
            user='plugin@argos-labs.com',
            passwd='argos0520',
            to=to,
            subject=subject,
            body_text='\n'.join(lines),
            body_type='text',
            attachments=attachments,
            logger=self.logger,
        )

    # ==========================================================================
    def _selftest(self, modds, modspec):
        self.sta.log(StatLogger.LT_2, "Self Testing for plugins")
        venv_dir = None
        if self.args.venv_dir:
            # 전체 하나의 venv에서 설치하고 테스트 하는 경우
            venv_dir = self.args.venv_dir
            # 만약 해당 폴더가 있다면 모두 지우고 시작
            if os.path.isdir(venv_dir):
                shutil.rmtree(venv_dir)
        ds = self._cmd_modspec(modds, modspec)
        if self.args.plugin_module:
            pms = self.args.plugin_module
        else:
            # for k, v in ds.items():
            #     self._selftest_one(k, v['plugin_version'], venv_dir)
            pms = list(ds.keys())
            # argoslabs.check.env 를 제일 먼저 호출하도록 함 (테스트 환경 정보 구하기)
            if 'argoslabs.check.env' in pms:
                pms.remove('argoslabs.check.env')
                pms.insert(0, 'argoslabs.check.env')
        st_r = []
        for pm in pms:
            if isinstance(ds[pm], (list, tuple)):
                dspm = ds[pm][0]
            elif isinstance(ds[pm], dict):
                dspm = ds[pm]
            else:
                raise RuntimeError('Invalid ds[pm] type')
            st_or = {
                'pkgname': pm,
                'display_name': dspm['display_name'],
                'plugin_version': dspm['plugin_version'],
                'install': 'n/a',
                'unittest': 'n/a',
                'zipped_log': None,
                'start_ts': None,
                'end_ts': None,
            }
            self._selftest_one(st_or, venv_dir=venv_dir)
            print(f'"{st_or["display_name"]}" testing... '
                  f'install {st_or["install"]}, unittest {st_or["unittest"]}')
            st_r.append(st_or)
        self._report_selftest(st_r)
        return 0

    # ==========================================================================
    def _venv_clean(self):
        py_root = os.path.join(str(Path.home()), '.argos-rpa.venv')
        if not os.path.exists(py_root):
            os.makedirs(py_root)
            return 0
        dirs = [os.path.join(py_root, o) for o in os.listdir(py_root)
                if os.path.isdir(os.path.join(py_root, o))]
        del_list = list()
        for dir in dirs:
            dbn = os.path.basename(dir)
            if not ('0' <= dbn[0] <= '9'):
                del_list.append(dir)
        for ditem in del_list:
            dirs.remove(ditem)
        for dir in dirs:
            shutil.rmtree(dir)
        return 0

    # ==========================================================================
    def do_plugin(self):
        ofp = sys.stdout
        tmpdir = tempfile.mkdtemp(prefix='do_plugin_')
        try:
            self.sta.log(StatLogger.LT_2, "Starting plugin %s command" % self.args.plugin_cmd)
            self.logger.info('PPM.do_plugin: starting... %s' % self.args.plugin_cmd)
            if self.args.plugin_cmd == 'venv-clean':
                self._venv_clean()
                print('Virtual Environment are cleaned.')
                return 0
            if not self.args.without_cache:
                # 속도를 위하여 hash 를 우선 가지고 옴
                self._get_dumpspec_hash()
                self.def_dumpspec = self._def_dumpspec_from_plugin()
            else:
                self.ds_hash = None
                self.def_dumpspec = {}

                # for pkg in self.PLUGIN_PKGS:
            #     # self.venv.venv_pip('install', pkg, *self.ndx_param)
            #     self.venv.venv_pip('install', pkg)

            if self.args.outfile:
                ofp = open(self.args.outfile, 'w', encoding='utf-8')

            # 만약 selftest 인 경우에는 'argoslabs.check.env' 첫번째 추가
            if self.args.plugin_cmd == 'selftest' and self.args.plugin_module:
                # self.args.plugin_module 에서 'argoslabs.check.env' 첫번째 추가
                pms = self.args.plugin_module
                f_mn_ndx = -1
                for i, mn in enumerate(pms):
                    if mn.startswith('argoslabs.check.env'):
                        f_mn_ndx = i
                        break
                if f_mn_ndx >= 0:
                    del pms[f_mn_ndx]
                pms.insert(0, 'argoslabs.check.env')
                self.args.plugin_module = pms

            ####################################################################
            # PAM용 환경설정 만들기
            ####################################################################
            if self.args.plugin_cmd == 'venv':
                self.sta.log(StatLogger.LT_2, "Preparing execution environment")
                if not (self.args.plugin_module or self.args.requirements_txt):
                    raise RuntimeError('PPM.do_plugin: plugin-modules parameters or --requirements-txt option must be specifiyed.')
                if self.args.requirements_txt and not os.path.exists(self.args.requirements_txt):
                    raise RuntimeError('PPM.do_plugin: --requirements-txt "%s" file does not exists.' % self.args.requirements_txt)
                # ~/.argos-rpa.venv/ 폴더 안에 YYYMMDD-HHMMSS 로 가상환경을 만듦
                venv_d = os.path.join(str(Path.home()), '.argos-rpa.venv')
                if not os.path.exists(venv_d):
                    os.makedirs(venv_d)
                modspec = self._get_modspec(tmpdir)
                # glob_f = os.path.join(venv_d, '**', 'freeze.json')
                glob_f = os.path.join(venv_d, '*')
                match_list = list()
                for f in glob.glob(glob_f):
                    if not os.path.isdir(f):
                        continue
                    if os.path.basename(f) == 'Python37-32':
                        continue
                    fzj = os.path.join(f, 'freeze.json')
                    if not os.path.exists(fzj):
                        shutil.rmtree(f)
                        continue
                    with open(fzj, encoding='utf-8') as ifp:
                        freeze_d = json.load(ifp)
                    if self._is_conflict(freeze_d, modspec):
                        continue
                    match_cnt = self._count_satisfy(freeze_d, modspec)
                    get_venv = os.path.abspath(f)
                    match_list.append((match_cnt, get_venv))
                # 설치가능한 venv가 발견되지 않았다면, 새로 만듦
                if not match_list:
                    self.sta.log(StatLogger.LT_1, 'Preparing ARGOS RPA+ environment. This process may take a few minutes.')
                    now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
                    get_venv = os.path.join(venv_d, now)
                    self._get_venv(get_venv)
                else:  # 아니면 가장 많이 매칭된 것을 찾아 이용
                    self.sta.log(StatLogger.LT_1, 'An ARGOS RPA+ environment was found.')
                    match_list.sort(key=lambda x: x[0])
                    get_venv = match_list[-1][1]
                    if match_list[-1][0] < len(modspec):
                        self._get_venv(get_venv)
                ofp.write(get_venv)
                return 0

            # 만약 CHIEF에 특정 사용자별 dumpspec 결과를 가져오려면 우선
            # 해당 모듈 리스트를 구함
            if self.args.plugin_cmd.endswith('dumpspec') and self.args.user:
                self._dumpspec_user(tmpdir)

            # 나머지는 CHIEF, STU용
            # 우선은 pypi 서버에서 해당 모듈 목록을 구해와서
            # 해당 모듈(wheel)만 다운로드하여 포함되어 있는 dumpspec.json을
            # 가져오는데 tempdir에 dumpspec-modulename-version.json 식으로 캐슁
            self.sta.log(StatLogger.LT_1, 'Downloading plugins. It may take a few minutes. Private plugins could take more.')

            if self.args.flush_cache:
                self._dumpspec_json_clear_cache()
            if self.args.plugin_cmd == 'versions' and not self.args.startswith:
                # versions 명령에서는 해당 모듈만 가져오도록 필터링
                self.args.startswith = self.args.plugin_module[0]
            modlist = self._list_modules(startswith=self.args.startswith,
                                         official_only=self.args.official_only,
                                         private_only=self.args.private_only)
            modd, modds = self._get_saved_dumpspec(modlist)
            if not (modd and modds):
                for mod in modlist:
                    eles = mod.rstrip('.whl').split('-')
                    if len(eles) not in (5,):
                        raise RuntimeError('PPM.do_plugin: Invalid format for wheel file "%s"' % mod)
                    ved = {
                        'version': eles[1],
                        'python-tag': eles[2],
                        'abi-tag': eles[3],
                        'flatform-tag': eles[4],
                    }
                    dsj = self._dumpspec_json(eles[0], eles[1])
                    ved['display_name'] = dsj.get('display_name')
                    ved['description'] = dsj.get('description')
                    ved['owner'] = dsj.get('owner')
                    ved['group'] = dsj.get('group')
                    ved['platform'] = dsj.get('platform')
                    ved['last_modify_datetime'] = dsj.get('last_modify_datetime')
                    ved['icon'] = dsj.get('icon')
                    ved['sha256'] = dsj.get('sha256')
                    if eles[0] not in modd:
                        modd[eles[0]] = [ved]
                        modds[eles[0]] = [dsj]
                    else:
                        b_found = False
                        for ve in modd[eles[0]]:
                            if ve['version'] == eles[1]:
                                b_found = True
                                break
                        if not b_found:
                            modd[eles[0]].append(ved)
                            modds[eles[0]].append(dsj)
                # modd 에 있는 ved 목록에 대하여 내림차순 정렬
                # cmp_items_py3 = cmp_to_key(version_compare)
                for k, v in modd.items():
                    if len(v) <= 1:
                        continue
                    modd[k] = sorted(v, key=cmp_to_key(version_compare), reverse=True)
                for k, v in modds.items():
                    if len(v) <= 1:
                        continue
                    modds[k] = sorted(v, key=cmp_to_key(plugin_version_compare), reverse=True)
                self._set_saved_dumpspec(modlist, modd, modds)

            ####################################################################
            # 사용자 plugin_modules를 포함한 --requirements-txt 의 모듈 스펙을 파싱
            ####################################################################
            modspec = self._get_modspec(tmpdir)

            ####################################################################
            # --user 옵션을 안주면 CHIEF에서 모든 플러그인 가져오기
            # 예) alabs.ppm plugin get --official-only --outfile get-all.json
            # --user 옵션을 주면 STU에서 해당 로그인 사용자의 플러그인 가져오기
            # 예) alabs.ppm plugin get --user a@b.c.d --official-only --outfile get-user.json
            # --official-only 는 공식사이트, --private-only는 자신의 private 만 (~/.argos-rpa.conf 에서)
            # 예) alabs.ppm plugin get --user a@b.c.d --private-only --outfile get-user-private.json
            # --last-only
            ####################################################################
            if self.args.plugin_cmd == 'get':
                self.sta.log(StatLogger.LT_2, "Getting the information of plugins")
                rd = self._cmd_modspec(modd, modspec)
                if not self.args.short_output:
                    if self.args.with_dumpspec:
                        for mod, dl in rd.items():
                            if isinstance(dl, dict):
                                self._get_with_dumpspec(mod, dl, modds)
                            elif isinstance(dl, list):
                                for d in dl:
                                    self._get_with_dumpspec(mod, d, modds)
                            else:
                                raise RuntimeError('Invalid type of get result, needed {dict, list}')
                    json.dump(rd, ofp)
                else:
                    for mod in sorted([x for x in rd.keys()]):
                        for ved in rd[mod]:
                            if isinstance(ved, list):
                                for v in ved:
                                    ofp.write('%s,%s%s' % (mod, v['version'], os.linesep))
                            else:
                                ofp.write('%s,%s%s' % (mod, ved['version'], os.linesep))

            elif self.args.plugin_cmd == 'versions':
                self.sta.log(StatLogger.LT_2, "Checking version numbers of plugin")
                if not self.args.plugin_module or len(self.args.plugin_module) != 1:
                    raise RuntimeError('plugin versions need only one plugin_module parameter')
                modname = self.args.plugin_module[0]
                if modname not in modd:
                    raise RuntimeError('module "%s" not in plugin module list' % modname)
                for ved in modd[modname]:
                    print(ved['version'])

            ####################################################################
            # --user 옵션을 안주면 CHIEF/STU에서 모든 플러그인 dumpspec 가져오기
            # 예) alabs.ppm plugin dumpspec --official-only --outfile dumpspec.json
            # --user 옵션을 주면 STU에서 해당 로그인 사용자의 플러그인 가져오기
            # 예) alabs.ppm plugin dumpspec --user a@b.c.d --official-only --outfile dumpspec.json
            # --official-only 는 공식사이트, --private-only는 자신의 private 만 (~/.argos-rpa.conf 에서)
            # 예) alabs.ppm plugin dumpspec --private-only --outfile dumpspec.json
            ####################################################################
            elif self.args.plugin_cmd.endswith('dumpspec'):
                self.sta.log(StatLogger.LT_2, "Getting the specifications of plugins")
                # rd = self._cmd_modspec(modds, modspec, version_attr='plugin_version')  # 2020.02.20
                rd = self._cmd_modspec(modds, modspec)
                json.dump(rd, ofp)

            elif self.args.plugin_cmd == 'unique':
                self.sta.log(StatLogger.LT_2, "Checking the uniqueness of plugins")
                setattr(self.args, 'venv', True)
                self._check_pkg()
                self._get_setup_config()

                ds = self._cmd_modspec(modds, modspec)
                if self.pkgname in ds:
                    print(f'Package name "{self.pkgname}" is already exists!')
                    return 2
                dn = self._get_pkg_display_name()
                if not dn:
                    print('Cannot get display_name')
                    return 3
                for ddl in ds.values():
                    for dd in ddl:
                        if dn == dd.get('display_name'):
                            print(f'Package name "{self.pkgname}" is already exists!')
                            return 4
                print(f'Package "{self.pkgname}" and Display name "{dn}" seems OK to use.')
                return 0
            ####################################################################
            # PAM selftest
            ####################################################################
            elif self.args.plugin_cmd == 'selftest':
                return self._selftest(modds, modspec)

            return 0
        finally:
            if self.args.outfile and ofp != sys.stdout:
                ofp.close()
            if tmpdir and os.path.exists(tmpdir):
                shutil.rmtree(tmpdir)
            self.logger.info('PPM.do_plugin: end. %s' % self.args.plugin_cmd)

    # ==========================================================================
    @staticmethod
    def _parse_req(req):
        o = urlparse(req)
        nls = o.netloc.split(':')
        port = None
        if len(nls) == 2:
            port = int(nls[1])
        else:
            if o.scheme == 'http':
                port = 80
            elif o.scheme == 'https':
                port = 443
        return nls[0], port

    # ==========================================================================
    def _do_upload(self, url, user, passwd, wheels):
        o = urlparse(url)
        raw_url = '{scheme}://{netloc}/'.format(scheme=o.scheme,
                                                netloc=o.netloc)
        # 기존의 twine으로 사설 pypiserver로 올리는데 https 문제 때문에
        # pypiuploader 를 가져와 처리
        # r = self.venv.venv_py('-m', 'twine', 'upload', wheel,
        #                       '--repository-url', raw_url,
        #                       '--username', user,
        #                       '--password', passwd,
        #                       stdout=True)
        cmd = [
            'files',
            '--index-url',
            raw_url,
            '--username', user,
            '--password', passwd,
        ]
        cmd.extend(wheels)
        self.logger.debug('_do_upload: cmd="%s"' % ' '.join(cmd))
        return pu_main(argv=cmd)

    # ==========================================================================
    def _can_self_upgrade(self):
        is_common, is_ppm = False, False
        # for alabs.common
        try:
            cur_common = pkg_resources.get_distribution("alabs.common").version
            last_common = self.mod_ver_list['alabs.common'][0]
            if ver_compare(last_common, cur_common) > 0:
                is_common = True
        except Exception as e:
            self.logger.error('Cannot get version of "alabs.common": %s' % str(e))
        # for alabs.ppm
        try:
            cur_ppm = pkg_resources.get_distribution("alabs.ppm").version
            last_ppm = self.mod_ver_list['alabs.ppm'][0]
            if ver_compare(last_ppm, cur_ppm) > 0:
                is_ppm = True
        except Exception as e:
            self.logger.error('Cannot get version of "alabs.common": %s' % str(e))
        return is_common, is_ppm

    # ==========================================================================
    def _get____tk____(self, u___i, p___w):
        try:
            root_url = self._get_URL_OAUTH()
            cookies = {
                'JSESSIONID': '04EFBA89842288248F32F9EC19B7423E',
            }

            headers = {
                'Accept': '*/*',
                'Authorization': 'Basic YXJnb3MtcnBhOjA0MGM1YTA1MTkzZWRjYWViZjk4NTY1MmMxOGE1MThj',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Host': '%s' % self._get_host_from_index(root_url),
                'Postman-Token': 'd010ec3c-d0b5-40cf-a3a5-4522fe73b2ad,0af02f20-2044-4983-9db4-ab7aa8453e06',
                'User-Agent': 'PostmanRuntime/7.13.0',
                'accept-encoding': 'gzip, deflate',
                'cache-control': 'no-cache',
                'content-length': '92',
                'content-type': 'application/x-www-form-urlencoded',
                'cookie': 'JSESSIONID=04EFBA89842288248F32F9EC19B7423E',
            }

            data = {
                'grant_type': 'password',
                'client_id': 'argos-rpa',
                'scope': 'read write',
                'username': u___i,
                'password': p___w,
            }
            self.sta.log(StatLogger.LT_2, "Getting OAuth")
            r = requests.post('%s/oauth/token' % root_url,
                              headers=headers, cookies=cookies, data=data, verify=False)
            if r.status_code // 10 != 20:
                raise RuntimeError('PPM._dumpspec_user: API Error!')
            self.sta.log(StatLogger.LT_3, "Getting OAuth done")
            jd = json.loads(r.text)
            return 'Bearer %s' % jd['access_token']
        except Exception as e:
            msg = '_get____tk____ Error: %s' % str(e)
            self.logger.error(msg)
            return None

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def get_version(self):
        su_yaml_files = [
            os.path.join(os.path.dirname(__file__), 'setup.yaml'),
        ]
        if hasattr(sys, '_MEIPASS'):
            # noinspection PyProtectedMember
            su_yaml_files.append(
                os.path.join(os.path.abspath(sys._MEIPASS), 'setup.yaml'))
        su_yaml_file = None
        for syf in su_yaml_files:
            if os.path.exists(syf):
                su_yaml_file = syf
                break
        if not su_yaml_file:
            raise IOError('Cannot get version info from setup.yaml')
        with open(su_yaml_file, encoding='utf-8') as ifp:
            if yaml.__version__ >= '5.1':
                # noinspection PyUnresolvedReferences
                su_yaml = yaml.load(ifp, Loader=yaml.FullLoader)
            else:
                su_yaml = yaml.load(ifp)
        print('Version %s' % su_yaml['setup']['version'])
        return 0

    # ==========================================================================
    def do(self):
        try:
            self.logger.info('PPM.do: starting... %s' % self.args.command)
            setattr(self.args, "last_only", getattr(self.args, "last_only", False))
            setattr(self.args, "official_only", getattr(self.args, "official_only", False))
            if not self.args.official_only:
                if self.args.pr_user:
                    setattr(self.args, 'user', self.args.pr_user)
                elif not hasattr(self.args, 'user'):
                    setattr(self.args, 'user', None)
                if self.args.pr_user_auth:
                    setattr(self.args, 'user_auth', self.args.pr_user_auth)
                elif not hasattr(self.args, 'user_auth'):
                    setattr(self.args, 'user_auth', None)
                # 만약 --pr-user, --pr-user-pass 를 입력한 경우
                if self.args.user and self.args.pr_user_pass and not self.args.pr_user_auth:
                    setattr(self.args, 'user_auth',
                            self._get____tk____(self.args.user, self.args.pr_user_pass))
                # pam_id 처리
                if not hasattr(self.args, 'pam_id'):
                    setattr(self.args, 'pam_id', None)

                if self.args.command in ('upload',):
                    # 만약 upload 에서 --pr-user 옵션을 안 준 경우, 사용자를 물어서 가져옴
                    if not self.args.user:
                        user = input('%s command need user id for ARGOS RPA, User ID? '
                                     % self.args.command)
                        setattr(self.args, 'user', user)
                    # 만약 upload 에서 --pr-user 옵션만 주고 실행했을 때는 암호를 물어서 가져옴
                    if not self.args.user_auth:
                        u___p = self.args.pr_user_pass
                        if not u___p:
                            u___p = getpass('%s command need user password for ARGOS RPA, User Password? '
                                            % self.args.command)
                        tk = self._get____tk____(self.args.user, u___p)
                        if not tk:
                            raise RuntimeError('Invalid UserID or Password')
                        setattr(self.args, 'user_auth', tk)

            if hasattr(self.args, 'subargs'):
                subargs = self._check_subargs(self.args.subargs)
            else:
                subargs = []
            # officail 및 private의 --index 내용 가져오기
            self._get_indices()
            # pypi-official의 module 및 버전 목록을 구해옴
            self.mod_ver_list = self._mod_ver_list_from_plugin()
            if not getattr(sys, 'frozen', False) and self.args.self_upgrade:
                is_common, is_ppm = self._can_self_upgrade()
                # noinspection PyProtectedMember
                self.venv._upgrade(self.ndx_param, is_common=is_common, is_ppm=is_ppm)

            # first do actions which do not need virtualenv
            ####################################################################
            # get commond
            ####################################################################
            if self.args.command == 'get':
                if self.args.get_cmd == 'version':
                    return self.get_version()
                if self.args.get_cmd == 'repository':
                    self.sta.log(StatLogger.LT_2, 'Connecting offcial repository')
                    print(self.indices[0])
                elif self.args.get_cmd == 'trusted-host':
                    self.sta.log(StatLogger.LT_2, 'Connecting trusted host')
                    print(self._get_host_from_index(self.indices[0]))
                elif self.args.get_cmd == 'private':
                    self.sta.log(StatLogger.LT_2, 'Connecting private repository')
                    prl = self.indices[1:]
                    if not prl:
                        print('No private repository')
                    else:
                        print('There are %s private repository(ies)' % len(prl))
                        print('\n'.join(prl))
                return 0
            # print('start %s ...' % self.args.command)

            ####################################################################
            # plugin commond
            ####################################################################
            if self.args.command == 'plugin':
                return self.do_plugin()

            ####################################################################
            # pip commond
            ####################################################################
            if self.args.command == 'install':
                self.sta.log(StatLogger.LT_2, 'install %s' % ' '.join(subargs))
                subargs.insert(0, 'install')
                subargs.extend(self.ndx_param)
                return self.venv.venv_pip(*subargs)
            elif self.args.command == 'show':
                self.sta.log(StatLogger.LT_2, 'show %s' % ' '.join(subargs))
                subargs.insert(0, 'show')
                subargs.append('--verbose')
                return self.venv.venv_pip(*subargs, getstdout=True)
            elif self.args.command == 'uninstall':
                self.sta.log(StatLogger.LT_2, 'uninstall %s' % ' '.join(subargs))
                subargs.insert(0, '-y')
                subargs.insert(0, 'uninstall')
                return self.venv.venv_pip(*subargs)
            elif self.args.command == 'search':
                self.sta.log(StatLogger.LT_2, 'search %s' % ' '.join(subargs))
                r = 1
                for ndx in self.indices:
                    sargs = copy.copy(subargs)
                    sargs.insert(0, 'search')
                    # subargs.extend(self.ndx_param)
                    sargs.append('--index')
                    sargs.append(ndx)
                    sargs.append('--trusted-host')
                    sargs.append(self._get_host_from_index(ndx))
                    r = self.venv.venv_pip(*sargs, getstdout=True)
                    # official repository 애서만 가져오도록 수정
                    break
                return r
            elif self.args.command == 'list':
                self.sta.log(StatLogger.LT_2, 'list modules')
                return self.venv.venv_pip('list', getstdout=True)

            # direct command for (pip, python, python setup.py)
            if self.args.command == 'pip':
                self.sta.log(StatLogger.LT_2, 'pip %s' % ' '.join(subargs))
                return self.venv.venv_pip(*subargs)
            elif self.args.command == 'py':
                self.sta.log(StatLogger.LT_2, 'py %s' % ' '.join(subargs))
                return self.venv.venv_py(*subargs)
            elif self.args.command == 'setup':
                self.sta.log(StatLogger.LT_2, 'setup %s' % ' '.join(subargs))
                return self.setup(*subargs)
            elif self.args.command == 'list-repository':
                self.sta.log(StatLogger.LT_2, 'list repositories')
                # noinspection PyTypeChecker
                modlist = self._list_modules(startswith=None,
                                             official_only=False,
                                             private_only=False)
                for mod in modlist:
                    print(mod)
                return 0 if bool(modlist) else 1

            ####################################################################
            # 만약 clear* 명령이면 venv를 강제로 true 시킴
            ####################################################################
            if self.args.command in ('clear', 'clear-py',
                                     'clear-all', 'dumpspec', 'submit',
                                     'list-repository') \
                    and not self.args.venv:
                self.args.venv = True  # 그래야 아래  _check_pkg에서 폴더 옮김
            self._check_pkg()
            self._get_setup_config()

            ####################################################################
            # ppm functions
            ####################################################################
            if self.args.command == 'clear':
                self.sta.log(StatLogger.LT_2, 'clear')
                return self._clear()
            elif self.args.command == 'clear-py':
                self.sta.log(StatLogger.LT_2, 'clear python environment')
                return self._clear_py()
            elif self.args.command == 'clear-all':
                self.sta.log(StatLogger.LT_2, 'clear all')
                self._clear()
                return self._clear_py()
            elif self.args.command == 'dumpspec':
                pass
            elif self.args.command == 'test':
                self.sta.log(StatLogger.LT_2, 'setup test')
                r = self.setup('test')
                print('test is done. success is %s' % (r == 0,))
                return r
            elif self.args.command == 'build':
                self.sta.log(StatLogger.LT_2, 'setup build')
                for pkg in self.BUILD_PKGS:
                    self.venv.venv_pip('install', pkg, *self.ndx_param, getstdout=True)
                self._dumpspec()
                r = self.setup('bdist_wheel')
                print('build is done. success is %s' % (r == 0,))
                return r
            elif self.args.command == 'submit':
                zf = None
                self.sta.log(StatLogger.LT_2, "submitting plugin candidate file")
                try:
                    if not self.args.submit_key:
                        raise RuntimeError('submit: Invalid submit key')
                    current_wd = os.path.abspath(getattr(self.args, '_cwd_'))
                    parent_wd = os.path.abspath(os.path.join(getattr(self.args, '_cwd_'), '..'))
                    if not os.path.exists(parent_wd):
                        raise RuntimeError('PPM.do: Cannot access parent monitor')
                    zf = os.path.join(parent_wd, '%s.zip' % self.pkgname)
                    shutil.make_archive(zf[:-4], 'zip',
                                        root_dir=os.path.dirname(current_wd),
                                        base_dir=os.path.basename(current_wd))
                    if not os.path.exists(zf):
                        raise RuntimeError('PPM.do: Cannot build zip file "%s" to submit' % zf)
                    req = self.args.submit_url
                    if not req:
                        raise RuntimeError('PPM.do: Cannot submit to "%s"' % req)
                    sdu = SimpleDownUpload(url=req, token=self.args.submit_key)
                    sfl = list()
                    sfl.append(self.pkgname)
                    emstr = self.setup_config.get('author_email', 'unknown email')
                    sfl.append(emstr.replace('@', '-'))
                    sfl.append(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
                    r = sdu.upload(zf, saved_filename='%s.zip' % ' '.join(sfl))
                    if not r:
                        raise RuntimeError('PPM.do: Cannot upload "%s"' % zf)
                    print('Succesfully submitted "%s"' % zf)
                    print('submit is done. success is True')
                    return 0
                finally:
                    if zf and os.path.exists(zf):
                        os.remove(zf)
            elif self.args.command == 'upload':
                self.sta.log(StatLogger.LT_2, "upload plugin file to the private repository")
                for pkg in self.UPLOAD_PKGS:
                    self.venv.venv_pip('install', pkg, *self.ndx_param)
                # _get_indices() 에서 'private-repositories' 정보를 구해왔음
                pri_reps = get_xpath(self.config, '/private-repositories')
                if not pri_reps:
                    raise RuntimeError('PPM.do: Private repository (private-repositories) '
                                       'is not set at %s' % YAML_NAME)
                pri_rep = None
                if not self.args.repository_name:
                    pri_rep = pri_reps[0]
                else:
                    for pr in pri_reps:
                        if pr.get('name') == self.args.repository_name:
                            pri_rep = pr
                            break
                if not pri_reps:
                    raise RuntimeError('PPM.do: Private repository "%s" is not exists at %s'
                                       % (self.args.repository_name, YAML_NAME))

                pr_url = pri_rep.get('url')
                pr_user = pri_rep.get('username')
                pr_pass = pri_rep.get('password')
                if not pr_url:
                    raise RuntimeError('PPM.do: url of private repository is not set, please '
                                       'check private-repositories at %s' % YAML_NAME)
                if not pr_user:
                    raise RuntimeError('PPM.do: username of private repository is not set, please '
                                       'check private-repositories at %s' % YAML_NAME)
                if not pr_pass:
                    raise RuntimeError('PPM.do: password of private repository is not set, please '
                                       'check private-repositories at %s' % YAML_NAME)
                gl = glob.glob('dist/%s*.whl' % self.pkgname)
                if not gl:
                    raise RuntimeError('PPM.do: Cannot find wheel package file at "%s",'
                                       ' please build first' %
                                       os.path.join(self.basepath, 'dist'))
                pr_wheels = [f for f in gl]
                kwargs = {
                    'url': pr_url,
                    'user': pr_user,
                    'passwd': pr_pass,
                    'wheels': pr_wheels,
                }
                r = self._do_upload(**kwargs)
                print('upload is done. success is %s' % (r == 0,))
                return r
            # elif self.args.command == 'unique':
            #     _ = self.pkgname
            #     setattr(self.args, 'plugin_cmd', '_dumpspec')
            #     setattr(self.args, 'without_cache', False)
            #     setattr(self.args, 'outfile', None)
            #     setattr(self.args, 'private_only', False)
            #     setattr(self.args, 'flush_cache', False)
            #     setattr(self.args, 'startswith', None)
            #     setattr(self.args, 'plugin_module', None)
            #     ds = self.do_plugin()
            #     if self.pkgname in ds:
            #         print(f'Package name "{self.pkgname}" is already exists!')
            #         return 2
            #     dn = self._get_pkg_display_name()
            #     if not dn:
            #         print('Cannot get display_name')
            #         return 3
            #     for dd in ds.values():
            #         if dn == dd.get('display_name'):
            #             print(f'Package name "{self.pkgname}" is already exists!')
            #             return 4
            #     print(f'Package "{self.pkgname}" and Display name "{dn}" seems OK to use.')
            #     return 0
            # else:
            #     raise RuntimeError('PPM.do: Cannot support command "%s"'
            #                        % self.args.command)
        except Exception as err:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.sta.error(''.join(_out))
            self.logger.error(''.join(_out))
            self.logger.error(str(err))
            raise
        finally:
            if self.args.clean:
                self._clear()
            # if self.args.command != 'get':
            #     print('done.')
            self.logger.info('PPM.do: end. %s' % self.args.command)

    # ==========================================================================
    def _get_pkg_display_name(self):
        init_file = os.path.join(self.basepath, self.pkgpath, '__init__.py')
        if not os.path.exists(init_file):
            raise IOError(f'Cannot read "{init_file}"')
        with open(init_file, encoding='utf-8') as ifp:
            is_in_mc = False
            for line in ifp:
                line = line.strip()
                if not line:
                    continue
                if line.find('with ModuleContext(') >= 0:
                    is_in_mc = True
                if not is_in_mc:
                    continue
                dn_ndx = line.find('display_name=')
                if dn_ndx >= 0:
                    dn = line[dn_ndx + len('display_name='):].rstrip(',')
                    return dn[1:-1]

    # ==========================================================================
    def append_pkg_history(self, pkghistory):
        fl = [f for f in
              glob.glob(os.path.join(self.pkgpath, '**', '__init__.py'),
                        recursive=True)]
        for d in map(os.path.dirname, fl):
            md = d.replace(os.path.sep, '.')
            # 'alabs.ppm.pyinst.venv.Lib.site-packages.pip' 와 같이
            # 'alabs.ppm.pyinst' 가 없는데 하위가 나올 수 있어서
            # 이런 경우에는 append 하지 않음
            md_list = md.split('.')
            b_missed = False
            for i in range(3, len(md_list)):
                md_prefix = '.'.join(md_list[:i])
                if "'%s'" % md_prefix not in pkghistory:
                    b_missed = True
                    break
            if b_missed:
                continue
            d = "'%s'" % md
            if d not in pkghistory:
                pkghistory.append(d)

    # ==========================================================================
    def _install_precompiled_wheel(self):
        for whl in glob.glob('%s%s*.whl' % (self.pkgpath, os.path.sep)):
            r = self.venv.venv_pip('install', whl,
                                   *self.ndx_param, getstdout=True)
            if r != 0:
                raise RuntimeError('PPM._install_precompiled_wheel: Error in installing "%s"' % whl)

    # ==========================================================================
    def _install_requirements(self):
        self._install_precompiled_wheel()
        requirements_txt = os.path.join(self.pkgpath, 'requirements.txt')
        if not os.path.exists(requirements_txt):
            with open(requirements_txt, 'w', encoding='utf-8') as ofp:
                ofp.write('# pip dependent packages\n')
        r = self.venv.venv_pip('install', '-r', requirements_txt,
                               *self.ndx_param, getstdout=True)
        if r != 0:
            raise RuntimeError('PPM._install_requirements: Error in installing "%s"' % requirements_txt)
        return requirements_txt

    # ==========================================================================
    def setup(self, *args):
        self.logger.info('PPM.setup: starting...')
        supath = 'setup.py'
        keywords = self.setup_config.get('keywords', [])
        for kw in self.pkgname.split('.'):
            if kw not in keywords:
                keywords.append(kw)
        requirements_txt = self._install_requirements()

        pkghistory = []
        eles = self.pkgname.split('.')
        for i in range(len(eles)):
            pkghistory.append("'%s'" % '.'.join(eles[0:i+1]))
        # pkghistory.append(self.pkgname)
        classifiers = self.setup_config.get('classifiers', [])
        for c in self.CLASSIFIERS:
            if c not in classifiers:
                classifiers.append(c)
        classifiers_str = '\n'.join(
            ["        '%s'," % c for c in sorted(classifiers)])
        self.append_pkg_history(pkghistory)
        if sys.platform == 'win32':
            requirements_txt = requirements_txt.replace('\\', '\\\\')
        # for package_data
        package_data = self.setup_config.get('package_data',
                                             {self.pkgname: ['icon.*', 'setup.yaml']})
        if self.pkgname not in package_data:
            # package_data[self.pkgname] = ['icon.*']
            raise RuntimeError('Please check package_data in setup.yaml')
        if self.DUMPSPEC_JSON not in package_data[self.pkgname]:
            package_data[self.pkgname].append(self.DUMPSPEC_JSON)
        with open(supath, 'w', encoding='utf-8') as ofp:
            setup_str = '''
import pip
import unittest
from setuptools import setup

pip_major_version = int(pip.__version__.split(".")[0])
if pip_major_version >= 20:
    from pip._internal.req import parse_requirements
    from pip._internal.network.session import PipSession
elif pip_major_version >= 10:
    from pip._internal.req import parse_requirements
    from pip._internal.download import PipSession
else:
    from pip.req import parse_requirements
    from pip.download import PipSession


################################################################################
def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('{pkgname}',
                                      pattern='test*.py')
    return test_suite


################################################################################
# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("{requirements_txt}", session=PipSession())
#reqs = [str(ir.req) for ir in install_reqs]
reqs = list()
for ir in install_reqs:
    if hasattr(ir, 'req'):
        req = ir.req
    elif hasattr(ir, 'requirement'):
        req = ir.requirement
    else:
        raise LookupError('Cannot get requirement')
    reqs.append(str(req))
reqs.extend({install_requires})

setup(
    name='{pkgname}',
    test_suite='setup.my_test_suite',
    packages=[
        {pkghistory}
    ],
    version='{version}',
    description='{description}',
    author='{author}',
    author_email='{author_email}',
    url='{url}',
    license='{license}',
    keywords={keywords},
    platforms={platforms},
    install_requires=reqs,
    python_requires='>=3.6',
    package_data={package_data},
    zip_safe=False,
    classifiers=[
{classifiers}
    ],
    entry_points={{
        'console_scripts': [
            '{pkgname}={pkgname}:main',
        ],
    }},
    include_package_data=True,
)
'''.format(
                pkghistory=','.join(pkghistory),
                requirements_txt=requirements_txt,
                pkgname=self.pkgname,
                version=self.setup_config.get('version', '0.1.0'),
                install_requires=self.setup_config.get('install_requires', []),
                description=self.setup_config.get('description', 'description'),
                author=self.setup_config.get('author', 'author'),
                author_email=self.setup_config.get('author_email', 'author_email'),
                url=self.setup_config.get('url', 'url'),
                license=self.setup_config.get('license', 'Proprietary License'),
                keywords=keywords,
                platforms=str(self.setup_config.get('platforms', [])),
                package_data=package_data,
                classifiers=classifiers_str,
            )
            ofp.write(setup_str)
            self.logger.debug('PPM.setup: %s=<%s>' % (supath, setup_str))
        # for setup.cfg
        sucpath = 'setup.cfg'
        _license = ''
        if os.path.exists(os.path.join(self.pkgpath, 'LICENSE.txt')):
            _license = "license_files = %s%sLICENSE.txt" \
                      % (self.pkgpath, os.path.sep)
        readme = ''
        if os.path.exists(os.path.join(self.pkgpath, 'README.md')):
            readme = "description-file = %s%sREADME.md" \
                      % (self.pkgpath, os.path.sep)
        with open(sucpath, 'w', encoding='utf-8') as ofp:
            sucstr = '''
[metadata]
# license_files = LICENSE.txt
{license}
# description-file = README.md
{readme}
'''.format(license=_license, readme=readme)
            ofp.write(sucstr)
            self.logger.debug('PPM.setup: %s=<%s>' % (sucpath, sucstr))
        # instead use package_data
        # if os.path.exists(os.path.join(self.pkgpath, 'MANIFEST.in')):
        #     shutil.copy(os.path.join(self.pkgpath, 'MANIFEST.in'), self.basepath)

        # for {pkgname}.tests.__main__.py
        if os.path.exists(os.path.join(self.pkgpath, 'tests')):
            tmpath = os.path.join(self.pkgpath, 'tests', '__main__.py')
            if not os.path.exists(tmpath):
                with open(tmpath, 'w', encoding='utf-8') as ofp:
                    tmstr = '''
import sys
from {pkgname}.tests.test_me import TU
from unittest import TestLoader, TextTestRunner


################################################################################
if __name__ == "__main__":
    suite = TestLoader().loadTestsFromTestCase(TU)
    result = TextTestRunner(verbosity=2).run(suite)
    ret = not result.wasSuccessful()
    sys.exit(ret)
'''.format(pkgname=self.pkgname)
                    ofp.write(tmstr)
                    self.logger.debug('PPM.setup: %s=<%s>' % (tmpath, tmstr))

        r = self.venv.venv_py(supath, *args, getstdout=True)
        self.logger.info('PPM.setup: end.')
        return r


# ################################################################################
# def get_repository_env():
#     cf = CONF_PATH
#     if not os.path.exists(cf):
#         with open(cf, 'w', encoding='utf-8') as ofp:
#             ofp.write(_conf_last_contents)
#     with open(cf, encoding='utf-8') as ifp:
#         if yaml.__version__ >= '5.1':
#             # noinspection PyUnresolvedReferences
#             dcf = yaml.load(ifp, Loader=yaml.FullLoader)
#         else:
#             dcf = yaml.load(ifp)
#     need_conf_upgrade = False
#     if 'version' not in dcf:
#         need_conf_upgrade = True
#     elif ver_compare(dcf['version'], _conf_last_version) < 0:
#         need_conf_upgrade = True
#     if need_conf_upgrade:
#         with open(cf, 'w', encoding='utf-8') as ofp:
#             ofp.write(_conf_last_contents)
#         with open(cf, encoding='utf-8') as ifp:
#             if yaml.__version__ >= '5.1':
#                 # noinspection PyUnresolvedReferences
#                 dcf = yaml.load(ifp, Loader=yaml.FullLoader)
#             else:
#                 dcf = yaml.load(ifp)
#     return dcf


################################################################################
def start_pbtail(g_dir):
    if sys.platform != 'win32':
        return False
    exe_f = g_dir + r'\Release\argos-pbtail.exe'
    if not os.path.exists(exe_f):
        return False
    global pbtail_po
    pbtail_po = subprocess.Popen([exe_f])
    return True


################################################################################
# noinspection PyUnresolvedReferences,PyProtectedMember
def ppm_exe_init(sta):
    tmpdir = None
    try:
        g_dir = os.path.abspath(sys._MEIPASS)
        # c_dir = os.path.abspath(os.path.dirname(sys.executable))
        # argos-pbtail.exe 실행
        start_pbtail(g_dir)
        # 일단은 윈도우만 실행된다고 가정
        set_venv(g_dir + r'\venv')
        # %HOME%argos-rpa.venv 에 Python37-32 에 원본 확인 및 복사
        py_root = os.path.join(str(Path.home()), '.argos-rpa.venv')
        if not os.path.exists(py_root):
            os.makedirs(py_root)
        if not os.path.exists(os.path.join(py_root, 'Python37-32', 'python.exe')):
            sta.log(StatLogger.LT_1, 'Installing Python 3. It may take some time.')
            zip_file = os.path.join(os.path.abspath(sys._MEIPASS), 'Python37-32.zip')
            if not os.path.exists(zip_file):
                raise RuntimeError('Cannot find "%s"' % zip_file)
            tmpdir = tempfile.mkdtemp(prefix='py37-32_')
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)
            if os.path.exists(os.path.join(py_root, 'Python37-32')):
                shutil.rmtree(os.path.join(py_root, 'Python37-32'))
            shutil.move(os.path.join(tmpdir, 'Python37-32'), py_root)
        # g_dir\venv\pyvenv.cfg 덮어씀
        with open(os.path.join(g_dir, 'venv', 'pyvenv.cfg'), 'w',
                  encoding='utf-8') as ofp:
            ofp.write('''home = %s
include-system-site-packages = false
version = 3.7.3
''' % os.path.join(py_root, 'Python37-32'))
        return 0
    finally:
        if tmpdir and os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)


################################################################################
def _main(argv=None):
    sta = StatLogger(is_clear=True)
    sta.log(StatLogger.LT_1, 'Preparing STU and PAM.')
    if getattr(sys, 'frozen', False):
        ppm_exe_init(sta)
    cwd = os.getcwd()
    try:
        # dcf = get_repository_env()
        # noinspection PyTypeChecker
        parser = ArgumentParser(
            description='''ARGOS-LABS Plugin Package Manager''',
            formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('--new-py', action='store_true',
                            help='making new python venv environment at py.%s' %
                            sys.platform)
        parser.add_argument('--venv', action='store_true',
                            help='if set use package top py.%s for virtual env.'
                                 ' If not set. Use system python instead.'
                                 % sys.platform)
        parser.add_argument('--self-upgrade', '-U', action='store_true',
                            help='If set this flag self upgrade this ppm.')
        parser.add_argument('--clean', '-c', action='store_true',
                            help='clean all temporary folders, etc.')
        parser.add_argument('--verbose', '-v', action='count', default=0,
                            help='verbose output eg) -v, -vv, -vvv, ...')
        parser.add_argument('--pr-user',
                            help="user id for private plugin repository command")
        parser.add_argument('--pr-user-pass',
                            help="user passwd for private plugin repository command")
        parser.add_argument('--pr-user-auth',
                            help="user authentication for private plugin repository command, usually this is for program")
        parser.add_argument('--on-premise', action='store_true',
                            help="If this flag is set applied to on-premise environment")
        parser.add_argument('--plugin-index',
                            help="Set official plugin index, default is https://pypi-official.argos-labs.com/pypi")

        subps = parser.add_subparsers(help='ppm command help', dest='command')
        ########################################################################
        # ppm functions
        ########################################################################
        _ = subps.add_parser('test', help='test this module')
        _ = subps.add_parser('build', help='build this module')
        ss = subps.add_parser('submit', help='submit to upload server')
        _ = ss.add_argument('--submit-key',
                            help="token key to submit")
        ss.add_argument('submit_url',
                        help="URL to submit for plugin")
        sp = subps.add_parser('upload', help='upload this module to pypi server')
        sp.add_argument('repository_name', nargs='?',
                        help="repository name from the list of private repositories. "
                             "If not specified then first item from private-repositories list.")
        _ = subps.add_parser('clear', help='clear all temporary folders')
        _ = subps.add_parser('clear-py',
                             help='clear py.%s virtual environment'
                                  % sys.platform)
        _ = subps.add_parser('clear-all',
                             help='clear all temporary folders and '
                                  'virtual environment')
        # _ = subps.add_parser('unique', help='Check for uniqueness for the pkgname and display name')

        ########################################################################
        # get command
        ########################################################################
        sp = subps.add_parser('get', help='get command')
        sp.add_argument('get_cmd', metavar='get_sub_cmd',
                        choices=['version', 'repository', 'trusted-host', 'private'],
                        help="get command {'version', 'repository', 'trusted-host', 'private'}")

        ########################################################################
        # plugin command
        ########################################################################
        sp = subps.add_parser('plugin', help='plugin command')
        sp.add_argument('plugin_cmd',
                        choices=[
                            'get', 'dumpspec', 'venv', 'versions', 'dumppi',
                            'unique', 'selftest', 'venv-clean',
                        ],
                        help="""plugin command, one of {'get', 'dumpspec', 'venv', 'versions', 'dumppi', 'unique', 'selftest', 'venv-clean']}.
   - get : get plugin info for STU
   - dumpspec : get plugin spec for STU
   - venv : making virtual environment for PAM
   - versions : get versions for a plugin
   - dumppi : dump all pypi index for mirroring to a folder
   - unique : check for uniqueness for the pkgname and display name of plugin
   - selftest : self test for plugin and report in case of failure
""")
        sp.add_argument('plugin_module',
                        nargs="*",
                        help="plugin module name eg) argoslabs.demo.helloworld or argoslabs.demo.helloworld==1.327.1731")
        # 2019.07.27 : 다음의 plugin 의존적인 --user, --user-auth 옵션은 놔두고
        # --pr-puser, --pr-user-auth 전체 옵션 추가
        sp.add_argument('--user',
                        help="user id for plugin command")
        sp.add_argument('--user-auth',
                        help="user authentication for plugin command")
        sp.add_argument('--pam-id',
                        help="PAM ID(mac addr or uuid) for plugin command")
        sp.add_argument('--startswith',
                        help="module filter to start with")
        sp.add_argument('--official-only', action="store_true",
                        help="do plugin command with official repository only")
        sp.add_argument('--private-only', action="store_true",
                        help="do plugin command with private repository only")
        sp.add_argument('--short-output', action="store_true",
                        help="just print module name and version only")
        sp.add_argument('--flush-cache', action="store_true",
                        help="dumpspec.json will be cached. If this flag is set, clear all cache first.")
        sp.add_argument('--last-only', action="store_true",
                        help="get or dumpspec last version only.")
        sp.add_argument('--with-dumpspec', action="store_true",
                        help="dumpspec.json will be added in result of get result. If --short-output is set, this option is not applied.")
        sp.add_argument('--dumppi-folder',
                        help="module filter to start with")
        sp.add_argument('--outfile',
                        help="filename to save the stdout into a file")
        sp.add_argument('--requirements-txt',
                        help="filename to read modules from requirements.txt instead plugin_module parameters")
        sp.add_argument('--without-cache', action='store_true',
                        help="module filter to start with")
        sp.add_argument('--venv-dir',
                        help="self testing directory for virtual environment")
        sp.add_argument('--selftest-email',
                        help="self testing report email, default is plugin@argos-labs.com")

        ########################################################################
        # pip command
        ########################################################################
        sp = subps.add_parser('install', help='install module')
        sp.add_argument('subargs', metavar='module', nargs=argparse.REMAINDER,
                        help='module[s] to install')
        sp = subps.add_parser('show', help='show module info')
        sp.add_argument('subargs', metavar='module', nargs=argparse.REMAINDER,
                        help='module[s] to show information')
        sp = subps.add_parser('uninstall', help='uninstall module')
        sp.add_argument('subargs', metavar='module', nargs=argparse.REMAINDER,
                        help='module[s] to uninstall')
        sp = subps.add_parser('search', help='search keywords')
        sp.add_argument('subargs', metavar='keyword', nargs=argparse.REMAINDER,
                        help='search module which have keywords')
        # sp = subps.add_parser('dumpspec', help='dumpspec keywords')
        # sp.add_argument('modulename',
        #                 help='dumpspec module which have modulename')
        _ = subps.add_parser('list', help='list installed module')
        _ = subps.add_parser('list-repository',
                             help='list all modules at remote')

        ########################################################################
        # direct command
        ########################################################################
        sp = subps.add_parser('pip', help='pip command')
        sp.add_argument('subargs', metavar='pip-arguments',
                        nargs=argparse.REMAINDER,
                        help='pip arguments (if option is first needed then '
                             'use pass first)')
        sp = subps.add_parser('py', help='python command')
        sp.add_argument('subargs', metavar='python-arguments',
                        nargs=argparse.REMAINDER,
                        help='python arguments (if option is first needed then '
                             'use pass first)')
        sp = subps.add_parser('setup', help='setup command with setup.yaml')
        sp.add_argument('subargs', metavar='setup-arguments',
                        nargs=argparse.REMAINDER,
                        help='setup arguments (if option is first needed then '
                             'use pass first)')
        # sys.stderr.write('<<SYS.argv="%s">>' % sys.argv)

        args = parser.parse_args(args=argv)
        setattr(args, '_cwd_', cwd)
        if args.verbose > 0:
            print(str(args).replace('Namespace', 'Arguments'))
        if not args.command:
            sys.stderr.write('Need command for ppm.\n')
            parser.print_help()
            return False
        else:
            if os.path.exists(OUT_PATH):
                os.remove(OUT_PATH)
            if os.path.exists(ERR_PATH):
                os.remove(ERR_PATH)
            # loglevel = logging.INFO if args.verbose <= 0 else logging.DEBUG
            loglevel = logging.DEBUG
            try:
                logger = get_logger(LOG_PATH, loglevel=loglevel)
                _venv = VEnv(args, logger=logger)
                ppm = PPM(_venv, args, logger=logger, sta=sta)
                return ppm.do()
            finally:
                logging.shutdown()
    finally:
        sta.log(StatLogger.LT_1, 'Preparing STU and PAM is done.')
        global pbtail_po
        if pbtail_po is not None:
            # noinspection PyUnresolvedReferences
            pbtail_po.wait()
            # pbtail_po.terminate()
            StatLogger().clear()
        os.chdir(cwd)


################################################################################
def main(argv=None):
    try:
        r = _main(argv)
        sys.exit(r)
    except Exception as err:
        _exc_info = sys.exc_info()
        _out = traceback.format_exception(*_exc_info)
        del _exc_info
        sys.stderr.write('%s\n' % ''.join(_out))
        sys.stderr.write('%s\n' % str(err))
        sys.stderr.write('  use -h option for more help\n')
        sys.exit(9)
