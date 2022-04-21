import sys
import os
import logging
from logging import Logger
import cpanel
from cpanel_api import Api
from typing import cast, List, Dict, Callable
from .cli import eatflag, configuration, version, die, usage
from .core import NullableStr, CPanelEndpoint, CPanelError, endpoint

HOME: NullableStr = os.environ.get('HOME')
RCFILE: str = (HOME + '/' if HOME else '') + '.' + cpanel.__name__ + 'rc'

#  Switch on debugging information if enviroment variable DEBUG is set to 1.
logging.basicConfig(stream = sys.stderr, level = logging.DEBUG if os.environ.get('DEBUG') else logging.INFO)
log: Logger = logging.getLogger(__name__)

# Force the underlying cpanel_api package to use the same log level as ours.
logging.getLogger('cpanel_api').setLevel(log.getEffectiveLevel())


def dispatch(host: CPanelEndpoint, args: List[str]) -> str:
	"""Make a cPanel API call corresponding to the args.

	host       reference to API endpoint
	args       list of arguments passed to the command line, minus options

	Returns    result data (usually a JSON string)
	"""
	log.debug(str(args))
	cmd: str = " ".join(args[0:3])  # Ignore everything beyond the 3rd arg.
	uapi: Api = host.client.uapi

	def cmd_is(cmd: str, *args: str) -> bool:
		for arg in args:
			if cmd[0:len(arg)] == arg:
				return True
		return False

	r: str = ""

	try:
		if cmd_is(cmd, "list feature"):
			r = host.dump(lambda: uapi.Features.list_features())

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

		elif cmd_is(cmd, "list mail account"):
			r = host.dump_extracted('email', lambda: uapi.Email.list_pops())

		elif cmd_is(cmd, "list mail filter"):
			r = host.dump_extracted('filtername', lambda: uapi.Email.list_filters(account = args[3]))

		elif cmd_is(cmd, "get mail filter"):
			r = host.dump(lambda: uapi.Email.get_filter(account = args[3], filtername = args[4]))

		elif cmd_is(cmd, "set mail filter"):
			r = host.set_mail_filter(args[3], args[4])

		elif cmd_is(cmd, "delete mail filter", "rm mail filter", "remove mail filter"):
			r = host.check(lambda: uapi.Email.delete_filter(account = args[3], filtername = args[4]))

		else:
			die("unrecognized command, {}".format(cmd))
	except IndexError:
		die("missing arguments for {}".format(cmd))
	except Exception as e:
		# Re-throw exception raised during API call.
		raise e
	return r


def main() -> None:
	hostname: NullableStr
	username: NullableStr
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
			print(usage(args[0]))
		elif args[0] == 'version':
			print(version())
		elif args[0] == 'help':
			if len(args) < 2:
				print(usage())
			else:
				if 'dir' in args[1]:
					args[1] = 'dir'
				print(usage(args[1]))
		else:
			args, hostname, username, utoken = configuration(args, os.environ, RCFILE)
			if hostname is None: die("missing cPanel hostname, use cpanel --help")
			if username is None: die("missing cPanel username, use cpanel --help")
			if utoken is None: die("missing cPanel UAPI token, use cpanel --help")
			log.debug("hostname: {}, username: {}, utoken: {}".format(hostname, username, utoken))

			r: str = dispatch(endpoint(hostname, username, utoken), args)
			if len(r) > 0:
				print(r)

	except Exception as e:
		if log.isEnabledFor(logging.DEBUG):
			raise e
		else:
			die(str(e))


if __name__ == '__main__':
	main()
