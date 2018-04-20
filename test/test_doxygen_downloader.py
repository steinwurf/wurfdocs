import mock
import os

import wurfdocs
import wurfdocs.doxygen_downloader


def test_doxygen_downloader(testdirectory):
    wurfdocs.doxygen_downloader.download(
        cwd=testdirectory.path())
