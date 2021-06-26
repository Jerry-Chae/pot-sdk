"""
====================================
 :mod:`alabs.common.util.vvencoding` Network util
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
#  * [2019/06/07]
#     - 본 모듈 작업 시작, get_file_encoding() 작업
################################################################################
# noinspection PyPackageRequirements
import chardet


################################################################################
def get_file_encoding(f, def_encoding='utf-8'):
    try:
        with open(f, encoding=def_encoding) as ifp:
            _ = ifp.read()
            return def_encoding
    except UnicodeDecodeError:
        with open(f, 'rb') as ifp:
            rfs = ifp.read()
        cd = chardet.detect(rfs)
        return cd['encoding']
