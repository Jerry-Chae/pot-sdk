#!/usr/bin/env python
"""
====================================
 :mod: Test case Module
====================================
.. module author:: 임덕규 <hong18s@gmail.com>
.. note:: MIT License
"""


import sys
from contextlib import contextmanager
from io import StringIO


@contextmanager
def captured_output():
    """
    with captured_output as (out, err):
        foo()
    output = out.getvalue().strip()
    self.assertEqual(output, 'hello world!')
    :return:
    """
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err
