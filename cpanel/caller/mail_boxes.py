from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "list mail box"):
		if len(args) > 4:
			r = host.dump(lambda: uapi.Email.browse_mailbox(account = args[3], dir = args[4], show_hidden_files = 1))
		if len(args) > 3:
			r = host.dump(lambda: uapi.Email.browse_mailbox(account = args[3], show_hidden_files = 1))
		else:
			r = host.dump(lambda: uapi.Email.browse_mailbox(show_hidden_files = 1))

	return r
