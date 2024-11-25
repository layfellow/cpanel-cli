import json
from typing import List
from cpanel_api import Api, Result
from ..core import CPanelEndpoint, CPanelError
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "list stats domain"):
		result: Result = uapi.Stats.list_sites(engine='webalizer', traffic='http')
		domains = [datum['domain'] for datum in result['data']]
		r = json.dumps(domains, indent=4, sort_keys=True)

	elif cmd_is(cmd, "get stats bandwidth"):
		r = host.dump(lambda: uapi.Stats.get_bandwidth())

	elif cmd_is(cmd, "get stats domain"):
		domain = args[3]
		engine = args[4] if len(args) > 4 else 'webalizer'
		traffic = args[5] if len(args) > 5 else 'http'

		result: Result = uapi.Stats.list_sites(engine = engine, traffic = traffic)
		path = None
		for datum in result['data']:
			if datum['domain'] == domain:
				path = datum['path']
		if path is not None:
			names = path.split('/')
			# HACK Remove the username from the path.
			path = '/'.join(names[1:2]) + '/' + '/'.join(names[3:])
			r = host.get_file_contents(path).decode('utf-8')
		else:
			raise CPanelError("domain not found")

	elif cmd_is(cmd, "get stats"):
		r = host.dump(lambda: uapi.StatsBar.get_stats(display = "|".join(args[2:])))

	return r
