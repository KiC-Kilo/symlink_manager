from shell_command.shell_command_container import ShellCommand


class RmCommand(ShellCommand):

    def __init__(self, rm_command):
        super().__init__(rm_command)

        self.target = self._canonicalize_path(rm_command[-1])

