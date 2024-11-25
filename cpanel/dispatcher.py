import logging
from logging import Logger
from typing import List
from .cli import die
from .core import CPanelEndpoint
from .caller import *

log: Logger = logging.getLogger(__name__)


def dispatch(host: CPanelEndpoint, args: List[str]) -> str:
	"""Make a cPanel API call corresponding to the args.

	host       reference to API endpoint
	args       list of arguments passed to the command line, minus options

	Returns    result data (usually a JSON string)
	"""

	log.debug(str(args))
	cmd: str = " ".join(args[0:4])  # Use the first 4 args to match command.

	r: str = ""

	try:
		r = r or features.call(host, cmd, args)
		r = r or quota.call(host, cmd, args)
		r = r or usage.call(host, cmd, args)
		r = r or stats.call(host, cmd, args)
		r = r or ssh.call(host, cmd, args)
		r = r or ip.call(host, cmd, args)
		r = r or accounts.call(host, cmd, args)
		r = r or subaccounts.call(host, cmd, args)
		r = r or backup.call(host, cmd, args)
		r = r or cache.call(host, cmd, args)
		r = r or locale.call(host, cmd, args)
		r = r or themes.call(host, cmd, args)
		r = r or dir.call(host, cmd, args)
		r = r or dns.call(host, cmd, args)
		r = r or domains.call(host, cmd, args)
		r = r or logmanager.call(host, cmd, args)
		r = r or bandwidth.call(host, cmd, args)
		r = r or files.call(host, cmd, args)
		r = r or mail_accounts.call(host, cmd, args)
		r = r or mail_settings.call(host, cmd, args)
		r = r or mail_incoming.call(host, cmd, args)
		r = r or mail_outgoing.call(host, cmd, args)
		r = r or mail_login.call(host, cmd, args)
		r = r or mail_boxes.call(host, cmd, args)
		r = r or mail_autoresponders.call(host, cmd, args)
		r = r or mail_forwarders.call(host, cmd, args)
		r = r or mail_filters.call(host, cmd, args)
		r = r or mail_quota.call(host, cmd, args)
		r = r or mail_usage.call(host, cmd, args)
		r = r or spam.call(host, cmd, args)
		r = r or webmail.call(host, cmd, args)
		r = r or mailman.call(host, cmd, args)
		r = r or ftp.call(host, cmd, args)
		r = r or mysql.call(host, cmd, args)
		r = r or postgres.call(host, cmd, args)
		
		if not r:
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
