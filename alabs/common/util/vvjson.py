"""
====================================
 :mod:`alabs.common.util.vvjson` JSON 및 XML 관련 작업 (XPath)
====================================
.. moduleauthor:: 채문창 <mcchae@vivans.net>
.. note:: ARGOS-LABS License
"""
# 설명
# =====
#
# 비정형 자료는 다음과 같이 호환가능
#
# XML <=> Python(OrderedDict) <=> JSON <=> BSON(mongoDB)
#
# 이와 관련된 작업 포함
#
# 관련 작업자
# ===========
#
# 본 모듈은 다음과 같은 사람들이 관여했습니다:
#    * 채문창
#
# 작업일지
# --------
#
# 다음과 같은 작업 사항이 있었습니다:
#
#  * [2019/03/15]
#     - set_xpath에서 최초 없던 상태에서 ABC/DEV[1] 에 값을 넣는 것
#  * [2019/03/12]
#     - change set_xpath for a[1][2]/b[3][4] for multiple index
#  * [2019/03/11]
#     - change get_xpath for a[1][2]/b[3][4] for multiple index
#  * [2017/10/19]
#     - add safe_jsonify
#  * [2017/04/10]
#     - 본 모듈 작업 시작

################################################################################
import re
import datetime
import collections
from io import StringIO
try:
    # noinspection PyPackageRequirements
    from bson.objectid import ObjectId
except ImportError:
    ObjectId = str
try:  # pragma no cover
    from collections import OrderedDict
except ImportError:  # pragma no cover
    OrderedDict = dict
xmlrpclib = __import__('xmlrpc.client')
# next is for DeprecationWarning: Using or importing the ABCs from 'collections'
#   instead of from 'collections.abc' is deprecated, and in 3.8 it will stop
#   working
try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping

################################################################################
__author__ = "MoonChang Chae <mcchae@vivans.net>"
__date__ = "2017/04/10"
__version__ = "1.17.0410"
__version_info__ = (1, 17, 410)
__license__ = "MIT"


################################################################################
def safe_jsonify(data):
    """dict 혹은 list 멤버 등을 돌면서 다음과 같은 작업 수행
        - unicode 이면 utf8로 변환하여 리턴
        - 문자열이면 문자열 리턴
        - dict 이면 이를 해체하여 개별 키:값 쌍을 Recursive 하게 호출하여 재조립
        - list나 tuple 이면 이를 해체하여 개별 값 요소를 Recursive 하게 호출하여 재조립
        - datetime은 flask-restplus 에서 오류가 발생하므로 isoformat() 변환

    :param data: 변환을 위한 객체

    >>> d = { u'spam': u'eggs', u'foo': True, u'foo': { u'baz': 97 } }
    >>> print d
    {u'foo': True, u'foo': {u'baz': 97}, u'spam': u'eggs'}
    >>> d2 = convert_str(d)
    >>> print d2
    {'foo': True, 'foo': {'baz': 97}, 'spam': 'eggs'}
    """
    if isinstance(data, dict) \
            and '_id' in data and isinstance(data[u'_id'], ObjectId):
        data[u'_id'] = str(data[u'_id'])
    if isinstance(data, str):
        return data
    elif isinstance(data, Mapping):
        return dict(map(safe_jsonify, data.items()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(safe_jsonify, data))
    elif isinstance(data, (datetime.date, datetime.datetime)):
        return data.isoformat()
    return data


################################################################################
def convert_str(data):
    """dict 혹은 list 멤버 등을 돌면서 다음과 같은 작업 수행
        - unicode 이면 utf8로 변환하여 리턴
        - 문자열이면 문자열 리턴
        - dict 이면 이를 해체하여 개별 키:값 쌍을 Recursive 하게 호출하여 재조립
        - list나 tuple 이면 이를 해체하여 개별 값 요소를 Recursive 하게 호출하여 재조립

    :param data: 변환을 위한 객체

    >>> d = { u'spam': u'eggs', u'foo': True, u'foo': { u'baz': 97 } }
    >>> print d
    {u'foo': True, u'foo': {u'baz': 97}, u'spam': u'eggs'}
    >>> d2 = convert_str(d)
    >>> print d2
    {'foo': True, 'foo': {'baz': 97}, 'spam': 'eggs'}
    """
    if isinstance(data, str):
        return data
    elif isinstance(data, collections.Mapping):
        return dict(map(convert_str, data.items()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert_str, data))
    return data


################################################################################
def convert_safe_str(data):
    """ 이전의 :func:`convert_str` 에 아래의 체크 추가
        - 만약 data가 dict이고 u'_id' 라는 키를 가지고 있으며, 해당 키값이
            bson.objectid.ObjectId 인스턴스인 경우 해당 값을 str()로 변환
        - 만약 해당 data 값이 int 인데 xmlrpclib.MAXINT 값 보다 더 크면 해당 값을
            long()으로 캐스팅하여 리턴

            .. warning:: long으로 캐스팅을 안 한 경우, XML-RPC를 통하여 해당 값을 읽을 때
                4바이트 정수 값을 넘으면 오류 예외 발생함
        - 기타인 경우 convert_str과 동일한 과정 수행
    :param data: 변환을 위한 객체
    """
    if isinstance(data, dict) \
            and '_id' in data and isinstance(data[u'_id'], ObjectId):
        data[u'_id'] = str(data[u'_id'])
    if isinstance(data, int):
        return int(data)
    if isinstance(data, str):
        return data
    if isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert_safe_str, data.items()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert_safe_str, data))
    else:
        return data


