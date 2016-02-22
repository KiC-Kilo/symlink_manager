from abc import ABCMeta

class PersistenceAdapter(metaclass=ABCMeta):

    def register_link(self, ln_container):
        raise NotImplemented

    def unregister_link(self, link_path):
        raise NotImplemented
