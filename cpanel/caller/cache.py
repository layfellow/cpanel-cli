from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "update cache"):
		r = host.dump(lambda: uapi.CacheBuster.update())

	elif cmd_is(cmd, "read cache"):
		r = host.dump(lambda: uapi.CacheBuster.read())

	return r
