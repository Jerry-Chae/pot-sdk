#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`alabs.icon.tests.test_me`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
# 작업일지
# --------
#
# 다음과 같은 작업 사항이 있었습니다:
#  * [2019/07/09]
#     - 본 모듈 작업 시작
################################################################################
import os
import sys
from unittest import TestCase
# noinspection PyProtectedMember
from alabs.icon import _main as main
from contextlib import contextmanager
from io import StringIO


# ################################################################################
# @contextmanager
# def captured_output():
#     new_out, new_err = StringIO(), StringIO()
#     old_out, old_err = sys.stdout, sys.stderr
#     try:
#         sys.stdout, sys.stderr = new_out, new_err
#         yield sys.stdout, sys.stderr
#     finally:
#         sys.stdout, sys.stderr = old_out, old_err


################################################################################
# noinspection PyUnusedLocal
class TU(TestCase):
    """
    TestCase for argoslabs.demo.helloworld
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        os.chdir(os.path.dirname(__file__))
        self.assertTrue(True)

    # ==========================================================================
    def test0100_failure(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_icon_png(self):
        try:
            _ = main('-c', 'icon.yaml')
            self.assertTrue(os.path.exists('icon.png'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0120_car(self):
        try:
            _ = main('-c', 'car.yaml', '-o', 'car.png')
            self.assertTrue(os.path.exists('car.png'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_folder_eye(self):
        try:
            _ = main('-c', 'folder-eye.yaml', '-o', 'folder-eye.png')
            self.assertTrue(os.path.exists('folder-eye.png'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_balls(self):
        try:
            _ = main('-c', 'balls.yaml', '-o', 'balls.png')
            self.assertTrue(os.path.exists('balls.png'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_myicon(self):
        try:
            _ = main('-c', 'myicon.yaml', '-o', 'myicon.png')
            self.assertTrue(os.path.exists('myicon.png'))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
