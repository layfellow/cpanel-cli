import json
from typing import List
from cpanel_api import Api, Result
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "enable spam assassin"):
		r = host.check(lambda: uapi.Email.enable_spam_assassin())

	elif cmd_is(cmd, "disable spam assassin"):
		r = host.check(lambda: uapi.Email.disable_spam_assassin())

	elif cmd_is(cmd, "enable spam box"):
		r = host.check(lambda: uapi.Email.enable_spam_box())

	elif cmd_is(cmd, "clear spam box"):
		r = host.check(lambda: uapi.SpamAssassin.clear_spam_box())

	elif cmd_is(cmd, "disable spam box"):
		r = host.check(lambda: uapi.Email.disable_spam_box())

	elif cmd_is(cmd, "get spam settings"):
		settings: Result = uapi.Email.get_spam_settings()
		preferences: Result = uapi.SpamAssassin.get_user_preferences()
		r = json.dumps({**settings['data'], **preferences['data']}, indent = 4, sort_keys = False)

	elif cmd_is(cmd, "set spam score"):
		r = host.check(lambda: uapi.SpamAssassin.update_user_preference(
			preference = 'required_score', value = args[3]))

	elif cmd_is(cmd, "add spam denylist"):
		r = host.update_spam_list(True, 'blacklist_from', *args[3:])

	elif cmd_is(cmd, "delete spam denylist", "rm spam denylist", "remove spam denylist"):
		r = host.update_spam_list(False, 'blacklist_from', *args[3:])

	elif cmd_is(cmd, "add spam allowlist"):
		r = host.update_spam_list(True, 'whitelist_from', *args[3:])

	elif cmd_is(cmd, "delete spam allowlist", "rm spam allowlist", "remove spam allowlist"):
		r = host.update_spam_list(False, 'whitelist_from', *args[3:])

	elif cmd_is(cmd, "set spam autodelete score"):
		r = host.check(lambda: uapi.Email.add_spam_filter(required_score = args[4]))

	elif cmd_is(cmd, "disable spam autodelete"):
		r = host.check(lambda: uapi.Email.disable_spam_autodelete())

	elif cmd_is(cmd, "list spam rule"):
		r = host.dump(lambda: uapi.SpamAssassin.get_symbolic_test_names())

	elif cmd_is(cmd, "set spam rule score"):
		r = host.check(lambda: uapi.SpamAssassin.update_user_preference(
			preference = 'score', value = f'{args[4]} {args[5]}'))

	return r
