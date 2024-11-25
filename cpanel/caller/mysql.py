import re
from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "create mysql user"):
		r = host.check(lambda: uapi.Mysql.create_user(name = args[3], password = args[4]))

	elif cmd_is(cmd, "list mysql user"):
		r = host.dump(lambda: uapi.Mysql.list_users())

	elif cmd_is(cmd, "rename mysql user"):
		r = host.check(lambda: uapi.Mysql.rename_user(oldname = args[3], newname = args[4]))

	elif cmd_is(cmd, "set mysql password"):
		r = host.check(lambda: uapi.Mysql.set_password(user = args[3], password = args[4]))

	elif cmd_is(cmd, "delete mysql user", "rm mysql user", "remove mysql user"):
		r = host.check(lambda: uapi.Mysql.delete_user(name = args[3]))

	elif cmd_is(cmd, "create mysql database"):
		r = host.check(lambda: uapi.Mysql.create_database(name = args[3]))

	elif cmd_is(cmd, "list mysql database"):
		r = host.dump(lambda: uapi.Mysql.list_databases())

	elif cmd_is(cmd, "rename mysql database"):
		r = host.check(lambda: uapi.Mysql.rename_database(oldname = args[3], newname = args[4]))

	elif cmd_is(cmd, "delete mysql database", "rm mysql database", "remove mysql database"):
		r = host.check(lambda: uapi.Mysql.delete_database(name = args[3]))

	elif cmd_is(cmd, "check mysql database"):
		r = host.dump(lambda: uapi.Mysql.check_database(name = args[3]))

	elif cmd_is(cmd, "repair mysql database"):
		r = host.dump(lambda: uapi.Mysql.repair_database(name = args[3]))

	elif cmd_is(cmd, "set mysql privilege"):
		privileges: str = re.sub(r'\s*,\s*', ",", ",".join(args[5:])).replace("_", " ").upper()
		r = host.check(lambda: uapi.Mysql.set_privileges_on_database(
			user = args[3], database = args[4], privileges = privileges))

	elif cmd_is(cmd, "list mysql privilege"):
		r = host.dump(lambda: uapi.Mysql.get_privileges_on_database(user = args[3], database = args[4]))

	elif cmd_is(cmd, "delete mysql privilege", "rm mysql privilege", "remove mysql privilege"):
		r = host.check(lambda: uapi.Mysql.revoke_access_to_database(user = args[3], database = args[4]))

	elif cmd_is(cmd, "list mysql routine"):
		if len(args) > 3:
			r = host.dump(lambda: uapi.Mysql.list_routines(database_user = args[3]))
		else:
			r = host.dump(lambda: uapi.Mysql.list_routines())

	elif cmd_is(cmd, "get mysql schema"):
		r = host.dump(lambda: uapi.Mysql.dump_database_schema(dbname = args[3]))
		if len(r) > 1:
			r = bytes(r, "utf-8").decode("unicode_escape")[1:-1]

	elif cmd_is(cmd, "add mysql host"):
		note: str = "Authorized host"
		if len(args) > 4:
			note = args[4]
		host.check(lambda: uapi.Mysql.add_host(host = args[3]))
		r = host.check(lambda: uapi.Mysql.add_host_note(host = args[3], note = note))

	elif cmd_is(cmd, "annotate mysql host"):
		r = host.check(lambda: uapi.Mysql.add_host_note(host = args[3], note = args[4]))

	elif cmd_is(cmd, "list mysql host"):
		r = host.dump(lambda: uapi.Mysql.get_host_notes())

	elif cmd_is(cmd, "delete mysql host", "rm mysql host", "remove mysql host"):
		r = host.check(lambda: uapi.Mysql.delete_host(host = args[3]))

	elif cmd_is(cmd, "get mysql server"):
		r = host.dump(lambda: uapi.Mysql.get_server_information())

	elif cmd_is(cmd, "get mysql restriction"):
		r = host.dump(lambda: uapi.Mysql.get_restrictions())

	return r
