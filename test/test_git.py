import wurfdocs.git
import wurfdocs.prompt


def test_git(testdirectory):
    git = wurfdocs.git.Git(
        git_binary='git', prompt=wurfdocs.prompt.Prompt())

    print(git.version(cwd=testdirectory.path()))
