from abc import ABCMeta


class ShellCommandContainer(metaclass=ABCMeta):

    def __init__(self, command):
        assert isinstance(command, list)
        self._raw_command = command


    def full_command(self):
        full_command = ''
        for string in self._raw_command:
            full_command += string + ' '

        return full_command
