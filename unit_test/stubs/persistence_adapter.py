from persistence.persistence_adapter import PersistenceAdapter


class StubbedPersistenceAdapter(PersistenceAdapter):

    def register_link(self, ln_container):
        return True

    def unregister_link(self, link_path):
        return True