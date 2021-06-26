#!/usr/bin/env python
# coding=utf8


################################################################################
import os
import sys
import uuid
from shutil import make_archive
from unittest import TestCase
from alabs.common.util.vvupdown import SimpleDownUpload
from tempfile import gettempdir


################################################################################
class TU(TestCase):
    # ==========================================================================
    isFirst = True
    url = 'https://pypi-req.argos-labs.com'
    token = 'aL0PK2Rhs6ed0mgqLC42'
    # url = 'http://router.vivans.net:25478'
    # token = 'KxnBsoIFABmzpqFBQtr0tqemlGO1tbv0dJyFLZtY'
    zf = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    tf = gettempdir()
    file = os.path.join(tf, 'alabs.common.zip')
    saved_filename = 'alabs.common-my saved file.zip'
    fsize = -1

    # ==========================================================================
    def test0000_init(self):
        os.chdir(self.tf)
        self.assertTrue(os.path.abspath(os.getcwd()), self.tf)
        if os.path.exists(self.file):
            os.remove(self.file)

    # ==========================================================================
    def test0010_make_zipfile(self):
        r = make_archive(self.file[:-4], 'zip', self.zf)
        self.assertTrue(r == self.file)
        self.assertTrue(os.path.exists(self.file) and os.path.getsize(self.file) > 0)
        TU.fsize = os.path.getsize(self.file)
        print('size of "%s" = %s' % (self.file, TU.fsize))

    # ==========================================================================
    def test0100_check_non_exists(self):
        try:
            sdu = SimpleDownUpload(url=self.url, token=self.token)
            r = sdu.exists(str(uuid.uuid4()))
            self.assertTrue(not r)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_upload(self):
        try:
            sdu = SimpleDownUpload(url=self.url, token=self.token)
            r = sdu.upload(self.file)
            self.assertTrue(r)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0210_check_exitsts(self):
        try:
            sdu = SimpleDownUpload(url=self.url, token=self.token)
            r = sdu.exists(self.file)
            self.assertTrue(r)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # TODO: simple-upload-download 서비스는 delete가 없어 한번 돌고 나면 존재함
    # # ==========================================================================
    # def test0300_check_not_exitsts(self):
    #     try:
    #         sdu = SimpleDownUpload(url=self.url, token=self.token)
    #         r = sdu.exists(self.saved_filename)
    #         self.assertTrue(not r)
    #     except Exception as e:
    #         sys.stderr.write('%s\n' % str(e))
    #         self.assertTrue(False)
    #
    # ==========================================================================
    def test0310_upload_saved_filename(self):
        try:
            sdu = SimpleDownUpload(url=self.url, token=self.token)
            r = sdu.upload(self.file, saved_filename=self.saved_filename)
            self.assertTrue(r)
            os.remove(self.file)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0320_check_exitsts(self):
        try:
            sdu = SimpleDownUpload(url=self.url, token=self.token)
            r = sdu.exists(self.saved_filename)
            self.assertTrue(r)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0400_download(self):

        try:
            sdu = SimpleDownUpload(url=self.url, token=self.token)
            dst = os.path.join(gettempdir(), 'download.zip')
            r = sdu.download(self.file, dst)
            self.assertTrue(r)
            self.assertTrue(
                os.path.exists(dst) and os.path.getsize(dst) == TU.fsize)
            os.remove(dst)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        if os.path.exists(self.file):
            os.remove(self.file)
        self.assertTrue(not os.path.exists(self.file))
