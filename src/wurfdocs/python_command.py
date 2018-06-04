#! /usr/bin/env python
# encoding: utf-8

import os


class PythonCommand(object):

    def __init__(self, scripts, variables, environment, prompt, log):
        """
        :param runner: A command.run function.
        """
        self.variables = variables
        self.environment = environment
        self.prompt = prompt

    def run(self):

        if self.requirements:

        env = self.environment.create()

        for script in self.scripts:
            command = self.variables.expand(script)
            self.prompt.run(command=command, env=env, cwd=self.cwd)
