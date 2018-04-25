from . import wurfdocs_error


class RunError(wurfdocs_error.WurfdocsError):
    """Basic exception for errors raised when running commands."""

    def __init__(self, run_result):
        super(RunError, self).__init__(str(run_result))
        self.run_result = run_result
