from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "check dns"):
		r = host.dump_null(
			lambda: uapi.DNS.ensure_domains_reside_only_locally(domain = args[2]), args[2])

	elif cmd_is(cmd, "authoritative dns"):
		r = host.dump(lambda: uapi.DNS.has_local_authority(domain = args[2]))

	elif cmd_is(cmd, "lookup dns"):
		r = host.dump(lambda: uapi.DNS.lookup(domain = args[2]))

	elif cmd_is(cmd, "list dynamic dns"):
		r = host.dump(lambda: uapi.DynamicDNS.list())

	elif cmd_is(cmd, "create dynamic dns"):
		if len(args) > 4:
			r = host.dump(lambda: uapi.DynamicDNS.create(domain = args[3], description = args[4]))
		else:
			r = host.dump(lambda: uapi.DynamicDNS.create(domain = args[3]))

	elif cmd_is(cmd, "recreate dynamic dns"):
		r = host.check(lambda: uapi.DynamicDNS.recreate(id = args[3]))

	elif cmd_is(cmd, "update dynamic dns"):
		r = host.check(lambda: uapi.DynamicDNS.set_description(id = args[3], description = args[4]))

	elif cmd_is(cmd, "delete dynamic dns", "rm dynamic dns", "remove dynamic dns"):
		r = host.check(lambda: uapi.DynamicDNS.delete(id = args[3]))

	return r
