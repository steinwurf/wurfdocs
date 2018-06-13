import click
import tempfile
import hashlib
import os
import logging
import json

import wurfdocs.factory
import wurfdocs.build_info


@click.command()
@click.option('--source_branch')
@click.option('--build_path')
@click.option('--wurfdocs_path')
@click.option('--json_config')
@click.argument('step')
@click.argument('repository')
def cli(step, repository, build_path, wurfdocs_path, json_config,
        source_branch):

    logging.basicConfig(filename='wurfdocs.log',
                        level=logging.DEBUG)

    log = logging.getLogger('wurfdocs.main')
    log.debug('build_path=%s', build_path)
    log.debug('wurfdocs_path=%s', wurfdocs_path)
    log.debug('json_config=%s', json_config)
    log.debug('source_branch=%s', source_branch)

    # Resolve the repository
    factory = wurfdocs.factory.resolve_factory(
        wurfdocs_path=wurfdocs_path, source_branch=source_branch)

    git_repository = factory.build()
    git_repository.clone(repository=repository)

    # Instantiate the cache
    cache_factory = wurfdocs.factory.cache_factory(
        data_path=wurfdocs_path,
        unique_name=git_repository.unique_name)

    cache = cache_factory.build()

    # Get the command
    with open(json_config, 'r') as config_file:
        config = json.load(config_file)

    # Run the command
    if config[step]['type'] == 'python':

        factory = wurfdocs.factory.build_python_factory(
            build_path=build_path, wurfdocs_path=wurfdocs_path,
            git_repository=git_repository, cache=cache,
            config=config[step])

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


if __name__ == "__main__":
    cli()
