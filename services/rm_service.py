from services.command_service import CommandService
from shell_command.rm_container import RmCommand


class RmService(CommandService):
    """
    Responsible for removing files and symbolic links and registering the changes
    with the given persistence adapter.
    """

    def __init__(self, rm_command, persistence_adapter):
        super().__init__(persistence_adapter)
        self.rm_container = RmCommand(rm_command)

    def remove_target_file(self):
        try:
            rm_command = self.rm_container

            print('Attempting to unregister all links for file...')
            if self.persistence_adapter.unregister_target(rm_command.target):
                print('File unregistered.')

            return True

        except Exception as e:
            return False


    def remove_link(self):
        try:
            rm_command = self.rm_container

            print('Attempting to unregister link...')
            if self.persistence_adapter.unregister_target(rm_command.target):
                print('Link unregistered.')

            return True

        except Exception as e:
            return False