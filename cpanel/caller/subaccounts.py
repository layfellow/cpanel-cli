from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "list subaccount"):
		r = host.dump(lambda: uapi.UserManager.list_users())

	elif cmd_is(cmd, "get subaccount"):
		r = host.dump(lambda: uapi.UserManager.lookup_user(guid = args[2]))

	elif cmd_is(cmd, "get service subaccount"):
		r = host.dump(lambda: uapi.UserManager.lookup_service_account(full_username = args[3], type = args[4]))
		
	elif cmd_is(cmd, "check subaccount conflicts"):
		r = host.dump(lambda: uapi.UserManager.check_account_conflicts(full_username=args[3]))

	return r
