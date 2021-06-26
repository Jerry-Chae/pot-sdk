# import os
# import select
# import tempfile
# import subprocess

# ################################################################################
# def do_1():
#     kwargs = {
#         'getstdout': True,
#     }
#     cmd = [
#         sys.executable,
#         'po_callee.py'
#     ]
#
#     (pipe_r, pipe_w) = os.pipe()
#
#     tmpdir = tempfile.mkdtemp(prefix='venv_py_')
#     out_path = os.path.join(tmpdir, 'stdout.txt')
#     err_path = os.path.join(tmpdir, 'stderr.txt')
#
#     with open(out_path, 'w', encoding='utf-8') as out_fp, \
#             open(err_path, 'w', encoding='utf-8') as err_fp:
#         po = subprocess.Popen(' '.join(cmd), shell=True,
#                               stdout=pipe_w, stderr=pipe_w)
#         while po.poll() is None:
#             # line = po.stdout.readline()
#             # line = line.decode("utf-8").rstrip()
#             # if line:
#             #     if kwargs['getstdout']:
#             #         print(line)
#             #     out_fp.write('%s\n' % line)
#             # line = po.stderr.readline()
#             # line = line.decode("utf-8").rstrip()
#             # if line:
#             #     if kwargs['getstdout']:
#             #         sys.stderr.write('%s\n' % line)
#             #     err_fp.write('%s\n' % line)
#             while len(select.select([pipe_r], [], [], 0)[0]) == 1:
#                 # Read up to a 1 KB chunk of data
#                 buf = os.read(pipe_r, 1024)
#                 # Stream data to our stdout's fd of 0
#                 os.write(0, buf)


import sys
import time
from subprocess import PIPE, Popen
from threading import Thread
from queue import Queue, Empty

ON_POSIX = 'posix' in sys.builtin_module_names


################################################################################
def enqueue_stdout(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


################################################################################
def enqueue_stderr(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()


################################################################################
def do():
    po = Popen([sys.executable, 'po_callee.py'],
              stdout=PIPE, stderr=PIPE,
              bufsize=1, close_fds=ON_POSIX)
    q_out, q_err = Queue(), Queue()
    t_out = Thread(target=enqueue_stdout, args=(po.stdout, q_out))
    t_out.daemon = True  # thread dies with the program
    t_out.start()
    t_err = Thread(target=enqueue_stderr, args=(po.stderr, q_err))
    t_err.daemon = True  # thread dies with the program
    t_err.start()

    while po.poll() is None:
        try:
            line = q_out.get_nowait()
            if line:
                print(line.decode('utf-8').rstrip())
        except Empty:
            pass
        try:
            line = q_err.get_nowait()  # or q.get(timeout=.1)
            if line:
                sys.stderr.write('%s\n' % line.decode('utf-8').rstrip())
        except Empty:
            pass
        time.sleep(1)


################################################################################
if __name__ == '__main__':
    do()
