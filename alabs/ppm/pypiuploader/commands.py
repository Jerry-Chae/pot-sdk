#!/usr/bin/env python
r"""Commands for **pypiupload** program.

:func:`main` is installed as a console script during package setup.

Examples:

.. code-block:: bash

    $ pypiupload requirements requirements.txt -i internal
    $ pypiupload packages mock==1.2.1 requests==2.0.0 -i internal
    $ pypiupload files packages/mock-1.2.1.tar.gz -i internal
    $ pypiupload requirements requirements.txt \
      -i http://localhost:8000 -u user -p password -d packages_download_dir
    $ pypiupload requirements requirements.txt \
      -i http://localhost:8000 --no-use-wheel

"""

import argparse
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import alabs.ppm.pypiuploader
from alabs.ppm.pypiuploader import download
from alabs.ppm.pypiuploader import exceptions
from alabs.ppm.pypiuploader import upload


def main(argv=None, stdout=None):
    """Run the :class:`Command`.

    :param argv:
        A list of arguments to parse, defaults to :data:`sys.argv`.
    :param stdout:
        Standard output file, defaults to :data:`sys.stdout`.

    """
    options = parse_args(argv)
    command = Command(options, stdout=stdout)
    command.run()
    return 0


class Command(object):

    """Runs a **pypiupload** command.

    Available commands:

    * requirements
    * packages
    * files

    For **files** command, upload the given source distribution files.

    For **requirements** and **packages**, first download the packages and
    then upload them.  **download_dir** option (``-d`` or ``--download-dir``)
    can specify the directory to which the files will be downloaded.  If not
    given, will create a temporary directory.
    With **no_use_wheel** option (``--no-use-wheel``), will not find and prefer
    wheel archives.

    **index** option (``-i`` or ``--index-url``) specifies the PyPI host or
    name from the ``~/.pypirc`` config file.
    If **username** (``-u`` or ``--username``) and
    **password** (``-p`` or ``--password``) are not given, will try to find
    them in the rc file.

    :param options:
        Command arguments, :class:`argparse.Namespace` instance parsed by
        the :func:`parse_args`.
    :param stdout:
        Standard output file, defaults to :data:`sys.stdout`.

    """

    def __init__(self, options, stdout=None):
        self.options = options
        self.stdout = stdout or sys.stdout

    def run(self):
        """Run the command.

        * Make the :class:`.upload.PackageUploader` instance.  If ``~/.pypirc``
          file exists, parse it using :class:`.pypirc.RCParser`
        * Define the files to upload -- download them if necessary, using
          :class:`.download.PackageDownloader`
        * Upload the packages

        """
        uploader = self._make_uploader()
        filenames = self._get_filenames()
        self._upload_files(uploader, filenames)

    def _make_uploader(self):
        uploader = upload.PackageUploader.from_rc_file(
            self.options.index, self.options.username, self.options.password)
        return uploader

    def _get_filenames(self):
        if self.options.command in ('packages', 'requirements'):
            filenames = self._download()
        else:  # 'files' command.
            filenames = self.options.files
        return filenames

    def _download(self):
        downloader = download.PackageDownloader(self.options.download_dir)
        filenames = downloader.download(
            requirements=getattr(self.options, 'packages', None),
            requirements_file=getattr(self.options, 'requirements_file', None),
            no_use_wheel=self.options.no_use_wheel)
        return filenames

    def _upload_files(self, uploader, filenames):
        self._print('Uploading packages to {0}\n'.format(uploader.host))
        for filename in filenames:
            self._upload_file(uploader, filename)

    def _upload_file(self, uploader, filename):
        self._print('Uploading {0}... '.format(filename))
        try:
            uploader.upload(filename)
        except exceptions.PackageConflictError:
            self._print('already uploaded.\n')
        else:
            self._print('success.\n')

    def _print(self, message):
        self.stdout.write(message)


def parse_args(argv):
    """Parse arguments for the commands.

    Return a :class:`argparse.Namespace` instance.

    :param argv:
        A list of arguments to parse.

    """
    description = (
        'Upload source distributions of your requirements to your PyPI server.'
    )
    parser = argparse.ArgumentParser(description=description)

    subparsers = parser.add_subparsers(dest='command')
    files_parser = subparsers.add_parser(
        'files',
        help='Upload source distributions (tarball, zip file, wheel, etc.)'
    )
    files_parser.add_argument(
        'files',
        metavar='FILE',
        nargs=argparse.ONE_OR_MORE,
        help='Source distribution file path'
    )
    _add_common_arguments(files_parser)

    dir_args, dir_kwargs = ('-d', '--download-dir'), {
        'dest': 'download_dir',
        'default': None,
        'help': 'Path to directory where the packages should be downloaded',
    }
    no_use_wheel_kwargs = {
        'action': 'store_true',
        'dest': 'no_use_wheel',
        'default': False,
        'help': 'Do not find and prefer wheel archives',
    }

    packages_parser = subparsers.add_parser(
        'packages',
        help='Download and upload packages by their names'
    )
    packages_parser.add_argument(
        'packages',
        metavar='PACKAGE',
        nargs=argparse.ONE_OR_MORE,
        help='Package name'
    )
    packages_parser.add_argument(*dir_args, **dir_kwargs)
    packages_parser.add_argument('--no-use-wheel', **no_use_wheel_kwargs)
    _add_common_arguments(packages_parser)

    requirements_parser = subparsers.add_parser(
        'requirements',
        help='Download and upload packages from requirements file'
    )
    requirements_parser.add_argument(
        'requirements_file',
        metavar='REQUIREMENTS_FILE',
        help='Path to requirements file'
    )
    requirements_parser.add_argument(*dir_args, **dir_kwargs)
    requirements_parser.add_argument('--no-use-wheel', **no_use_wheel_kwargs)
    _add_common_arguments(requirements_parser)

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=alabs.ppm.pypiuploader.__version__
    )

    options = parser.parse_args(argv)
    if not options.command:  # pragma: no cover
        # Bug in Python 3: http://bugs.python.org/issue16308
        from gettext import gettext as _
        parser.error(_('too few arguments'))
    return options


def _add_common_arguments(subparser):
    subparser.add_argument(
        '-i',
        '--index-url',
        dest='index',
        required=True,
        help='PyPI server name or URL',
    )
    subparser.add_argument(
        '-u',
        '--username',
        dest='username',
        default=None,
        help='Username'
    )
    subparser.add_argument(
        '-p',
        '--password',
        dest='password',
        default=None,
        help='Password'
    )


if __name__ == '__main__':
    main()
