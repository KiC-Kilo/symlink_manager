from abc import ABCMeta

from persistence.persistence_adapter import PersistenceAdapter


class CommandService(metaclass=ABCMeta):

    def __init__(self, persistence_adapter):
        assert issubclass(persistence_adapter.__class__, PersistenceAdapter)

        self.persistence_adapter = persistence_adapter

