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
@click.option('--config_file')
@click.argument('step')
@click.argument('repository')
def cli(step, repository, build_path, wurfdocs_path, config_file):

    logging.basicConfig(filename='wurfdocs.log', level=logging.DEBUG)

    log = logging.getLogger('wurfdocs.main')

    return

    # Resolve the repository
    factory = wurfdocs.factory.resolve_factory(
        data_path=data_path)

    git_repository = factory.build()
    git_repository.clone(repository=repository)

    # Instantiate the cache
    cache_factory = wurfdocs.factory.cache_factory(
        data_path=data_path, unique_name=git_repository.unique_name)

    cache = cache_factory.build()

    # Build the documentation
    factory = wurfdocs.factory.build_factory(
        data_path=data_path, output_path=output_path,
        git_repository=git_repository, cache=cache)

    versions = {
        'output_path': output_path,
        'builds': []
    }

    with cache:

        task_generator = factory.build()

        tasks = task_generator.tasks()

        for task in tasks:

            try:
                build_info = wurfdocs.build_info.BuildInfo()
                task.run(build_info=build_info)

                version = {
                    'slug': build_info.slug,
                    'type': build_info.type,
                    'path': build_info.output_path
                }

                versions['builds'].append(version)

            except RuntimeError as re:
                log.debug(re)

    with open('versions.json', 'w') as versions_json:

        json.dump(versions, versions_json, indent=2, sort_keys=True,
                  separators=(',', ': '))

    # If needed push the docs




if __name__ == "__main__":
    cli()
