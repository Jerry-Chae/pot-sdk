"""
====================================
 :mod:`vivans.util.vvhash` 해쉬 관련 함수
====================================
.. moduleauthor:: 채문창 <mcchae@vivans.net>
.. note:: MIT License
"""

# 설명
# =====
#
# 해쉬 관련 기능
#
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
#  * [2017/06/22]
#       - 기존 소스 정리

################################################################################
import hashlib


################################################################################
def get_passwd_hash(passwd):
    hash_object = hashlib.sha256(passwd.encode())
    return hash_object.hexdigest()


################################################################################
def get_file_md5(filename, blocksize=65536):
    afile = open(filename, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()
