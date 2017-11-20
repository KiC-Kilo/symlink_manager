from symmv.shell_command.shell_command_container import ShellCommand


class MvCommand(ShellCommand):

    def __init__(self, mv_command: list):
        super().__init__(mv_command)
        self.source         = self._canonicalize_path(mv_command[-2])
        self.destination    = self._canonicalize_path(mv_command[-1])
    
    def raw_command(self):
        """
        The `mv` shell command seems to not like being given an array of command
        parameters, and requires a single string command to run as a subprocess in Python.
        """
        return ' '.join(self._raw_command)
