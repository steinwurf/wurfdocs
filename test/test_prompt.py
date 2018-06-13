
import wurfdocs.prompt


def test_run(testdirectory):

    prompt = wurfdocs.prompt.Prompt()
    prompt.run('python --version', cwd=testdirectory.path())
