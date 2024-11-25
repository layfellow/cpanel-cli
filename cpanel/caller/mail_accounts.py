from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "count mail account"):
		r = host.dump(lambda: uapi.Email.count_pops())

	elif cmd_is(cmd, "list mail account"):
		r = host.dump_extracted('email', lambda: uapi.Email.list_pops())

	return r
