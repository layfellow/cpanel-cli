from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "get log settings"):
		r = host.dump(lambda: uapi.LogManager.get_settings())

	elif cmd_is(cmd, "set log settings"):
		r = host.set_log_settings(1, *args[3:])

	elif cmd_is(cmd, "unset log settings"):
		r = host.set_log_settings(0, *args[3:])

	elif cmd_is(cmd, "list log archives"):
		r = host.dump(lambda: uapi.LogManager.list_archives())

	return r
