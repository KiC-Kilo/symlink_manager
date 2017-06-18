import os
import subprocess
from abc import ABCMeta


class ShellCommand(metaclass=ABCMeta):

	def __init__(self, command: list):
		self.raw_command = command


	def full_command(self):
		full_command = ''
		for string in self.raw_command:
			full_command += string + ' '

		return full_command

	def _canonicalize_path(self, path: str) -> str:
		if path[0] == '~':
			path = os.path.join(self.__get_user_home_dir(), path[2:])
		elif path[0] != '/':
			path = os.path.abspath(path)

		return path

	@staticmethod
	def __get_user_home_dir():
		"""
		This assumes the user has the standard home configuration of their home directory being
		equivalent to /home/<user>, and has the whoami utility installed.
		:return: Returns the user's home directory.
		"""
		# TODO move this and other directory-related methods to a directory utility or service?
		result = subprocess.run('whoami',
								stdout=subprocess.PIPE,
								stderr=subprocess.PIPE,
								shell=True,
								universal_newlines=True)
		err = result.stderr
		if err:
			raise Exception('Error resolving home directory for current user: ' + err)

		whoami = result.stdout.strip()
		if whoami == 'root':
			user_dir = '/root'
		else:
			user_dir = '/home/' + whoami

		return user_dir
