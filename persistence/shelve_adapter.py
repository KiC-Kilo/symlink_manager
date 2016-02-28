import os
import shelve

from persistence.persistence_adapter import PersistenceAdapter


class ShelveAdapter(PersistenceAdapter):

    def __init__(self, ln_db_dir):
        self.ln_db_file_path = self._open_link_db(ln_db_dir, 'symlink_db.shelve')

    def register_link(self, ln_container):
        try:
            with shelve.open(self.ln_db_file_path, writeback=True) as db:
                source = ln_container.source
                target = ln_container.target

                print(db.get(target))

                if not db.__contains__(target):
                    db[target] = [source]
                else:
                    db[target].append(source)

                print(db.get(target))

            return True

        except Exception: return False

    def unregister_link(self, ln_container):

        with shelve.open(self.ln_db_file_path, writeback=True) as db:
            source = ln_container.source
            target = ln_container.target

            if db.get(target):
                db.get(target).remove(source)

        return True
