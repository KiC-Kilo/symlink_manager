import os
import shelve

from persistence.persistence_adapter import PersistenceAdapter


class ShelveAdapter(PersistenceAdapter):

    def __init__(self, ln_db_file_path):
        self.ln_db_file_path = ln_db_file_path

    def register_link(self, ln_container):
        db = shelve.open(self.ln_db_file_path, writeback=True)

        source = ln_container.source
        target = ln_container.target

        if not db.keys().__contains__(target):
            db[target] = source
            return True
        else:
            db[target].append(source)
            return False

        pass


    def __create_link_db(self):
        link_db_path = '/home/kmcvay/.symlink_manager/'
        link_db_file = 'link_database'
        if not os.path.exists(link_db_path):
            os.makedirs(link_db_path)

        return link_db_path + link_db_file
