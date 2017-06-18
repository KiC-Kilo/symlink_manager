import logging

import copy
import os
import time
import uuid
from abc import ABCMeta
from abc import abstractmethod


def transaction(fn):
    """
    A decorator to be used for all transactional functions.  The rationale behind making
    functions transactional rather than making entire calls to the main program
    transactional is that, while not currently implemented, at some point the program may
    ask for user input (e.g. to confirm overwriting a file).  If this were to happen, it
    would lock the symlink database for all other instances of the program.
    
    :param fn:  The function to be decorated with a transaction.
    :return:    Returns a transactional version of the given function.
    """
    def transactional_fn(self, *args):
        self._lock_db()
        self._db = self._load_link_data()
        self._current_transaction = copy.deepcopy(self._db)
        try:
            fn(self, *args)
            self.commit()
        except Exception as e:
            # TODO log error
            self.rollback()
            pass
        self._unlock_db()
        # Ensure that we can't reuse the link data outside this transaction
        self._current_transaction, self._db = None, None

    return transactional_fn

class PersistenceAdapter(metaclass=ABCMeta):

    _LOCK_FILE_NAME = 'symlink_db.lock'

    def __init__(self, link_db_dir):
        self._current_transaction   = None
        self._db                    = None
        self._instance_id           = uuid.uuid4()


    def _is_db_locked(self):
        return os.path.exists(self._LOCK_FILE_NAME)


    def _lock_db(self):
        while self._is_db_locked():
            logging.debug('Waiting for data file lock (instance %s)', self._instance_id)
            time.sleep(0.25)

        with open(self._LOCK_FILE_NAME, mode='w') as lockfile:
            lockfile.write(str(self._instance_id) + "\n")

        if not self._this_instance_owns_lock():
            # Another PersistenceAdapter (probably another instance of the program)
            # beat us to the punch; try to lock again.
            self._lock_db()

        logging.debug('Instance %s has data file lock.', self._instance_id)


    def _this_instance_owns_lock(self):
        if os.path.isfile(self._LOCK_FILE_NAME):
            with open(self._LOCK_FILE_NAME) as lockfile:
                instance_id = lockfile.read().strip()
                return instance_id == str(self._instance_id)
        else:
            return False


    def _unlock_db(self):
        if self._this_instance_owns_lock():
            os.remove(self._LOCK_FILE_NAME)


    @abstractmethod
    def register_link(self, ln_container):
        raise NotImplemented

    @abstractmethod
    def unregister_link(self, target_path, link_path):
        raise NotImplemented

    @abstractmethod
    def unregister_target(self, file_path):
        raise NotImplemented

    @abstractmethod
    def contains_symlink(self, symlink_path):
        raise NotImplemented

    @abstractmethod
    def contains_target_file(self, target_file_path):
        raise NotImplemented

    @abstractmethod
    def target_file_for_link(self, symlink_path):
        raise NotImplemented

    @abstractmethod
    def reregister_target_file(self, old_filepath, new_filepath):
        raise NotImplemented

    @abstractmethod
    def commit(self):
        """
        Writes all pending data changes.
        :return: 
        """
        raise NotImplemented

    @abstractmethod
    def rollback(self):
        """
        Reset the state of the transaction to match the unmodified database.
        :return: 
        """
        raise NotImplemented

    def link_exists(self, symlink_path: str):
        raise os.path.lexists(symlink_path)

    def target_exists(self, target_path: str):
        return os.path.exists(target_path)

    @abstractmethod
    def _load_link_data(self):
        raise NotImplemented

    @abstractmethod
    def _save_link_data(self, data):
        raise NotImplemented
