#! /usr/bin/env python
# encoding: utf-8

import os
import sys
import hashlib
import shutil
import logging

import wurfdocs.prompt
import wurfdocs.git
import wurfdocs.git_url_parser
import wurfdocs.git_repository
import wurfdocs.cache
import wurfdocs.virtualenv
import wurfdocs.tasks
import wurfdocs.python_config
import wurfdocs.python_environment
import wurfdocs.python_command


class Factory(object):

    def __init__(self, build_name):

        self.build_name = build_name
        self.providers = {}

    def provide_value(self, name, value):

        assert name not in self.providers

        def call():
            return value

        self.providers[name] = call

    def provide_function(self, name, function, override=False):

        if override:
            assert name in self.providers
        else:
            assert name not in self.providers

        def call():
            return function(self)

        self.providers[name] = call

    def require(self, name):
        return self.providers[name]()

    def build(self):
        return self.require(name=self.build_name)


def require_prompt(factory):
    return wurfdocs.prompt.Prompt()


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


def require_git_repository(factory):
    git = factory.require(name='git')
    git_url_parser = factory.require(name='git_url_parser')
    source_branch = factory.require(name='source_branch')
    log = logging.getLogger(name='wurfdocs.git_repository')
    clone_path = factory.require(name='clone_path')

    return wurfdocs.git_repository.GitRepository(
        git=git, git_url_parser=git_url_parser, clone_path=clone_path,
        log=log, source_branch=source_branch)


def provide_clone_path(factory):

    data_path = factory.require(name='wurfdocs_path')

    return os.path.join(data_path, 'clones')


def require_cache(factory):

    data_path = factory.require(name='data_path')
    unique_name = factory.require(name='unique_name')

    return wurfdocs.cache.Cache(
        cache_path=data_path, unique_name=unique_name)


def require_task_generator(factory):

    git_repository = factory.require(name='git_repository')
    command = factory.require(name='command')
    build_path = factory.require(name='build_path')
    git = factory.require(name='git')
    # cache = factory.require(name='cache')

    workingtree_generator = wurfdocs.tasks.WorkingtreeGenerator(
        git_repository=git_repository,
        command=command, build_path=build_path)

    git_branch_generator = wurfdocs.tasks.GitBranchGenerator(
        git=git, git_repository=git_repository,
        command=command, build_path=build_path)

    task_generator = wurfdocs.tasks.TaskFactory()

    task_generator.add_generator(workingtree_generator)
    task_generator.add_generator(git_branch_generator)

    if command.config.recurse_tags:

        git_tag_generator = wurfdocs.tasks.GitTagGenerator(
            git=git, git_repository=git_repository,
            command=command, build_path=build_path)

        task_generator.add_generator(git_tag_generator)

    return task_generator


def resolve_factory(wurfdocs_path, source_branch):

    factory = Factory(build_name='git_repository')

    factory.provide_value(name='git_binary', value='git')
    factory.provide_value(name='wurfdocs_path', value=wurfdocs_path)
    factory.provide_value(name='source_branch', value=source_branch)

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


def require_python_config(factory):

    config = factory.require(name='config')
    return wurfdocs.python_config.PythonConfig.from_dict(
        config=config)


def require_python_environement(factory):

    prompt = factory.require(name='prompt')
    virtualenv = factory.require(name='virtualenv')
    log = logging.getLogger(name='wurfdocs.python_environement')

    return wurfdocs.python_environment.PythonEnvironment(
        prompt=prompt, virtualenv=virtualenv, log=log)


def require_python_command(factory):

    config = factory.require(name='python_config')
    environment = factory.require(name='python_environment')
    prompt = factory.require(name='prompt')
    log = logging.getLogger(name='wurfdocs.python_command')

    return wurfdocs.python_command.PythonCommand(
        config=config, environment=environment, prompt=prompt, log=log)


def build_python_factory(build_path, wurfdocs_path, git_repository,
                         cache, config):

    factory = Factory(build_name='require_task_generator')

    factory.provide_value(
        name='config', value=config)

    factory.provide_value(
        name='build_path', value=build_path)

    factory.provide_value(
        name='wurfdocs_path', value=wurfdocs_path)

    factory.provide_value(
        name='git_repository', value=git_repository)

    factory.provide_function(
        name='python_config', function=require_python_config)

    factory.provide_function(
        name='prompt', function=require_prompt)

    factory.provide_function(
        name='python_environment', function=require_python_environement)

    factory.provide_function(
        name='command', function=require_python_command)

    factory.provide_value(name='output_path', value=wurfdocs_path)
    factory.provide_function(name='clone_path', function=provide_clone_path)

    virtualenv_root_path = os.path.join(wurfdocs_path, 'virtualenvs')
    factory.provide_value(name='virtualenv_root_path',
                          value=virtualenv_root_path)

    factory.provide_value(name='git_binary', value='git')

    factory.provide_function(name='git_url_parser',
                             function=require_git_url_parser)
    factory.provide_function(name='git', function=require_git)

    factory.provide_function(name='virtualenv', function=require_virtualenv)

    factory.provide_function(
        name='require_task_generator', function=require_task_generator)

    return factory
