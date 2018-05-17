import wurfdocs
import wurfdocs.git


def test_git(testdirectory):
    git = wurfdocs.git.build()

    print(git.version(cwd=testdirectory.path()))
