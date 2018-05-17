def test_build(testdirectory):

    data_dir = testdirectory.mkdir('data')
    output_dir = testdirectory.mkdir('output')

    url = 'git@github.com:steinwurf/stub.git'

    cmd = ['wurfdocs', '--repository', url,
           '--data_path', data_dir.path(),
           '--output_path', output_dir.path()]

    r = testdirectory.run(cmd)

    print(r)

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
