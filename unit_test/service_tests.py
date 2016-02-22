import os
import subprocess
import tempfile
import unittest

from services.link_service import LinkService
from unit_test.stubs.persistence_adapter import StubbedPersistenceAdapter


class LinkServiceTests(unittest.TestCase):
    def test_creates_symlink_with_valid_ln_command(self):
        # Arrange
        # self.setup()
        persistence_adapter = StubbedPersistenceAdapter()

        link_source = self.dummy_file_full_path()
        link_target = os.path.join(self.test_dir.name, 'link')
        ln_command = ['ln', '-s', link_source, link_target]

        # Act
        link_service = LinkService(ln_command, persistence_adapter)
        link_service.create_link()

        dummy_file_content = 'foooooo bar'.encode('UTF8')
        self.test_file.write(dummy_file_content)
        self.test_file.flush()
        linked_content = subprocess.Popen(['cat', link_target],
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE).communicate()[0]
        # TODO ^^^ Iterate through file, cat is a hack.
        # Assert
        self.assertEqual(dummy_file_content, linked_content)

    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file = tempfile.NamedTemporaryFile(delete=False,  # dir will be deleted
                                                     dir=self.test_dir.name)

    def dummy_file_full_path(self):
        return os.path.join(self.test_dir.name, str(self.test_file.name))

if __name__ == '__main__':
    unittest.main()
