import os
from abc import ABCMeta

class PersistenceAdapter(metaclass=ABCMeta):

    def register_link(self, ln_container):
        raise NotImplemented

    def unregister_link(self, link_path):
        raise NotImplemented


    def _open_link_db(self, ln_db_dir, ln_db_filename):
        if not os.path.exists(ln_db_dir):
            os.makedirs(ln_db_dir)

        file_path = os.path.join(ln_db_dir, ln_db_filename)
        if not os.path.exists(file_path):
            open(file_path, mode='w').close()

        return file_path
