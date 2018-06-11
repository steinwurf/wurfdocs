import mock
import wurfdocs.config_reader


def test_config_reader():

    config_dict = {
        'type': 'python',
        'scripts': [
            'python test.py ${out}'
        ],
        'allow_failure': True,
        'cwd': '${source_path}',
        'variables': {
            'source_branch:master:out': 'yoyo',
            'source_branch:out': 'yiyi',
            'tag:out': 'yuyu ${boing} ${build_path}',
            'tag:1.0.0:boing': 'hip ${boo}',
            'tag:boing': 'hop ${boo}',
            'tag:boo': 'hap'
        }
    }

    config = wurfdocs.python_config.PythonConfig.from_dict(
        config=config_dict)

    context = {
        'scope': 'tag',
        'name': '1.0.0',
        'build_path': '/tmp/build',
        'source_path': '/tmp/clone'
    }

    reader = wurfdocs.config_reader.ConfigReader(
        config=config, context=context)

    assert len(reader.scripts) == 1
    assert reader.scripts[0] == 'python test.py yuyu hip hap /tmp/build'
    assert reader.cwd == '/tmp/clone'
    assert reader.allow_failure == True