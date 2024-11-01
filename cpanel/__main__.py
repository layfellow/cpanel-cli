import logging
import os
import re
import sys
import json
from logging import Logger
from typing import List
from cpanel_api import Api, Result
import cpanel
from .cli import eatflag, configuration, version, die, usage
from .core import JSONType, NullableStr, CPanelEndpoint, CPanelError, endpoint

#  Switch on debugging information if environment variable DEBUG is set to 1.
logging.basicConfig(stream = sys.stderr, level = logging.DEBUG if os.environ.get('DEBUG') else logging.INFO)
log: Logger = logging.getLogger(__name__)

# Force the underlying cpanel_api package to use the same log level as ours.
logging.getLogger('cpanel_api').setLevel(log.getEffectiveLevel())


def username(email: str) -> str:
	n: int = email.find("@")
	if n < 0:
		raise CPanelError("invalid email, {}".format(email))
	return email[:n]


def domain(email: str) -> str:
	n: int = email.find("@")
	if n < 0:
		raise CPanelError("invalid email, {}".format(email))
	return email[n + 1:]


def dispatch(host: CPanelEndpoint, args: List[str]) -> str:  # type: ignore [reportGeneralTypeIssues]
	"""Make a cPanel API call corresponding to the args.

	host       reference to API endpoint
	args       list of arguments passed to the command line, minus options

	Returns    result data (usually a JSON string)
	"""
	log.debug(str(args))
	cmd: str = " ".join(args[0:4])  # Ignore everything beyond the 4th arg.
	uapi: Api = host.client.uapi

	def cmd_is(command: str, *arglist: str) -> bool:
		for arg in arglist:
			if command[0:len(arg)] == arg:
				return True
		return False

	r: str = ""

	try:
		if cmd_is(cmd, "list feature"):
			r = host.dump(lambda: uapi.Features.list_features())

		elif cmd_is(cmd, "get feature detail"):
			r = host.dump(lambda: uapi.Features.get_feature_metadata())

		elif cmd_is(cmd, "has feature"):
			r = host.dump(lambda: uapi.Features.has_feature(name = args[2]))

		elif cmd_is(cmd, "get quota"):
			r = host.dump(lambda: uapi.Quota.get_quota_info())

		elif cmd_is(cmd, "get usage"):
			r = host.dump(lambda: uapi.ResourceUsage.get_usages())

		elif cmd_is(cmd, "get stat"):
			r = host.dump(lambda: uapi.StatsBar.get_stats(display = "|".join(args[2:])))

		elif cmd_is(cmd, "get ssh port"):
			r = host.dump(lambda: uapi.SSH.get_port())

		elif cmd_is(cmd, "block ip"):
			r = host.check(lambda: uapi.BlockIP.add_ip(ip = args[2]))

		elif cmd_is(cmd, "unblock ip"):
			r = host.check(lambda: uapi.BlockIP.remove_ip(ip = args[2]))

		elif cmd_is(cmd, "list account"):
			r = host.dump(lambda: uapi.Resellers.list_accounts())

		elif cmd_is(cmd, "get account"):
			r = host.dump(lambda: uapi.Variables.get_user_information())

		elif cmd_is(cmd, "list subaccount"):
			r = host.dump(lambda: uapi.UserManager.list_users())

		elif cmd_is(cmd, "get subaccount"):
			r = host.dump(lambda: uapi.UserManager.lookup_user(guid = args[2]))

		elif cmd_is(cmd, "create backup"):
			r = host.create_backup(*args[2:])

		elif cmd_is(cmd, "list backup"):
			r = host.dump(lambda: uapi.Backup.list_backups())

		elif cmd_is(cmd, "restore backup"):
			r = host.check(lambda: uapi.Backup.restore_files(backup = args[2]))

		elif cmd_is(cmd, "update cache"):
			r = host.dump(lambda: uapi.CacheBuster.update())

		elif cmd_is(cmd, "read cache"):
			r = host.dump(lambda: uapi.CacheBuster.read())

		elif cmd_is(cmd, "list locale"):
			r = host.dump(lambda: uapi.Locale.list_locales())

		elif cmd_is(cmd, "get locale"):
			r = host.dump(lambda: uapi.Locale.get_attributes())

		elif cmd_is(cmd, "set locale"):
			r = host.check(lambda: uapi.Locale.set_locale(locale = args[2]))

		elif cmd_is(cmd, "list style"):
			r = host.dump(lambda: uapi.Styles.list())

		elif cmd_is(cmd, "get style"):
			r = host.dump(lambda: uapi.Styles.current())

		elif cmd_is(cmd, "set style"):
			r = host.check(lambda: uapi.Styles.update(name = args[2], type = 'default'))

		elif cmd_is(cmd, "default style"):
			r = host.check(lambda: uapi.Styles.set_default(name = args[2], type = 'default'))

		elif cmd_is(cmd, "list theme"):
			r = host.dump(lambda: uapi.Themes.list(show_mail_themes = 1))

		elif cmd_is(cmd, "get theme"):
			r = host.dump(lambda: uapi.Themes.get_theme_base())

		elif cmd_is(cmd, "set theme"):
			r = host.check(lambda: uapi.Themes.update(theme = args[2]))

		elif cmd_is(cmd, "list dir indexing"):
			r = host.dump(lambda: uapi.DirectoryIndexes.list_directories(dir = args[3]))

		elif cmd_is(cmd, "get dir indexing"):
			r = host.dump(lambda: uapi.DirectoryIndexes.get_indexing(dir = args[3]))

		elif cmd_is(cmd, "set dir indexing"):
			r = host.check(lambda: uapi.DirectoryIndexes.set_indexing(dir = args[3], type = args[4]))

		elif cmd_is(cmd, "list dir privacy"):
			r = host.dump(lambda: uapi.DirectoryPrivacy.list_directories(dir = args[3]))

		elif cmd_is(cmd, "get dir privacy"):
			r = host.dump(lambda: uapi.DirectoryPrivacy.is_directory_protected(dir = args[3]))

		elif cmd_is(cmd, "enable dir privacy"):
			r = host.check(lambda: uapi.DirectoryPrivacy.configure_directory_protection(
				dir = args[3], authname = 'protectandserve', enabled = 1))

		elif cmd_is(cmd, "disable dir privacy"):
			r = host.check(lambda: uapi.DirectoryPrivacy.configure_directory_protection(
				dir = args[3], authname = 'protectandserve', enabled = 0))

		elif cmd_is(cmd, "add dir user"):
			r = host.check(lambda: uapi.DirectoryPrivacy.add_user(
				dir = args[3], user = args[4], password = args[5]))

		elif cmd_is(cmd, "delete dir user", "rm dir user", "remove dir user"):
			r = host.check(lambda: uapi.DirectoryPrivacy.delete_user(dir = args[3], user = args[4]))

		elif cmd_is(cmd, "list dir users"):
			r = host.dump(lambda: uapi.DirectoryPrivacy.list_users(dir = args[3]))

		elif cmd_is(cmd, "list dir protection"):
			r = host.dump(lambda: uapi.DirectoryProtection.list_directories(dir = args[3]))

		elif cmd_is(cmd, "check dns"):
			r = host.dump_null(
				lambda: uapi.DNS.ensure_domains_reside_only_locally(domain = args[2]), args[2])

		elif cmd_is(cmd, "authoritative dns"):
			r = host.dump(lambda: uapi.DNS.has_local_authority(domain = args[2]))

		elif cmd_is(cmd, "lookup dns"):
			r = host.dump(lambda: uapi.DNS.lookup(domain = args[2]))

		elif cmd_is(cmd, "list dynamic dns"):
			r = host.dump(lambda: uapi.DynamicDNS.list())

		elif cmd_is(cmd, "create dynamic dns"):
			if len(args) > 4:
				r = host.dump(lambda: uapi.DynamicDNS.create(domain = args[3], description = args[4]))
			else:
				r = host.dump(lambda: uapi.DynamicDNS.create(domain = args[3]))

		elif cmd_is(cmd, "recreate dynamic dns"):
			r = host.check(lambda: uapi.DynamicDNS.recreate(id = args[3]))

		elif cmd_is(cmd, "update dynamic dns"):
			r = host.check(lambda: uapi.DynamicDNS.set_description(id = args[3], description = args[4]))

		elif cmd_is(cmd, "delete dynamic dns", "rm dynamic dns", "remove dynamic dns"):
			r = host.check(lambda: uapi.DynamicDNS.delete(id = args[3]))

		elif cmd_is(cmd, "list domains"):
			r = host.dump(lambda: uapi.DomainInfo.list_domains())

		elif cmd_is(cmd, "list domain data"):
			r = host.dump(lambda: uapi.DomainInfo.domains_data(
				format = 'hash', return_https_redirects_status = 1))

		elif cmd_is(cmd, "get domain data"):
			r = host.dump(lambda: uapi.DomainInfo.single_domain_data(
				domain = args[3], return_https_redirects_status = 1))

		elif cmd_is(cmd, "get domain aliases"):
			r = host.dump(lambda: uapi.DomainInfo.main_domain_builtin_subdomain_aliases())

		elif cmd_is(cmd, "get log settings"):
			r = host.dump(lambda: uapi.LogManager.get_settings())

		elif cmd_is(cmd, "set log settings"):
			r = host.set_log_settings(1, *args[3:])

		elif cmd_is(cmd, "unset log settings"):
			r = host.set_log_settings(0, *args[3:])

		elif cmd_is(cmd, "list log archives"):
			r = host.dump(lambda: uapi.LogManager.list_archives())

		elif cmd_is(cmd, "get bandwidth services"):
			r = host.dump(lambda: uapi.Bandwidth.get_enabled_protocols())

		elif cmd_is(cmd, "get bandwidth retention"):
			r = host.dump(lambda: uapi.Bandwidth.get_retention_periods())

		elif cmd_is(cmd, "list files"):
			r = host.dump(lambda: uapi.Fileman.list_files(
				dirs = args[2] if len(args) > 2 else '/', include_mime = 1, include_permissions = 1, show_hidden = 1))

		elif cmd_is(cmd, "glob files"):
			r = host.dump(lambda: uapi.Fileman.autocompletedir(path = args[2], html = 0))

		elif cmd_is(cmd, "get file info"):
			r = host.dump(lambda: uapi.Fileman.get_file_information(
				path = args[3], include_mime = 1, include_permissions = 1, show_hidden = 1))

		elif cmd_is(cmd, "cat file"):
			sys.stdout.write(host.get_file_contents(args[2]).decode('utf-8'))

		elif cmd_is(cmd, "write file"):
			r = host.write_file(args[2], args[3])

		elif cmd_is(cmd, "upload file"):
			r = host.upload_file(args[2], args[3])

		elif cmd_is(cmd, "delete file trash", "rm file trash", "remove file trash"):
			r = host.check(lambda: uapi.Fileman.empty_trash(older_than = int(args[3]) if len(args) > 3 else 0))

		elif cmd_is(cmd, "count mail account"):
			r = host.dump(lambda: uapi.Email.count_pops())

		elif cmd_is(cmd, "get mail setting"):
			r = host.dump(lambda: uapi.Email.get_client_settings(account = args[3]))

		elif cmd_is(cmd, "list mail account"):
			r = host.dump_extracted('email', lambda: uapi.Email.list_pops())

		elif cmd_is(cmd, "list mail boxes"):
			if len(args) > 4:
				r = host.dump(lambda: uapi.Email.browse_mailbox(account = args[3], dir = args[4], show_hidden_files = 1))
			if len(args) > 3:
				r = host.dump(lambda: uapi.Email.browse_mailbox(account = args[3], show_hidden_files = 1))
			else:
				r = host.dump(lambda: uapi.Email.browse_mailbox(show_hidden_files = 1))

		elif cmd_is(cmd, "list mail autoresponder"):
			r = host.dump(lambda: uapi.Email.list_auto_responders(domain = args[3]))

		elif cmd_is(cmd, "count mail autoresponder"):
			r = host.dump(lambda: uapi.Email.count_auto_responders())

		elif cmd_is(cmd, "get mail autoresponder"):
			r = host.dump(lambda: uapi.Email.get_auto_responder(email = args[3]))

		elif cmd_is(cmd, "set mail autoresponder"):
			r = host.set_mail_autoresponder(*args[3:])

		elif cmd_is(cmd, "delete mail autoresponder", "rm mail autoresponder", "remove mail autoresponder"):
			r = host.check(lambda: uapi.Email.delete_auto_responder(email = args[3]))

		elif cmd_is(cmd, "add mail forwarder"):
			if args[3].find("@") < 0:
				r = host.check(lambda: uapi.Email.add_domain_forwarder(domain = args[3], destdomain = args[4]))
			else:
				r = host.check(lambda: uapi.Email.add_forwarder(
					domain = domain(args[3]), email = args[3], fwdopt = 'fwd', fwdemail = ','.join(args[4:])))

		elif cmd_is(cmd, "list mail forwarder"):
			if len(args) > 3:
				r = host.dump(lambda: uapi.Email.list_forwarders(domain = args[3]))
			else:
				r = host.dump(lambda: uapi.Email.list_domain_forwarders())

		elif cmd_is(cmd, "count mail forwarder"):
			r = host.dump(lambda: uapi.Email.count_forwarders())

		elif cmd_is(cmd, "delete mail forwarder", "rm mail forwarder", "remove mail forwarder"):
			if args[3].find("@") < 0:
				r = host.check(lambda: uapi.Email.delete_domain_forwarder(domain = args[3]))
			else:
				r = host.check(lambda: uapi.Email.delete_forwarder(
					address = args[3], forwarder = host.get_mail_forwarder(args[3], domain(args[3]))))

		elif cmd_is(cmd, "list mail filter"):
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

		elif cmd_is(cmd, "enable spam assassin"):
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

		elif cmd_is(cmd, "list spam rules"):
			r = host.dump(lambda: uapi.SpamAssassin.get_symbolic_test_names())

		elif cmd_is(cmd, "set spam rule score"):
			r = host.check(lambda: uapi.SpamAssassin.update_user_preference(
				preference = 'score', value = f'{args[4]} {args[5]}'))

		elif cmd_is(cmd, "get mail quota"):
			if args[3].lower() == "default":
				r = host.dump(lambda: uapi.Email.get_default_email_quota_mib())
			elif args[3].lower() == "max":
				r = host.dump(lambda: uapi.Email.get_max_email_quota_mib())
			else:
				r = host.dump(lambda: uapi.Email.get_pop_quota(email = args[3]))

		elif cmd_is(cmd, "set mail quota"):
			r = host.check(lambda: uapi.Email.edit_pop_quota(
				email = username(args[3]), domain = domain(args[3]), quota = args[4]))

		elif cmd_is(cmd, "get mail usage"):
			r = host.dump(lambda: uapi.Email.get_disk_usage(
				user = username(args[3]), domain = domain(args[3])))

		elif cmd_is(cmd, "get webmail setting"):
			if len(args) > 3:
				r = host.dump(lambda: uapi.Email.get_webmail_settings(account = args[3]))
			else:
				r = host.dump(lambda: uapi.Email.get_webmail_settings())

		elif cmd_is(cmd, "list webmail app"):
			r = host.dump(lambda: uapi.WebmailApps.list_webmail_apps())

		elif cmd_is(cmd, "add mailman list"):
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

		elif cmd_is(cmd, "create ftp"):
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

		elif cmd_is(cmd, "create mysql user"):
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

		elif cmd_is(cmd, "create postgres user"):
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

		else:
			die("unrecognized command, {}".format(cmd))

	except IndexError:
		if len(args) > 1:
			die("missing arguments for {}, please use ‘cpanel help {}’".format(cmd, args[1]))
		else:
			die("missing arguments for {}, please use ‘cpanel --help’".format(cmd))

	except Exception as e:
		# Re-throw exception raised during API call.
		raise e
	return r


