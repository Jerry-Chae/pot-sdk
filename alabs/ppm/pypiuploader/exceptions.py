"""Custom exception classes."""


class ConfigFileError(Exception):

    """Raised when a PyPI config file does not exist."""


class PackageConflictError(Exception):

    """Raised when the version of the package was already uploaded.

    The PyPI server responds with HTTP 409 and the
    :class:`.upload.PackageUploader` raises this exception instead.

    """
