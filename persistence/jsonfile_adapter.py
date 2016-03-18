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
            elif not db[target].__contains__(link):
                db[target].append(link)

            self.__save_json_content(db)

            return True

        except Exception as e:
            return False

    def unregister_link(self, target_path, link_path):
        try:
            db = self.__load_json_content()

            if not db.__contains__(target_path):
                raise Exception('No target `' + target_path +
                                '`found in link database.')

            for link in db[target_path]:
                if link == link_path:
                    db[target_path].remove(link)

            self.__save_json_content(db)
            return True

        except Exception as e:
            return False


    def unregister_target(self, target_path):
        try:
            db = self.__load_json_content()

            if db.__contains__(target_path):
                db.pop(target_path)

            return True
        except Exception as e: return False

    def __load_json_content(self):
        try:
            with open(self._db_file_path, mode='r') as db_file:
                db = json.load(db_file)

            return db
        except ValueError as e:
            return dict()

    # TODO convert to decorator?
    def __save_json_content(self, content):
        with open(self._db_file_path, mode='w') as db_file:
            db_file.write(json.dumps(content, indent=4, separators=(',', ' : ')))