################################################################################
make_safe_json = convert_safe_str


################################################################################
def get_python_val(value, to_lower=False):
    """문자열인데 파이썬 변환 가능한 값으로 변환가능하면 변환하여 리턴
        - unicode 이면 utf8로 변환
        - 문자열인데 int로 변환 가능하면 변환
        - 문자열인데 float로 변환 가능하면 변환
        - 소문자가 ('false','off') 속하면 False로 변환
        - 소문자가 ('true','on') 속하면 True로 변환
        - 소문자가 ('none','null') 속하면 None로 변환

    :param value: 원본 값
    :param bool to_lower: 소문자로 강제 변환할 것인가 하는 플래그 (디폴트 False)
    :return: object 파이썬으로 변환된 값 (str, int, long, float, bool, None, object 등)
    """
    v = value
    if v is None:
        return v
    if isinstance(v, str):
        if to_lower:
            v = v.lower()
        # 문자열 값에서 INT 혹은 FLOAT 등의 상수가 있는지 체크
        # 2014/03/19 CID를 base64 encoding 안된 상태에서
        # float('000000006E0600001400010000000000') 가 inf 로 return 되는 경우 발생
        # 따라서 2^64 의 길이 (21)을 넘어서는 문자열은 그냥 문자열로 리턴
        if len(v) > 21:
            return v
        trans = False
        if not trans:
            # noinspection PyBroadException
            try:
                v = int(v)
                trans = True
            except Exception:
                pass
        if not trans:
            # noinspection PyBroadException
            try:
                v = float(v)
                trans = True
            except Exception:
                pass
        # xtm chk_setting 을 1.0에서는 on/off로 표기하여 강제로 true/false로 변환했으나
        # 다시 장비로 적용 시 형변환을 해야하므로 on/off는 그대로 표기하고
        # true/false 일경우에만 python boolean 값으로 변환한다
        if not trans:
            # if v.lower() in ('false','off'): v = False;trans=True
            if v.lower() in ('false',):
                v = False
                trans = True
        if not trans:
            # if v.lower() in ('true','on'): v = True;trans=True
            if v.lower() in ('true',):
                v = True
                trans = True
        if not trans:
            if v.lower() in ('none', 'null'):
                v = None
                # trans = True
    return v


################################################################################
def postprocessor(path, key, value):
    """XML 문자열을 xmltodict로 변환할 때, xmltodict.parse 등을 할 때 후처리를 담당할 함수

    :param str path: 경로명
    :param str key: XML의 태그 혹은 속성명이 변경된 키 값

        .. note:: XML의 경우 해당 태그명 혹은 속성명이 모두 소문자로 구분해야 할 필요가 있어
            모두 소문자로 변경되었음

    :param str value: 속성값 태그값 등의 값

        .. note:: 값은 :func:`get_python_val` 를 거친 값

    :return: (key, value) 의 변환된 값

    .. warning:: 본 함수는 아래와 같이 xmltodict.parse 에 사용됨

    # >>>    with open('test.xml') as ifp:
    # ...        xmldict = xmltodict.parse(ifp, postprocessor=postprocessor)
    """
    _ = path
    k = key
    v = value
    if isinstance(k, str):
        k = k.lower()
    if v is None:
        return k, v
    return k, get_python_val(v)


