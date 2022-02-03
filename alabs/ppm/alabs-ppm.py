"""
====================================
 :mod:alabs-ppm ARGOS-LABS Plugin Module Manager
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS
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
#  * [2022/01/24]
#     - 다시 *.venvInfo clear 하는 부분 해지
#  * [2022/01/22]
#     - MK System에 PAM R21.1021.60 을 새로 실행시키는데 기존 ebot를 제대로 돌리기 위하여
#     - .argos-rpa.cache 가 없을 경우 %appdata%\ARGOS Pam\ArgosRPAUxRobotAgent.V3\ScenarioInfo\ 폴더내
#     - *venvInfo 파일을 모두 지움
#  * [2022/01/20]
#     - 기존 __init__.py 작업했던 부분을 별도로 빼서 alabs.ppm 모듈을 실행하도록 함
#  * [2018/10/31]
#     - 본 모듈 작업 시작
################################################################################
import os
import sys
import glob
import struct
import shutil
import pathlib
import zipfile
import logging
import logging.handlers
import tempfile
import platform
import traceback
import subprocess
from pathlib import Path


################################################################################
LOG_NAME = '.argos-rpa.log'
LOG_PATH = os.path.join(str(Path.home()), LOG_NAME)


################################################################################
def get_logger(logfile,
               logsize=500*1024, logbackup_count=4,
               logger=None, loglevel=logging.DEBUG):
    loglevel = loglevel
    pathlib.Path(logfile).parent.mkdir(parents=True, exist_ok=True)
    if logger is None:
        logger = logging.getLogger(os.path.basename(logfile))
    logger.setLevel(loglevel)
    if logger.handlers is not None and len(logger.handlers) >= 0:
        for handler in logger.handlers:
            logger.removeHandler(handler)
        logger.handlers = []
    loghandler = logging.handlers.RotatingFileHandler(
        logfile,
        maxBytes=logsize, backupCount=logbackup_count,
        encoding='utf8')
    # else:
    #     loghandler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s-%(name)s-%(levelname)s-'
        '%(filename)s:%(lineno)s-[%(process)d] %(message)s')
    loghandler.setFormatter(formatter)
    logger.addHandler(loghandler)
    return logger


################################################################################
def is_valid_install_files(py_root):
    if not os.path.exists(os.path.join(py_root, 'python.exe')):
        return False
    if not os.path.exists(os.path.join(py_root, 'Scripts', 'alabs.ppm.exe')):
        return False
    return True


################################################################################
# noinspection PyUnresolvedReferences,PyProtectedMember
def ppm_exe_init(logger):
    tmpdir = None
    try:
        g_dir = os.path.abspath(sys._MEIPASS)
        logger.info(f'ppm_exe_init: g_dir="{g_dir}"')
        # c_dir = os.path.abspath(os.path.dirname(sys.executable))
        # 일단은 윈도우만 실행된다고 가정
        # set_venv(g_dir + r'\venv')
        # %HOME%argos-rpa.venv 에 Python37-32 에 원본 확인 및 복사
        venv_root = os.path.join(str(Path.home()), '.argos-rpa.venv')
        if not os.path.exists(venv_root):
            os.makedirs(venv_root)
        py_root = os.path.join(venv_root, 'Python37-32')
        if not is_valid_install_files(py_root):
            logger.info('Installing Python 3. It may take some time.')
            zip_file = os.path.join(os.path.abspath(sys._MEIPASS), 'Python37-32.zip')
            logger.info(f'Python37-32 is not installed, trying to unzip "{zip_file}"')
            if not os.path.exists(zip_file):
                raise RuntimeError('Cannot find "%s"' % zip_file)
            tmpdir = tempfile.mkdtemp(prefix='py37-32_')
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)
            if os.path.exists(py_root):
                shutil.rmtree(py_root)
            shutil.move(os.path.join(tmpdir, 'Python37-32'), venv_root)
#         # g_dir\venv\pyvenv.cfg 덮어씀
#         with open(os.path.join(g_dir, 'venv', 'pyvenv.cfg'), 'w',
#                   encoding='utf-8') as ofp:
#             ofp.write(f'''home = {py_root}
# include-system-site-packages = false
# version = 3.7.3
# ''')
        return 0
    finally:
        if tmpdir and os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)


################################################################################
def check_python_version(logger):
    #   - PYTHONPATH unset 후 sys.path의 마지막에
    #     C:\Users\toor\.argos-rpa.venv\Python37-32\Lib\site-packages 추가
    # if sys.platform == 'win32':
    #     if 'PYTHONPATH' in os.environ:
    #         del os.environ['PYTHONPATH']
    #     spdir = r'C:\Users\toor\.argos-rpa.venv\Python37-32\Lib\site-packages'
    #     if os.path.exists(spdir) and spdir not in sys.path:
    #         sys.path.append(spdir)

    # >>> import struct;print( 8 * struct.calcsize("P"))
    # 32
    # >>> import platform
    # >>> platform.python_version_tuple()
    # ('3', '7', '3')
    errmsg = 'It is needed Python interpreter version 3.7.3 32 bits.\n'
    if sys.platform == 'win32':
        errmsg += 'You can download https://www.python.org/ftp/python/3.7.3/python-3.7.3.exe'
    pvt = platform.python_version_tuple()
    archi_32_64 = 8 * struct.calcsize("P")
    # if not getattr(sys, 'frozen', False):
    #     if not (pvt == ('3', '7', '3') and archi_32_64 == 32):
    #         raise RuntimeError(errmsg)
    logger.info(f'alabs-ppm:check_python_version: Python {".".join(pvt)} {archi_32_64}bit interpreter')


# ################################################################################
# def clear_venvinfo():
#     venv_cache = os.path.join(str(Path.home()), '.argos-rpa.cache')
#     if os.path.exists(venv_cache):
#         return False
#     #     - .argos-rpa.cache 가 없을 경우 %appdata%\ARGOS Pam\ArgosRPAUxRobotAgent.V3\ScenarioInfo\ 폴더내
#     #     - *venvInfo 파일을 모두 지움
#     si_folder = os.path.join(os.environ['appdata'], r'ARGOS Pam\ArgosRPAUxRobotAgent.V3\ScenarioInfo')
#     if not os.path.exists(si_folder):
#         return False
#     vi_files = os.path.join(si_folder, '*.venvInfo')
#     for f in glob.glob(vi_files):
#         os.remove(f)

################################################################################
def check_main():
    loglevel = logging.DEBUG
    logger = get_logger(LOG_PATH, loglevel=loglevel)
    check_python_version(logger)
    if getattr(sys, 'frozen', False):
        ppm_exe_init(logger)


################################################################################
def get_embeded_pbtail():
    g_dir = os.path.abspath(sys._MEIPASS)
    exe_f = g_dir + r'\Release\argos-pbtail.exe'
    return exe_f


################################################################################
def do_ppm():
    try:
        # 일부 경우에 미리 설치된 alabs.ppm.exe 를 호출하면 이전 설치되었던 경로를 그대로 읽어 문제됨
        # py_exe = os.path.join(str(Path.home()), '.argos-rpa.venv', 'Python37-32', 'Scripts', 'alabs.ppm.exe')
        py_exe = os.path.join(str(Path.home()), '.argos-rpa.venv', 'Python37-32', 'python.exe')
        cmd = [
            py_exe, '-m', 'alabs.ppm',
        ]
        if getattr(sys, 'frozen', False) and '--argos-pbtail-exe' not in cmd:
            cmd.extend([
                '--argos-pbtail-exe',
                get_embeded_pbtail(),
            ])
        cmd.extend(sys.argv[1:])
        # print(' '.join(cmd))
        po = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
        po.communicate()
        return po.returncode
    except Exception as err:
        _exc_info = sys.exc_info()
        _out = traceback.format_exception(*_exc_info)
        del _exc_info
        sys.stderr.write(''.join(_out) + str(err) + '\n')


################################################################################
if __name__ == '__main__':
    # sys.path 중에 '' 현재 디렉터리를 제일 나중에 찾도록 수정
    if not sys.path[0]:
        sys.path.reverse()
    try:
        # clear_venvinfo()
        check_main()
        r = do_ppm()
        sys.exit(r)
    except Exception as err:
        sys.stderr.write('%s\n' % str(err))
        sys.stderr.write('  use -h option for more help\n')
        sys.exit(9)
