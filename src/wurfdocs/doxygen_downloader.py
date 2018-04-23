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


download_filename = {
    'linux': 'doxygen-1.8.14.linux.bin.tar.gz',
}

download_base_urls = {
    'linux': 'http://ftp.stack.nl/pub/users/dimitri'
}


def current_platform():
    """Get current platform name by short string."""
    if sys.platform.startswith('linux'):
        return 'linux'

    elif sys.platform.startswith('win'):
        if sys.maxsize > 2 ** 31 - 1:
            return 'win64'
        return 'win32'

    raise OSError('Unsupported platform: ' + sys.platform)


def download_url():

    platform = current_platform()

    url = os.path.join(
        download_base_urls[platform], download_filename[platform])

    return url


def download(cwd, url):
    """ Download the file specified by the source.
    :param cwd: The directory where to download the file.
    :param source: The URL of the file to download.
    :param filename: The filename to store the file under.
    """

    platform = current_platform()

    filename = download_filename[platform]
    url = os.path.join(download_base_urls[platform], filename)

    response = urlopen(url=url)

    filepath = os.path.join(cwd, filename)

    # From http://stackoverflow.com/a/1517728
    CHUNK = 16 * 1024
    with open(filepath, 'wb') as f:
        while True:
            chunk = response.read(CHUNK)
            if not chunk:
                break
            f.write(chunk)

    return filepath


# def extract(cwd, filena):
#     filepath = download(cwd=cwd)
#     return archive.extract(filepath)
