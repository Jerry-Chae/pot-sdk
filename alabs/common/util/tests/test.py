#!/usr/bin/env python
# coding=utf8


################################################################################
import os
from unittest import TestCase
from alabs.common.util.vvargs import get_icon_path


################################################################################
G_PARAMS = ['y', '50', '0.5', '1.2.3.4', 'tom', 'jerry', 'foo', 'foo']


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    # noinspection PyMethodMayBeStatic
    def myInit(self):
        if TU.isFirst:
            TU.isFirst = False

    # ==========================================================================
    def setUp(self):
        self.myInit()

    # ==========================================================================
    def tearDown(self):
        pass

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0010_timer(self):
        from alabs.common.util.timer import test_main
        self.assertTrue(test_main())

    # ==========================================================================
    def test0020_vvargs(self):
        from alabs.common.util.vvargs import ModuleContext, str2bool
        with ModuleContext(
                owner='ARGOS-LABS',
                group='demo-test',
                version='1.0',
                platform=['windows', 'darwin', 'linux'],
                output_type='text',
                display_name='Unit Test',
                icon_path=get_icon_path(__file__),
                description='Test friends',
        ) as mcxt:
            mcxt.add_argument('boolparam', type=str2bool,
                              help='boolean parameter')
            mcxt.add_argument('intparam', type=int,
                              greater=40, less_eq=50,
                              help='integer parameter')
            mcxt.add_argument('floatparam', type=float,
                              greater=0.0, less=1.0,
                              help='float parameter')
            mcxt.add_argument('ipaddr', type=str,
                              re_match='^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',
                              help='ipv4 address')
            argspec = mcxt.parse_args(['y', '50', '0.5', '1.2.3.4'])
            print(argspec)
            self.assertTrue(True)

    # ==========================================================================
    def test0030_vvlogger(self):
        print('vvlogger need test: but vvargs use it instead!')
        self.assertTrue(True)

    # ==========================================================================
    def test0040_vvjson(self):
        from alabs.common.util.vvjson import do_test
        self.assertTrue(do_test())

    # ==========================================================================
    def test9999_quit(self):
        if os.path.exists('_jb_unittest_runner.py.log'):
            os.unlink('_jb_unittest_runner.py.log')
        self.assertTrue(True)
