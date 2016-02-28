import argparse

from persistence.shelve_adapter import ShelveAdapter
from services.mv_service import MvService
from services.ln_service import LnService



def main():
    """
    This implementation only supports form 1 of the ln command

    TODO support other forms.
    :return:
    """
    link_db_dir = '/home/kmcvay/.symlink_manager/link_database'
    persistence_adapter = ShelveAdapter(link_db_dir)

    raw_command = parse_args()
    root_command = raw_command[0]
    if root_command == 'ln':
        link_service = LnService(raw_command, persistence_adapter)
        link_service.create_link()

    elif root_command == 'mv':
        file_service = MvService(raw_command, persistence_adapter)
        file_service.move_file()    # TODO generalize these move_file and create_link calls
                                    # in a superclass?
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