#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import fnmatch
import paramiko


class FileInfo(object):

    def __init__(self, source_file, remote_file):
        self.source_file = source_file
        self.remote_file = remote_file


class FileList(object):

    def __init__(self, source_path, remote_path, exclude_patterns=[]):
        self.source_path = source_path
        self.remote_path = remote_path
        self.exclude_patterns = exclude_patterns

    def __iter__(self):
        for root, dirs, files in os.walk(self.source_path, topdown=True):

            for f in files:
                source_file = os.path.join(root, f)

                if not self._exclude(filename=source_file):

                    relative_path = os.path.relpath(
                        source_file, self.source_path)

                    remote_file = os.path.join(self.remote_path, relative_path)

                    yield FileInfo(source_file=source_file,
                                   remote_file=remote_file)

    def _exclude(self, filename):

        for e in self.exclude_patterns:

            if fnmatch.fnmatch(filename, e):
                return True

        return False


class FileTransfer(object):

    def __init__(self, ssh):
        self.ssh = ssh

    def connect(self, username, hostname):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_.connect(hostname=hostname,
                          username=username)

    def transfer(self, filelist):

        sftp_client = self.ssh_client.open_sftp()

        for fileinfo in filelist:
            self.transfer_file(source_file=fileinfo.source_file,
                               remote_file=fileinfo.remote_file)

    def transfer_file(self, source_file, remote_file):
        remote_path, remote_file = self._path_split(remote_file=remote_file)

        for path in remote_path:

            try:
                # http://docs.paramiko.org/en/2.4/api/sftp.html
                self.sftp.chdir(path=path)
            except IOError:
                self.sftp.mkdir(path=path)
                self.sftp.chdir(path=path)

        self.sftp.put(localpath=source_file, remotepath=remote_file)

    @staticmethod
    def _path_split(remote_file):

        assert remote_file.startswith('/'), "must be absolute %s" % remote_file

        path = remote_file
        path_split = []

        while True:
            path, leaf = os.path.split(path)
            if leaf:
                # Adds one element, at the beginning of the list
                path_split = [leaf] + path_split
            else:
                path_split = [path] + path_split
                break

        return path_split[:-1], path_split[-1]


class SFTP(object):

    def __init__(self, ssh_client):
        self.ssh_client = ssh_client

    def connect(self, username, hostname):
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname=hostname,
                                username=username)

    def transfer(self, source_path, remote_path, exclude_patterns):

        sftp_client = self.ssh_client.open_sftp()

        filelist = FileList(source_path=source_path,
                            remote_path=remote_path,
                            exclude_patterns=exclude_patterns)

        filetransfer = FileTransfer(filelist=filelist, sftp=sftp_client)
        filetransfer.transfer()

        sftp_client.close()


def test_filetransfer(testdirectory):

    a_dir = testdirectory.mkdir('a')

    a_dir.write_text(filename='helloworld.txt',
                     data=u'hello', encoding='utf-8')
    b_dir = a_dir.mkdir('b')

    b_dir.write_text(filename='helloworld.txt',
                     data=u'hello', encoding='utf-8')

    ssh_client = paramiko.SSHClient()

    sftp = SFTP(ssh_client=ssh_client)

    sftp.connect(hostname='buildbot.steinwurf.dk', username='buildbot')

    sftp.transfer(source_path=testdirectory.path(),
                  remote_path='/tmp',
                  exclude_patterns=[])


def test_filetransfer_path_split():

    path, filename = FileTransfer._path_split(remote_file='/www/var/file.txt')

    assert path == ['/', 'www', 'var']
    assert filename == 'file.txt'


def test_filelist(testdirectory):
    a_dir = testdirectory.mkdir('a')
    b_dir = testdirectory.mkdir('b')
    c_dir = testdirectory.mkdir('c')
    d_dir = testdirectory.mkdir('d')

    a_dir.write_text(filename='a.txt', data=u'a', encoding='utf-8')
    b_dir.write_text(filename='b.txt', data=u'b', encoding='utf-8')
    c_dir.write_text(filename='c.txt', data=u'c', encoding='utf-8')
    d_dir.write_text(filename='d.txt', data=u'd', encoding='utf-8')

    a_a_dir = a_dir.mkdir('a')
    a_b_dir = a_dir.mkdir('b')
    b_c_dir = b_dir.mkdir('c')
    c_d_dir = c_dir.mkdir('d')

    a_a_dir.write_text(filename='a_a.txt', data=u'a', encoding='utf-8')
    a_b_dir.write_text(filename='a_b.txt', data=u'b', encoding='utf-8')
    b_c_dir.write_text(filename='b_c.txt', data=u'c', encoding='utf-8')
    c_d_dir.write_text(filename='c_d.txt', data=u'd', encoding='utf-8')

    #     .
    # ├── a
    # │   ├── a
    # │   │   └── a_a.txt
    # │   ├── a.txt
    # │   └── b
    # │       └── a_b.txt
    # ├── b
    # │   ├── b.txt
    # │   └── c
    # │       └── b_c.txt
    # ├── c
    # │   ├── c.txt
    # │   └── d
    # │       └── c_d.txt
    # └── d
    #     └── d.txt

    # 8 directories, 8 files

    excludes = [
        os.path.join(testdirectory.path(), 'c/d/*'),
        os.path.join(testdirectory.path(), 'a/*')
    ]

    filelist = FileList(source_path=testdirectory.path(),
                        remote_path='/var/www',
                        exclude_patterns=excludes)

    result = list(filelist)

    source_result = [f.source_file for f in result]
    remote_result = [f.remote_file for f in result]

    # There should be 4 files
    assert len(source_result) == 4
    assert len(remote_result) == 4

    file1 = os.path.join(testdirectory.path(), 'b/b.txt')
    file2 = os.path.join(testdirectory.path(), 'b/c/b_c.txt')
    file3 = os.path.join(testdirectory.path(), 'c/c.txt')
    file4 = os.path.join(testdirectory.path(), 'd/d.txt')

    assert file1 in source_result
    assert file2 in source_result
    assert file3 in source_result
    assert file4 in source_result

    file1 = '/var/www/b/b.txt'
    file2 = '/var/www/b/c/b_c.txt'
    file3 = '/var/www/c/c.txt'
    file4 = '/var/www/d/d.txt'

    assert file1 in remote_result
    assert file2 in remote_result
    assert file3 in remote_result
    assert file4 in remote_result