################################################################################
def decode_list(data):
    """list 객체 디코드
    각 list의 원소를 읽어 다음과 같은 작업 수행
        - 만약 unicode면 utf8로 인코딩 된 결과 문자열
        - 만약 nest된 list라면 재귀 호출
        - 만약 nest된 dict라면 decode_dict를 재괴 호출

    :param data: 디코드할 객체
    :return: 새로 변경된 값을 채운 list 객체

    .. note:: decode_dict 에서 호출됨
    """
    rv = []
    for item in data:
        if isinstance(item, list):
            item = decode_list(item)
        elif isinstance(item, dict):
            item = decode_dict(item)
        rv.append(item)
    return rv


################################################################################
def decode_dict(data, case_sensitive=False):
    """dict 객체 디코드
    각 dict의 key:value를 읽어 value에 대하여 다음과 같은 작업 수행 후 새로운 dict에 채움
        - 만약 value가 dict이면 재귀 호출
        - 만약 value가 list이면 decode_list 재귀 호출
        - 그렇지 않으면 get_python_val 결과값

    :param data: 디코드할 객체
    :param bool case_sensitive: 만약 False이면 키 값을 모두 소문자로 변경 (디폴트 False)
    :return: 새로 변경된 값을 채운 dict 객체

    # >>> xmldict = xmltodict.parse(xmlstr, postprocessor=vvjson.postprocessor)
    # >>> jstr = json.dumps(xmldict)
    # >>> js = json.loads(jstr, object_hook=vvjson.decode_dict)
    """
    rv = {}
    for key, value in data.items():
        if isinstance(key, str):
            if not case_sensitive:
                key = key.lower()
        if isinstance(value, list):
            value = decode_list(value)
        elif isinstance(value, dict):
            value = decode_dict(value)
        else:
            # 아래의 getPythonVal에서 to_loser 값을 True로 준 결과 Side-Effect 가 너무 많음
            value = get_python_val(value)
        rv[key] = value
    return rv


################################################################################
def decode_dict_cs(data):
    """dict 객체 디코드
    각 dict의 key:value를 읽어 value에 대하여 다음과 같은 작업 수행 후 새로운 dict에 채움
        - 만약 value가 dict이면 재귀 호출
        - 만약 value가 list이면 decode_list 재귀 호출
        - 그렇지 않으면 get_python_val 결과값

    :param data: 디코드할 객체
    :return: 새로 변경된 값을 채운 dict 객체

    .. warning:: decode_dict_cs는 decode_dict(data, case_sensitive=True)를 호출함으로써
        무조건 dict의 키 값을 소문자로 변경합니다

    # >>> xmldict = xmltodict.parse(xmlstr, postprocessor=vvjson.postprocessor)
    # >>> jstr = json.dumps(xmldict)
    # >>> js = json.loads(jstr, object_hook=vvjson.decode_dict_cs)
    """
    return decode_dict(data, case_sensitive=True)


