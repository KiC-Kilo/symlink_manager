import json
import logging
import os
import tempfile
import unittest
import uuid

from main import configure_logging
from persistence.jsonfile_adapter import JsonFileAdapter
from shell_command.ln_container import LnCommand


class PersistenceAdapterTests(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		print(os.getcwd())
		configure_logging(logging.DEBUG, 'symlink_manager.test.log')

	def test_adds_new_file_keys(self):
		# Arrange
		test_dir = tempfile.TemporaryDirectory()
		json_adapter = JsonFileAdapter(test_dir.name)
		ln_container = LnCommand(['ln', '-s', 'TARGET', 'LINK_NAME'])

		# Act
		json_adapter.register_link(ln_container)
		json_adapter.commit()

		# Assert
		db_content = self.load_json_content(json_adapter)

		assert os.path.join(os.getcwd(), 'TARGET') in db_content

		pass

	def test_appends_values_to_existing_keys(self):
		# Arrange
		test_dir = tempfile.TemporaryDirectory()
		json_adapter = JsonFileAdapter(test_dir.name)
		ln_container_1 = LnCommand(['ln', '-s', 'TARGET', 'LINK_NAME_1'])
		ln_container_2 = LnCommand(['ln', '-s', 'TARGET', 'LINK_NAME_2'])

		# Act
		json_adapter.register_link(ln_container_1)
		json_adapter.register_link(ln_container_2)
		json_adapter.commit()

		# Assert
		db_content = self.load_json_content(json_adapter)
		target = os.path.join(os.getcwd(), 'TARGET')
		assert target in db_content
		target = db_content.get(target)
		link_1 = os.path.join(os.getcwd(), 'LINK_NAME_1')
		link_2 = os.path.join(os.getcwd(), 'LINK_NAME_2')
		assert(link_1 in target and
			   link_2 in target and len(target) == 2)

		pass

	def test_removes_existing_links(self):
		# Arrange
		db_dir = tempfile.TemporaryDirectory()
		json_adapter = JsonFileAdapter(db_dir.name)

		test_dir = 'target_directory'
		test_file = 'target_filename'
		ln_command_1 = self._random_ln_command(test_dir, test_file)
		ln_command_2 = self._random_ln_command(test_dir, test_file)
		ln_command_3 = self._random_ln_command(test_dir, test_file)

		json_adapter.register_link(ln_command_1)
		json_adapter.register_link(ln_command_2)
		json_adapter.register_link(ln_command_3)
		json_adapter.commit()

		# Act
		json_adapter.unregister_link(ln_command_2.target_name,
									 ln_command_2.link_name)
		json_adapter.commit()

		# Assert
		db_content = self.load_json_content(json_adapter)

		target_file_path = os.path.join(os.getcwd(), test_dir, test_file)
		link_list = db_content[target_file_path]
		link_1 = os.path.join(os.getcwd(), ln_command_1.link_name)
		link_2 = os.path.join(os.getcwd(), ln_command_2.link_name)
		link_3 = os.path.join(os.getcwd(), ln_command_3.link_name)
		assert      link_1 in link_list
		assert      link_3 in link_list
		assert not  link_2 in link_list


	def load_json_content(self, json_adapter):
		with open(json_adapter._db_file_path, mode='r') as file:
			content = json.load(file)

		return content

	def _random_ln_command(self, test_dir, test_file):
		file_path = os.path.join(test_dir, test_file)
		link_path = os.path.join(test_dir, uuid.uuid4().hex)

		return LnCommand(['ln', '-s', file_path, link_path])
