import sys
import subprocess

# python.exe
# -m
# pip
# install
# argoslabs.system.screenlock
# --extra-index-url
# https://pypi-official.argos-labs.com/pypi
# --trusted-host
# pypi-official.argos-labs.com
# --extra-index-url
# https://mcchae:mcchae@pypi-private.argos-labs.com/simple
# --trusted-host
# pypi-private.argos-labs.com

cmd = [
    sys.executable,
    '-m',
    'pip',
    'uninstall',
    '-y',
    'argoslabs.system.screenlock',
]
po = subprocess.Popen(cmd)
po.wait()
print(po.returncode)

stdin_f = 'stdin.txt'
with open(stdin_f, 'w') as ofp:
    ofp.write('\n')

cmd = [
    sys.executable,
    '-m',
    'pip',
    'install',
    'argoslabs.system.screenlock',
    '--extra-index-url',
    'https://pypi-official.argos-labs.com/pypi',
    '--trusted-host',
    'pypi-official.argos-labs.com',
    '--extra-index-url',
    'https://mcchae:mcchae1!@pypi-private.argos-labs.com/simple',
    '--trusted-host',
    'pypi-private.argos-labs.com',
]

with open(stdin_f) as ifp:
    po = subprocess.Popen(cmd, stdin=ifp)
    po.wait()
    print(po.returncode)

