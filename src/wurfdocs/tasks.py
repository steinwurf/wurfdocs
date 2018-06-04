import json
import os
import shutil
import hashlib
import sys


class WorkingtreeTask(object):

    def __init__(self, command):
        self.command =

    def run(self):

        build_info.output_path = os.path.join(self.output_path, 'workingtree')
        build_info.repository_path = self.workingtree_path
        build_info.slug = 'workingtree'
        build_info.type = 'workingtree'

        self.sphinx.build(build_info=build_info)


class WorkingtreeGenerator(object):

    def __init__(self, repository, command):
        self.repository = repository
        self.command = command

    def tasks(self):

        if self.repository.workingtree_path:

            command.set_scope(scope='workingtree')
            command.set.selector(selector='')
            command.set_variable(variable='source_path',
                                 value=self.repository.workingtree_path)

            return [command]

        else:

            return []


class GitTask(object):

    def __init__(self, checkout_type, checkout, repository_path, output_path,
                 sphinx, git, cache):

        self.checkout_type = checkout_type
        self.checkout = checkout
        self.repository_path = repository_path
        self.output_path = output_path
        self.sphinx = sphinx
        self.git = git
        self.cache = cache

    def run(self, build_info):

        cwd = self.repository_path

        # https://stackoverflow.com/a/8888015/1717320
        self.git.reset(branch=self.checkout, hard=True, cwd=cwd)

        output_path = os.path.join(
            self.output_path, self.checkout_type, self.checkout)

        sha1 = self.git.current_commit(cwd=cwd)

        build_info.output_path = output_path
        build_info.repository_path = self.repository_path
        build_info.slug = self.checkout
        build_info.type = self.checkout_type

        if self.cache.match(sha1=sha1):
            path = self.cache.path(sha1=sha1)

            if path != output_path:
                shutil.copytree(src=path, dst=output_path)

        else:

            self.sphinx.build(build_info=build_info)

            self.cache.update(sha1=sha1, path=output_path)

        return build_info


class GitBranchGenerator(object):

    def __init__(self, repository, command):

        self.repository = repository
        self.command = command

    def tasks(self):

        branch_name = self.repository.current_branch()

        command.set_scope(scope='source_branch')
        command.set.selector(selector=branch_name)
        command.set_variable(
            variable='source_path', value=self.repository.repository_path)
        command.set_variable(
            variable='branch_name', value=branch_name)

        return tasks


class GitTagGenerator(object):

    def __init__(self, repository, output_path,
                 sphinx, git, cache):

        self.repository = repository
        self.output_path = output_path
        self.sphinx = sphinx
        self.git = git
        self.cache = cache

    def tasks(self):

        tasks = []

        for tag in self.repository.tags():

            task = GitTask(checkout_type='tag', checkout=tag,
                           repository_path=self.repository.repository_path,
                           output_path=self.output_path, sphinx=self.sphinx,
                           git=self.git, cache=self.cache)

            tasks.append(task)

        return tasks


class TaskFactory(object):

    def __init__(self):
        self.generators = []

    def add_generator(self, generator):
        self.generators.append(generator)

    def tasks(self):

        tasks = []

        for generator in self.generators:

            generator_tasks = generator.tasks()

            tasks += generator_tasks

        return tasks
