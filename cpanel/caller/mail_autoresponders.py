from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "list mail autoresponder"):
		r = host.dump(lambda: uapi.Email.list_auto_responders(domain = args[3]))

	elif cmd_is(cmd, "count mail autoresponder"):
		r = host.dump(lambda: uapi.Email.count_auto_responders())

	elif cmd_is(cmd, "get mail autoresponder"):
		r = host.dump(lambda: uapi.Email.get_auto_responder(email = args[3]))

	elif cmd_is(cmd, "set mail autoresponder"):
		r = host.set_mail_autoresponder(*args[3:])

	elif cmd_is(cmd, "delete mail autoresponder", "rm mail autoresponder", "remove mail autoresponder"):
		r = host.check(lambda: uapi.Email.delete_auto_responder(email = args[3]))

	return r
