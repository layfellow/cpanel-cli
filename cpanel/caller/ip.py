from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "block ip"):
		r = host.check(lambda: uapi.BlockIP.add_ip(ip = args[2]))

	elif cmd_is(cmd, "unblock ip"):
		r = host.check(lambda: uapi.BlockIP.remove_ip(ip = args[2]))

	return r
