#! /usr/bin/env python
# encoding: utf-8

import os
import sys
import hashlib

import giit.config_reader


class GhPagesCommand(object):

    def __init__(self, config, log):
        """
        :param config: A PushConfig object
        :param log: The log to use
        """
        self.config = config
        self.log = log

    def run(self, context):
        """ Run the git push command based on the context

        :param context: A dict containing the context of the command
        """

        self.log.debug("context=%s", context)

        self.git.fetch(all=True, cwd=cwd)

        _, others = self.git.branch(cwd=cwd, remote=True)

        if current == 'gh_pages' or 'gh_pages' in

        reader = giit.config_reader.ConfigReader(
            config=self.config, context=context)

    def _ensure_gh_pages(self):

        # Do we already have a checkout
        branches = self.git.local_branches(cwd=cwd)

        if 'gh-pages' in branches:
            return

        # Is the branch already on the remote
        branches = self.git.remote_branches(cwd=cwd)

        if 'origin/gh-pages' in branches:
            return

        # We need to create it

        _, others = self.git.branch(cwd=cwd, remote=True)

        if 'origin/gh-pages' in others:
            self.git.checkout(branch=)

    def _init_gh_pages(self):
        self.log.info('Creating gh_pages branch')

        self.git.checkout()
