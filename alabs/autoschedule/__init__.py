"""
====================================
 :mod:alabs.autoschedule
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
automatic testing scheduler for plugins
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/09/26]
#     - Starting

################################################################################
import os
import sys
import yaml
import time
import pathlib
import datetime
import requests
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from alabs.common.util.vvlogger import get_logger
from io import StringIO
from tempfile import gettempdir, TemporaryFile


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
            cmd[-1] += f'=={version}'
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

    # # ==========================================================================
    # def do_stats(self):
    #     s_ts = datetime.datetime.now()
    #     self._init_report()
    #     self.prepare_venv(is_clear=self.args.clear_venv)
    #
    #     statdir = self.conf['environment']['statdir']
    #     if not os.path.exists(statdir):
    #         os.makedirs(statdir)
    #
    #     pr = PluginReport(statdir, logger=self.logger)
    #     pr.get_report(s_ts)
    #
    #     e_ts = datetime.datetime.now()
    #     self.email_report_stats(s_ts, e_ts, pr)

    # ==========================================================================
    def do(self):
        # if self.args.stat:
        #     return self.do_stats()
        return self.do_tests()


################################################################################
class AutoTestScheduler(object):
    # ==========================================================================
    def __init__(self, argspec):
        self.argspec = argspec
        self.conf_file = self.argspec.conf
        if not os.path.exists(self.conf_file):
            raise IOError(f'Cannot find Config file "{self.conf_file}"')
        with open(self.conf_file, encoding='utf_8') as ifp:
            self.conf = yaml.load(ifp, yaml.Loader)
        # for internal
        self.logger = get_logger(self.conf['environment']['log'])
        self.logger.info('Starting AutoTest Service...')
        self.stat = {}
        self.curr_ts = None
        self.last_ts = datetime.datetime.now() - datetime.timedelta(
            seconds=self.conf['supervisor']['every_check'])
        self.last_weekly_ts = datetime.datetime.now() - datetime.timedelta(
            days=8)
        self.is_stop = False

    # ==========================================================================
    def get_stat(self):
        date_s = self.last_ts.strftime('%Y-%m-%d')
        params = (
            ('startDate', date_s),
            ('endDate', date_s),
        )
        rp = requests.get(self.conf['supervisor']['api_url'], params=params)
        if rp.status_code // 10 != 20:
            self.logger.error(f'Cannot get statistics API: return code is {rp.status_code}')
            return False
        rj = rp.json()
        try:
            #self.stat = rj['data'][date_s]
            stat_d = {}
            for p_i in rj['data'][date_s]:
                p_v = p_i['plugin_name'], p_i['plugin_version']
                if p_v in stat_d:
                    self.logger.error(f'{p_v} is duplicated at the statistics result!')
                stat_d[p_v] = p_i
            self.stat = stat_d
            return True
        except Exception as err:
            self.logger.error(f'Cannot get statistics Json data from {rj}: {str(err)}')
            self.stat = None
            return False

    # ==========================================================================
    def start(self):
        self.get_stat()
        while not self.is_stop:
            self.curr_ts = datetime.datetime.now()
            self.do_check()
            time.sleep(self.conf['supervisor']['every_check'])
            self.last_ts = self.curr_ts

    # ==========================================================================
    def do_check(self):
        if self.last_ts.day != self.curr_ts.day:
            td = self.curr_ts - self.last_weekly_ts
            if td.days >= 7:
                self.test_weekly()
            self.test_dailly()
        elif self.last_ts.hour != self.curr_ts.hour:
            self.test_hourly()

    # ==========================================================================
    def test_weekly(self):
        self.logger.info('Starting: Weekly Testing')
        try:
            self.check_test('weekly')
            self.last_weekly_ts = self.curr_ts
        finally:
            self.logger.info('Ended: Weekly Testing')

    # ==========================================================================
    def test_daily(self):
        self.logger.info('Starting: Dayly Testing')
        try:
            self.check_test('daily')
        finally:
            self.logger.info('Ended: Dayly Testing')

    # ==========================================================================
    def test_hourly(self):
        self.logger.info('Starting: Hourly Testing')
        try:
            self.check_test('hourly')
        finally:
            self.logger.info('Ended: Hourly Testing')

    # ==========================================================================
    def check_test(self, how_often):
        self.logger.info(f'Starting: {how_often} testing')
        try:
            check_list = self.conf['supervisor']['check_list']
            for cl_i in check_list:
                plugin_name = cl_i['plugin']
                for version in cl_i['versions']:
                    p_v = plugin_name, version
                    if p_v not in self.stat:
                        self.logger.error(f'Cannot find matching {p_v} at statistics')
                    plugin_d = self.stat[p_v]
                    self.do_test(how_often, plugin_d)
        finally:
            self.logger.info(f'Ended: {how_often} testing')

    # ==========================================================================
    def do_test(self, how_often, plugin_d):
        p_v = plugin_d["plugin_name"], plugin_d["plugin_version"]
        if how_often == 'weekly' and plugin_d['weekly'] == 'O':
            self.logger.info(f'Starting: {how_often} testing for {p_v}')
            self.do_plugin_test(*p_v)
        elif how_often == 'daily' and plugin_d['daily'] == 'O':
            self.logger.info(f'Starting: {how_often} testing for {p_v}')
            self.do_plugin_test(*p_v)
        elif how_often == 'hourly' and plugin_d['hourly'] == 'O':
            self.logger.info(f'Starting: {how_often} testing for {p_v}')
            self.do_plugin_test(*p_v)
        else:
            self.logger.error(f'[{p_v}] cannot get testing scheme from statistics item {plugin_d}')

    # ==========================================================================
    def do_plugin_test(self, plugin_name, plugin_version):
        ...


################################################################################
def _main(*args):
    with ModuleContext(
        owner='ARGOS-LABS',
        group='alabs',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Argos Labs ACTiVE Scheduler',
        icon_path=get_icon_path(__file__),
        description='alabs.autoscheduler util for automatic plugin testing scheduler',
    ) as mcxt:
        mcxt.add_argument('--conf', '-c',
                          default='autotest.yaml',
                          help='set config file, default is "autotest.yaml"')
        argspec = mcxt.parse_args(args)

        os.environ['PYTHONIOENCODING'] = 'UTF-8'
        ats = AutoTestScheduler(argspec)
        ats.start()
        return 0


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass

