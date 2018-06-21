#! /usr/bin/env python
# encoding: utf-8

import os
import sys
import hashlib

import wurfdocs.config_reader


class PythonCommand(object):

    def __init__(self, config, environment, prompt, log):
        """
        :param config: A PythonConfig object
        """
        self.config = config
        self.environment = environment
        self.prompt = prompt
        self.log = log

    def run(self, context):

        self.log.debug("context=%s", context)

        reader = wurfdocs.config_reader.ConfigReader(
            config=self.config, context=context)

        env = self.environment.from_requirements(
            requirements=reader.requirements,
            pip_packages=reader.pip_packages)

        for script in reader.scripts:

            try:

                self.log.info('Python: %s', script)

                self.prompt.run(command=script, cwd=reader.cwd,
                                env=env)

            except Exception:

                if reader.allow_failure:
                    self.log.debug("#TEMP Caught exception")
                    self.log.exception('run')
                else:
                    self.log.debug("#TEMP Raise exception")
                    raise
