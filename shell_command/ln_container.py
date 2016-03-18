from shell_command.shell_command_container import ShellCommandContainer


class LnCommand(ShellCommandContainer):

    def __init__(self, ln_command):
        super().__init__(ln_command)

        if not (ln_command.__contains__('-s') or
                ln_command.__contains__('--symbolic')):
            raise Exception('This implementation only supports symlinks.')

        self.link_name      = ln_command[-1]
        self.target_name    = ln_command[-2]

        pass

