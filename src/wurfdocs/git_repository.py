import os
import hashlib


class GitRepository(object):

    def __init__(self, git, git_url_parser, clone_path, source_branch, log):
        self.git = git
        self.git_url_parser = git_url_parser
        self.log = log
        self.clone_path = clone_path

        self.git_info = None

        self.git_url = None

        # Path to the local working tree (if one exists)
        self.workingtree_path = None

        # Path to where this repository is cloned
        self.repository_path = None

        # A unique name computed based on the git URL
        self.unique_name = None

        # The branch which should be the source branch
        self.source_branch = source_branch

    def clone(self, repository):

        assert repository

        self.clone_path = os.path.abspath(
            os.path.expanduser(self.clone_path))

        if not os.path.isdir(self.clone_path):
            os.makedirs(self.clone_path)

        # Get the URL to the repository
        if os.path.isdir(repository):
            self.workingtree_path = repository
            git_url = self.git.remote_origin_url(cwd=repository)

            if not self.source_branch:
                # If we don't have a source branch we use the one which is
                # currently checked out in the working tree
                self.source_branch, _ = self.git.branch(cwd=repository)
        else:
            git_url = repository

            if not self.source_branch:
                # If we don't have a source branch we use 'master
                self.source_branch = 'master'

        # Compute the clone path
        git_info = self.git_url_parser.parse(url=git_url)

        url_hash = hashlib.sha1(git_url.encode('utf-8')).hexdigest()[:6]
        self.unique_name = git_info.name + '-' + url_hash

        self.repository_path = os.path.join(self.clone_path, self.unique_name)

        # Get the updates
        if os.path.isdir(self.repository_path):
            self.git.fetch(cwd=self.repository_path, all=True)
        else:
            self.git.clone(repository=git_url,
                           directory=self.repository_path, cwd=self.clone_path)

    def tags(self):
        return self.git.tags(cwd=self.repository_path)

    def branches(self):
        _, remote = self.git.branch(cwd=self.repository_path, remote=True)

        # Remote branches look like origin/master, origin/some_branch etc.
        # We flatten this.

        return remote
