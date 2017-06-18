import logging
import subprocess

import os

from symmv.persistence.persistence_adapter import PersistenceAdapter
from symmv.services.command_service import CommandService
from symmv.shell_command.mv_container import MvCommand


class MvService(CommandService):
	"""
	Responsible for handling mv commands for symlinks and their target files.
	"""

	def __init__(self, mv_command: list, persistence_adapter: PersistenceAdapter):
		super().__init__(persistence_adapter)
		self.mv_command = MvCommand(mv_command)

	def execute_mv(self):
		src     = self.mv_command.source
		dest    = self.mv_command.destination

		if _is_symlink(src):
			self.__reregister_symlink(src, dest)
		else:
			self.__reregister_target_file(src, dest)

		mv_result = subprocess.run(self.mv_command.raw_command,
								   stderr=subprocess.PIPE,
								   universal_newlines=True,
								   shell=True)
		if mv_result.returncode:
			logging.error('Error moving file: ' + mv_result.stderr)
			self.persistence_adapter.rollback()
		else:
			self.persistence_adapter.commit()

	def __reregister_symlink(self, src, dest):
		persistence = self.persistence_adapter

		targetfile = persistence.targetfile_for_symlink(src)
		if targetfile:
			persistence.unregister_link(targetfile, src)
			persistence.register_link(targetfile, dest)

	def __reregister_target_file(self, src, dest):
		persistence = self.persistence_adapter

		if persistence.contains_target_file(src):
			persistence.reregister_target_file(src, dest)	# TODO standardize, targetfile or target_file

		else:
			pass


def _is_symlink(filepath):
	return os.path.islink(filepath)
