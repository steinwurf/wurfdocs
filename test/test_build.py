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

    r = testdirectory.run(cmd)

    cmd = ['wurfdocs', 'landing_page', url,
           '--build_path', build_dir.path(),
           '--wurfdocs_path', wurfdocs_dir.path(),
           '--json_config', config_file,
           '--source_branch', 'origin/add-docs']

    r = testdirectory.run(cmd)

    # print(r)

    # pass


# def test_help(testdirectory):

#     data_dir = testdirectory.mkdir('data')
#     output_dir = testdirectory.mkdir('output')

#     url = 'git@github.com:steinwurf/stub.git'

#     cmd = ['wurfdocs', '--repository', url,
#            '--data_path', data_dir.path(),
#            '--output_path', output_dir.path(), 'push', '--help']

#     r = testdirectory.run(cmd)
#     print(r)
#     assert 0

#     # pass
