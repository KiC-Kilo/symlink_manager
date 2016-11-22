import logging
import subprocess

from services.command_service import CommandService
from shell_command.rm_container import RmCommand


class RmService(CommandService):
	"""
	Responsible for removing files and symbolic links and registering the changes
	with the given persistence adapter.
	"""

	def __init__(self, rm_command, persistence_adapter):
		super().__init__(persistence_adapter)
		self.rm_container = RmCommand(rm_command)

	def remove_target_file(self):
		try:
			rm_command = self.rm_container

			logging.info('Attempting to unregister all links for file...')
			if self.persistence_adapter.unregister_target(rm_command.target):
				logging.info('File unregistered.')

			rm_result = subprocess.run(rm_command.raw_command.split(),
									   stderr=subprocess.PIPE,
									   universal_newlines=True,
									   shell=True)

			if rm_result.returncode != 0:
				logging.error('Error moving file: ' + rm_result.stderr)
				self.persistence_adapter.rollback()
				return False
			else:
				self.persistence_adapter.commit()

		except Exception as e:
			return False

		return True

def remove_link(self):
	try:
		rm_command = self.rm_container

		logging.info('Attempting to unregister link...')
		if self.persistence_adapter.unregister_target(rm_command.target):
			logging.info('Link unregistered.')

			rm_result = subprocess.run(rm_command.raw_command.split(),
									   stderr=subprocess.PIPE,
									   universal_newlines=True,
									   shell=True)

			if rm_result.returncode != 0:
				logging.error('Error moving file: ' + rm_result.stderr)
				self.persistence_adapter.rollback()
				return False
			else:
				self.persistence_adapter.commit()

	except Exception as e:
		return False

	return True