from services.command_service import CommandService
from shell_command.rm_container import RmCommand


class RmService(CommandService):
    """
    Responsible for removing files and symbolic links and registering the changes
    with the given persistence adapter.
    """

    def __init__(self, rm_command, persistence_adapter):
        super(RmService).__init__(persistence_adapter)
        self.rm_container = RmCommand(rm_command)