################################################################################
# noinspection RegExpSingleCharAlternation
def get_xpath(d, xpath, raise_exception=False, default_value=None):
    """XML 접근 방법으로 XPath가 있듯이 유사한 방법으로 파이썬의 dict를 XPath로 접속하는 함수

    :param dict d: 정보를 담고 있을 파이썬의 dict 객체
    :param str xpath: XPath 접근 문자열 (예, "/foo/lst[0]/@name2")
    :param bool raise_exception:
        - 만약 True 이고 접근이 불가능하면 ReferenceError 예외발생
        - 만약 False 이고 접근이 불가능하면 None 리턴
        - 디폴트는 False
    :param default_value: 만약 loop up 실패시 return 되는 디폴트 값
    :return: object dict에서 XPath 해당 값
    :raises ReferenceError: 만약 raise_exception 패러미터가 True 이고 접근이
        불가능하면 ReferenceError 예외발생 (디폴트 False)

    >>> ud = { u'spam': u'eggs', u'foo': True, u'foo': { u'baz': 97,
    ... 'lst':[{'@name':'aaa'},{'@name':'bbb'},{'@name':'ccc'},]}}
    >>> print ud[u'foo']['baz'] # dict 를 바로 접근함
    97
    >>> get_xpath(ud,'/foo/baz') # XPath 형식으로 가져옴
    97
    """
    if not isinstance(d, dict):
        if raise_exception:
            raise ReferenceError('vvjson.get_xpath: Invalid type <%s> must dict'
                                 % type(d))
        return default_value
    try:
        if xpath.strip() == '/':
            return d
        xeles = re.split(r'/|\[', xpath.strip('/'))
        for xele in xeles:
            xele = xele.strip()
            if xele[-1] == ']':
                xndx = int(xele[:-1])
                if not isinstance(d, (list, tuple)):
                    if xndx == 0:
                        continue  # regards /a[0] == /a
                    if raise_exception:
                        raise ReferenceError('vvjson.get_xpath: '
                                             'Invalid Index <%s>' % xndx)
                    return default_value
                d = d[xndx]
            else:
                d = d[xele]
        return d
    except KeyError as e:
        if raise_exception:
            raise ReferenceError('vvjson.get_xpath: Invalid Key <%s>'
                                 % str(e))
    except Exception as e:
        if raise_exception:
            raise ReferenceError('vvjson.get_xpath: Error <%s>' % str(e))
        return default_value


################################################################################
# noinspection RegExpSingleCharAlternation
def set_xpath(d, xpath, xval, is_make_attribute=True, is_delete=False):
    """파이썬의 dict 객체를 XPath로 특정 값을 설정하는 함수

    :param dict d: 정보를 담고 있을 파이썬의 dict 객체
    :param str xpath: 설정할 XPath 접근 문자열 (예, "/foo/lst[0]/@name2")
    :param object xval: 설정할 값 (어떠한 파이썬 객체/값도 OK)
    :param bool is_make_attribute:
        - 만약 True 이고 접근이 불가능하면 해당 내용을 접근 가능하도록 dict d를 수정
        - 만약 False 이고 접근이 불가능하면 None 리턴
        - 디폴트는 False
    :param bool is_delete:
        - 만약 True이면 xval의 값에 관계 없이 해당 키를 삭제함
        - 디폴트는 False
    :return: 불리언 리턴
        - True : 성공적으로 d의 xpath위치에 xval을 설정한 경우
        - False : 그렇지 않으면
    :raises ReferenceError: 만약 d가 dict가 아니면

    >>> ud = {u'foo': True, u'foo': {'lst': [{'@name': 'aaa'}, \
    {'@name': 'bbb'}, {'@name': 'ccc'}], u'baz': 97}, u'spam': u'eggs'}
    >>> set_xpath(ud, '/foo', 123)
    True
    >>> ud
    {u'foo': 123, u'foo': {'lst': [{'@name': 'aaa'}, {'@name': 'bbb'},
    {'@name': 'ccc'}], u'baz': 97}, u'spam': u'eggs'}
    >>> set_xpath(ud, '/foo', None, is_delete=True)
    True
    >>> ud
    {u'foo': 123, u'spam': u'eggs'}

    .. warning:: 만약 주어진 xpath 로 접근 할 수 없고 is_make_attribute가 True이면

        - 특정 키였다면 해당 키를 만듦
        - 특정 목록을 접근하는데 접근 길이가 해당 list의 길이보다 크다면 해당 목록을
            None 항목으로 생성
    """
    if not isinstance(d, dict):
        raise ReferenceError('vvjson.set_xpath: Invalid type <%s> must dict'
                             % type(d))
    try:
        xeles = re.split(r'/|\[', xpath.strip('/'))
        last_ndx = len(xeles) - 1
        for i, xele in enumerate(xeles):
            xele = xele.strip()
            if xele[-1] == ']':
                xndx = int(xele[:-1])
                if not isinstance(d, (list, tuple)):
                    return False
                if len(d) <= xndx:
                    if is_make_attribute:
                        extlst = [None for _ in range(len(d), xndx + 1)]
                        d.extend(extlst)
                    else:  # out of index
                        return False
                if i == last_ndx:
                    if is_delete:
                        del d[xndx]
                    else:
                        d[xndx] = xval
                else:
                    if xeles[i+1][-1] == ']':
                        d[xndx] = []
                    else:
                        d[xndx] = {}
                    d = d[xndx]
            else:
                if not (is_make_attribute or xele in d):
                    return False
                if i == last_ndx:
                    if is_delete:
                        del d[xele]
                    else:
                        d[xele] = xval
                else:
                    if xele not in d:
                        if xeles[i + 1][-1] == ']':
                            d[xele] = []
                        else:
                            d[xele] = {}
                    d = d[xele]
        return True
    except Exception as e:
        raise ReferenceError('vvjson.set_xpath: Error <%s>' % str(e))


