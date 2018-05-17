import mock
import os

import wurfdocs
from wurfdocs.sphinx_environment import SphinxEnvironment
from wurfdocs.build_info import BuildInfo


def test_sphinx_environment_no_requirements(testdirectory):

    prompt = mock.Mock()
    virtualenv = mock.Mock()
    build_info = BuildInfo()

    env = {'PATH': '/oki/doki'}
    virtualenv.create_environment.side_effect = lambda name: env

    build_info.config_dir = testdirectory.path()

    sphinx_environment = SphinxEnvironment(
        prompt=prompt, virtualenv=virtualenv)

    sphinx_environment.create_environment(build_info=build_info)

    assert 'sphinx_env' in build_info

    command = 'python -m pip install sphinx'
    prompt.run.assert_called_once_with(command=command, env=env)


def test_sphinx_environment_requirements(testdirectory):

    prompt = mock.Mock()
    virtualenv = mock.Mock()
    build_info = BuildInfo()

    env = {'PATH': '/oki/doki'}
    virtualenv.create_environment.side_effect = lambda name: env

    build_info.config_dir = testdirectory.path()
    testdirectory.write_text(filename='requirements.txt',
                             data=u'okok', encoding='utf-8')

    sphinx_environment = SphinxEnvironment(
        prompt=prompt, virtualenv=virtualenv)

    sphinx_environment.create_environment(build_info=build_info)

    assert 'sphinx_env' in build_info

    command = 'python -m pip install -r {}'.format(
        os.path.join(testdirectory.path(), 'requirements.txt'))
    prompt.run.assert_called_once_with(command=command, env=env)
