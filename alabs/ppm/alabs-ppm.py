"""
====================================
 :mod:alabs.ppm ARGOS-LABS Plugin Module Manager
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
#  * [2018/10/31]
#     - 본 모듈 작업 시작
################################################################################
import sys
if sys.platform == 'win32':
    import six                  # for pyinstaller
    import packaging            # for pyinstaller
    import packaging.version    # for pyinstaller
    import packaging.specifiers # for pyinstaller
from alabs.ppm import main

################################################################################
if __name__ == '__main__':
    # sys.path 중에 '' 현재 디렉터리를 제일 나중에 찾도록 수정
    if not sys.path[0]:
        sys.path.reverse()
    try:
        _r = main(sys.argv[1:])
        sys.exit(_r)
    except Exception as err:
        sys.stderr.write('%s\n' % str(err))
        sys.stderr.write('  use -h option for more help\n')
        sys.exit(9)
