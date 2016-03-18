import json
import os
import tempfile
import unittest
import uuid

from persistence.jsonfile_adapter import JsonFileAdapter
from shell_command.ln_container import LnCommand


class PersistenceAdapterTests(unittest.TestCase):

    def test_adds_new_file_keys(self):
        # Arrange
        test_dir = tempfile.TemporaryDirectory()
        json_adapter = JsonFileAdapter(test_dir.name)
        ln_container = LnCommand(['ln', '-s', 'TARGET', 'LINK_NAME'])

        # Act
        json_adapter.register_link(ln_container)

        # Assert
        db_content = self.load_json_content(json_adapter)

        assert db_content.__contains__('TARGET')

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

        # Assert
        db_content = self.load_json_content(json_adapter)
        assert db_content.__contains__('TARGET')
        target = db_content.get('TARGET')
        assert('LINK_NAME_1' in target and
               'LINK_NAME_2' in target and len(target) == 2)

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

        # Act
        json_adapter.unregister_link(ln_command_2.target_name,
                                     ln_command_2.link_name)

        # Assert
        db_content = self.load_json_content(json_adapter)

        target_file_path = os.path.join(test_dir, test_file)
        link_list = db_content[target_file_path]
        assert      link_list.__contains__(ln_command_1.link_name)
        assert      link_list.__contains__(ln_command_3.link_name)
        assert not  link_list.__contains__(ln_command_2.link_name)


    def load_json_content(self, json_adapter):
        with open(json_adapter._db_file_path, mode='r') as file:
            content = json.load(file)

        return content

    def _random_ln_command(self, test_dir, test_file):
        file_path = os.path.join(test_dir, test_file)
        link_path = os.path.join(test_dir, uuid.uuid4().hex)

        return LnCommand(['ln', '-s', file_path, link_path])
