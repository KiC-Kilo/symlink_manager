def file_contents_equal(filepath_1, filepath_2):

    with open(filepath_1, mode='rb') as file_1:
        with open(filepath_2, mode='rb') as file_2:
            content_1 = file_1.read()
            content_2 = file_2.read()

            return content_1 == content_2

def file_content_equals_string(filepath, string):

    with open(filepath, mode='rb') as file:
        file_content = file.read()

        return file_content == string
