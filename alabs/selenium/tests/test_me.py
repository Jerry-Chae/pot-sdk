################################################################################
import os
import sys
import traceback
import logging
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
from alabs.selenium import PySelenium


################################################################################
class GoogleSearch(PySelenium):
    def __init__(self, search, **kwargs):
        kwargs['url'] = 'https://www.google.com/'
        self.search = search
        PySelenium.__init__(self, **kwargs)
        self.logger.info(f'Starting Google "{search}"')
    def start(self):
        try:
            # Search : 
            # /html/body/div[1]/div[3]/form/div[2]/div[1]/div[1]/div/div[2]/input
            # /html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input
            e = self.get_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input')
            e.send_keys(self.search)

            # Search button
            # /html/body/div[1]/div[3]/form/div[2]/div[1]/div[3]/center/input[1]
            # /html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]
            e = self.get_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]',
                                cond='element_to_be_clickable',
                                move_to_element=True)
            self.safe_click(e)
            self.implicitly_wait(after_wait=2)
        except Exception as e:
            _exc_info = sys.exc_info()
            _out = traceback.format_exception(*_exc_info)
            del _exc_info
            self.logger.error('do_search Error: %s\n' % str(e))
            self.logger.error('%s\n' % ''.join(_out))
            raise


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0100_google_search_chrome(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            logger = logging.getLogger('GoogleSearch')
            kwargs = {
                'browser': 'Chrome',
                # 'search': 'New Balance 608 7 ½ 4E',
                # 'search': 'New Balance 608 7 1/2 4E',
                'search': 'Sony A7 R3',
                'logger': logger,
            }
            with GoogleSearch(
                kwargs['search'],
                browser=kwargs.get('browser', 'Chrome'),
                width=int(kwargs.get('width', '1200')),
                height=int(kwargs.get('height', '800')),
                logger=kwargs['logger']) as ws:
                ws.start()
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0110_google_search_edge(self):
        sg = sys.gettrace()  # 디버그는 괜찮지만 실제 build.bat 에서는 오류 발생 때문
        if sg is None:  # Not in debug mode
            print('Skip testing at test/build time')
            return
        try:
            logger = logging.getLogger('GoogleSearch')
            kwargs = {
                'browser': 'Edge',
                # 'search': 'New Balance 608 7 ½ 4E',
                # 'search': 'New Balance 608 7 1/2 4E',
                'search': 'Sony A7 R3',
                'logger': logger,
            }
            with GoogleSearch(
                kwargs['search'],
                browser=kwargs.get('browser', 'Chrome'),
                width=int(kwargs.get('width', '1200')),
                height=int(kwargs.get('height', '800')),
                logger=kwargs['logger']) as ws:
                ws.start()
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
