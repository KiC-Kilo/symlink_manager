import json

import copy
import os

from symmv.logging import logger
from symmv.persistence.persistence_adapter import PersistenceAdapter
from symmv.persistence.persistence_adapter import transaction


class JsonFileAdapter(PersistenceAdapter):


    def __init__(self, link_db_dir: str):
        super().__init__(link_db_dir)
        db_file_name = 'symlink_db.json'
        self._db_file_path = self._open_link_db(link_db_dir, db_file_name)


    @transaction
    def register_link(self, target_path: str, link_path: str):
        try:
            self._register_link(target_path, link_path)
        except Exception as e:
            logger.error(str(e))
            return False
        return True


    @transaction
    def unregister_link(self, target_path: str, link_path: str):
        self._unregister_link(target_path, link_path)


    def _target_file_for_link(self, link_path: str):
        for targetfile in self._current_transaction:
            for symlink in self._current_transaction[targetfile]:
                if symlink == link_path: return targetfile


    @transaction
    def unregister_target(self, target_path: str):
        try:
            if target_path in self._current_transaction:
                self._current_transaction.pop(target_path)
        except Exception as e: return False
        return True


    @transaction
    def reregister_target_file(self, old_filepath: str, new_filepath: str):
        for link in self._current_transaction[old_filepath]:
            self._unregister_link(old_filepath, link)
            self._register_link(link, new_filepath)


    @transaction
    def reregister_link(self, old_link_path: str, new_link_path: str):
        target_path = self._target_file_for_link(old_link_path)
        self._unregister_link(target_path, old_link_path)
        self._register_link(target_path, new_link_path)


    def commit(self):
        self._save_link_data(self._current_transaction)


    def rollback(self):
        self._current_transaction = copy.deepcopy(self._db)


    def _open_link_db(self, link_db_dir, ln_db_filename):
        logger.debug("Opening link DB: " + link_db_dir + ln_db_filename)
        if not os.path.exists(link_db_dir):
            os.makedirs(link_db_dir)

        file_path = os.path.join(link_db_dir, ln_db_filename)
        if not os.path.exists(file_path):
            open(file_path, mode='w').close()

        return file_path


    def _load_link_data(self):
        try:
            with open(self._db_file_path, mode='r') as db_file:
                return json.load(db_file)

        except ValueError as e:
            # No json file exists.
            # TODO this error could also be thrown if the JSON is invalid.
            return dict()


    def _save_link_data(self, data):
        with open(self._db_file_path, mode='w') as db_file:
            db_file.write(json.dumps(data,
                                     indent=4,
                                     separators=(',', ' : ')))


    def _register_link(self, target: str, link: str):
        db_dict = self._current_transaction

        if not target in db_dict:
            db_dict[target] = [link]
        elif not link in db_dict[target]:
            db_dict[target].append(link)

        return True


    def _unregister_link(self, target_path: str, link_path: str):
        db_dict = self._current_transaction
        try:
            if not target_path in db_dict:
                raise Exception('No target `' + target_path +
                                '`found in link data file.')

            for link in db_dict[target_path]:
                if link == link_path:
                    db_dict[target_path].remove(link)

        except Exception as e:
            return False
        return True


    def contains_symlink(self, symlink_path):
        for key in self._current_transaction:
            if symlink_path in self._current_transaction[key]:
                return True
        return False


    def contains_target_file(self, target_path):
        return target_path in self._current_transaction
