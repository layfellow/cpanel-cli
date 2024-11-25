from typing import List
from cpanel_api import Api, Result
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "list mail filter"):
		r = host.dump_extracted('filtername', lambda: uapi.Email.list_filters(account = args[3]))

	elif cmd_is(cmd, "count mail filter"):
		r = host.dump(lambda: uapi.Email.count_filters())

	elif cmd_is(cmd, "get mail filter"):
		r = host.dump(lambda: uapi.Email.get_filter(account = args[3], filtername = args[4]))

	elif cmd_is(cmd, "set mail filter"):
		r = host.set_mail_filter(args[3], args[4])

	elif cmd_is(cmd, "enable mail filter"):
		r = host.check(lambda: uapi.Email.enable_filter(account = args[3], filtername = args[4]))

	elif cmd_is(cmd, "disable mail filter"):
		r = host.check(lambda: uapi.Email.disable_filter(account = args[3], filtername = args[4]))

	elif cmd_is(cmd, "delete mail filter", "rm mail filter", "remove mail filter"):
		r = host.check(lambda: uapi.Email.delete_filter(account = args[3], filtername = args[4]))

	elif cmd_is(cmd, "move mail filter"):
		r = host.move_mail_filter(*args[3:])

	elif cmd_is(cmd, "trace mail filter"):
		result: Result = uapi.Email.trace_filter(account = args[3], msg = args[4])
		r = result['data']['trace']

	elif cmd_is(cmd, "list filter domain"):
		r = host.dump(lambda: uapi.Email.list_filters_backups())

	return r
