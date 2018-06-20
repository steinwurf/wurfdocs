def test_godot(testdirectory):

    config_file = testdirectory.copy_file('test/data/godot_giit.json')

    url = 'https://github.com/godotengine/godot-docs.git'

    cmd = ['wurfdocs', 'docs', url,
           '--json_config', config_file]

    # testdirectory.run(cmd)
