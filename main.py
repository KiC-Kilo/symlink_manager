import argparse

from persistence.jsonfile_adapter import JsonFileAdapter
from services.mv_service import MvService
from services.ln_service import LnService


def main():
    """
    This implementation only supports form 1 of the ln command

    TODO support other forms.
    :return:
    """
    link_db_dir = '~/.symlink_manager/link_database' # TODO find a real home for this.
    persistence_adapter = JsonFileAdapter(link_db_dir)

    raw_command = parse_args()
    root_command = raw_command[0]
    if root_command == 'ln':
        link_service = LnService(raw_command, persistence_adapter)
        link_service.create_link()

    elif root_command == 'mv':
        move_service = MvService(raw_command, persistence_adapter)
        move_service.execute_mv()
    elif root_command == 'rm':
        pass # TODO
    else:
        raise Exception('No arguments given') #todo use argparse for this

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs=argparse.REMAINDER)
    return parser.parse_args().command


if __name__ == '__main__':
    main()