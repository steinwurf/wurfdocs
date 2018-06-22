#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mock


import giit.push_command


def test_push_command_to_path(testdirectory):

    assert '/tmp/git' == giit.push_command.PushCommand._to_path(
        repository_path='/tmp', to_path='/git/')

    assert '/tmp/git' == giit.push_command.PushCommand._to_path(
        repository_path='/tmp', to_path='./git/')

    assert '/tmp/git' == giit.push_command.PushCommand._to_path(
        repository_path='/tmp', to_path='git')

    assert '/tmp/git' == giit.push_command.PushCommand._to_path(
        repository_path='/tmp', to_path='git/')

    assert '/tmp' == giit.push_command.PushCommand._to_path(
        repository_path='/tmp', to_path='.')

    assert '/tmp' == giit.push_command.PushCommand._to_path(
        repository_path='/tmp', to_path='/')


def test_push_command(testdirectory):

    prompt = mock.Mock()
    config = {}
    log = mock.Mock()

    build_dir = testdirectory.mkdir('build')
    build_dir.write_text(
        filename='hello.txt', data=u'world', encoding='utf-8')

    config['to_path'] = '/'
    config['from_path'] = '${build_path}'
    config['variables'] = ''
    config['exclude_patterns'] = []
    config['git_url'] = 'git@github.com:org/project.git'
    config['target_branch'] = 'gh-pages'
    config['commit_name'] = 'Giit Bot'
    config['commit_email'] = 'deploy@giit.bot'

    command = giit.push_command.PushCommand(
        prompt=prompt, config=config, log=log)

    context = {
        'scope': 'tag',
        'name': '1.0.0',
        'build_path': build_dir.path()
    }

    command.run(context=context)

    calls = [
        mock.call.run(command=["git", "init"], cwd='/tmp/giit_push'),
        mock.call.run(command=["git", "add", "."], cwd='/tmp/giit_push'),
        mock.call.run(
            command=["git", "-c", "user.name='Giit Bot'",
                     "-c", "user.email='deploy@giit.bot'",
                     "commit", "-m", "'giit push'"],
            cwd='/tmp/giit_push'),
        mock.call.run(
            command=['git', 'push', '--force',
                     "git@github.com:org/project.git",
                     'master:gh-pages'],
            cwd='/tmp/giit_push')
    ]

    prompt.assert_has_calls(calls)
