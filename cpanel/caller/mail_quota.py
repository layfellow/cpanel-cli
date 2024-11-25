from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is, username, domain


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "get mail quota"):
		if args[3].lower() == "default":
			r = host.dump(lambda: uapi.Email.get_default_email_quota_mib())
		elif args[3].lower() == "max":
			r = host.dump(lambda: uapi.Email.get_max_email_quota_mib())
		else:
			r = host.dump(lambda: uapi.Email.get_pop_quota(email = args[3]))

	elif cmd_is(cmd, "set mail quota"):
		r = host.check(lambda: uapi.Email.edit_pop_quota(
			email = username(args[3]), domain = domain(args[3]), quota = args[4]))

	return r
