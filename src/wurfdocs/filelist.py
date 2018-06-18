import os
import fnmatch

import wurfdocs.fileinfo


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

                    yield wurfdocs.fileinfo.FileInfo(
                        source_file=source_file,
                        remote_file=remote_file)

    def _exclude(self, filename):

        for e in self.exclude_patterns:

            if fnmatch.fnmatch(filename, e):
                return True

        return False
