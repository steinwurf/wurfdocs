#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import fnmatch
import paramiko

import wurfdocs.filelist
import wurfdocs.sftp_transfer


def test_filetransfer(testdirectory):

    a_dir = testdirectory.mkdir('a')

    a_dir.write_text(filename='helloworld.txt',
                     data=u'hello', encoding='utf-8')
    b_dir = a_dir.mkdir('b')

    b_dir.write_text(filename='helloworld.txt',
                     data=u'hello', encoding='utf-8')

    ssh = paramiko.SSHClient()

    filetransfer = wurfdocs.sftp_transfer.SFTPTransfer(ssh=ssh)
    filetransfer.connect(hostname='buildbot.steinwurf.dk', username='buildbot')

    filetransfer.transfer(local_path=testdirectory.path(),
                          remote_path='/tmp',
                          exclude_patterns=[])


def test_filetransfer_path_split():

    path, filename = wurfdocs.sftp_transfer.SFTPTransfer._path_split(
        remote_file='/www/var/file.txt')

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

    filelist = wurfdocs.filelist.FileList(
        source_path=testdirectory.path(),
        remote_path='/var/www',
        exclude_patterns=excludes)

    result = list(filelist)

    source_result = [f.local_file for f in result]
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
