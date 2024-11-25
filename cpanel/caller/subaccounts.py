from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "list subaccount"):
		r = host.dump(lambda: uapi.UserManager.list_users())

	elif cmd_is(cmd, "get subaccount"):
		r = host.dump(lambda: uapi.UserManager.lookup_user(guid = args[2]))

	return r
