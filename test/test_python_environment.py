import mock
import os
import sys
import hashlib

import wurfdocs


class PythonEnvironment(object):

    def __init__(self, prompt, virtualenv, requirements):
        self.prompt = prompt
        self.virtualenv = virtualenv
        self.requirements = requirements

    def create_environment(self):

        name = self._environment_name()
        env = self.virtualenv.create_environment(name=name)

        # Install the requirements
        command = 'python -m pip install -r {}'.format(self.requirements)
        self.prompt.run(command=command, env=env)

        return env

    def _environment_name(self):
        """ Create an unique name for the environment. """

        # The Python executable
        python = sys.executable
        python_hash = hashlib.sha1(
            python.encode('utf-8')).hexdigest()[:6]

        # The requirements
        requirements_hash = hashlib.sha1(
            self.requirements.encode('utf-8')).hexdigest()[:6]

        name = 'wurfdocs-virtualenv-' + requirements_hash + '-' + python_hash

        return name


def test_python_environment(testdirectory):

    prompt = mock.Mock()
    virtualenv = mock.Mock()
    requirements = testdirectory.write_text(
        filename='requirements.txt', data=u'sphinx', encoding='utf-8')

    env = {'PATH': '/oki/doki'}
    virtualenv.create_environment.side_effect = lambda name: env

    python_environment = PythonEnvironment(
        prompt=prompt, virtualenv=virtualenv, requirements=requirements)

    venv = python_environment.create_environment()

    assert venv == env

    command = 'python -m pip install -r {}'.format(
        os.path.join(testdirectory.path(), 'requirements.txt'))
    prompt.run.assert_called_once_with(command=command, env=env)
