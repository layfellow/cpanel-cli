from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "list locale"):
		r = host.dump(lambda: uapi.Locale.list_locales())

	elif cmd_is(cmd, "get locale"):
		r = host.dump(lambda: uapi.Locale.get_attributes())

	elif cmd_is(cmd, "set locale"):
		r = host.check(lambda: uapi.Locale.set_locale(locale = args[2]))

	return r
