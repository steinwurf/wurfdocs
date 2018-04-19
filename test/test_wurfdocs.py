import os


def test_run(testdirectory):

    testdirectory.run('python -m wurfdocs')
    testdirectory.run('wurfdocs')


def test_build_docs(testdirectory):

    cpp_coffee = testdirectory.copy_dir(directory='test/data/cpp_coffee')

    docs = cpp_coffee.join('docs')
    docs.run('sphinx-build -w log.txt -b html . _build')

    log_file = os.path.join(docs.path(), 'log.txt')

    # The log file should have zero size - i.e. now warnings or errors..
    # As you can see we are not quite there :)
    assert os.path.getsize(log_file) == 620
