from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is, domain


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "add mail forwarder"):
		if args[3].find("@") < 0:
			r = host.check(lambda: uapi.Email.add_domain_forwarder(domain = args[3], destdomain = args[4]))
		else:
			r = host.check(lambda: uapi.Email.add_forwarder(
				domain = domain(args[3]), email = args[3], fwdopt ='fwd', fwdemail =','.join(args[4:])))

	elif cmd_is(cmd, "list mail forwarder"):
		if len(args) > 3:
			r = host.dump(lambda: uapi.Email.list_forwarders(domain = args[3]))
		else:
			r = host.dump(lambda: uapi.Email.list_domain_forwarders())

	elif cmd_is(cmd, "count mail forwarder"):
		r = host.dump(lambda: uapi.Email.count_forwarders())

	elif cmd_is(cmd, "delete mail forwarder", "rm mail forwarder", "remove mail forwarder"):
		if args[3].find("@") < 0:
			r = host.check(lambda: uapi.Email.delete_domain_forwarder(domain = args[3]))
		else:
			r = host.check(lambda: uapi.Email.delete_forwarder(
				address = args[3], forwarder = host.get_mail_forwarder(args[3], domain(args[3]))))

	return r
