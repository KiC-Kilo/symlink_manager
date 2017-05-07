from shell_command.shell_command_container import ShellCommand


class LnCommand(ShellCommand):

    def __init__(self, ln_command: list):
        super().__init__(ln_command)

        if not (ln_command.__contains__('-s') or
                ln_command.__contains__('--symbolic')):
            raise Exception('This application only supports symlinks.')

        self.link_name      = self._canonicalize_path(ln_command[-1])
        self.target_name    = self._canonicalize_path(ln_command[-2])

        pass

