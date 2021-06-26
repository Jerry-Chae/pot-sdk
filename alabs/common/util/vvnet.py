"""
====================================
 :mod:`alabs.common.util.vvnet` Network util
    Network util
====================================
.. moduleauthor:: 채문창 <mcchae@argos-labs.com>
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
#  * [2019/02/26]
#     - is_svc_opeded 추가
#  * [2018/10/11]
#     - 본 모듈 작업 시작, find_free_port() 작업
################################################################################
import socket
from contextlib import closing


################################################################################
# noinspection PyBroadException
def is_svc_opeded(host, port):
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        if result == 0:
            return True
        return False
    except Exception:
        return False
    finally:
        if sock is not None:
            sock.close()


################################################################################
def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


################################################################################
def get_ipaddress(host='gmail.com', port=80):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((host, port))
    r = s.getsockname()[0]
    s.close()
    return r


################################################################################
if __name__ == '__main__':
    for i in range(2):
        ffp = find_free_port()
        print("find_free_port=%s" % ffp)
    print('get_ipaddress="%s"' % get_ipaddress())
