import mock
import os
import vcr
import pytest
import shutil

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

    # wurfdocs.doxygen_downloader.download(url=url, filepath=filepath)
    # assert os.path.isfile(filepath)


# def test_doxygen_downloader_download_url(testdirectory):

#     for platform in wurfdocs.doxygen_downloader.supported_platforms.keys():
#         assert wurfdocs.doxygen_downloader.download_url(platform) != ""


def test_doxygen_downloader_current_platform():

    assert wurfdocs.doxygen_downloader.current_platform() in ['linux']


@pytest.mark.download_test
def test_doxygen_downloader_download_linux(testdirectory):

    download_path = os.path.join(testdirectory.path(), 'archive')

    executable = wurfdocs.doxygen_downloader.doxygen_executable(
        from_path=download_path, platform='linux')

    assert not os.path.isfile(executable)

    assert not wurfdocs.doxygen_downloader.check_doxygen(
        platform='linux', download_path=download_path)

    downloaded_exectuable = wurfdocs.doxygen_downloader.download_doxygen(
        download_path=download_path, platform='linux')

    assert executable == downloaded_exectuable

    assert os.path.isfile(executable)

    if wurfdocs.doxygen_downloader.current_platform() == 'linux':
        testdirectory.run(executable+' --version')


@pytest.mark.download_test
def test_doxygen_downloader_download_win32(testdirectory):

    download_path = os.path.join(testdirectory.path(), 'archive')

    wurfdocs.doxygen_downloader.download_doxygen(
        download_path=download_path, platform='win32')


@pytest.mark.download_test
def test_doxygen_downloader_download_win64(testdirectory):

    download_path = os.path.join(testdirectory.path(), 'archive')

    wurfdocs.doxygen_downloader.download_doxygen(
        download_path=download_path, platform='win64')


@pytest.mark.ensure_doxygen
def test_doxygen_downloader_ensure_doxygen():

    default_path = wurfdocs.doxygen_downloader.default_download_path()

    shutil.rmtree(default_path)

    executable = wurfdocs.doxygen_downloader.ensure_doxygen()

    assert os.path.isfile(executable)


# def test_doxygen_downloader_paths(testdirectory):

#     assert os.path.isdir(wurfdocs.doxygen_downloader.home_path())

#     download_path = os.path.join(testdirectory.path(), '.wurfdocs')

#     assert download_path == wurfdocs.doxygen_downloader.download_path(
#         home_path=testdirectory.path())

#     assert not os.path.isdir(download_path)

#     wurfdocs.doxygen_downloader.ensure_path(download_path)

#     assert os.path.isdir(download_path)


# def test_doxygen_downloader_extract(testdirectory):
#     testdirectory.copy_file('test/data/archive/test_files.zip')

#     archive = os.path.join(testdirectory.path(), 'test_files.zip')
#     to_path = os.path.join(testdirectory.path(), 'output')

#     wurfdocs.doxygen_downloader.extract(archive_path=archive, to_path=to_path)
