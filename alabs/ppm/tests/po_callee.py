import sys
import time
import datetime
import argparse


################################################################################
def do(args):
    for i in range(args.loop):
        if 0 < i and args.stderr > 0 and i % args.stderr == 0:
            msg = '[%s] message stderr [%d]\n' % (datetime.datetime.now(), i)
            sys.stderr.write(msg)
        else:
            msg = '[%s] message stdout [%d]\n' % (datetime.datetime.now(), i)
            sys.stdout.write(msg)
        time.sleep(1)


################################################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Popen callee test program')
    parser.add_argument('--loop', type=int,
                        default=30,
                        help='loop for the test, default is 30')
    parser.add_argument('--stderr', type=int,
                        default=10,
                        help='every other n print stdout, default is 10. 0 means no stderr')
    _args = parser.parse_args()
    do(_args)
