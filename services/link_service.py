import os

from command_containers.ln_component_container import LinkCommandComponentContainer
from persistence.persistence_adapter import PersistenceAdapter


class LinkService:

    def __init__(self, ln_command, persistence_adapter):
        assert isinstance(ln_command, list)
        assert isinstance(persistence_adapter, PersistenceAdapter)

        self.ln_container = LinkCommandComponentContainer(ln_command)
        self.persistence_adapter = persistence_adapter


    def create_link(self):

        if (self.persistence_adapter.register_link(self.ln_container)):
            print('Creating the link!')
            os.system(self.ln_container.full_command()) # TODO Use subprocess?
            print('Link created!')
        else:
            print('Could not register symlink in the database.')

        pass