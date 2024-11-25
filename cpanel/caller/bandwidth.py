from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "get bandwidth services"):
		r = host.dump(lambda: uapi.Bandwidth.get_enabled_protocols())

	elif cmd_is(cmd, "get bandwidth retention"):
		r = host.dump(lambda: uapi.Bandwidth.get_retention_periods())

	return r
