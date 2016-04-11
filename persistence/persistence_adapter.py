import os
from abc import ABCMeta

class PersistenceAdapter(metaclass=ABCMeta):

    def register_link(self, ln_container):
        raise NotImplemented

    def unregister_link(self, target_path, link_path):
        raise NotImplemented

    def unregister_target(self, file_path):
        raise NotImplemented

    def contains_symlink(self, symlink_path):
        raise NotImplemented

    def contains_target_file(self, target_file_path):
        raise NotImplemented

    def _open_link_db(self, ln_db_dir, ln_db_filename):
        if not os.path.exists(ln_db_dir):
            os.makedirs(ln_db_dir)

        file_path = os.path.join(ln_db_dir, ln_db_filename)
        if not os.path.exists(file_path):
            open(file_path, mode='w').close()

        return file_path
