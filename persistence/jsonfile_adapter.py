import json
import os
import logging
import time

from persistence.persistence_adapter import PersistenceAdapter


def transactional(function):
	def decorated_function(*args):
		pass

	return decorated_function

class JsonFileAdapter(PersistenceAdapter):

	def __init__(self, ln_db_dir):
		db_file_name = 'symlink_db.json'
		self._db_file_path = self._open_link_db(ln_db_dir, db_file_name)
		self._db = self._load_json_content()
		self.__LOCK_FILE = os.path.join(ln_db_dir, 'symlink_db.lock')

	def contains_symlink(self, symlink_path):
		return self.targetfile_for_link(symlink_path)

	def contains_target_file(self, target_file_path):
		self._db = self._load_json_content()
		return self._db.__contains__(target_file_path)

	def register_link(self, ln_container, transactional=True):
		if transactional:
			db_dict = self._get_open_transaction()
		else:
			db_dict = self._db

		try:
			link    = ln_container.link_name
			target  = ln_container.target_name

			if not target in db_dict:
				db_dict[target] = [link]
			elif not link in db_dict[target]:
				db_dict[target].append(link)

			self._uncommitted_db = db_dict

			return True

		except Exception as e:
			return False

	def unregister_link(self, target_path, link_path, transactional=True):
		if transactional:
			db_dict = self._get_open_transaction()
		else:
			db_dict = self._db

		try:
			if not db_dict.__contains__(target_path):
				raise Exception('No target `' + target_path +
								'`found in link database.')

			for link in db_dict[target_path]:
				if link == link_path:
					db_dict[target_path].remove(link)

			return True
		except Exception as e:
			return False

	def targetfile_for_link(self, link_path):
		for targetfile in self._db:
			for symlink in targetfile:
				if symlink == link_path: return targetfile

	def unregister_target(self, target_path):
		try:
			if self._db.__contains__(target_path):
				self._db.pop(target_path)

			return True
		except Exception as e: return False

	def commit(self):
		if self._uncommitted_db:
			self._db = self._uncommitted_db
			self._save_json_content()

	def _load_json_content(self):
		try:
			self._lock_db()

			with open(self._db_file_path, mode='r') as db_file:
				return json.load(db_file)

		except ValueError as e:
			# No json database exists.
			# TODO this error could also be thrown if the JSON is invalid.
			return dict()

	def _save_json_content(self):
		with open(self._db_file_path, mode='w') as db_file:
			db_file.write(json.dumps(self._db, indent=4, separators=(',', ' : ')))

	def _get_open_transaction(self):
		if self._uncommitted_db:
			db_dict = self._uncommitted_db
		else:
			db_dict = self._db.copy()
		return db_dict

	def _is_db_locked(self):
		if os.path.isfile(self.__LOCK_FILE):
			return True
		else:
			return False

	def _lock_db(self):
		while self._is_db_locked():
			logging.debug('Waiting for database lock...')
			time.sleep(0.25)

		with open(self.__LOCK_FILE, mode='w'):
			pass
