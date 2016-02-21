class LinkCommandComponentContainer:

    def __init__(self, ln_command):
        assert isinstance(ln_command, list)
        self._raw_command_list = ln_command

        self.symbolic = \
            ln_command.__contains__('-s') or \
            ln_command.__contains__('--symbolic')

        if not self.symbolic:
            raise Exception('This implementation only supports symlinks.')

        self.source = ln_command[-1]
        self.target = ln_command[-2]

        pass


    def full_command(self):
        full_command = ''
        for string in self._raw_command_list:
            full_command += string + ' '

        return full_command