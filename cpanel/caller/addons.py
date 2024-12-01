from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "list addon instance"):
		r = host.dump(lambda: uapi.cPAddons.list_addon_instances(addon = args[3]))

	elif cmd_is(cmd, "list addon"):
		r = host.dump(lambda: uapi.cPAddons.get_available_addons())

	elif cmd_is(cmd, "get addon instance"):
		r = host.dump(lambda: uapi.cPAddons.list_addon_instances(unique_id = args[3]))

	return r
