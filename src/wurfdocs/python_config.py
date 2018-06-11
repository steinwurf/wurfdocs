import os


class PythonConfig(object):

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
        assert config['type'] == 'python'
        assert len(config['scripts']) > 0

        # Optional
        if not 'variables' in config:
            config['variables'] = ''

        if not 'requirements' in config:
            config['requirements'] = None

        if not 'cwd' in config:
            config['cwd'] = os.getcwd()

        if not 'allow_failure' in config:
            config['allow_failure'] = False

        if not 'recurse_tags' in config:
            config['recurse_tags'] = False

        return PythonConfig(config=config)
