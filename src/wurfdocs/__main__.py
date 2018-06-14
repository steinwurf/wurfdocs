import click

import wurfdocs.build


@click.command()
@click.option('--source_branch')
@click.option('--build_path')
@click.option('--wurfdocs_path')
@click.option('--json_config')
@click.argument('step')
@click.argument('repository')
def cli(step, repository, build_path, wurfdocs_path, json_config,
        source_branch):

    build = wurfdocs.build.Build(
        step=step, repository=repository,
        build_path=build_path, wurfdocs_path=wurfdocs_path,
        json_config=json_config, source_branch=source_branch)

    build.run()


if __name__ == "__main__":
    cli()
