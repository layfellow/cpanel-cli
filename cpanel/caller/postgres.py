from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "create postgres user"):
		r = host.check(lambda: uapi.Postgresql.create_user(name = args[3], password = args[4]))

	elif cmd_is(cmd, "list postgres user"):
		r = host.dump(lambda: uapi.Postgresql.list_users())

	elif cmd_is(cmd, "rename postgres user"):
		r = host.check(lambda: uapi.Postgresql.rename_user(oldname = args[3], newname = args[4], password = args[5]))

	elif cmd_is(cmd, "set postgres password"):
		r = host.check(lambda: uapi.Postgresql.set_password(user = args[3], password = args[4]))

	elif cmd_is(cmd, "delete postgres user", "rm postgres user", "remove postgres user"):
		r = host.check(lambda: uapi.Postgresql.delete_user(name = args[3]))

	elif cmd_is(cmd, "create postgres database"):
		r = host.check(lambda: uapi.Postgresql.create_database(name = args[3]))

	elif cmd_is(cmd, "list postgres database"):
		r = host.dump(lambda: uapi.Postgresql.list_databases())

	elif cmd_is(cmd, "rename postgres database"):
		r = host.check(lambda: uapi.Postgresql.rename_database(oldname = args[3], newname = args[4]))

	elif cmd_is(cmd, "delete postgres database", "rm postgres database", "remove postgres database"):
		r = host.check(lambda: uapi.Postgresql.delete_database(name = args[3]))

	elif cmd_is(cmd, "set postgres privilege"):
		r = host.check(lambda: uapi.Postgresql.grant_all_privileges(user = args[3], database = args[4]))

	elif cmd_is(cmd, "delete postgres privilege", "rm postgres privilege", "remove postgres privilege"):
		r = host.check(lambda: uapi.Postgresql.revoke_all_privileges(user = args[3], database = args[4]))

	elif cmd_is(cmd, "sync postgres grant"):
		r = host.check(lambda: uapi.Postgresql.update_privileges())

	elif cmd_is(cmd, "get postgres restriction"):
		r = host.dump(lambda: uapi.Postgresql.get_restrictions())

	return r
