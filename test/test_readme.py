def test_godot(testdirectory):

    config_file = testdirectory.copy_file('test/data/flask_giit.json')

    url = 'https://github.com/pallets/flask'

    cmd = ['wurfdocs', 'docs', url,
           '--json_config', config_file]

    # testdirectory.run(cmd)
