#! /usr/bin/env python
# encoding: utf-8

import os
import sys
import hashlib

import wurfdocs.config_reader


class SFTPCommand(object):

    def __init__(self, config, sftp, log):
        """
        :param config: A SFTPConfig object
        :param sftp: A SFTPTransfer object
        :param log: The log to use
        """
        self.config = config
        self.sftp = sftp
        self.log = log

    def run(self, context):
        """ Run the SFTP command based on the context

        :param context: A dict containing the context of the command
        """

        self.log.debug("RUN context=%s", context)

        reader = wurfdocs.config_reader.ConfigReader(
            config=self.config, context=context)

        hostname = reader.hostname
        username = reader.username

        self.sftp.connect(hostname=hostname, username=username)

        source_path = reader.source_path
        remote_path = reader.remote_path
        exclude_patterns = reader.exclude_patterns

        self.sftp.transfer(source_path=source_path, remote_path=remote_path,
                           exclude_patterns=exclude_patterns)
