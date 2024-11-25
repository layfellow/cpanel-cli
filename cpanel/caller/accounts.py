from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "list account"):
		r = host.dump(lambda: uapi.Resellers.list_accounts())

	elif cmd_is(cmd, "get account"):
		r = host.dump(lambda: uapi.Variables.get_user_information())

	return r
