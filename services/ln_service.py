import logging
import subprocess

from persistence.persistence_adapter import PersistenceAdapter
from services.command_service import CommandService
from shell_command.ln_container import LnCommand


class LnService(CommandService):
    """
    Responsible for creating symbolic links and registering them with the given
    persistence adapter.
    """
    def __init__(self, ln_command: list, persistence_adapter: PersistenceAdapter):
        super().__init__(persistence_adapter)
        self.ln_container = LnCommand(ln_command)


    def create_link(self):
        ln_command = self.ln_container
        if self.persistence_adapter.register_link(ln_command):
            logging.info('Creating link at ' + ln_command.link_name + ' to file '
                  + ln_command.target_name)

            ln_status = subprocess.run(self.ln_container.raw_command).returncode

            if ln_status != 0:
                logging.error('Link creation failed.')
                self.persistence_adapter.unregister_link(
                    self.ln_container.target_name,
                    self.ln_container.link_name)
            else:
                logging.info('Link created!')
        else:
            logging.error('Persistence adapter could not register symlink.')

