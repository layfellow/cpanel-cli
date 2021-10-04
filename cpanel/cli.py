import os
import sys
import textwrap
from configparser import ConfigParser
import logging
from logging import Logger
import cpanel
from typing import List, Mapping, Tuple
from .core import NullableStr, CPanelError


log: Logger = logging.getLogger(__name__)


def die(message: NullableStr = None) -> None:
	"""Print (optional) message and exit to shell with error."""
	if message:
		print("{}: {}".format(cpanel.__name__, message), file = sys.stderr)
	sys.exit(1)


def eatvalue(args: List[str], shortopt: str, longopt: str) -> Tuple[List[str], NullableStr]:
	"""Scan args list looking for a short or long option with a value.

	args       list of arguments passed to the command line
	shortopt   short option, e.g. -x VALUE
	longopt    long option, e.g. --xxx=VALUE

	Returns tuple:
		args with options and VALUE possibly removed,
		VALUE if option is found, None otherwise
	"""
	reargs: List[str] = []
	value: NullableStr = None
	n: int = len(longopt)

	for i in range(0, len(args)):
		# Eat [ ..., '-x', 'xvalue', ... ]
		if args[i] == shortopt and i + 1 < len(args):
			value = args[i + 1]
		# Eat [ ..., '--xxx=xvalue', ... ]
		elif len(args[i]) > n and args[i][0:n + 1] == longopt + '=':
			value = args[i][n + 1:]
		elif i == 0 or args[i - 1] != shortopt:
			reargs.append(args[i])

	return reargs, value


def eatflag(args: List[str], shortopt: str, longopt: str) -> Tuple[List[str], bool]:
	"""Scan args list looking for a short or long flag option.

	args       list of arguments passed to the command line
	shortopt   short flag option, e.g. -x
	longopt    long flag option, e.g. --xxx

	Returns tuple:
		args with options possibly removed,
		True if option is found, False otherwise
	"""
	reargs: List[str] = []
	flag: bool = False

	for arg in args:
		# Eat [ ..., '-x', ... ] or [ ..., '--xxx', ... ]
		if arg == shortopt or arg == longopt:
			flag = True
		else:
			reargs.append(arg)

	return reargs, flag


def configuration(args: List[str], env: Mapping[str, str], rcfile: str) \
		-> Tuple[List[str], NullableStr, NullableStr, NullableStr]:
	"""Return a tuple with credentials to hit the cPanel API.

	args       list of arguments passed to the command line
	env        dict of current environment variables
	rcfile     an .rc properties file, with name=value lines

	Returns tuple:
		args with option values possibly removed,
		hostname,
		username,
		UAPI token associated to username
	"""
	hostname: NullableStr = None
	username: NullableStr = None
	utoken: NullableStr = None

	# Parse optional CLI values (they override both environment variables and the .rc file).
	# I don’t like argparse, manual parsing is much simpler and readable.
	args, hostname = eatvalue(args, '-H', '--hostname')
	args, username = eatvalue(args, '-U', '--username')
	args, utoken = eatvalue(args, '-T', '--utoken')

	# Check environment variables (they override the .rc file).
	if hostname is None: hostname = env.get('CPANEL_HOSTNAME')
	if username is None: username = env.get('CPANEL_USERNAME')
	if utoken is None: utoken = env.get('CPANEL_UTOKEN')

	# Finally, parse the .rc file.
	if os.path.isfile(rcfile):
		config : ConfigParser = ConfigParser()
		with open(rcfile, 'r') as stream:
			config.read_string('[cpanel]\n' + stream.read())
		try:
			if hostname is None: hostname = config['cpanel']['hostname']
			if username is None: username = config['cpanel']['username']
			if utoken is None: utoken = config['cpanel']['utoken']
		except KeyError as e:
			raise CPanelError("missing property in {}, {}".format(rcfile, str(e)))

	return args, hostname, username, utoken


def version() -> str:
	"""Return package version."""
	return "{} client version {}".format(cpanel.__description__, cpanel.__version__)


def usage(cmd: NullableStr = None) -> str:
	help: str

	if cmd == "features":
		help = """\
		Usage: cpanel list features
		"""
	elif cmd == "mail":
		help = """\
		Usage:
		  cpanel list mail accounts
		  cpanel list mail filters ACCOUNT
		  cpanel get mail filter ACCOUNT FILTER_NAME
		  cpanel set mail filter ACCOUNT FILTER_FILE
		  cpanel delete mail filter ACCOUNT FILTER_NAME
		"""
	else:
		help = """\
		Usage: cpanel [OPTIONS] COMMAND...
		"""

	return textwrap.dedent(help)
