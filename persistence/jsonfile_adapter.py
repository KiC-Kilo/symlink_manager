import copy
import json

from persistence.persistence_adapter import PersistenceAdapter
from shell_command.ln_container import LnCommand


class JsonFileAdapter(PersistenceAdapter):

	def __init__(self, ln_db_dir: str):
		super().__init__(ln_db_dir)

		db_file_name = 'symlink_db.json'
		self._db_file_path = self._open_link_db(ln_db_dir, db_file_name)
		self._db = self._load_json_content()
		self._current_transaction = copy.deepcopy(self._db)

	def contains_symlink(self, symlink_path: str):
		return self.target_file_for_link(symlink_path)

	def contains_target_file(self, target_file_path: str):
		return target_file_path in self._current_transaction

	def register_link(self, ln_container: LnCommand):
		db_dict = self._current_transaction

		try:
			link    = ln_container.link_name
			target  = ln_container.target_name

			if not target in db_dict:
				db_dict[target] = [link]
			elif not link in db_dict[target]:
				db_dict[target].append(link)

		except Exception as e:
			return False

		return True

	def unregister_link(self, target_path: str, link_path: str):
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

	def target_file_for_link(self, link_path: str):
		for targetfile in self._current_transaction:
			for symlink in targetfile:
				if symlink == link_path: return targetfile

	def unregister_target(self, target_path: str):
		try:
			if target_path in self._current_transaction:
				self._current_transaction.pop(target_path)

		except Exception as e: return False

		return True

	def reregister_target_file(self, old_filepath: str, new_filepath: str):
		for link in self._current_transaction[old_filepath]:
			self.unregister_link(old_filepath, link)
			self._register_link(link, new_filepath)

	def commit(self):
		self._db = copy.deepcopy(self._current_transaction)
		self._save_json_content()

	def rollback(self):
		self._current_transaction = copy.deepcopy(self._db)
		self._save_json_content()

	def _load_json_content(self):
		try:
			self._lock_db()

			with open(self._db_file_path, mode='r') as db_file:
				return json.load(db_file)

		except ValueError as e:
			# No json file exists.
			# TODO this error could also be thrown if the JSON is invalid.
			return dict()

	def _save_json_content(self):
		with open(self._db_file_path, mode='w') as db_file:
			db_file.write(json.dumps(self._db, indent=4, separators=(',', ' : ')))

	def _register_link(self, target: str, link: str):
		db_dict = self._current_transaction

		if not target in db_dict:
			db_dict[target] = link
		elif not link in db_dict[target]:
			db_dict[target].append(link)

		return True
