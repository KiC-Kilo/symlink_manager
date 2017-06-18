from abc import ABCMeta

from symmv.persistence.persistence_adapter import PersistenceAdapter


class CommandService(metaclass=ABCMeta):

    def __init__(self, persistence_adapter: PersistenceAdapter):
        self.persistence_adapter = persistence_adapter

