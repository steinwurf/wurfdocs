import mock
import os
import sys
import string


class Variables(object):

    def __init__(self, scope, selector, variables, build_path, clone_path):
        self.scope = scope
        self.selector = selector
        self.variables = variables
        self.build_path = build_path
        self.clone_path = clone_path

    def expand(self, element):
        return string.Template(element).safe_substitute(self)

    def __getitem__(self, key):

        variable = self._find_item(key=key)
        return string.Template(variable).safe_substitute(self)

    def _find_item(self, key):
        if key == 'build_path':
            return self.build_path

        if key == 'clone_path':
            return self.clone_path

        explicit = ':'.join([self.scope, self.selector, key])

        if explicit in self.variables:
            return self.variables[explicit]

        partial = ':'.join([self.scope, key])

        if partial in self.variables:
            return self.variables[partial]

        raise AttributeError("Not found {}".format(key))


class PythonRequirements(object):
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

    d = Variables(scope=scope, selector=selector, variables=variables,
                  build_path=build_path, clone_path=clone_path)

    r = d.expand('$out likes')

    assert r == 'yuyu hip hap /tmp/build likes'
