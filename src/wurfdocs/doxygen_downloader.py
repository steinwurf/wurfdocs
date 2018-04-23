#! /usr/bin/env python
# encoding: utf-8

import cgi
import os
import sys
import archive

from .compat import IS_PY2

if IS_PY2:

    # Python 2
    from urllib2 import urlopen
    from urlparse import urlparse
else:

    # Python 3
    from urllib.request import urlopen
    from urllib.parse import urlparse

# Example URLs:
#
# http://ftp.stack.nl/pub/users/dimitri/doxygen-1.8.14.linux.bin.tar.gz
# http://ftp.stack.nl/pub/users/dimitri/doxygen-1.8.14.windows.bin.zip
# http://ftp.stack.nl/pub/users/dimitri/doxygen-1.8.14.windows.x64.bin.zip

BASE_URL = "http://ftp.stack.nl/pub/users/dimitri/"
VERSION = "1.8.14"


def current_platform():

    if sys.platform.startswith('linux'):
        return 'linux'

    if sys.platform.startswith('win'):

        # Checking for 64 bit
        # https://docs.python.org/3/library/platform.html#cross-platform

        if sys.maxsize > 2**32:
            return "win64"
        else:
            return "win32"

    raise OSError('Unsupported platform: ' + sys.platform)


def archive_name(platform):

    if platform == 'linux':
        return 'doxygen-' + VERSION + '.linux.bin.tar.gz'

    if platform == 'win32':
        return 'doxygen-' + VERSION + '.windows.bin.zip'

    if platform == 'win64':
        return 'doxygen-' + VERSION + '.windows.x64.bin.zip'

    raise OSError('Unsupported platform: ' + platform)


def doxygen_exectuable(from_path, platform):

    if platform == 'linux':
        return os.path.join(from_path, 'doxygen-' + VERSION, 'bin/doxygen')

    if platform == 'win32':
        return os.path.join(from_path, 'doxygen.exe')

    if platform == 'win64':
        return os.path.join(from_path, 'doxygen.exe')

    raise OSError('Unsupported platform: ' + platform)


def doxygen_url(platform):
    return os.path.join(BASE_URL, archive_name(platform))


def default_download_path():

    # https://stackoverflow.com/a/4028943
    home_path = os.path.join(os.path.expanduser("~"))
    return os.path.join(home_path, '.wurfdocs', 'local-doxygen', VERSION)


def download_archive(url, to_path):
    """ Download the file specified by the source.
    :param cwd: The directory where to download the file.
    :param url: The URL of the file to download.
    :param filename: The filename to store the file under.
    """

    response = urlopen(url=url)

    # From http://stackoverflow.com/a/1517728
    CHUNK = 16 * 1024
    with open(to_path, 'wb') as f:
        while True:
            chunk = response.read(CHUNK)
            if not chunk:
                break
            f.write(chunk)


def extract_archive(from_path, to_path):

    assert os.path.isfile(from_path)

    archive.extract(path=from_path, to_path=to_path)

    return to_path


def download_doxygen(platform=None, download_path=None):

    if platform == None:
        platform = current_platform()

    # Where to download the archive
    if download_path == None:
        download_path = default_download_path()

    if not os.path.isdir(download_path):
        os.makedirs(download_path)

    archive_path = os.path.join(download_path, archive_name(platform))

    url = doxygen_url(platform=platform)

    download_archive(url=url, to_path=archive_path)

    extract_archive(from_path=archive_path, to_path=download_path)

    executable = doxygen_exectuable(from_path=download_path, platform=platform)

    assert os.path.isfile(executable)

    return executable


def check_doxygen(platform=None, download_path=None):

    if platform == None:
        platform = current_platform()

    if download_path == None:
        download_path = default_download_path()

    executable = doxygen_exectuable(from_path=download_path, platform=platform)

    return os.path.isfile(executable)


def ensure_doxygen(platform=None, download_path=None):

    if check_doxygen(platform=platform, download_path=download_path):
        return doxygen_exectuable(platform=platform, from_path=download_path)
    else:
        return download_doxygen(platform=platform, download_path=download_path)
