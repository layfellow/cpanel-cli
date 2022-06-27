import os
import sys
import re
import pkgutil
from configparser import ConfigParser
import logging
from logging import Logger
import cpanel
from typing import List, Mapping, Tuple, Match, Union
from .core import NullableStr, NullableBytes, CPanelError

NullableMatch = Union[Match[str], None]

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
	hostname: NullableStr
	username: NullableStr
	utoken: NullableStr

	# Parse optional CLI values (they override both environment variables and the .rc file).
	# I don’t like argparse, manual parsing is much simpler and readable.
	args, hostname = eatvalue(args, '-H', '--hostname')
	args, username = eatvalue(args, '-U', '--username')
	args, utoken = eatvalue(args, '-T', '--utoken')

	# Check environment variables (they override the .rc file).
	if hostname is None:
		hostname = env.get('CPANEL_HOSTNAME')
	if username is None:
		username = env.get('CPANEL_USERNAME')
	if utoken is None:
		utoken = env.get('CPANEL_UTOKEN')

	# Finally, parse the .rc file.
	if os.path.isfile(rcfile):
		config: ConfigParser = ConfigParser()
		with open(rcfile, 'r') as stream:
			config.read_string('[cpanel]\n' + stream.read())
		try:
			if hostname is None:
				hostname = config['cpanel']['hostname']
			if username is None:
				username = config['cpanel']['username']
			if utoken is None:
				utoken = config['cpanel']['utoken']
		except KeyError as e:
			raise CPanelError("missing property in {}, {}".format(rcfile, str(e)))

	return args, hostname, username, utoken


def version() -> str:
	"""Return package version."""
	return "{} client version {}".format(cpanel.__description__, cpanel.__version__)


def usage(*args: str) -> str:
	"""Return usage string depending on help arguments.

	args arguments after `cpanel help`

	Return multiline string with usage description
	"""

	def is_usage(*arglist: str) -> bool:
		if len(arglist) == 0:
			return True
		if len(arglist) == 1:
			# HACK  Redirect to USAGE to get help for mail and dir submodules
			if arglist[0][:3].lower() == "mod" or \
				arglist[0][:4].lower() == "mail" or \
				arglist[0][:3].lower() == "dir":
				return True
		return False 
		
	# Read USAGE or REFERENCE data file.
	stream: NullableBytes = pkgutil.get_data(__name__, 'USAGE' if is_usage(*args) else 'REFERENCE')

	# HACK  Allow ANSI color codes using a tortuous decode/encode chain.
	# See https://stackoverflow.com/questions/14820429/how-do-i-decodestring-escape-in-python-3
	text: NullableStr = stream.decode('unicode-escape').encode('latin-1').decode('utf-8') if stream else None

	if text:
		match: NullableMatch = None
		if len(args) > 0:
			# Find the appropriate usage section according to help.
			match = re.search(
				r'^Usage:[ \n]+cpanel [A-Za-z\[\]]+ %s' % " ".join(args).rstrip("s"), text, re.M | re.I)

		if match is None:
			# Find the default usage section.
			match = re.search(r'^Usage: cpanel \[OPTIONS\] COMMAND', text, re.M | re.I)

		if match:
			start: int = match.start()
			# ‘---’ marks the end of the section.
			match = re.search(r'---', text[start:], re.M)
			end: int = start + match.end() if match else len(text)
			return text[start:end].rstrip("-\n")

	return "cpanel: use --help"
