def test_build(testdirectory):

    build_dir = testdirectory.mkdir('build')
    wurfdocs_dir = testdirectory.mkdir('wurfdocs')
    config_file = testdirectory.copy_file('test/data/wurfdocs.json')

    url = 'git@github.com:steinwurf/stub.git'

    cmd = ['wurfdocs', 'sphinx', url,
           '--build_path', build_dir.path(),
           '--wurfdocs_path', wurfdocs_dir.path(),
           '--json_config', config_file,
           '--source_branch', 'origin/add-docs']

    testdirectory.run(cmd)

    cmd = ['wurfdocs', 'landing_page', url,
           '--build_path', build_dir.path(),
           '--wurfdocs_path', wurfdocs_dir.path(),
           '--json_config', config_file,
           '--source_branch', 'origin/add-docs']

    testdirectory.run(cmd)

    cmd = ['wurfdocs', 'publish', url,
           '--build_path', build_dir.path(),
           '--wurfdocs_path', wurfdocs_dir.path(),
           '--json_config', config_file]

    testdirectory.run(cmd)