################################################################################
def get_safe_int(istr):
    """안전한 Int 값 구하기

    :param str istr: 정수 문자열
    :return: int 정수 값 리턴

    .. warning:: 만약 정수로 변환할 수 없는 istr 문자열이라면 -1을 리턴
    """
    # noinspection PyBroadException
    try:
        return int(istr)
    except Exception:
        return -1


################################################################################
def get_safe_len(obj):
    """안전한 객체 길이 구하기

    :param object obj: 길이를 구할 객체
    :return: int 길이 값 리턴

    .. warning:: 만약 길이를 구할 수 없는 객체라면 -1을 리턴
    """
    # noinspection PyBroadException
    try:
        # noinspection PyTypeChecker
        return len(obj)
    except Exception:
        return -1


################################################################################
def get_safe_list(obj):
    """안전한 list 혹은 tuple객체 구하기

    :param object obj: 처리하고픈 객체
    :return: list 혹은 tuple

    .. note:: 다음과 같은 결과를 리턴하게 됨

        - 만약 None이면 [] 리턴
        - 만약 list 객체면 해당 객체 리턴
        - 만약 tuple 객체면 해당 객체 리턴
        - 기타 객체라면 [ obj ] 리턴
    """
    if obj is None:
        return []
    if isinstance(obj, (list, tuple)):
        return obj
    return [obj]  # in case of single obj


################################################################################
def get_safe_val(d, t, raise_exception=False):
    """파이썬의 dict를 tuple의 항목으로 접근하여 해당 값을 구하는 함수

    :param dict d: 정보를 담고 있을 파이썬의 dict 객체
    :param tuple t: 문자열 tuple. 예, ('foo','lst',0,'@name2')
    :param bool raise_exception:
        - 만약 True 이고 접근이 불가능하면 ReferenceError 예외발생
        - 만약 False 이고 접근이 불가능하면 None 리턴
        - 디폴트는 False
    :return: object dict에서 tuple로 찾은 해당 값

    >>> ud = {u'foo': 123, u'foo': {'lst': [{'@name': 'aaa'}, {'@name': 'bbb'},\
     {'@name': 'ccc'}], u'baz': 97}, u'spam': u'eggs'}
    >>> get_safe_val(ud,(u'foo',u'lst',1,'@name'))
    'bbb'
    """
    xpath = ''
    for x in t:
        if isinstance(x, int):
            xpath += '[%d]' % x
        else:
            xpath += '/%s' % x
    return get_xpath(d, xpath, raise_exception=raise_exception)


################################################################################
def set_safe_val(d, t, v, raise_exception=False):
    """파이썬의 dict를 tuple의 항목으로 접근하여 주어진 값으로 설정하는 함수

    :param dict d: 정보를 담고 있을 파이썬의 dict 객체
    :param tuple t: 문자열 tuple. 예, ('foo','lst',0,'@name2')
    :param object v: 값을 넣을 객체 값
    :param bool raise_exception:
        - 만약 True 이고 접근이 불가능하면 ReferenceError 예외발생
        - 만약 False 이고 접근이 불가능하면 None 리턴
        - 디폴트는 False
    :return: object dict에서 tuple로 찾은 해당 값

    >>> ud = {u'foo': True, u'foo': {'lst': [{'@name': 'aaa'}, \
    {'@name': 'bbb'}, {'@name': 'ccc'}], u'baz': 97}, u'spam': u'eggs'}
    >>> set_safe_val(ud, (u'foo',), 123)
    True
    >>> ud
    {u'foo': 123, u'foo': {'lst': [{'@name': 'aaa'}, {'@name': 'bbb'}, \
    {'@name': 'ccc'}], u'baz': 97}, u'spam': u'eggs'}
    """
    xpath = ''
    for x in t:
        if isinstance(x, int):
            xpath += '[%d]' % x
        else:
            xpath += '/%s' % x
    return set_xpath(d, xpath, v, is_make_attribute=not raise_exception)


