"""
====================================
 :mod:alabs.icon
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS
"""

# 관련 작업자
# ===========
#
# 본 모듈은 다음과 같은 사람들이 관여했습니다:
#  * 채문창
#
# 작업일지
# --------
#
# 다음과 같은 작업 사항이 있었습니다:
#  * [2019/07/09]
#     - 본 모듈 작업 시작
################################################################################
# from __future__ import absolute_import, unicode_literals
import os
import sys
import yaml
import shutil
import tempfile
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path
from icon_font_to_png import command_line
from PIL import Image


################################################################################
class IconGen(object):
    # ==========================================================================
    def __init__(self, argspec, logger):
        self.args = argspec
        self.logger = logger
        conf_file = self.args.config_file
        if not os.path.exists(conf_file):
            raise IOError('Cannot find config yaml file "%s"' % conf_file)
        with open(conf_file) as ifp:
            if yaml.__version__ >= '5.1':
                # noinspection PyUnresolvedReferences
                self.config = yaml.load(ifp, Loader=yaml.FullLoader)
            else:
                self.config = yaml.load(ifp)
        self.css_file = None
        self.ttf_file = None
        self.mod_dir = os.path.dirname(__file__)

    # ==========================================================================
    def _get_font_css(self):
        css_file = self.args.css if self.args.css else os.path.join(self.mod_dir, 'fontawesome.css')
        if not os.path.exists(css_file):
            raise IOError('Cannot find FontAwesome CSS file "%s"' % css_file)
        self.css_file = css_file
        ttf_file = self.args.ttf if self.args.ttf else os.path.join(self.mod_dir, 'fontawesome-webfont.ttf')
        if not os.path.exists(ttf_file):
            raise IOError('Cannot find FontAwesome Font file "%s"' % ttf_file)
        self.ttf_file = ttf_file

    # ==========================================================================
    def gen(self):
        _tmpdir = tempfile.mkdtemp(prefix='alabs_icon_')
        try:
            self._get_font_css()
            im_blank = Image.open(os.path.join(self.mod_dir, 'icon_blank.png'))
            sz_blank = im_blank.size
            for icon_conf in self.config.get('merge_icons', []):
                if 'from' in icon_conf:
                    img_file = icon_conf['from']
                    if not os.path.exists(img_file):
                        raise IOError('Image from file "%s" does not exists' % img_file)
                    img = Image.open(img_file)
                    img_width, img_height = img.size
                    if img_width > img_height:
                        wsize = int(icon_conf['size'])
                        wpercent = (wsize / float(img.size[0]))
                        hsize = int((float(img.size[1]) * float(wpercent)))
                    else:
                        hsize = int(icon_conf['size'])
                        hpercent = (hsize / float(img.size[1]))
                        wsize = int((float(img.size[0]) * float(hpercent)))
                    im_icon = img.resize((wsize, hsize), Image.ANTIALIAS)
                else:
                    command_line.run([
                        '--css', self.css_file,
                        '--ttf', self.ttf_file,
                        '--size', str(icon_conf.get('size', 30)),
                        '--color', icon_conf.get('color', "#403f3d"),
                        '--filename', os.path.join(_tmpdir, icon_conf['name']),
                        icon_conf['name'],
                    ])
                    im_icon = Image.open(os.path.join(_tmpdir, '%s.png' % icon_conf['name']))
                sz_icon = im_icon.size
                offset_x = int((sz_blank[0] - sz_icon[0]) / 2)
                offset_y = int((sz_blank[1] - sz_icon[1]) / 2)
                if offset_x < 4 or offset_y < 4:
                    raise RuntimeError('Internal Icon is too big to fit in the frame')
                if 'offset' in icon_conf:
                    offset_x += icon_conf['offset'].get('x', 0)
                    offset_y += icon_conf['offset'].get('y', 0)
                im_blank.paste(im_icon, (offset_x, offset_y), im_icon)
            im_blank.save(self.args.output_file)
            print('The result icon is saved as "%s"' % self.args.output_file)
            return 0
        finally:
            if os.path.exists(_tmpdir):
                shutil.rmtree(_tmpdir)


################################################################################
@func_log
def do_icon(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        ig = IconGen(argspec, mcxt.logger)
        r = ig.gen()
        return r
    except Exception as e:
        msg = 'alabs.icon Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        raise
    finally:
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    with ModuleContext(
        owner='ARGOS-LABS',
        group='data',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Argos Icon',
        icon_path=get_icon_path(__file__),
        description='alabs.icon util for making icon for ARGOS LABS plugin SDK',
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('--config-file', '-c',
                          display_name='Config File', show_default=True,
                          default='icon.yaml', input_method='fileread',
                          help='Icon definition configuration file, default is "icon.yaml"')
        mcxt.add_argument('--output-file', '-o',
                          display_name='Icon Output', show_default=True,
                          default='icon.png', input_method='fileread',
                          help='Icon output file, default is "icon.png"')
        mcxt.add_argument('--css',
                          display_name='CSS File',
                          input_method='fileread',
                          help='FontAwesome css file')
        mcxt.add_argument('--ttf',
                          display_name='TTF File',
                          input_method='fileread',
                          help='FontAwesome font file')

        # ##################################### for app dependent parameters
        argspec = mcxt.parse_args(args)
        return do_icon(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass

# ################################################################################
# def main():
#     parser = ArgumentParser(
#         description='alabs.icon util for making icon for ARGOS LABS plugin SDK',
#         formatter_class=RawTextHelpFormatter)
#     # Add for optinos
#     parser.add_argument('--config-file',
#                         help='making new python venv environment at py.%s' %
#                              sys.platform)

