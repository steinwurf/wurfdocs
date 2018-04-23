import mock
import os
import vcr

import wurfdocs
import wurfdocs.doxygen_downloader


@vcr.use_cassette('test/data/archive/test_files.yaml')
def test_doxygen_downloader_download(testdirectory):

    # If you want to change the file downloaded - you also need to update the
    # url - such that VCR can make the recording. After the recording
    # has been made it is not necessary that the url stays alive.

    url = 'https://github.com/steinwurf/wurfdocs/raw/' \
        'intial-commit/test/data/archive/test_files.zip'

    filepath = os.path.join(testdirectory.path(), 'test_files.zip')

    wurfdocs.doxygen_downloader.download(url=url, filepath=filepath)
    assert os.path.isfile(filepath)


def test_doxygen_downloader_download_url(testdirectory):

    for platform in wurfdocs.doxygen_downloader.supported_platforms.keys():
        assert wurfdocs.doxygen_downloader.download_url(platform) != ""


def test_doxygen_downloader_current_platform():

    return wurfdocs.doxygen_downloader.current_platform() in ['linux']
