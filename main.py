import argparse
import logging
import logging.config
import os

from persistence.jsonfile_adapter import JsonFileAdapter
from services.mv_service import MvService
from services.ln_service import LnService


def main():
	"""
	This implementation only supports form 1 of the ln command as of GNU coreutils version
	8.24.  Per the man pages:

		ln [OPTION]... [-T] TARGET LINK_NAME

	:return:
	"""
	configure_logging(logging.DEBUG, 'log/symlink_manager.log')

	link_db_dir = os.path.join('/home/', os.environ['USER'],
							   '.symlink_manager/link_data')	# TODO find a real home for this.
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
		raise Exception('No arguments given') # TODO use argparse for this


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('command', nargs=argparse.REMAINDER)
	return parser.parse_args().command


def configure_logging(level, filename):
	logging.config.fileConfig('../config/logging.conf')


if __name__ == '__main__':
	main()