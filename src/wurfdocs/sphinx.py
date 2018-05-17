#! /usr/bin/env python
# encoding: utf-8

import os


class Sphinx(object):

    def __init__(self, sphinx_config, sphinx_environment, prompt):
        """
        :param runner: A command.run function.
        """
        self.sphinx_config = sphinx_config
        self.sphinx_environment = sphinx_environment
        self.prompt = prompt

    def build(self, build_info):

        # Running sphinx-build will fail if the repository does
        # not have working docs for the given branch, tag etc.
        self.sphinx_config.update_build(build_info=build_info)

        # Create the environment (with sphinx installed etc)
        self.sphinx_environment.create_environment(build_info=build_info)

        command = ['sphinx-build', '-b', 'html']

        # Specify the config file
        command += ['-c', build_info.config_dir]

        # Specify the sources directory
        command += [build_info.source_path]

        # Specify the outputdir
        command += [build_info.output_path]

        self.prompt.run(command=command, cwd=build_info.source_path,
                        env=build_info.sphinx_env)
