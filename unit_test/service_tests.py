import os
import tempfile
import unittest

from services.ln_service import LnService
from unit_test.stubs.persistence_adapter import AlwaysSuccessfulPersistenceAdapter
from util.test_utils import file_content_equals_string


class LnServiceTests(unittest.TestCase):
    def test_creates_symlink_with_valid_ln_command(self):
        # Arrange
        persistence_adapter = AlwaysSuccessfulPersistenceAdapter()

        link_source = self.dummy_file_full_path()
        link_target = os.path.join(self.test_dir.name, 'link')
        ln_command = ['ln', '-s', link_source, link_target]

        # Act
        link_service = LnService(ln_command, persistence_adapter)
        link_service.create_link()

        dummy_file_content = 'foooooo bar'.encode('UTF8')
        self.test_file.write(dummy_file_content)
        self.test_file.flush()
        self.test_file.close()

        assert(file_content_equals_string(link_target, dummy_file_content))

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file = tempfile.NamedTemporaryFile(delete=False,  # dir will be deleted
                                                     dir=self.test_dir.name)

    def dummy_file_full_path(self):
        return os.path.join(self.test_dir.name, str(self.test_file.name))


if __name__ == '__main__':
    unittest.main()
