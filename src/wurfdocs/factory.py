#! /usr/bin/env python
# encoding: utf-8

import os
import sys
import hashlib
import shutil
import logging
import paramiko

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
import wurfdocs.sftp_config
import wurfdocs.sftp_transfer
import wurfdocs.sftp_command


class Factory(object):

    def __init__(self):

        self.default_build = None
        self.providers = {}

    def set_default_build(self, default_build):
        self.default_build = default_build

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
        return self.require(name=self.default_build)


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


def provide_output_path(factory):

    return factory.require(name='data_path')


def provide_clone_path(factory):

    data_path = factory.require(name='data_path')

    return os.path.join(data_path, 'clones')


def provide_virtualenv_root_path(factory):

    data_path = factory.require(name='data_path')

    return os.path.join(data_path, 'virtualenvs')


def require_cache(factory):

    data_path = factory.require(name='data_path')
    unique_name = factory.require(name='unique_name')

    return wurfdocs.cache.Cache(
        cache_path=data_path, unique_name=unique_name)


def require_task_generator(factory):

    git_repository = factory.require(name='git_repository')
    command = factory.require(name='command')
    command_config = factory.require(name='command_config')
    build_path = factory.require(name='build_path')
    git = factory.require(name='git')
    # cache = factory.require(name='cache')

    task_generator = wurfdocs.tasks.TaskFactory()

    if 'workingtree' in command_config.scope:

        workingtree_generator = wurfdocs.tasks.WorkingtreeGenerator(
            git_repository=git_repository,
            command=command, build_path=build_path)

        task_generator.add_generator(workingtree_generator)

    if 'source_branch' in command_config.scope:

        git_branch_generator = wurfdocs.tasks.GitBranchGenerator(
            git=git, git_repository=git_repository,
            command=command, build_path=build_path)

        task_generator.add_generator(git_branch_generator)

    if 'tag' in command_config.scope:

        git_tag_generator = wurfdocs.tasks.GitTagGenerator(
            git=git, git_repository=git_repository,
            command=command, build_path=build_path)

        task_generator.add_generator(git_tag_generator)

    return task_generator


def resolve_factory(data_path, source_branch):

    factory = Factory()
    factory.set_default_build(default_build='git_repository')

    factory.provide_value(name='git_binary', value='git')
    factory.provide_value(name='data_path', value=data_path)
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

    factory = Factory()
    factory.set_default_build(default_build='cache')
    factory.provide_value(name='data_path', value=data_path)
    factory.provide_value(name='unique_name', value=unique_name)
    factory.provide_function(name='cache', function=require_cache)

    return factory


def require_python_config(factory):

    config = factory.require(name='config')
    return wurfdocs.python_config.PythonConfig.from_dict(
        config=config)


def require_sftp_config(factory):

    config = factory.require(name='config')
    return wurfdocs.sftp_config.SFTPConfig.from_dict(
        config=config)


def require_python_environement(factory):

    prompt = factory.require(name='prompt')
    virtualenv = factory.require(name='virtualenv')
    log = logging.getLogger(name='wurfdocs.python_environement')

    return wurfdocs.python_environment.PythonEnvironment(
        prompt=prompt, virtualenv=virtualenv, log=log)


def require_python_command(factory):

    config = factory.require(name='command_config')
    environment = factory.require(name='python_environment')
    prompt = factory.require(name='prompt')
    log = logging.getLogger(name='wurfdocs.python_command')

    return wurfdocs.python_command.PythonCommand(
        config=config, environment=environment, prompt=prompt, log=log)


def provide_ssh(factory):
    return paramiko.SSHClient()


def build_python_factory(factory):

    factory.set_default_build(default_build='require_task_generator')

    factory.provide_function(
        name='command_config', function=require_python_config)

    factory.provide_function(
        name='prompt', function=require_prompt)

    factory.provide_function(
        name='python_environment', function=require_python_environement)

    factory.provide_function(
        name='command', function=require_python_command)

    factory.provide_function(name='output_path', function=provide_output_path)
    factory.provide_function(name='clone_path', function=provide_clone_path)

    factory.provide_function(name='virtualenv_root_path',
                             function=provide_virtualenv_root_path)

    factory.provide_value(name='git_binary', value='git')

    factory.provide_function(name='git_url_parser',
                             function=require_git_url_parser)
    factory.provide_function(name='git', function=require_git)

    factory.provide_function(name='virtualenv', function=require_virtualenv)

    factory.provide_function(
        name='require_task_generator', function=require_task_generator)

    return factory


def provide_sftp(factory):

    ssh = factory.require(name='ssh')
    return wurfdocs.sftp_transfer.SFTPTransfer(ssh=ssh)


def provide_sftp_command(factory):

    config = factory.require(name='command_config')
    sftp = factory.require(name='sftp')
    log = logging.getLogger(name='wurfdocs.SFTPCommand')

    return wurfdocs.sftp_command.SFTPCommand(config=config, sftp=sftp, log=log)


def build_sftp_factory(factory):

    factory.set_default_build(default_build='require_task_generator')

    factory.provide_function(
        name='command_config', function=require_sftp_config)

    factory.provide_function(
        name='command', function=provide_sftp_command)

    factory.provide_function(
        name='sftp', function=provide_sftp)

    factory.provide_function(
        name='ssh', function=provide_ssh)

    factory.provide_function(
        name='require_task_generator', function=require_task_generator)

    factory.provide_value(name='git_binary', value='git')
    factory.provide_function(name='git', function=require_git)
    factory.provide_function(name='prompt', function=require_prompt)

    return factory


def build_factory(build_type):

    factory = Factory()

    if build_type == 'python':
        return build_python_factory(factory=factory)

    if build_type == 'sftp':
        return build_sftp_factory(factory=factory)

    raise RuntimeError("%s not a known build type" % build_type)


class GiitJson(object):

    def __init__(self, paths, log):
        """ A new instance.

        :param paths: A list of paths to search for the giit.json file
        :param log: A logging object
        """

        self.paths = paths
        self.log = log

        # The loaded config dict
        self.config = None

    def load(self):

        giit_path = self._find_config()
        self.log.info('Using config: %s', giit_path)

        with open(giit_path, 'r') as giit_file:
            self.config = json.load(giit_file)

    def _find_config(self):

        for p in self.paths:

            giit_file = os.path.join(p, 'giit.json')

            if os.path.isfile(giit_file):
                return giit_file

        raise RuntimeError("Could not find giit.json in %s" % self.paths)

    def config(self, step):
        if step not in self.config:
            raise RuntimeError("Error step %s not found in giit.json" % step)

        return self.config[step]

    def config_hash(self, step):

        step_config = self.config(step=step)
        step_json = json.dumps(step_config, sort_keys=True)
        step_hash = hashlib.sha1(step_json.encode('utf-8')).hexdigest()[:6]

        return step
