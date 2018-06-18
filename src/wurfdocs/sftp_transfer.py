import os
import paramiko

import wurfdocs.filelist


class SFTPTransfer(object):

    def __init__(self, ssh):
        self.ssh = ssh

    def connect(self, username, hostname):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=hostname,
                         username=username)

    def transfer(self, source_path, remote_path, exclude_patterns):

        filelist = wurfdocs.filelist.FileList(
            source_path=source_path,
            remote_path=remote_path,
            exclude_patterns=exclude_patterns)

        self.transfer_filelist(filelist=filelist)

    def transfer_filelist(self, filelist):

        with self.ssh.open_sftp() as sftp:

            for fileinfo in filelist:
                self.transfer_file(sftp=sftp,
                                   source_file=fileinfo.source_file,
                                   remote_file=fileinfo.remote_file)

    def transfer_file(self, sftp, source_file, remote_file):
        remote_path, remote_file = self._path_split(remote_file=remote_file)

        for path in remote_path:

            try:
                # http://docs.paramiko.org/en/2.4/api/sftp.html
                sftp.chdir(path=path)
            except IOError:
                sftp.mkdir(path=path)
                sftp.chdir(path=path)

        sftp.put(localpath=source_file, remotepath=remote_file)

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
