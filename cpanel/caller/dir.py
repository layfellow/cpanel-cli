from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "list dir indexing"):
		r = host.dump(lambda: uapi.DirectoryIndexes.list_directories(dir = args[3]))

	elif cmd_is(cmd, "get dir indexing"):
		r = host.dump(lambda: uapi.DirectoryIndexes.get_indexing(dir = args[3]))

	elif cmd_is(cmd, "set dir indexing"):
		r = host.check(lambda: uapi.DirectoryIndexes.set_indexing(dir = args[3], type = args[4]))

	elif cmd_is(cmd, "list dir privacy"):
		r = host.dump(lambda: uapi.DirectoryPrivacy.list_directories(dir = args[3]))

	elif cmd_is(cmd, "get dir privacy"):
		r = host.dump(lambda: uapi.DirectoryPrivacy.is_directory_protected(dir = args[3]))

	elif cmd_is(cmd, "enable dir privacy"):
		r = host.check(lambda: uapi.DirectoryPrivacy.configure_directory_protection(
			dir = args[3], authname = 'protectandserve', enabled = 1))

	elif cmd_is(cmd, "disable dir privacy"):
		r = host.check(lambda: uapi.DirectoryPrivacy.configure_directory_protection(
			dir = args[3], authname = 'protectandserve', enabled = 0))

	elif cmd_is(cmd, "add dir user"):
		r = host.check(lambda: uapi.DirectoryPrivacy.add_user(
			dir = args[3], user = args[4], password = args[5]))

	elif cmd_is(cmd, "delete dir user", "rm dir user", "remove dir user"):
		r = host.check(lambda: uapi.DirectoryPrivacy.delete_user(dir = args[3], user = args[4]))

	elif cmd_is(cmd, "list dir users"):
		r = host.dump(lambda: uapi.DirectoryPrivacy.list_users(dir = args[3]))

	elif cmd_is(cmd, "list dir protection"):
		r = host.dump(lambda: uapi.DirectoryProtection.list_directories(dir = args[3]))

	return r
