import logging
import os
import sys
from logging import Logger
from typing import List
from cpanel_api import Api
import cpanel
from .cli import eatflag, configuration, version, die, usage
from .core import NullableStr, CPanelEndpoint, CPanelError, endpoint

HOME: NullableStr = os.environ.get('HOME')
RCFILE: str = (HOME + '/' if HOME else '') + '.' + cpanel.__name__ + 'rc'

#  Switch on debugging information if enviroment variable DEBUG is set to 1.
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


def dispatch(host: CPanelEndpoint, args: List[str]) -> str:
	"""Make a cPanel API call corresponding to the args.

	host       reference to API endpoint
	args       list of arguments passed to the command line, minus options

	Returns    result data (usually a JSON string)
	"""
	log.debug(str(args))
	cmd: str = " ".join(args[0:3])  # Ignore everything beyond the 3rd arg.
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

		elif cmd_is(cmd, "delete mysql user", "rm delete mysql user", "remove mysql user"):
			r = host.check(lambda: uapi.Mysql.delete_user(name = args[3]))

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
			args, hostname, user, utoken = configuration(args, os.environ, RCFILE)
			if hostname is None:
				die("missing cPanel hostname, use cpanel --help")
			if user is None:
				die("missing cPanel username, use cpanel --help")
			if utoken is None:
				die("missing cPanel UAPI token, use cpanel --help")

			log.debug("hostname: {}, username: {}, utoken: {}".format(hostname, user, utoken))

			r: str = dispatch(endpoint(hostname, user, utoken), args)
			if len(r) > 0:
				print(r)

	except Exception as e:
		if log.isEnabledFor(logging.DEBUG):
			raise e
		else:
			die(str(e))


if __name__ == '__main__':
	main()
