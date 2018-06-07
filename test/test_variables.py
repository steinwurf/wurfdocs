import mock
import os
import sys
import string


class Variables(object):

    def __init__(self, variables, context):
        self.variables = variables
        self.context = context

    def _find_item(self, key):

        scope = self.context['scope']
        name = self.context['name']

        explicit = ':'.join([self.scope, self.name, key])

        if explicit in self.variables:
            return self.variables[explicit]

        partial = ':'.join([self.scope, key])

        if partial in self.variables:
            return self.variables[partial]

        raise AttributeError("Not found {}".format(key))

    def __getitem__(self, key):

        variable = self._find_item(key=key)
        return string.Template(variable).safe_substitute(self)

    def expand(self, element):

        return string.Template(element).safe_substitute(self)


class SystemEnvironment(object):
    pass


def test_variables():

    scope = 'tag'
    selector = '1.0.0'
    variables = {
        'source_branch:master:out': 'yoyo',
        'source_branch:out': 'yiyi',
        'tag:out': 'yuyu ${boing} ${build_path}',
        'tag:1.0.0:boing': 'hip ${boo}',
        'tag:boing': 'hop ${boo}',
        'tag:boo': 'hap'
    }
    build_path = '/tmp/build'
    clone_path = '/tmp/clone'

    # d = Variables(scope=scope, selector=selector, variables=variables,
    #               build_path=build_path, clone_path=clone_path)

    # r = d.expand(element='$out likes')

    # assert r == 'yuyu hip hap /tmp/build likes'


class PythonConfig(object):

    def __init__(self, config):
        self.config = config

    @staticmethod
    def from_dict(self, config):

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

    def __getattr__(self, attribute):

        if not attribute in self.config:
            raise AttributeError("Not found")

        return self.config[attribute]


class ConfigContext(object):

    def __init__(self, config, context):
        self.config = config
        self.variables = Variables(
            variables=config.variables, context=context)

    def __getattr__(self, attribute):

        if not attribute in self.config:
            raise AttributeError("Not found")

        element = self.config[attribute]

        return self._expand(element=element)

    def _expand(self, element):

        if type(element) == str:
            return self.variables.expand(element=element)

        if type(element) == list:

            values = []
            for e in element:
                values.append(self.__expand(element=e))

            return values

        return element
