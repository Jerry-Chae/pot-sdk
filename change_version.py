"""
====================================
 :mod:change_version
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
#  * [2018/12/27]
#     - 버전의 마지막 postfix를 년월일, 시분초 로 지정하도록 함
#  * [2018/12/08]
#     - normalize 옵션 추가
#  * [2018/12/06]
#     - 본 모듈 작업 시작
################################################################################
import os
import sys
import yaml
import datetime
import argparse


################################################################################
def change_version(yf, old_ver, new_ver):
    # with open(yf) as ifp:
    #     yfs = ifp.read()
    # with open(yf, 'w') as ofp:
    #     ofp.write(yfs.replace(old_ver, new_ver))
    now = datetime.datetime.utcnow().strftime('%y%m%d-%H%M%S')
    with open(yf) as ifp:
        yc = yaml.load(ifp)
    yc['setup']['version'] = new_ver
    yc['setup']['classifiers'].\
        append('Topic :: Change :: Log :: Auto Build & Release at %s for %s' %
               (now, sys.platform))
    with open(yf, 'w') as ofp:
        yaml.dump(yc, ofp, default_flow_style=False)
    print('"%s" version: "%s" => "%s"' %(yf, old_ver, new_ver))
    return True


################################################################################
def get_version(yf):
    if not os.path.exists(yf):
        raise IOError('Cannot find setup.yaml "%s"' % yf)
    with open(yf) as ifp:
        yc = yaml.load(ifp)
        return yc['setup']['version']


################################################################################
def new_version(ver):
    now = datetime.datetime.utcnow()
    now_ymd = '%02d%02d%02d' % (now.year-2000, now.month, now.day)
    now_hms = '%02d%02d%02d' % (now.hour, now.minute, now.second)
    if not ver:
        ver = '0.1'
    if not isinstance(ver, str):
        ver = str(ver)
    vs = ver.split('.')
    if len(vs) < 4:
        while True:
            vs.append('0')
            if len(vs) == 4:
                break
    if len(vs) > 4:
        vs = vs[:4]
    vs[2] = now_ymd
    vs[3] = now_hms
    return '.'.join(vs)


################################################################################
def new_version_n(ver):
    now = datetime.datetime.utcnow()
    now_ymd = '%02d.%02d%02d' % (now.year-2000, now.month, now.day)
    now_hms = '%02d%02d%02d' % (now.hour, now.minute, now.second)
    return '%s.%s' % (now_ymd, now_hms)


################################################################################
def parse_params():
    parser = argparse.ArgumentParser(
        description='''get version and change version:

Version changing rule is:
  version is seems like: 1.2.180123.8
  Only change third and forth version info (eg. 180123.083456)

    180123.083456
    ==
    Two digits of year

    180123.083456
      ====
      Month and Day
    180123.083456
           ==
           Hour
    180123.083456
             ==
             Minute
    180123.083456
               ==
               Second

  Howevery if '--normalize' or '-n' option is given
    18.1207.131740
    ==
    Two digits of year

    18.1207.131740
       ====
       Month and Day
    18.1207.131740
            ==
            Hour
    18.1207.131740
              ==
              Minute
    18.1207.131740
                ==
                Second
    above VERSION is set  

''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--version', '-v', action='store',
                        help='version info like "1.2.18012308"')
    parser.add_argument('--normalize', '-m', action='store_true',
                        help='Normalized VERSION like "18.1207.10", '
                             'refer help')
    parser.add_argument('--no-convert', '-n', action='store_true',
                        help='Use direct version from setup.yaml')
    parser.add_argument('yamls', metavar='setup-file', nargs='+',
                        help='setup.yaml file path (one or more)')
    args = parser.parse_args()
    return args


################################################################################
if __name__ == '__main__':
    _args = parse_params()
    for yf in _args.yamls:
        ov = get_version(yf)
        if not _args.version:
            if _args.no_convert:
                pass
            else:
                if _args.normalize:
                    _args.version = new_version_n(ov)
                else:
                    _args.version = new_version(ov)
                change_version(yf, ov, _args.version)
