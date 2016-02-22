import argparse

from persistence.shelve_adapter import ShelveAdapter
from services.file_service import FileService
from services.link_service import LinkService



def main():
    link_db_dir = '/home/kmcvay/.symlink_manager/link_database'
    persistence_adapter = ShelveAdapter(link_db_dir)

    raw_command = parse_args()
    root_command = raw_command[0]
    if root_command == 'ln':
        link_service = LinkService(raw_command, persistence_adapter)
        link_service.create_link()

    elif root_command == 'mv':
        file_service = FileService(raw_command, persistence_adapter)
        file_service.move_file()

    else:
        raise Exception('No arguments given') #todo use argparse for this

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs=argparse.REMAINDER)
    return parser.parse_args().command


if __name__ == '__main__':
    main()