################################################################################
# noinspection PyUnresolvedReferences,PyStringFormat
def _dict2xml(key, val, output, depth=0, attr_prefix='@', cdata_key='#text'):
    if key.startswith("_"):
        return
    if val is not None and isinstance(val, list) and len(val) == 0:
        return
    output.write('\n%s<%s' % ('\t'*depth, key))
    if val is None:
        if depth == 0:
            output.write('>\n</%s>' % key)
        else:
            output.write('></%s>' % key)
    elif isinstance(val, str) or isinstance(val, str):
        output.write('>%s</%s>' % (val, key))
    elif type(val) in (int, float):
        output.write('>%d</%s>' % (val, key))
    elif type(val) is bool:
        output.write('>%s</%s>' % ('true' if val is True else 'false', key))
    elif isinstance(val, dict) or isinstance(val, OrderedDict) \
            or isinstance(val, list):
        vlist = val if isinstance(val, list) else [val]
        # for val in vlist:
        for i in range(len(vlist)):
            val = vlist[i]
            if i > 0:
                output.write('\n%s<%s' % ('\t'*depth, key))
            _has_attr = False
            _has_other = False
            _cd_text = ''
            if isinstance(val, str) or isinstance(val, int):
                output.write('>%s</%s>' % (val, key))
            else:
                for k, v in val.items():
                    if k.startswith(attr_prefix):
                        _has_attr = True
                    elif k == cdata_key:
                        _cd_text = v
                    else:
                        if not k.startswith("_"):
                            _has_other = True
                if not _has_other and not _has_attr:
                    output.write('>%s</%s>' % (_cd_text, key))
            if _has_attr:
                for k, v in val.items():
                    if k.startswith(attr_prefix):
                        if type(v) is bool:
                            output.write(' %s="%s"' %
                                         (k[1:], 'on' if v is True else 'off'))
                        elif k == "@cid" \
                                and v == "00000000000000000000000000000000":
                            # cid(ANY)일 경우 xtm에서는 null로 변경해야한다.
                            output.write(' %s="%s"' % (k[1:], 'null'))
                        else:
                            output.write(' %s="%s"' % (k[1:], v))
                if _has_other:
                    output.write('>')
                elif _cd_text != '':
                    output.write('>%s</%s>' % (_cd_text, key))
                else:
                    output.write(' />')
            if _has_other:
                if not _has_attr: 
                    output.write('>')
                for k, v in val.items():
                    if not k.startswith(attr_prefix) and k != cdata_key:
                        _dict2xml(k, v, output, depth+1)
                output.write('\n%s</%s>' % ('\t'*depth, key))
    else:
        print('unknown value types [%s]' % type(val))


################################################################################
def dict2xml(jsondict, output=None):
    if output is None:
        output = StringIO()

    # ((key, val),)    = jsondict.items()
    for key, val in jsondict.items():
        _dict2xml(key, val, output)
    return output


################################################################################
def dict2xml_ex(jsondict, root_tag=None, idepth=0):
    _dict = {}
    output = StringIO()
    if root_tag is not None:
        _dict[root_tag] = convert_safe_str(jsondict)
    else:
        _dict = convert_safe_str(jsondict)

    try:
        if _dict is not None:
            for key, val in _dict.items():
                _dict2xml(key, val, output, depth=idepth)
    except Exception as e:
        print("dict2xml_ex Error [%s] : %s" % (root_tag, e))
        pass

    return output


