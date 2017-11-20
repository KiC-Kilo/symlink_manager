import tempfile
import unittest

import os

from symmv.persistence.jsonfile_adapter import JsonFileAdapter
from symmv.services.mv_service import MvService

from symmv.services.ln_service import LnService
from symmv.unit_test.services.base_service_test import BaseServiceTest
from symmv.unit_test.stubs.persistence_adapter import AlwaysSuccessfulPersistenceAdapter


class LnServiceTests(BaseServiceTest):

    def test_creates_symlink_with_valid_ln_command(self):
        # Arrange
        persistence_adapter = AlwaysSuccessfulPersistenceAdapter('')
        link_source = self.dummy_file_full_path()
        link_target = self.link_file_full_path()
        ln_command = ['ln', '-s', link_source, link_target]

        # Act
        link_service = LnService(ln_command, persistence_adapter)
        link_service.create_link()
        dummy_file_content = 'foooooo bar'
        self.write_to_dummy_file(dummy_file_content)

        # Assert
        assert(BaseServiceTest.file_content_equals_string(
            link_target, dummy_file_content))


class MvServiceTests(BaseServiceTest):
    def test_updates_link_when_moving_link(self):
        # Arrange
        link_source = self.dummy_file_full_path()
        link_target = self.link_file_full_path()
        ln_command = ['ln', '-s', link_source, link_target]
        persistence_adapter = JsonFileAdapter(self.data_dir_name())
        link_service = LnService(ln_command, persistence_adapter)
        link_service.create_link()

        # Act
        new_name = link_target + '_moved'
        mv_command = ['mv', link_target, new_name]
        mv_service = MvService(mv_command, persistence_adapter)
        self.write_to_dummy_file('foo')
        mv_service.execute_mv()

        # Assert
        assert(BaseServiceTest.file_content_equals_string(
            link_target + '_moved', 'foo'
        ))


class RmServiceTests(BaseServiceTest):
    pass

if __name__ == '__main__':
    unittest.main()
