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

        reader = ConfigReader(config=config, context=context)

        if reader.requirements:
            env = self.environment.from_requirements(
                requirements=self.requirements)
        else:
            env = self.environment.from_system()

        for script in reader.scripts:

            command = se

            try:
                self.prompt.run(command=script, cwd=self.config.cwd,
                                env=env)
            except Exception:

                if not self.config.allow_failure:
                    raise
                else:
                    self.log.exception('run')

    def expand(element, default, context):

        if element in self.config:
            return element
        else:
            return default


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


class PythonConfig(object):

    def __init__(self, config):
        self.config = config
        self.context = None

        # Validate the config
        assert config['type'] == 'python'
        assert len(config['scripts']) > 0

        def expand(context, variables):
            var = wurfdocs.variables.Variables(
                context=context)

        # Set defaults
        if 'requirements' not in self.config:
            self.config['requirement'] = None

        if 'allow_failure' not in self.config:
            self.config['allow_failure'] = False

        if 'recurse_tags' not in self.config:
            self.config['recurse_tags'] = False

        if 'variables' not in self.config:
            self.config['variables'] = None

    def __getattr__(self, attribute):
        """ Return the value corresponding to the attribute.
        :param attribute: The name of the attribute to return as a string.
        :return: The attribute value, if the attribute does not exist
            return None
        """

        raise AttributeError("No key {}".format(attribute))

    def set_context(self, context):
        self.context = context
