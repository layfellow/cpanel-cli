from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "get webmail setting"):
		if len(args) > 3:
			r = host.dump(lambda: uapi.Email.get_webmail_settings(account = args[3]))
		else:
			r = host.dump(lambda: uapi.Email.get_webmail_settings())

	elif cmd_is(cmd, "list webmail app"):
		r = host.dump(lambda: uapi.WebmailApps.list_webmail_apps())

	return r
