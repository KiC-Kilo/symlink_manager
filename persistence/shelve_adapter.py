import os
import shelve

from persistence.persistence_adapter import PersistenceAdapter


class ShelveAdapter(PersistenceAdapter):

    def __init__(self, ln_db_dir):
        self.ln_db_file_path = self.__create_link_db(ln_db_dir)

    def register_link(self, ln_container):

        with shelve.open(self.ln_db_file_path, writeback=True) as db:
            source = ln_container.source
            target = ln_container.target

            print(db.get(target))

            if not db.keys().__contains__(target):
                db[target] = [source]
            else:
                db[target].append(source)

            print(db.get(target))

        return True

    def unregister_link(self, ln_container):

        with shelve.open(self.ln_db_file_path, writeback=True) as db:
            source = ln_container.source
            target = ln_container.target

            if db.get(target):
                db.get(target).remove(source)

        return True

    def __create_link_db(self, ln_db_dir):
        link_db_file = 'symlink_database'
        if not os.path.exists(ln_db_dir):
            os.makedirs(ln_db_dir)

        return os.path.join(ln_db_dir, link_db_file)
