import os
import mock

import wurfdocs
from wurfdocs.sphinx_config import SphinxConfig


def test_sphinx_config_path(testdirectory):

    nested_a = testdirectory.mkdir('a')
    nested_b = nested_a.mkdir('b')

    nested_b.write_text(filename='conf.py', data=u'hello', encoding='utf-8')

    sphinx = SphinxConfig()

    build_info = mock.Mock()
    build_info.repository_path = testdirectory.path()

    sphinx.update_build(build_info=build_info)

    assert build_info.config_file_path == os.path.join(
        nested_b.path(), 'conf.py')

    assert build_info.config_file == 'conf.py'
    assert build_info.config_dir == nested_b.path()
