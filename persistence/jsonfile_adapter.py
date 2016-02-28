import json

from persistence.persistence_adapter import PersistenceAdapter


class JsonFileAdapter(PersistenceAdapter):

    def __init__(self, ln_db_dir):
        self._db_file_name = 'symlink_db.json'
        self._db_file_path = self._open_link_db(ln_db_dir, self._db_file_name)

    def register_link(self, ln_container):
        try:
            db = self.__load_json_content()

            link    = ln_container.link_name
            target  = ln_container.target_name

            if not db.__contains__(target):
                db[target] = [link]
            else:
                db[target].append(link)

            self.__save_json_content(db)

            return True

        except Exception as e:
            return False

    def unregister_link(self, ln_container):
        try:
            db = self.__load_json_content()

            target = ln_container.target

            if db.__contains__(target):
                db.pop(target)

            return True

        except Exception: return False


    def __load_json_content(self):
        try:
            with open(self._db_file_path, mode='r') as db_file:
                db = json.load(db_file)

            return db
        except ValueError as e:
            return dict()

    def __save_json_content(self, content):
        with open(self._db_file_path, mode='w') as db_file:
            db_file.write(json.dumps(content, indent=4, separators=(',', ' : ')))
