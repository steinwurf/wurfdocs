def test_build(testdirectory):

    build_dir = testdirectory.mkdir('build')
    wurfdocs_dir = testdirectory.mkdir('wurfdocs')
    config_file = testdirectory.copy_file('test/data/wurfdocs.json')

    url = 'git@github.com:steinwurf/stub.git'

    cmd = ['wurfdocs', 'sphinx', url,
           '--json_config', config_file,
           '--source_branch', 'origin/add-docs']

    testdirectory.run(cmd)

    cmd = ['wurfdocs', 'landing_page', url,
           '--json_config', config_file,
           '--source_branch', 'origin/add-docs']

    testdirectory.run(cmd)

    cmd = ['wurfdocs', 'publish', url,
           '--json_config', config_file]

    testdirectory.run(cmd)
