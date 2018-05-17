#! /usr/bin/env python
# encoding: utf-8

import os
import sys
import hashlib
import shutil
import logging

import wurfdocs.commandline
import wurfdocs.git
import wurfdocs.git_url_parser
import wurfdocs.git_repository
import wurfdocs.cache
import wurfdocs.sphinx_config
import wurfdocs.virtualenv
import wurfdocs.sphinx_environment
import wurfdocs.sphinx
import wurfdocs.tasks


class Factory(object):

    def __init__(self):

        self.providers = {}

    def provide_value(self, name, value):

        assert name not in self.providers

        def call():
            return value

        self.providers[name] = call

    def provide_function(self, name, function):

        assert name not in self.providers

        def call():
            return function(self)

        self.providers[name] = call

    def build(self, name):
        return self.providers[name]()


def build_prompt(factory):
    return wurfdocs.commandline.Prompt()


def build_git(factory):

    prompt = factory.build(name='prompt')
    git_binary = factory.build(name='git_binary')

    return wurfdocs.git.Git(git_binary=git_binary, prompt=prompt)


def build_git_url_parser(factory):
    return wurfdocs.git_url_parser.GitUrlParser()


def build_virtualenv(factory):

    git = factory.build(name='git')
    clone_path = factory.build(name='clone_path')
    virtualenv_root_path = factory.build(name='virtualenv_root_path')
    log = logging.getLogger(name='wurfdocs.virtualenv')

    venv = wurfdocs.virtualenv.VirtualEnv.from_git(
        git=git, clone_path=clone_path, log=log)

    venv = wurfdocs.virtualenv.NameToPathAdapter(
        virtualenv=venv, virtualenv_root_path=virtualenv_root_path)

    return venv


def build_sphinx_environment(factory):

    prompt = factory.build(name='prompt')
    virtualenv = factory.build(name='virtualenv')

    return wurfdocs.sphinx_environment.SphinxEnvironment(
        prompt=prompt, virtualenv=virtualenv)


def build_sphinx_config(factory):
    return wurfdocs.sphinx_config.SphinxConfig()


def build_sphinx(factory):

    sphinx_config = factory.build(name='sphinx_config')
    sphinx_environment = factory.build(name='sphinx_environment')
    prompt = factory.build(name='prompt')

    return wurfdocs.sphinx.Sphinx(
        sphinx_config=sphinx_config, sphinx_environment=sphinx_environment,
        prompt=prompt)


def build_git_repository(factory):
    git = factory.build(name='git')
    git_url_parser = factory.build(name='git_url_parser')
    log = logging.getLogger(name='wurfdocs.git_repository')
    clone_path = factory.build(name='clone_path')

    return wurfdocs.git_repository.GitRepository(
        git=git, git_url_parser=git_url_parser, clone_path=clone_path,
        log=log)


def provide_clone_path(factory):

    data_path = factory.build(name='data_path')

    return os.path.join(data_path, 'clones')


def build_cache(factory):

    data_path = factory.build(name='data_path')
    unique_name = factory.build(name='unique_name')

    return wurfdocs.cache.Cache(
        cache_path=data_path, unique_name=unique_name)


def build_task_generator(factory):

    output_path = factory.build(name='output_path')
    git_repository = factory.build(name='git_repository')
    sphinx = factory.build(name='sphinx')
    git = factory.build(name='git')
    cache = factory.build(name='cache')

    workingtree_generator = wurfdocs.tasks.WorkingtreeGenerator(
        repository=git_repository,
        output_path=output_path, sphinx=sphinx)

    git_branch_generator = wurfdocs.tasks.GitBranchGenerator(
        repository=git_repository,
        output_path=output_path, sphinx=sphinx, git=git, cache=cache)

    git_tag_generator = wurfdocs.tasks.GitTagGenerator(
        repository=git_repository,
        output_path=output_path, sphinx=sphinx, git=git, cache=cache)

    task_generator = wurfdocs.tasks.TaskFactory()

    task_generator.add_generator(workingtree_generator)
    task_generator.add_generator(git_branch_generator)
    task_generator.add_generator(git_tag_generator)

    return task_generator


def resolve_factory(data_path):

    factory = Factory()

    factory.provide_value(name='git_binary', value='git')
    factory.provide_value(name='data_path', value=data_path)
    factory.provide_function(name='clone_path', function=provide_clone_path)
    factory.provide_function(name='git_url_parser',
                             function=build_git_url_parser)
    factory.provide_function(name='git', function=build_git)
    factory.provide_function(name='git_repository',
                             function=build_git_repository)
    factory.provide_function(name='prompt', function=build_prompt)

    return factory


def cache_factory(data_path, unique_name):

    factory = Factory()
    factory.provide_value(name='data_path', value=data_path)
    factory.provide_value(name='unique_name', value=unique_name)
    factory.provide_function(name='cache', function=build_cache)

    return factory


def build_factory(data_path, output_path, git_repository, cache):

    factory = Factory()

    virtualenv_root_path = os.path.join(data_path, 'virtualenvs')

    factory.provide_value(name='git_binary', value='git')
    factory.provide_function(name='clone_path', function=provide_clone_path)

    factory.provide_value(name='data_path', value=data_path)
    factory.provide_value(name='cache', value=cache)

    factory.provide_value(name='output_path', value=output_path)
    factory.provide_value(name='virtualenv_root_path',
                          value=virtualenv_root_path)
    factory.provide_function(name='prompt', function=build_prompt)
    factory.provide_function(name='git_url_parser',
                             function=build_git_url_parser)
    factory.provide_function(name='git', function=build_git)
    factory.provide_function(name='virtualenv', function=build_virtualenv)
    factory.provide_function(name='sphinx_environment',
                             function=build_sphinx_environment)
    factory.provide_function(name='sphinx_config',
                             function=build_sphinx_config)
    factory.provide_function(name='sphinx',
                             function=build_sphinx)

    factory.provide_value(name='git_repository',
                          value=git_repository)

    factory.provide_function(name='task_generator',
                             function=build_task_generator)

    return factory
