from symmv.persistence.persistence_adapter import PersistenceAdapter


class AlwaysSuccessfulPersistenceAdapter(PersistenceAdapter):

    def contains_target_file(self, target_file_path):
        return True

    def commit(self):
        return True

    def reregister_target_file(self, old_filepath, new_filepath):
        return True

    def target_file_for_link(self, symlink_path):
        return True

    def contains_symlink(self, symlink_path):
        return True

    def rollback(self):
        return True

    def unregister_target(self, file_path):
        return True

    def register_link(self, ln_container):
        return True

    def unregister_link(self, target_path, link_path):
        return True