from persistence.persistence_adapter import PersistenceAdapter


class FileService:

    def __init__(self, mv_command, persistence_adapter):
        assert isinstance(mv_command, list)
        assert isinstance(persistence_adapter, PersistenceAdapter)

        self.persistence_adapter = persistence_adapter

    def move_file(self, original_path, new_path):

        pass
