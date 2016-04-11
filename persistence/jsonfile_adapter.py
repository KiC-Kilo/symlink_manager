import json

from persistence.persistence_adapter import PersistenceAdapter


def read_write_operation(function):
	def wrapped_function(*args):
		self = args[0]
		self._load_json_content()
		result = function(*args)
		self._save_json_content()

		return result and self._save_json_content()

	return wrapped_function

def read_operation(function):
	def wrapped_function(*args):
		self = args[0]
		self._load_json_content()
		result = function(*args)

		return result

class JsonFileAdapter(PersistenceAdapter):

	def __init__(self, ln_db_dir):
		self._db_file_name = 'symlink_db.json'
		self._db_file_path = self._open_link_db(ln_db_dir, self._db_file_name)

	@read_operation
	def contains_symlink(self, symlink_path):
		return self._db.__contains__(symlink_path)

	@read_operation
	def contains_target_file(self, target_file_path):
		self._db = self._load_json_content()
		return self._db.__contains__(target_file_path)

	@read_write_operation
	def register_link(self, ln_container):
		try:
			link    = ln_container.link_name
			target  = ln_container.target_name
			db = self._db

			if not db.__contains__(target):
				db[target] = [link]
			elif not db[target].__contains__(link):
				db[target].append(link)

			return True

		except Exception as e:
			return False

	@read_write_operation
	def unregister_link(self, target_path, link_path):
		try:
			db = self._db

			if not db.__contains__(target_path):
				raise Exception('No target `' + target_path +
								'`found in link database.')

			for link in db[target_path]:
				if link == link_path:
					db[target_path].remove(link)

			return True
		except Exception as e:
			return False

	@read_write_operation
	def unregister_target(self, target_path):
		try:
			db = self._db

			if db.__contains__(target_path):
				db.pop(target_path)

			return True
		except Exception as e: return False

	def _load_json_content(self):
		try:
			with open(self._db_file_path, mode='r') as db_file:
				self._db = json.load(db_file)

		except ValueError as e:
			# No json database exists.
			self._db = dict()

	def _save_json_content(self):
		with open(self._db_file_path, mode='w') as db_file:
			db_file.write(json.dumps(self._db, indent=4, separators=(',', ' : ')))

