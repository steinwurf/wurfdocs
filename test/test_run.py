import os

import wurfdocs
import wurfdocs.run


def test_run(testdirectory):
    wurfdocs.run.run('python --version', cwd=testdirectory.path())
