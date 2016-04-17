import logging
import subprocess

from services.command_service import CommandService
from shell_command.mv_container import MvCommand


class MvService(CommandService):
	"""
	Responsible for handling mv commands for symlinks and their target files.
	"""

	def __init__(self, mv_command, persistence_adapter):
		super().__init__(persistence_adapter)
		self.mv_command = MvCommand(mv_command)

	def execute_mv(self):
		src     = self.mv_command.source
		dest    = self.mv_command.destination

		if _is_symlink(src):
			self.__reregister_symlink(src, dest)
		else:
			self.__reregister_targetfile(src, dest)

		mv_result = subprocess.run(self.mv_command._raw_command,
								   stderr=subprocess.PIPE,
								   universal_newlines=True,
								   shell=True)

		if mv_result.returncode != 0:
			logging.error('Error moving file: ' + mv_result.stderr)
			# TODO revert the change in the db

	def __reregister_symlink(self, src, dest):
		db = self.persistence_adapter

		targetfile = db.targetfile_for_symlink(src)
		if targetfile:
			db.unregister_link(targetfile, src)
			db.register_link(targetfile, dest)


	def __reregister_targetfile(self, src, dest):
		db = self.persistence_adapter

		if db.contains_target_file(src):
			pass
			# TODO


def _is_symlink(filepath):
	return subprocess.run(['test', '-L', filepath]).returncode
