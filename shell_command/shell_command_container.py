import os
import subprocess
from abc import ABCMeta


class ShellCommand(metaclass=ABCMeta):

	def __init__(self, command):
		assert isinstance(command, list)
		self._raw_command = command


	def full_command(self):
		full_command = ''
		for string in self._raw_command:
			full_command += string + ' '

		return full_command

	def _canonicalize_path(self, path):
		if path[0] == '~':
			path = os.path.join(self.__get_user_home_dir(), path[2:])
		elif path[0] != '/':
			path = os.path.abspath(path)

		return path

	def __get_user_home_dir(self):
		result = subprocess.run('whoami',
								stdout=subprocess.PIPE,
								stderr=subprocess.PIPE,
								shell=True,
								universal_newlines=True)
		err = result.stderr
		whoami = result.stdout.strip()

		if err:
			raise Exception('Error resolving home directory for current user: ' + err)

		if whoami == 'root':
			user_dir = '/root'
		else:
			user_dir = '/home/' + whoami

		return user_dir