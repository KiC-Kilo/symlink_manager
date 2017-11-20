import os
import tempfile


class BaseServiceTest(object):
    def setUp(self):
        self.data_dir = tempfile.TemporaryDirectory()
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file = tempfile.NamedTemporaryFile(delete=False,  # dir will be deleted
                                                     dir=self.test_dir.name)

    def tearDown(self):
        self.data_dir.cleanup()
        self.test_dir.cleanup()

    def dummy_file_full_path(self):
        return os.path.join(self.test_dir.name, str(self.test_file.name))

    def link_file_full_path(self):
        return os.path.join(self.test_dir.name, 'link')

    def write_to_dummy_file(self, string):
        self.test_file.write(string.encode('UTF8'))
        self.test_file.flush()
        self.test_file.close()

    def data_dir_name(self):
        return self.data_dir.name

    @staticmethod
    def file_contents_equal(filepath_1, filepath_2):
        with open(filepath_1, mode='rb') as file_1:
            with open(filepath_2, mode='rb') as file_2:
                content_1 = file_1.read()
                content_2 = file_2.read()
                return content_1 == content_2

    @staticmethod
    def file_content_equals_string(filepath, string):
        with open(filepath, mode='rb') as file:
            file_content = file.read()
            return file_content == string.encode('UTF8')
