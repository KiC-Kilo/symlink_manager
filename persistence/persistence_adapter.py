import logging

import copy
import os
import time
import uuid
from abc import ABCMeta
from abc import abstractmethod


def transaction(fn):
	def transactional_fn(self, *args):
		self._lock_db()
		self._db = self._load_link_data()
		self._current_transaction = copy.deepcopy(self._db)
		try:
			fn(self, *args)
			self.commit()
		except Exception as e:
			# TODO
			self.rollback()
			pass
		self._unlock_db()
	return transactional_fn


class PersistenceAdapter(metaclass=ABCMeta):

	def __init__(self, link_db_dir):
		self._instance_id = uuid.uuid4()
		self._LOCK_FILE = os.path.join(link_db_dir, 'symlink_db.lock')


	def _open_link_db(self, link_db_dir, ln_db_filename):
		if not os.path.exists(link_db_dir):
			os.makedirs(link_db_dir)

		file_path = os.path.join(link_db_dir, ln_db_filename)
		if not os.path.exists(file_path):
			open(file_path, mode='w').close()

		return file_path


	def _is_db_locked(self):
		return os.path.exists(self._LOCK_FILE)


	def _lock_db(self):
		while self._is_db_locked():
			logging.debug('Waiting for data file lock (instance %s)', self._instance_id)
			time.sleep(0.25)

		with open(self._LOCK_FILE, mode='w') as lockfile:
			lockfile.write(str(self._instance_id) + "\n")

		if not self._owns_lock():
			# Another PersistenceAdapter (probably another instance of the program)
			# beat us to the punch; try to lock again.
			self._lock_db()

		logging.debug('Instance %s has data file lock.', self._instance_id)


	def _owns_lock(self):
		if os.path.isfile(self._LOCK_FILE):
			with open(self._LOCK_FILE) as lockfile:
				instance_id = lockfile.read().strip()
				return instance_id == str(self._instance_id)
		else:
			return False


	def _unlock_db(self):
		if self._owns_lock():
			os.remove(self._LOCK_FILE)


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
		raise NotImplemented

	@abstractmethod
	def rollback(self):
		raise NotImplemented

	@abstractmethod
	def link_exists(self, symlink_path: str):
		raise NotImplemented

	@abstractmethod
	def target_exists(self, target_path: str):
		raise NotImplemented

	@abstractmethod
	def _load_link_data(self):
		raise NotImplemented

	@abstractmethod
	def _save_link_data(self):
		raise NotImplemented
