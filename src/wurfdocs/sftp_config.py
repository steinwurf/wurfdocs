import os


class SFTPConfig(object):

    def __init__(self, config):
        self.config = config

    def __getattr__(self, attribute):

        if not attribute in self.config:
            raise AttributeError("Not found")

        return self.config[attribute]

    def __getitem__(self, key):

        if not key in self.config:
            raise AttributeError("Not found")

        return self.config[key]

    def __contains__(self, attribute):
        """ Checks if the attribute is available.
        :return: True if the attribute is available otherwise False
        """
        return attribute in self.config

    @staticmethod
    def from_dict(config):

        # Mandatory
        assert config['type'] == 'sftp'
        assert 'username' in config and config['username']
        assert 'hostname' in config and config['hostname']
        assert 'remote_path' in config and config['remote_path']
        assert 'source_path' in config and config['source_path']

        # Optional
        if not 'exclude_patterns' in config:
            config['exclude_patterns'] = []

        if not 'scope' in config:
            config['scope'] = ['source_branch']

        if not 'variables' in config:
            config['variables'] = ''

        return SFTPConfig(config=config)
