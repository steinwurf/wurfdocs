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

    def __init__(self, build_name):

        self.build_name = build_name
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

    def require(self, name):
        return self.providers[name]()

    def build(self):
        return self.require(name=self.build_name)


def require_prompt(factory):
    return wurfdocs.commandline.Prompt()


def require_git(factory):

    prompt = factory.require(name='prompt')
    git_binary = factory.require(name='git_binary')

    return wurfdocs.git.Git(git_binary=git_binary, prompt=prompt)


def require_git_url_parser(factory):
    return wurfdocs.git_url_parser.GitUrlParser()


def require_virtualenv(factory):

    git = factory.require(name='git')
    clone_path = factory.require(name='clone_path')
    virtualenv_root_path = factory.require(name='virtualenv_root_path')
    log = logging.getLogger(name='wurfdocs.virtualenv')

    venv = wurfdocs.virtualenv.VirtualEnv.from_git(
        git=git, clone_path=clone_path, log=log)

    venv = wurfdocs.virtualenv.NameToPathAdapter(
        virtualenv=venv, virtualenv_root_path=virtualenv_root_path)

    return venv


def require_sphinx_environment(factory):

    prompt = factory.require(name='prompt')
    virtualenv = factory.require(name='virtualenv')

    return wurfdocs.sphinx_environment.SphinxEnvironment(
        prompt=prompt, virtualenv=virtualenv)


def require_sphinx_config(factory):
    return wurfdocs.sphinx_config.SphinxConfig()


def require_sphinx(factory):

    sphinx_config = factory.require(name='sphinx_config')
    sphinx_environment = factory.require(name='sphinx_environment')
    prompt = factory.require(name='prompt')

    return wurfdocs.sphinx.Sphinx(
        sphinx_config=sphinx_config, sphinx_environment=sphinx_environment,
        prompt=prompt)


def require_git_repository(factory):
    git = factory.require(name='git')
    git_url_parser = factory.require(name='git_url_parser')
    log = logging.getLogger(name='wurfdocs.git_repository')
    clone_path = factory.require(name='clone_path')

    return wurfdocs.git_repository.GitRepository(
        git=git, git_url_parser=git_url_parser, clone_path=clone_path,
        log=log)


def provide_clone_path(factory):

    data_path = factory.require(name='data_path')

    return os.path.join(data_path, 'clones')


def require_cache(factory):

    data_path = factory.require(name='data_path')
    unique_name = factory.require(name='unique_name')

    return wurfdocs.cache.Cache(
        cache_path=data_path, unique_name=unique_name)


def require_task_generator(factory):

    output_path = factory.require(name='output_path')
    git_repository = factory.require(name='git_repository')
    sphinx = factory.require(name='sphinx')
    git = factory.require(name='git')
    cache = factory.require(name='cache')

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

    factory = Factory(build_name='git_repository')

    factory.provide_value(name='git_binary', value='git')
    factory.provide_value(name='data_path', value=data_path)
    factory.provide_function(name='clone_path', function=provide_clone_path)
    factory.provide_function(name='git_url_parser',
                             function=require_git_url_parser)
    factory.provide_function(name='git', function=require_git)
    factory.provide_function(name='git_repository',
                             function=require_git_repository)
    factory.provide_function(name='prompt', function=require_prompt)

    return factory


def cache_factory(data_path, unique_name):

    factory = Factory(build_name='cache')
    factory.provide_value(name='data_path', value=data_path)
    factory.provide_value(name='unique_name', value=unique_name)
    factory.provide_function(name='cache', function=require_cache)

    return factory


def require_python_generator(factory):

    config = factory.require(name='config')

    python_prompt = factory.require(name='python_prompt')

    workingtree_generator = wurfdocs.tasks.WorkingtreeGenerator(
        repository=git_repository,
        output_path=output_path, python_prompt=python_prompt)

    task_generator = wurfdocs.tasks.TaskFactory()
    task_generator.add_generator(workingtree_generator)


def build_python_factory(build_path, wurfdocs_path, git_repository,
                         cache, step_config):

    factory = Factory(build_name='python_generator')

        workingtree_generator = wurfdocs.tasks.WorkingtreeGenerator(
            repository=git_repository,
            output_path=output_path, python_prompt=python_prompt)

    return factory


def build_factory(wurfdocs_path, build_path, git_repository,
                  cache, command):

    if command["type"] == "python":
        return build_python_factory(
            wurfdocs_path=wurfdocs_path,
            build_path=build_path, git_repository=git_repository,
            cache=cache, command=command)

    assert 0

# def build_factory(data_path, output_path, git_repository, cache, config):

#     factory = Factory(build_name='task_generator')

#     virtualenv_root_path = os.path.join(data_path, 'virtualenvs')

#     factory.provide_value(name='git_binary', value='git')
#     factory.provide_function(name='clone_path', function=provide_clone_path)

#     factory.provide_value(name='data_path', value=data_path)
#     factory.provide_value(name='cache', value=cache)

#     factory.provide_value(name='output_path', value=output_path)
#     factory.provide_value(name='virtualenv_root_path',
#                           value=virtualenv_root_path)
#     factory.provide_function(name='prompt', function=require_prompt)
#     factory.provide_function(name='git_url_parser',
#                              function=require_git_url_parser)
#     factory.provide_function(name='git', function=require_git)
#     factory.provide_function(name='virtualenv', function=require_virtualenv)
#     factory.provide_function(name='sphinx_environment',
#                              function=require_sphinx_environment)
#     factory.provide_function(name='sphinx_config',
#                              function=require_sphinx_config)
#     factory.provide_function(name='sphinx',
#                              function=require_sphinx)

#     factory.provide_value(name='git_repository',
#                           value=git_repository)

#     factory.provide_function(name='task_generator',
#                              function=require_task_generator)

#     return factory
