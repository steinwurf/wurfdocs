import mock

import wurfdocs
from wurfdocs.sphinx import Sphinx
from wurfdocs.build_info import BuildInfo


def test_sphinx_build(testdirectory):

    sphinx_config = mock.Mock()
    sphinx_environment = mock.Mock()
    prompt = mock.Mock()

    build_info = BuildInfo()

    source_dir = testdirectory.mkdir('sources')
    output_dir = testdirectory.mkdir('output')

    conf_file = source_dir.write_text(
        filename='conf.py', data=u'bla', encoding='utf-8')

    build_info.source_path = source_dir.path()
    build_info.output_path = output_dir.path()
    build_info.config_dir = source_dir.path()

    env = {"PATH": "/tmp"}

    build_info.sphinx_env = env

    sphinx = Sphinx(sphinx_config=sphinx_config,
                    sphinx_environment=sphinx_environment,
                    prompt=prompt)

    sphinx.build(build_info=build_info)

    sphinx_config.update_build.assert_called_once_with(build_info=build_info)
    sphinx_environment.create_environment.assert_called_once_with(
        build_info=build_info)

    command = ['sphinx-build', '-b', 'html']

    # Specify the config file
    command += ['-c', source_dir.path()]

    # Specify the sources directory
    command += [source_dir.path()]

    # Specify the outputdir
    command += [output_dir.path()]

    prompt.run.assert_called_once_with(
        command=command, cwd=source_dir.path(), env=env)
