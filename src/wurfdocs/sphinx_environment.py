#! /usr/bin/env python
# encoding: utf-8

import os
import sys
import hashlib

import wurfdocs.virtualenv
import wurfdocs.commandline


class SphinxEnvironment(object):
    """ Update the environment to have the needed dependencies in PATH.

    """

    def __init__(self, prompt, virtualenv):
        self.prompt = prompt
        self.virtualenv = virtualenv

    def create_environment(self, build_info):
        """ Populates the build_info object with the sphinx_env key. """

        # Check if there is a requirements.txt file next to the Sphinx
        # configuration file if so we install it

        requirements_path = os.path.join(
            build_info.config_dir, 'requirements.txt')

        if os.path.isfile(requirements_path):

            self._create_from_requirements_file(
                build_info=build_info,
                requirements_path=requirements_path)

        else:

            self._create_default(build_info=build_info)

    def _create_from_requirements_file(self, requirements_path, build_info):

        with open(requirements_path, 'r') as requirements_file:
            requirements = requirements_file.read()

        name = self._environment_name(requirements=requirements)
        build_info.sphinx_env = self.virtualenv.create_environment(name=name)

        command = 'python -m pip install -r {}'.format(requirements_path)

        # Ensure the dependencies are available
        self.prompt.run(command=command, env=build_info.sphinx_env)

    def _create_default(self, build_info):

        name = self._environment_name(requirements='sphinx')
        build_info.sphinx_env = self.virtualenv.create_environment(name=name)

        command = 'python -m pip install sphinx'

        # Ensure the dependencies are available
        self.prompt.run(command=command, env=build_info.sphinx_env)

    def _environment_name(self, requirements):
        """ Create an unique name for the environment. """

        # The Python executable
        python = sys.executable
        python_hash = hashlib.sha1(
            python.encode('utf-8')).hexdigest()[:6]

        # The requirements
        requirements_hash = hashlib.sha1(
            requirements.encode('utf-8')).hexdigest()[:6]

        name = 'sphinx-virtualenv-' + requirements_hash + '-' + python_hash

        return name


def build(application_info):
    pass
