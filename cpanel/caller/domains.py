from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "list domain data"):
		r = host.dump(lambda: uapi.DomainInfo.domains_data(
			format = 'hash', return_https_redirects_status = 1))

	elif cmd_is(cmd, "list domain"):
		r = host.dump(lambda: uapi.DomainInfo.list_domains())

	elif cmd_is(cmd, "get domain data"):
		r = host.dump(lambda: uapi.DomainInfo.single_domain_data(
			domain = args[3], return_https_redirects_status = 1))

	elif cmd_is(cmd, "get domain aliases"):
		r = host.dump(lambda: uapi.DomainInfo.main_domain_builtin_subdomain_aliases())

	return r
