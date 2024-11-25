from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is, username, domain


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "create ftp"):
		homedir: str = username(args[2]) + '_ftp'
		if len(args) > 5:
			homedir = args[5]
		r = host.check(lambda: uapi.Ftp.add_ftp({
			'user': username(args[2]), 'domain': domain(args[2]),
			'pass': args[3], 'quota': int(args[4]), 'homedir': homedir }))

	elif cmd_is(cmd, "check ftp"):
		r = host.check(lambda: uapi.Ftp.ftp_exists(
			user = username(args[2]), domain = domain(args[2])))

	elif cmd_is(cmd, "get ftp quota"):
		r = host.dump(lambda: uapi.Ftp.get_quota(
			account = username(args[3]), domain = domain(args[3])))

	elif cmd_is(cmd, "get ftp anon"):
		if len(args) > 3 and args[3].lower() == "incoming":
			r = host.dump(lambda: uapi.Ftp.allows_anonymous_ftp_incoming())
		else:
			r = host.dump(lambda: uapi.Ftp.allows_anonymous_ftp())

	elif cmd_is(cmd, "get ftp welcome"):
		r = host.dump(lambda: uapi.Ftp.get_welcome_message())

	elif cmd_is(cmd, "get ftp port"):
		r = host.dump(lambda: uapi.Ftp.get_port())

	elif cmd_is(cmd, "get ftp server"):
		r = host.dump(lambda: uapi.Ftp.get_ftp_daemon_info())

	elif cmd_is(cmd, "get ftp"):
		r = host.dump_selected('login', args[2], lambda: uapi.Ftp.list_ftp_with_disk())

	elif cmd_is(cmd, "set ftp quota"):
		r = host.check(lambda: uapi.Ftp.set_quota(
			user = username(args[3]), domain = domain(args[3]), quota = int(args[4])))

	elif cmd_is(cmd, "set ftp dir"):
		r = host.check(lambda: uapi.Ftp.set_homedir(
			user = username(args[3]), domain = domain(args[3]), homedir = args[4]))

	elif cmd_is(cmd, "set ftp password"):
		r = host.check(lambda: uapi.Ftp.passwd({
			'user': username(args[3]), 'domain': domain(args[3]), 'pass': args[4]}))

	elif cmd_is(cmd, "set ftp welcome"):
		r = host.check(lambda: uapi.Ftp.set_welcome_message(message = args[3]))

	elif cmd_is(cmd, "list ftp account"):
		r = host.dump(lambda: uapi.Ftp.list_ftp_with_disk())

	elif cmd_is(cmd, "list ftp session"):
		r = host.dump(lambda: uapi.Ftp.list_sessions())

	elif cmd_is(cmd, "kill ftp session"):
		if args[3].lower() == "all":
			r = host.check(lambda: uapi.Ftp.kill_session(user = 'all'))
		else:
			r = host.check(lambda: uapi.Ftp.kill_session(user = username(args[3])))

	elif cmd_is(cmd, "delete ftp", "rm ftp", "remove ftp"):
		r = host.check(lambda: uapi.Ftp.delete_ftp(
			user = username(args[2]), domain = domain(args[2]), destroy = 1))

	elif cmd_is(cmd, "enable ftp anon"):
		if len(args) > 3 and args[3].lower() == "incoming":
			r = host.check(lambda: uapi.Ftp.set_anonymous_ftp_incoming(set = 1))
		else:
			r = host.check(lambda: uapi.Ftp.set_anonymous_ftp(set = 1))

	elif cmd_is(cmd, "disable ftp anon"):
		if len(args) > 3 and args[3].lower() == "incoming":
			r = host.check(lambda: uapi.Ftp.set_anonymous_ftp_incoming(set = 0))
		else:
			r = host.check(lambda: uapi.Ftp.set_anonymous_ftp(set = 0))

	return r
