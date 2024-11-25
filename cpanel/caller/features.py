from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "list feature"):
		r = host.dump(lambda: uapi.Features.list_features())

	elif cmd_is(cmd, "get feature detail"):
		r = host.dump(lambda: uapi.Features.get_feature_metadata())

	elif cmd_is(cmd, "has feature"):
		r = host.dump(lambda: uapi.Features.has_feature(name = args[2]))

	return r
