from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is, username, domain


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "add mailman list"):
		private: int = 1 if len(args) > 5 and args[5].lower() == "private" else 0
		r = host.check(lambda: uapi.Email.add_list(
			domain = domain(args[3]), list = username(args[3]), password = args[4], private = private))

	elif cmd_is(cmd, "delete mailman list"):
		r = host.check(lambda: uapi.Email.delete_list(list = args[3]))

	elif cmd_is(cmd, "count mailman list"):
		r = host.dump(lambda: uapi.Email.count_lists())

	elif cmd_is(cmd, "list mailman list"):
		r = host.dump(lambda: uapi.Email.list_lists())

	elif cmd_is(cmd, "add mailman delegate"):
		r = host.check(lambda: uapi.Email.add_mailman_delegates(list = args[3], delegates = ','.join(args[4:])))

	elif cmd_is(cmd, "delete mailman delegate", "rm mailman delegate", "remove mailman delegate"):
		r = host.check(lambda: uapi.Email.remove_mailman_delegates(list = args[3], delegates = ','.join(args[4:])))

	elif cmd_is(cmd, "list mailman delegate"):
		r = host.dump(lambda: uapi.Email.get_mailman_delegates(list= args[3]))

	elif cmd_is(cmd, "check mailman delegate"):
		r = host.dump(lambda: uapi.Email.has_delegated_mailman_lists(delegate = args[3]))

	elif cmd_is(cmd, "generate mailman password"):
		r = host.dump(lambda: uapi.Email.generate_mailman_otp(list = args[3]))

	elif cmd_is(cmd, "set mailman password"):
		r = host.check(lambda: uapi.Email.passwd_list(list = args[3], password = args[4]))

	elif cmd_is(cmd, "get mailman usage"):
		r = host.dump(lambda: uapi.Email.get_lists_total_disk_usage())

	elif cmd_is(cmd, "set mailman private"):
		r = host.check(lambda: uapi.Email.set_list_privacy_options(
			list = args[3], advertised = 0, archive_private = 1, subscribe_policy = 3))

	elif cmd_is(cmd, "set mailman public"):
		r = host.check(lambda: uapi.Email.set_list_privacy_options(
			list = args[3], advertised = 1, archive_private = 0, subscribe_policy = 1))

	return r
