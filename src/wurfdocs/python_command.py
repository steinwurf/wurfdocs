#! /usr/bin/env python
# encoding: utf-8

import os
import sys
import hashlib


class PythonCommand(object):

    def __init__(self, config, environment, prompt, log):
        """
        :param runner: A command.run function.
        """
        self.config = config
        self.environment = environment
        self.prompt = prompt
        self.log = log

    def run(self, context):

        self.config.set_context(context=context)

        if 'requirements' in self.config:
            env = self.environment.from_requirements(
                requirements=self.config.requirements)
        else:
            env = self.environment.from_system()

        for script in self.config.scripts:

            try:
                self.prompt.run(command=script, cwd=self.config.cwd,
                                env=env)
            except Exception:

                if not self.config.allow_failure:
                    raise
                else:
                    self.log.exception('run')


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


class Config(object):

    def __init__(self, config):
        pass
