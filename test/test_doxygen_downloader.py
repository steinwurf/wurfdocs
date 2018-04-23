import mock
import os

import wurfdocs
import wurfdocs.doxygen_downloader


def test_doxygen_downloader(testdirectory):
    pass
    # wurfdocs.doxygen_downloader.extract(
    #     cwd=testdirectory.path())


# @vcr.use_cassette('test/vcr_cassettes/https_cxx_prettyprint_resolver.yaml')
# def test_url_download_cxx_prettyprint_rename(testdirectory):
#     source = 'https://github.com/louisdx/cxx-prettyprint/zipball/master'
#     cwd = testdirectory.path()

#     download = UrlDownload()

#     path = download.download(cwd=cwd, source=source, filename='test.zip')

#     assert os.path.join(cwd, 'test.zip') == path
