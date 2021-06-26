"""Packages uploading."""

import os.path

import requests

from . import exceptions
from . import pypirc


class PackageUploader(object):

    """Uploads source distributions to a PyPI server.

    Example::

        >>> uploader = PackageUploader('http://localhost:8000', 'user', 'pass')
        >>> uploader.upload('amqp-1.4.4.tar.gz')
        <Response [200]>
        >>> uploader.upload('amqp-1.4.4.tar.gz')
        Traceback (most recent call last):
          ...
        PackageConflictError: Package amqp-1.4.4.tar.gz already uploaded.

    :param host:
        The host of the PyPI server, e.g. ``'http://localhost:8000'``.
    :param username:
        Optional username for HTTP authentication.
    :param password:
        Optional password for HTTP authentication.

    """

    def __init__(self, host, username=None, password=None):
        self.host = host
        self.username = username
        self.password = password
        self._data = {':action': 'file_upload'}
        self._session = requests.Session()
        if username:
            self._session.auth = self.username, self.password

    @classmethod
    def from_rc_file(
            cls, repository, username=None, password=None, config_path=None):
        """Instantiate the uploader using configuration from .pypirc file.

        Read the rc file using :class:`.pypirc.RCParser`.

        Use the **repository**'s authentication config from the rc file,
        if the file exists and the repository section is defined.
        The **username** and **password** defined in the file can be overriden
        by the given arguments.

        If the rc file or the section for the **repository** doesn't exist,
        use the **repository** argument as the server host.

        Return a new instance of :class:`PackageUploader`.

        :param repository:
            PyPI server name or URL.
        :param username:
            Optional username for authentication.
        :param password:
            Optional password for authentication.
        :param config_path:
            Optional config path to use instead of ``~/.pypirc``.

        """
        try:
            parser = pypirc.RCParser.from_file(config_path)
        except exceptions.ConfigFileError:
            config = None
        else:
            config = parser.get_repository_config(repository)
        if config:
            uploader = cls.from_repository_config(
                config, username=username, password=password)
        else:
            uploader = cls(repository, username, password)
        return uploader

    @classmethod
    def from_repository_config(cls, repo_config, username=None, password=None):
        """Instantiate the uploader using repository configuration dictionary.

        Examples::

            >>> repo_config = {
            ...     'repository': 'http://localhost:8000',
            ...     'username': 'foo',
            ...     'password': 'foo',
            ... }
            >>> uploader = PackageUploader.from_repository_config(repo_config)
            >>> uploader.host, uploader.username, uploader.password
            'http://localhost:8000', 'foo', 'foo'
            >>> uploader = PackageUploader.from_repository_config(
            ...     repo_config, username='foo')
            >>> uploader.host, uploader.username, uploader.password
            'http://localhost:8000', 'foo', 'foo'

        Return a new instance of :class:`PackageUploader`.

        :param repo_config:
            A dictionary with the repository configuration, must contain
            three keys:

            * repository,
            * username
            * password

        :param username:
            Optional username to override the one from the **repo_cofig**.
        :param password:
            Optional password to override the one from the **repo_cofig**.

        """
        host = repo_config['repository']
        username = username or repo_config['username']
        password = password or repo_config['password']
        return cls(host, username, password)

    def upload(self, filepath):
        """Upload a package under the given path.

        Return :class:`requests.Response` from the PyPI server.

        If the package is already uploaded, raise
        :exc:`.exceptions.PackageConflictError`.
        On other errors raise :class:`requests.exceptions.HTTPError`.

        :param filepath:
            A path to the package file you want to upload.

        """
        files = self._make_request_files(filepath)
        self._session.verify = False
        response = self._session.post(self.host, data=self._data, files=files)
        self._raise_for_status(response, filepath)
        return response

    def _make_request_files(self, filepath):
        filename = os.path.basename(filepath)
        content = self._read_file(filepath)
        return {'content': (filename, content)}

    def _read_file(self, filepath):
        with open(filepath, 'rb') as buf:
            content = buf.read()
        return content

    def _raise_for_status(self, response, filepath):
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            if exc.response.status_code == 409:
                error = 'Package {0} already uploaded.'.format(filepath)
                raise exceptions.PackageConflictError(error)
            raise
