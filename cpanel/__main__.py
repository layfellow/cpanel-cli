import os
import sys
import logging
from logging import Logger
from typing import List
from .cli import eatflag, configuration, version, die, usage
from .core import NullableStr, endpoint
from .dispatcher import dispatch


#  Switch on debugging information if environment variable DEBUG is set to 1.
logging.basicConfig(stream = sys.stderr, level = logging.DEBUG if os.environ.get('DEBUG') else logging.INFO)
log: Logger = logging.getLogger(__name__)

# Force the underlying cpanel_api package to use the same log level as ours.
logging.getLogger('cpanel_api').setLevel(log.getEffectiveLevel())


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
