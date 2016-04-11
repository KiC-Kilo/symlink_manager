from services.command_service import CommandService
from shell_command.mv_container import MvCommand


class MvService(CommandService):
    """
    Responsible for handling mv commands for symlinks and their target files.
    """

    def __init__(self, mv_command, persistence_adapter):
        super().__init__(persistence_adapter)
        self.mv_command = MvCommand(mv_command)

    def execute_mv(self):


        pass
