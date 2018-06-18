import click
import tempfile
import hashlib
import os
import logging
import json
import sys

import wurfdocs.factory


class Build(object):

    def __init__(self, step,
                 repository,
                 build_path=None,
                 wurfdocs_path=None,
                 json_config=None,
                 source_branch=None):

        self.step = step
        self.repository = repository
        self.build_path = build_path
        self.wurfdocs_path = wurfdocs_path
        self.json_config = json_config
        self.source_branch = source_branch

    def run(self):

        # Location for giit files - if not user specified
        giit_path = os.path.join(tempfile.gettempdir(), 'giit')

        # Setup some defaults
        if not self.build_path:
            self.build_path = os.path.join(giit_path, 'build')

            if not os.path.isdir(self.build_path):
                os.makedirs(self.build_path)

        if not self.wurfdocs_path:
            self.wurfdocs_path = os.path.join(giit_path, 'data')

            if not os.path.isdir(self.wurfdocs_path):
                os.makedirs(self.wurfdocs_path)

        logger = logging.getLogger('wurfdocs')
        logger.setLevel(logging.DEBUG)

        # create file handler which logs even debug messages
        logfile = os.path.join(self.wurfdocs_path, 'wurfdocs.log')
        fh = logging.FileHandler(logfile)
        fh.setLevel(logging.DEBUG)

        # create console handler with a higher log level
        ch = logging.StreamHandler(stream=sys.stdout)
        ch.setLevel(logging.INFO)

        # create formatter and add it to the handlers
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)

        log = logging.getLogger('wurfdocs.main')
        log.debug('build_path=%s', self.build_path)
        log.debug('wurfdocs_path=%s', self.wurfdocs_path)
        log.debug('json_config=%s', self.json_config)
        log.debug('source_branch=%s', self.source_branch)

        log.info('Lets go!')

        # Resolve the repository
        factory = self.resolve_factory()

        git_repository = factory.build()
        git_repository.clone(repository=self.repository)

        # Instantiate the cache
        cache_factory = self.clone_factory(
            unique_name=git_repository.unique_name)

        cache = cache_factory.build()

        # Get the command
        if not self.json_config:
            self.json_config = os.path.join(
                git_repository.repository_path, 'wurfdocs.json')

        with open(self.json_config, 'r') as config_file:
            config = json.load(config_file)

        # All steps has a type which controls the available options and actions
        build_type = config[self.step]['type']

        factory = wurfdocs.factory.build_factory(build_type=build_type)

        # Provide the different needed by the factory
        factory.provide_value(name='config', value=config[self.step])
        factory.provide_value(name='build_path', value=self.build_path)
        factory.provide_value(name='wurfdocs_path', value=self.wurfdocs_path)
        factory.provide_value(name='git_repository', value=git_repository)

        # Run the command

        with cache:

            task_generator = factory.build()

            tasks = task_generator.tasks()

            for task in tasks:

                try:
                    task.run()

                except RuntimeError as re:
                    log.debug(re)

    def resolve_factory(self):
        return wurfdocs.factory.resolve_factory(
            wurfdocs_path=self.wurfdocs_path,
            source_branch=self.source_branch)

    def clone_factory(self, unique_name):
        return wurfdocs.factory.cache_factory(
            data_path=self.wurfdocs_path,
            unique_name=unique_name)
