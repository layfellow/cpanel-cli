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

	r: str = ""
	try:
		if cmd == "list features":
			r = host.dump(lambda: uapi.Features.list_features())

		elif cmd == "list mail accounts":
			r = host.dump_extracted('email', lambda: uapi.Email.list_pops())

		elif cmd == "list mail filters":
			r = host.dump_extracted('filtername', lambda: uapi.Email.list_filters(account = args[3]))

		elif cmd == "get mail filter":
			r = host.dump(lambda: uapi.Email.get_filter(account = args[3], filtername = args[4]))

		elif cmd == "set mail filter":
			r = host.set_mail_filter(args[3], args[4])

		elif cmd in ("delete mail filter", "rm mail filter" , "remove mail filter"):
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
				print(usage(args[1]))
		else:
			args, hostname, username, utoken = configuration(args, os.environ, RCFILE)
			if hostname is None: die("missing cPanel hostname, use cpanel --help")
			if username is None: die("missing cPanel username, use cpanel --help")
			if utoken is None: die("missing cPanel UAPI token, use cpanel --help")
			log.debug("hostname: {}, username: {}, utoken: {}".format(hostname, username, utoken))

			print(dispatch(endpoint(hostname, username, utoken), args))

	except Exception as e:
		if log.isEnabledFor(logging.DEBUG):
			raise e
		else:
			die(str(e))


if __name__ == '__main__':
	main()
