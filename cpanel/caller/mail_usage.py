from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is, username, domain


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "get mail usage"):
		r = host.dump(lambda: uapi.Email.get_disk_usage(
			user = username(args[3]), domain = domain(args[3])))

	return r