def main() -> None:
	hostname: NullableStr
	user: NullableStr
	utoken: NullableStr

	_help: bool
	_version: bool

	try:
		args: List[str] = sys.argv[1:]

		# Parse options (I don’t like argparse, manual parsing is much simpler and readable.)
		args, _help = eatflag(args, '-h', '--help')
		args, _version = eatflag(args, '-V', '--version')

		if _version:
			print(version())
		elif len(args) < 1:
			print(usage())
		elif _help:
			print(usage(*args[1:]))
		elif args[0] == 'version':
			print(version())
		elif args[0] == 'help':
			if len(args) < 2:
				print(usage())
			else:
				print(usage(*args[1:]))
		else:
			args, hostname, user, utoken = configuration(args, os.environ)
			if hostname is None:
				die("missing cPanel hostname, use cpanel --help")
			if user is None:
				die("missing cPanel username, use cpanel --help")
			if utoken is None:
				die("missing cPanel UAPI token, use cpanel --help")

			log.debug("hostname: {}, username: {}, utoken: {}".format(hostname, user, utoken))

			r: str = dispatch(endpoint(str(hostname), str(user), str(utoken)), args)
			if len(r) > 0:
				print(r)

	except Exception as e:
		if log.isEnabledFor(logging.DEBUG):
			raise e
		else:
			die(str(e))


if __name__ == '__main__':
	main()
