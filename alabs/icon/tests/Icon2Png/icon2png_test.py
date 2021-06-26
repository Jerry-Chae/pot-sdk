# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import sys
# import shutil
from contextlib import contextmanager
from io import StringIO
from icon_font_to_png import command_line
from unittest import TestCase, TestLoader, TextTestRunner
from PIL import Image


################################################################################
@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


################################################################################
# noinspection PyUnresolvedReferences
class TU(TestCase):
    # ==========================================================================
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    # ==========================================================================
    def test_0100_list_option(self):
        try:
            command_line.run(
                '--css fontawesome.css --ttf fontawesome-webfont.ttf --list'.split()
            )
            # stdout = out.getvalue().strip()
            # print(stdout)
            # self.assertTrue(not stdout)
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test_0110_icon(self):
        try:
            command_line.run(
                '--css fontawesome.css --ttf fontawesome-webfont.ttf --size 30 '
                '--color #6a76f6 car'.split()
            )
            # stdout = out.getvalue().strip()
            # print(stdout)
            # self.assertTrue(not stdout)
            self.assertTrue(True)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test_0120_icon_combine(self):
        try:
            im_blank = Image.open('icon_blank.png')
            sz_blank = im_blank.size
            im_icon = Image.open('exported/car.png')
            sz_icon = im_icon.size
            offset = int((sz_blank[0] - sz_icon[0]) / 2)
            if offset < 5:
                raise RuntimeError('Internal Icon is too big to fit in the frame')
            im_blank.paste(im_icon, (offset, offset), im_icon)
            im_blank.save('icon_car.png')
            self.assertTrue(True)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test_0200_foloder_eye(self):
        try:
            command_line.run(
                '--css fontawesome.css --ttf fontawesome-webfont.ttf --size 30 '
                '--color #403f3d folder'.split()
            )
            command_line.run(
                '--css fontawesome.css --ttf fontawesome-webfont.ttf --size 20 '
                '--color #6a76f6 eye'.split()
            )

            im_blank = Image.open('icon_blank.png')
            sz_blank = im_blank.size
            im_icons = map(Image.open, ('exported/folder.png', 'exported/eye.png'))
            for im_icon in im_icons:
                sz_icon = im_icon.size
                offset = int((sz_blank[0] - sz_icon[0]) / 2)
                if offset < 5:
                    raise RuntimeError('Internal Icon is too big to fit in the frame')
                im_blank.paste(im_icon, (offset, offset), im_icon)
            im_blank.save('icon_folder_eye.png')
            self.assertTrue(True)
        except Exception as e:
            sys.stderr.write('%s\n' % str(e))
            self.assertTrue(False)


################################################################################
if __name__ == "__main__":
    suite = TestLoader().loadTestsFromTestCase(TU)
    result = TextTestRunner(verbosity=2).run(suite)
    ret = not result.wasSuccessful()
    sys.exit(ret)
