from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "suspend mail login"):
		r = host.check(lambda: uapi.Email.suspend_login(email = args[3]))
	elif cmd_is(cmd, "unsuspend mail login"):
		r = host.check(lambda: uapi.Email.unsuspend_login(email = args[3]))
	return r
