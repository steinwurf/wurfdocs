import click
import tempfile
import hashlib
import os
import logging
import json

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

        logfile = os.path.join(self.wurfdocs_path, 'wurfdocs.log')

        logging.basicConfig(filename=logfile,
                            level=logging.DEBUG)

        log = logging.getLogger('wurfdocs.main')
        log.debug('build_path=%s', self.build_path)
        log.debug('wurfdocs_path=%s', self.wurfdocs_path)
        log.debug('json_config=%s', self.json_config)
        log.debug('source_branch=%s', self.source_branch)

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

        # Run the command
        if config[self.step]['type'] == 'python':

            factory = wurfdocs.factory.build_python_factory(
                build_path=self.build_path, wurfdocs_path=self.wurfdocs_path,
                git_repository=git_repository, cache=cache,
                config=config[self.step])

        else:
            assert 0

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
