#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`F33.util.Timer` 1초 혹은 주기마다 어떤 작업을 수행할 경우 이용할 타이머 클래스
====================================
"""

# 설명
# =====
#
# 1초 혹은 주기마다 어떤 작업을 수행할 경우 이용할 타이머 클래스
#
#
# 관련 작업자
# ===========
#
# 작업일지
# --------
#
# 다음과 같은 작업 사항이 있었습니다:
#  * [2015/11/17]
#     - F33용으로 refine
#  * [2014/05/03]
#         add reset
#  * [2013/03/08]
#         add __enter__, __exit__ for with clause
#  * [2012/12/12]
#     - 본 모듈 작업 시작

__date__ = "2015/11/17"
__version__ = "1.15.1117"
__version_info__ = (1, 15, 1117)
__license__ = "MIT"

################################################################################
import sys
import time


################################################################################
class Timer:
    """ 타이머 클래스
    :param int secs: 얼마만큼의 주기로 실행되는가 (디폴트 1초)
    .. note:: 주어진 시간(디폴트 1초) 안에 특정한 일을 수행한 경우 1초가 되도록 time.sleep()을
        하는데, 만약 그보다 더 걸리면 sleep을 하지 않고 그 다음 작업을 바로 수행함

    >>> import random
    >>> tse = Timer()
    >>> for i in range(3):
    ...     with tse:
    ...         rnd = random.random()
    ...         time.sleep(rnd)
    ...         print('rnd=%f ===> %s' % (rnd, tse))
    ...         if rnd <= 0 and tse.count != i: return False
    rnd=0.955333 ===> start_ts=1391318778.141574:end_ts=0.000000:
        done_ts=0.000000:sleep_ts=0.000000:delta=0.000000:count=0
    rnd=0.332995 ===> start_ts=1391318779.141698:end_ts=1391318779.097757:
        done_ts=0.956183:sleep_ts=0.043817:delta=0.000124:count=1
    rnd=0.676098 ===> start_ts=1391318780.142478:end_ts=1391318779.475601:
        done_ts=0.333903:sleep_ts=0.665973:delta=0.000904:count=2
    """

    # ==========================================================================
    def __init__(self, secs=1):
        """
            secs is the total seconds todo something and sleep to meet this secs
        """
        self.secs = secs
        self.clear()
        self.count = 0
        self.orig_ts = None
        self.start_ts = 0.0
        self.end_ts = 0.0
        self.done_ts = 0.0
        self.sleep_ts = 0.
        self.delta = 0.0
        self.last_ts = None

    # ==========================================================================
    def clear(self):
        self.count = 0
        self.orig_ts = None
        self.start_ts = 0.0
        self.end_ts = 0.0
        self.done_ts = 0.0
        self.sleep_ts = 0.
        self.delta = 0.0
        self.last_ts = None

    # ==========================================================================
    def reset(self):
        self.clear()
        self.start()

    # ==========================================================================
    def start(self):
        """처음 타이머 시작
        .. note:: with context의 __enter__ 시 호출됨
        """
        self.start_ts = time.time()
        if self.orig_ts is None:
            self.orig_ts = self.start_ts
        self.delta = (self.start_ts - (self.secs * self.count)) - self.orig_ts

    # ==========================================================================
    def end(self):
        """타이머 종료
        .. note:: with context의 __exit__ 시 호출됨
        """
        self.end_ts = time.time()
        self.last_ts = self.start_ts
        self.count += 1
        self.sleep()

    # ==========================================================================
    def sleep(self):
        """주기적으로 작업할 시간에 맞추어 sleep
        """
        self.done_ts = self.end_ts - self.start_ts
        if self.done_ts >= self.secs:
            # 가상머신 등에서 많은 시간이 갑자기 jump 된 경우 CPU 100%가 되고
            # loop을 돌기 때문에 reset() 기능을 넣음
            # self.sleep_ts = 0.0
            self.reset()
            return
        self.sleep_ts = self.secs - self.done_ts - self.delta
        if self.sleep_ts > 0:
            time.sleep(self.sleep_ts)

    # ==========================================================================
    def __repr__(self):
        s = 'start_ts=%f:end_ts=%f:done_ts=%f:sleep_ts=%f:delta=%f:count=%d' % (
            self.start_ts, self.end_ts, self.done_ts, self.sleep_ts,
            self.delta, self.count)
        return s

    # ==========================================================================
    def __enter__(self):
        self.start()

    # ==========================================================================
    def __exit__(self, *args):
        _ = args
        self.end()


################################################################################
def test_main():
    """
    @brief Timer module's test function
    """
    import random
    tse = Timer()
    for i in range(3):
        with tse:
            rnd = random.random()
            if i == 2:
                time.sleep(2)
            else:
                time.sleep(rnd)
            print('rnd=%f ===> %s' % (rnd, tse))
            if rnd <= 0 and tse.count != i:
                return False
    return True


################################################################################
if __name__ == '__main__':
    r = test_main()
    sys.exit(0 if r else 1)
