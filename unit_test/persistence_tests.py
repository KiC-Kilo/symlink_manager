import json
import tempfile
import unittest

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


    def load_json_content(self, json_adapter):
        with open(json_adapter._db_file_path, mode='r') as file:
            content = json.load(file)

        return content