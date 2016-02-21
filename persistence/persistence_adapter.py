import shelve

from abc import ABCMeta

class PersistenceAdapter(metaclass=ABCMeta):

    def register_link(self, ln_container):
        raise NotImplemented

