"""
====================================
 :mod:`alabs.common.util.vvupdown` SimpleUpload download module

====================================
.. moduleauthor:: 채문창 <mcchae@argos-labs.com>
.. note:: refer
    - http://mcchae.egloos.com/11324796
    - https://hub.docker.com/r/mayth/simple-upload-server/
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
#  * [2019/03/26]
#     - 최초 작업
#     - TODO: static_token: alabs.ppm 에서 submit 시 사용하는 key는
#        pypi.argos-labs.com:25478
#        업로드 서버 (pypi-out 으로 esx 서버에 구축된 것의 docker-compose.yaml에 있는
#        키로 나중에는 vault 서비스에서 받아서 주기적으로 수정되도록 함
################################################################################
import os
import string
import shutil
import unicodedata
from requests import get, post, head
from urllib.parse import quote_plus

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255


################################################################################
def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # replace spaces
    for r in replace:
        filename = filename.replace(r, '_')

    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII',
                                                                      'ignore').decode()
    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename) > char_limit:
        print(
            "Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(
                char_limit))
    return cleaned_filename[:char_limit]


################################################################################
class SimpleDownUpload(object):
    # refer: https://hub.docker.com/r/mayth/simple-upload-server/
    static_token = 'aL0PK2Rhs6ed0mgqLC42'

    # ==========================================================================
    def __init__(self, url, token):
        self.url = url
        self.token = token

    # ==========================================================================
    @staticmethod
    def safe_basename(f):
        f = clean_filename(os.path.basename(f))
        return quote_plus(f)

    # ==========================================================================
    def upload(self, file, saved_filename=None):
        url = '%s/upload' % self.url
        params = {'token': self.token}
        with open(file, 'rb') as ifp:
            fn = self.safe_basename(saved_filename) if saved_filename \
                else self.safe_basename(file)
            multiple_files = [('file', (fn, ifp))]
            r = post(url, params=params, files=multiple_files, verify=False)
        if r.status_code // 10 != 20:
            raise RuntimeError('Cannot upload "%s" to "%s": %s' %
                               (file, url, r.text))
        return True

    # ==========================================================================
    def download(self, remote_file, local_file):
        url = '%s/files/%s?token=%s' % \
              (self.url, os.path.basename(remote_file), self.token)
        r = get(url, stream=True, verify=False)
        if r.status_code == 200:
            with open(local_file, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            return True
        raise RuntimeError('Cannot download "%s": [%s] %s'
                           % (remote_file, r.status_code, r.text))

    # ==========================================================================
    def exists(self, file):
        url = '%s/files/%s?token=%s' % \
              (self.url, self.safe_basename(file), self.token)
        r = head(url, verify=False)
        return r.status_code == 200
