#! /usr/bin/env python
# encoding: utf-8


class PythonEnvironment(object):

    def __init__(self, prompt, virtualenv):
        self.prompt = prompt
        self.virtualenv = virtualenv

    def from_requirements(self, requirements):

        name = self._environment_name(requirements=requirements)
        env = self.virtualenv.create_environment(name=name)

        # Install the requirements
        command = 'python -m pip install -r {}'.format(requirements)

        self.prompt.run(command=command, env=env)

        return env

    def from_system(self):
        return dict(os.environ)

    def _environment_name(self, requirements):
        """ Create an unique name for the environment. """

        # The Python executable
        python = sys.executable
        python_hash = hashlib.sha1(
            python.encode('utf-8')).hexdigest()[:6]

        # The requirements
        requirements_hash = hashlib.sha1(
            requirements.encode('utf-8')).hexdigest()[:6]

        name = 'wurfdocs-virtualenv-' + requirements_hash + '-' + python_hash

        return name
