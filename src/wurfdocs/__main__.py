import click
import tempfile
import hashlib
import os
import logging
import json

import wurfdocs.factory
import wurfdocs.build_info


@click.command()
@click.option('--build_path')
@click.option('--wurfdocs_path')
@click.option('--json_config')
@click.argument('step')
@click.argument('repository')
def cli(step, repository, build_path, wurfdocs_path, json_config):

    logging.basicConfig(filename='wurfdocs.log', level=logging.DEBUG)

    log = logging.getLogger('wurfdocs.main')

    # Resolve the repository
    factory = wurfdocs.factory.resolve_factory(
        data_path=wurfdocs_path)

    git_repository = factory.build()
    git_repository.clone(repository=repository)

    # Read the config
    with open(json_config, 'r') as config_file:

        config = json.load(config_file)
        step_config = config[step]

    # Instantiate the cache
    cache_factory = wurfdocs.factory.cache_factory(
        data_path=wurfdocs_path, unique_name=git_repository.unique_name)

    cache = cache_factory.build()

    return

    # Build the documentation
    factory = wurfdocs.factory.build_factory(
        wurfdocs_path=wurfdocs_path, build_path=build_path,
        git_repository=git_repository, cache=cache, config=step_config)

    with cache:

        task_generator = factory.build()

        tasks = task_generator.tasks()

        for task in tasks:

            try:
                build_info = wurfdocs.build_info.BuildInfo()
                task.run(build_info=build_info)

            except RuntimeError as re:
                log.debug(re)


if __name__ == "__main__":
    cli()
