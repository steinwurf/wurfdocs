import wurfdocs
import wurfdocs.commandline as cli


def test_run(testdirectory):

    prompt = cli.Prompt()
    prompt.run('python --version', cwd=testdirectory.path())
