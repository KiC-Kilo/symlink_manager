import subprocess

from services.command_service import CommandService
from shell_command.ln_container import LnCommand


class LnService(CommandService):
    """
    Responsible for creating symbolic links and registering them with the given
    persistence adapter.
    """
    def __init__(self, ln_command, persistence_adapter):
        super().__init__(persistence_adapter)
        self.ln_container = LnCommand(ln_command)


    def create_link(self):
        ln_command = self.ln_container
        if (self.persistence_adapter.register_link(ln_command)):
            print('Creating link at ' + ln_command.link_name + ' to file '
                  + ln_command.target_name)

            ln_status = subprocess.call(self.ln_container._raw_command)

            if ln_status != 0:
                print('Link creation failed.')
                self.persistence_adapter.unregister_link(self.ln_container)
            else:
                print('Link created!')
        else:
            print('Could not register symlink in the database.')

