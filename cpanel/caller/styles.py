from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "list style"):
		r = host.dump(lambda: uapi.Styles.list())

	elif cmd_is(cmd, "get style"):
		r = host.dump(lambda: uapi.Styles.current())

	elif cmd_is(cmd, "set style"):
		r = host.check(lambda: uapi.Styles.update(name = args[2], type = 'default'))

	elif cmd_is(cmd, "default style"):
		r = host.check(lambda: uapi.Styles.set_default(name = args[2], type = 'default'))

	return r
