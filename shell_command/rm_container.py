from shell_command.shell_command_container import ShellCommandContainer


class RmCommand(ShellCommandContainer):

    def __init__(self, rm_command):
        super().__init__(rm_command)

        self.target = rm_command[-1]