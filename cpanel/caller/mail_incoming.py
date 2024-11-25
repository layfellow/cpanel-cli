from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "suspend mail incoming"):
		r = host.check(lambda: uapi.Email.suspend_incoming(email = args[3]))
	elif cmd_is(cmd, "unsuspend mail incoming"):
		r = host.check(lambda: uapi.Email.unsuspend_incoming(email = args[3]))

	return r
