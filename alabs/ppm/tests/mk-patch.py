"""
====================================
 :mod:mk-patch ARGOS-LABS
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS patch for MK System
"""

################################################################################
import os
import sys
import shutil
import traceback
import subprocess
from pathlib import Path


################################################################################
def get_exe(app_folder):
    for path in Path(app_folder).rglob('alabs-ppm.exe'):
        yield str(path)


################################################################################
def do_cmd(*args):
        cmd = args
        print(' '.join(cmd))
        po = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
        po.communicate()
        return po.returncode


################################################################################
def do_patch(app_folder, patch_exe):
    try:
        last_exe = None
        for exe_path in get_exe(app_folder):
            os.remove(exe_path)
            shutil.copy(patch_exe, exe_path)
            last_exe = exe_path
        if not last_exe:
            # nothing to replace
            return 1
        return do_cmd(last_exe, 'get', 'version')
    except Exception as err:
        _exc_info = sys.exc_info()
        _out = traceback.format_exception(*_exc_info)
        del _exc_info
        sys.stderr.write(''.join(_out) + str(err) + '\n')
        return 99

################################################################################
if __name__ == '__main__':
    # app_folder = r'C:\Users\toor'
    # patch_exe = r'C:\work\tmp\alabs-ppm.exe'
    app_folder = os.environ.get('appdata')
    patch_exe = r"{patch_exe}"
    rc = do_patch(app_folder, patch_exe)
    sys.exit(rc)
