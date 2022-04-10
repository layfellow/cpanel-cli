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

	def cmd_starts_with(cmd: NullableStr, text: str) -> bool:
		return cmd is not None and cmd[0:len(text)].lower() == text

	if cmd_starts_with(cmd, "mod"):
		help = """\
		Usage: cpanel help MODULE

		For a complete User’s Guide go to: https://cpanel-cli.readthedocs.io/en/latest/

		MODULES
		The currently implemented modules and functions are:

		features
		    cpanel list features

		quota
		    cpanel get quota

		usage
		    cpanel get usage

		stats
		    cpanel get stats STAT...

		subaccounts
		    cpanel list subaccounts
		    cpanel get subaccount GUID

		backups
		    cpanel create backup home [EMAIL]
		    cpanel create backup ftp USERNAME PASSWORD HOST [DIRECTORY] [EMAIL]
		    cpanel create backup scp USERNAME PASSWORD HOST [DIRECTORY] [EMAIL]
		    cpanel list backups

		mail
		    cpanel list mail accounts
		    cpanel list mail filters ACCOUNT
		    cpanel get mail filter ACCOUNT FILTERNAME
		    cpanel set mail filter ACCOUNT FILE
		    cpanel delete mail filter ACCOUNT FILTERNAME

		Use ‘cpanel help MODULE’ to learn more about the functions implemented
		for MODULE; for example, ‘cpanel help mail’ to print detailed help on all
		the functions implemented for the ‘mail’ module.
		"""
	elif cmd_starts_with(cmd, "feat"):
		help = """\
		Usage: cpanel list features

		List a cPanel account’s features. Output is JSON-formatted.

		For a complete User’s Guide go to: https://cpanel-cli.readthedocs.io/en/latest/
		"""
	elif cmd_starts_with(cmd, "quo"):
		help = """\
		Usage: cpanel get quota

		Get the cPanel account’s total disk quota information in megabytes.
		Output is JSON-formatted.

		For a complete User’s Guide go to: https://cpanel-cli.readthedocs.io/en/latest/
		"""
	elif cmd_starts_with(cmd, "usage"):
		help = """\
		Usage: cpanel get usage

		Show resource usage and some statistics, like bandwidth, number of subdomains,
		disk usage, number of mail filters, etc.
		Output is JSON-formatted.

		For a complete User’s Guide go to: https://cpanel-cli.readthedocs.io/en/latest/
		"""
	elif cmd_starts_with(cmd, "stat"):
		help = """\
		Usage: cpanel get stats STAT...

		Show detailed data and statistics, like hostname, file usage, database usage,
		dedicated IPs, etc. Output is JSON-formatted.

		STAT is the name of the statistic you want, you can provide a list of STATs to
		be displayed. For a complete list ot STAT names, see ‘display parameters’ at:
		https://api.docs.cpanel.net/openapi/cpanel/operation/get_stats/

		EXAMPLES
		    cpanel get stats hostname
		    cpanel get stats machinetype cpanelversion

		For a complete User’s Guide go to: https://cpanel-cli.readthedocs.io/en/latest/
		"""
	elif cmd_starts_with(cmd, "subacc"):
		help = """\
		Usage:
		    cpanel list subaccounts
		    cpanel get subaccount GUID

		For a complete User’s Guide go to: https://cpanel-cli.readthedocs.io/en/latest/

		COMMANDS

		list subaccounts
		    List the sub-accounts of the main cPanel account, along with detailed information
		    of each sub-account. Output is JSON-formatted.

		    EXAMPLE
		        cpanel list subaccounts

		get subaccount GUID
		    Show detailed information of a sub-account, identified by its GUID. To get
		    this GUID, use ‘cpanel list subaccounts’. Note that only sub-accounts with a
		    sub_account_exists flag set to 1 can be queried. Output is JSON-formatted.

		    EXAMPLE
		        cpanel get subaccount EXAMPLE1:EXAMPLE.COM:564CD663:FE50072F2620B50988EA4E5F46022546FBE6BDDE3C36C2F2534F4967C661EC37
		"""
	elif cmd_starts_with(cmd, "back"):
		help = """\
		Usage:
		    cpanel create backup home [EMAIL]
		    cpanel create backup ftp USERNAME PASSWORD HOST [DIRECTORY] [EMAIL]
		    cpanel create backup scp USERNAME PASSWORD HOST [DIRECTORY] [EMAIL]
		    cpanel list backups

		For a complete User’s Guide go to: https://cpanel-cli.readthedocs.io/en/latest/

		COMMANDS

		All ‘create backup’ commands create a backup tarball (a .tar.gz file) of
		the user’s home directory along with other account data, such as the crontab,
		API tokens, log files and DB data. The backup tarball’s name is
		backup-MM.DD.YYYY_HH-MM-SS_USERNAME.tar.gz.

		If you pass an optional EMAIL argument, the backup engine will send a
		confirmation email after it completes the backup.

		create backup home [EMAIL]
		    Create a backup tarball and store it in the user’s home directory itself.

		create backup ftp USERNAME PASSWORD HOST [DIRECTORY] [EMAIL]
		    Create a backup tarball and store it on a remote FTP server.

		    HOST is the hostname of the remote FTP server.
		    USERNAME and PASSWORD are the credentials to log in to it.
		    Optional DIRECTORY is the destination directory on the remote server;
		    by default use the remote user’s login directory. Note that DIRECTORY
		    is not an absolute path, but a path relative to the login directory, i.e.,
		    /public corresponds to <remote login directory>/public.

		create backup scp USERNAME PASSWORD HOST [DIRECTORY] [EMAIL]
		    Create a backup tarball and store it on a remote SCP server.

		    USERNAME, PASSWORD, HOST and DIRECTORY are the same as for ‘create backup ftp’.

		    EXAMPLES
		        cpanel backup home
		        cpanel backup home scott@example.com
		        cpanel backup ftp scott tiger ftp.example.com
		        cpanel backup ftp scott tiger ftp.example.com /backup
		        cpanel backup scp scott tiger ssh.example.com /backup scott@example.com

		list backups
		    List the account’s backup files. Output is JSON-formatted.

		    EXAMPLE
		        cpanel list backups
		"""
	elif cmd_starts_with(cmd, "mail"):
		help = """\
		Usage:
		    cpanel list mail accounts
		    cpanel list mail filters ACCOUNT
		    cpanel get mail filter ACCOUNT FILTERNAME
		    cpanel set mail filter ACCOUNT FILE
		    cpanel delete mail filter ACCOUNT FILTERNAME

		For a complete User’s Guide go to: https://cpanel-cli.readthedocs.io/en/latest/

		COMMANDS

		list mail accounts
		    Lists cPanel email accounts. Output is JSON-formatted.

		    EXAMPLE
		        cpanel list mail accounts

		list mail filters ACCOUNT
		    Lists mail filters associated to ACCOUNT. Output is a JSON-formatted
		    array of filter names.
		    ACCOUNT is the name of a cPanel email account, usually user@domain

		    EXAMPLE
		        cpanel list mail filters scott@example.com

		get mail filter ACCOUNT FILTERNAME
		    Return a JSON-formatted description of email filter FILTERNAME associated
		    to email ACCOUNT. To get a list of current filter names, use
		    ‘cpanel list mail filters ACCOUNT’

		    EXAMPLE
		        cpanel get mail filter scott@example.com spamkiller

		set mail filter ACCOUNT FILE
		    Create or update an email filter associated with email ACCOUNT.
		    If the filter already exists, it updates it; otherwise, it creates a new filter.
		    Use a JSON FILE to describe the filter rules. This JSON FILE has the same
		    textual format as the output from ‘cpanel get mail filter’, so the easiest way
		    to create a new filter is to dump an existing filter into a filter.json file,
		    edit it and then upload it with ‘cpanel set mail filter’.
		    See the EXAMPLE below.

		    EXAMPLE
		        cpanel get mail filter scott@example.com spamkiller > filter.json
		        # Edit filter.json, and then run:
		        cpanel set mail filter scott@example.com filter.json

		delete mail filter ACCOUNT FILTERNAME
		    Delete email filter FILTERNAME associated to ACCOUNT. To get a list of current
		    filter names, use ‘cpanel list mail filters ACCOUNT’

		    EXAMPLE
		         cpanel delete mail filter scott@example.com spamkiller
		"""
	else:
		help = """\
		Usage: cpanel [OPTIONS] COMMAND...

		CLI utility to run tasks on a website controlled with cPanel.

		For a complete User’s Guide go to: https://cpanel-cli.readthedocs.io/en/latest/

		OPTIONS
		    -h, --help                  print this help and exit
		    -V, --version               print version information and exit
		    -H HOST, --hostname=HOST    cPanel server hostname
		    -U USER, --username=USER    username on cPanel server
		    -T UTOKEN, --utoken=UTOKEN  UAPI token associated to USER

		AUTHENTICATION
		You can pass the HOST, USER and UTOKEN credentials directly as options, as
		shown above, or, better yet, write a .cpanelrc file on your $HOME
		directory. See the Authentication section in the User’s Guide at:
		https://cpanel-cli.readthedocs.io/en/latest/installation.html#authentication

		COMMAND is a sequence of two or more keywords describing a task; the general
		form of the command keyword list is:

		    cpanel VERB MODULE TARGET [ARGUMENTS...]

		EXAMPLES
		    cpanel list features
		    cpanel list mail accounts
		    cpanel get mail filter scott@example.com spamkiller

		Notice the keywords follow the natural English sentence order, i.e.,
		‘list features’, ‘get mail filter’, etc.

		MODULES
		The currently implemented modules are:

		    features
		    quota
		    usage
		    stats
		    subaccounts
		    backups
		    mail

		Use ‘cpanel help modules’ for more information about them.

		DEVELOPMENT
		    Visit the project page at: https://github.com/layfellow/cpanel-cli/
		"""
	return textwrap.dedent(help)
