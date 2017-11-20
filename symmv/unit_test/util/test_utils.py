

# def random_ln_command():
#     test_dir = tempfile.TemporaryDirectory()
#     test_file = tempfile.NamedTemporaryFile(delete=False,
#                                             dir=test_dir.name)
#     file_path = os.path.join(test_dir.name, test_file.name)
#     link_path = os.path.join(test_dir.name, uuid.uuid4().hex)
#
#     return LnCommand(['ln', '-s', file_path, link_path])
#
