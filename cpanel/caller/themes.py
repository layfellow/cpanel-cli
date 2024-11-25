from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "list theme"):
		r = host.dump(lambda: uapi.Themes.list(show_mail_themes = 1))

	elif cmd_is(cmd, "get theme"):
		r = host.dump(lambda: uapi.Themes.get_theme_base())

	elif cmd_is(cmd, "set theme"):
		r = host.check(lambda: uapi.Themes.update(theme = args[2]))

	return r