################################################################################
# noinspection PyStatementEffect,PyBroadException
def do_test():
    """테스트 함수

    :return: bool 다음의 값을 리턴

        - True : 성공적으로 테스트 완수
        - False : 어딘가에 실패한 결과 있음
    """
    ud = {
        u'spam': u'eggs', u'foo': True,
        u'foo': {
            u'baz': 97,
            'lst': [{'@name': 'aaa'}, {'@name': 'bbb'}, {'@name': 'ccc'}]
        },
        u'aaa': [
            1,
            2,
            [
                3,
                4,
                [
                    5,
                    6,
                    {
                        'ccc': 7,
                        'zzz': 999
                    }
                ]
            ]
        ]
    }
    sd = convert_str(ud)

    if sd['spam'] != 'eggs':
        return False
    if sd['foo'].get('baz') != 97:
        return False

    ut = (u'spam', u'eggs', u'foo', True, u'foo')
    _ = convert_str(ut)
    if sd['spam'] != 'eggs':
        return False

    # test for get_xpath
    if get_xpath(sd, 'aaa[1]') != 2:
        return False
    if get_xpath(sd, 'aaa[2][1]') != 4:
        return False
    if get_xpath(sd, 'aaa[2][2][2]/zzz') != 999:
        return False
    #  org test
    if get_xpath(sd, '/spam') != 'eggs':
        return False
    if get_xpath(sd, '/foo/baz') != 97:
        return False
    if not isinstance(get_xpath(sd, '/foo/lst'), (list, tuple)):
        return False
    if not isinstance(get_xpath(sd, '/foo/lst[2]'), dict):
        return False
    if get_xpath(sd, '/foo/lst[1]/@name') != 'bbb':
        return False
    try:
        get_xpath(sd, '/bar2', raise_exception=True)
        return False
    except Exception:
        pass
    try:
        get_xpath(sd, '/foo/lst[3]', raise_exception=True)
        return False
    except Exception:
        pass
    try:
        get_xpath(sd, '/foo/lst[0]/@name2', raise_exception=True)
        return False
    except Exception:
        pass

    # test for set_xpath
    if not set_xpath(sd, '/spam', 'roll'):
        return False
    if get_xpath(sd, '/spam') != 'roll':
        return False
    if set_xpath(sd, '/@att1', 'foobar', is_make_attribute=False):
        return False
    if not set_xpath(sd, '/@att1', 'foobar'):
        return False
    if not get_xpath(sd, '/@att1') != 'roll':
        return False
    if set_xpath(sd, '/foo/lst[3]', 'lst3', is_make_attribute=False):
        return False
    if not set_xpath(sd, '/foo/lst[5]/@att2/#text', 'att2_text'):
        return False
    if get_xpath(sd, '/foo/lst[5]/@att2/#text') != 'att2_text':
        return False
    if not set_xpath(sd, 'aaa[2][2][2]/zzz', 888):
        return False
    if get_xpath(sd, 'aaa[2][2][2]/zzz') != 888:
        return False
    if set_xpath(sd, 'aaa[5][5][5]', 888, is_make_attribute=False):
        return False
    if not set_xpath(sd, 'aaa[3][4][5]', 888):
        return False
    if get_xpath(sd, 'aaa[3][4][5]') != 888:
        return False
    if not set_xpath(sd, 'aaa[3][4][5]/a/b/c', 777):
        return False
    if get_xpath(sd, 'aaa[3][4][5]/a/b/c') != 777:
        return False
    # empty set
    ed = {}
    if not set_xpath(ed, 'ABC/DEV[1]', 'abcde'):
        return False
    if get_xpath(ed, 'ABC/DEV[1]') != 'abcde':
        return False

    # test getSafe...
    if get_safe_int('f00') != -1:
        return False
    if get_safe_int(' 300 ') != 300:
        return False
    if get_safe_len('f00bar') != 6:
        return False
    if get_safe_len(3) != -1:
        return False
    if get_safe_list(None):
        return False
    if get_safe_list(3) != [3]:
        return False
    if get_safe_list([3, 4]) != [3, 4]:
        return False
    if get_safe_val(ud, (u'foo', 'lst', 1, '@name')) != 'bbb':
        return False
    if not set_safe_val(ud, (u'foo', 'lst', 1, '@name'), 'kkk'):
        return False
    if get_safe_val(ud, (u'foo', 'lst', 1, '@name')) != 'kkk':
        return False

    return True


################################################################################
if __name__ == '__main__':
    print(do_test())
