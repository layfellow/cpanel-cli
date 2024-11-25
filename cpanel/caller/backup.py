from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "create backup"):
		r = host.create_backup(*args[2:])

	elif cmd_is(cmd, "list backup"):
		r = host.dump(lambda: uapi.Backup.list_backups())

	elif cmd_is(cmd, "restore backup"):
		r = host.check(lambda: uapi.Backup.restore_files(backup = args[2]))

	return r
