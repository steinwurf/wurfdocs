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


# On these platforms we support downloading doxygen
supported_platforms = {
    'linux': 'http://ftp.stack.nl/pub/users/dimitri/'
    'doxygen-1.8.14.linux.bin.tar.gz'
}


def current_platform():

    if sys.platform.startswith('linux'):
        return 'linux'

    raise OSError('Unsupported platform: ' + sys.platform)


def download_url(platform):

    if platform in supported_platforms:
        return supported_platforms[platform]

    raise OSError('Unsupported platform: ' + sys.platform)


def download(url, filepath):
    """ Download the file specified by the source.
    :param cwd: The directory where to download the file.
    :param url: The URL of the file to download.
    :param filename: The filename to store the file under.
    """

    response = urlopen(url=url)

    # From http://stackoverflow.com/a/1517728
    CHUNK = 16 * 1024
    with open(filepath, 'wb') as f:
        while True:
            chunk = response.read(CHUNK)
            if not chunk:
                break
            f.write(chunk)


# def extract(cwd, filena):
#     filepath = download(cwd=cwd)
#     return archive.extract(filepath)
