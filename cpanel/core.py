import os
import json
import logging
import requests
import time
import parsedatetime
from datetime import datetime, timezone, timedelta
from urllib.parse import urljoin
from logging import Logger
from json import JSONDecodeError
from cpanel_api import CPanelApi, Result
from typing import Any, Union, Dict, List, Mapping, Callable

NullableStr = Union[str, None]
NullableResult = Union[Result, None]
NullableBytes = Union[bytes, None]
JSONType = Dict[str, Any]
StringOrInteger = Union[str, int]

log: Logger = logging.getLogger(__name__)


class CPanelError(Exception):
	pass


class CPanelEndpoint:
	"""A wrapper over CPanelApi with some utility functions."""

	def __init__(self, client: CPanelApi) -> None:
		self.client = client


	def safely(self, r: Result, method: Callable) -> str:
		"""Check for possible errors in API call result, then call method.

		r          API call result
		method     callback to process r if r has no errors

		Returns processed r or empty string
		"""
		if r.status == 1:
			if r.errors is None:
				return method()
			elif isinstance(r.errors, str) and r.errors.lower().find("no error") > -1:
				return method()
			elif isinstance(r.errors, List) and r.errors[0].lower().find("no error") > -1:
				return method()
		else:
			raise CPanelError(r['errors'][0])
		return ""


	def extract(self, r: Result, key: str) -> str:
		"""Get r['data'] values corresponding to key.

		r          API call result
		key        key name

		Returns stringified JSON array with key: value pairs
		"""
		data: List[Mapping[str, str]] = []
		for datum in r['data']:
			data.append({ key: datum[key] })
		return json.dumps(data, indent = 4, sort_keys = True)


	def select(self, r: Result, key: str, value: str) -> str:
		"""Get a single element from array r['data'] which has a key == value.

		r          API call result
		key        key name
		value      key value to select

		Returns stringified JSON array with selected key: value pairs
		"""
		data: Result = Result({})
		for datum in r['data']:
			if datum[key] == value:
				data = datum
		return json.dumps(data, indent = 4, sort_keys = True)


	def check(self, apicall: Callable) -> str:
		"""Call API and check if request was OK, do not print results.

		apicall    deferred API call

		Returns "OK" or prints error
		"""
		r: Result = apicall()
		return self.safely(r, lambda: "OK")


	def dump(self, apicall: Callable) -> str:
		"""Call API and get stringified JSON result.

		apicall    deferred API call

		Returns stringified JSON data
		"""
		r: Result = apicall()
		return self.safely(r, lambda: json.dumps(r.data, indent = 4, sort_keys = True))


	def dump_extracted(self, key: str, apicall: Callable) -> str:
		"""Call API and get stringified JSON result filtered by key.

		key        key name to filter result
		apicall    deferred API call

		Returns stringified JSON data
		"""
		r: Result = apicall()
		return self.safely(r, lambda: self.extract(r, key))


	def dump_selected(self, key: str, value: str, apicall: Callable) -> str:
		"""Call API and get a stringified JSON result whose key == value.

		key        key name to select result
		value      key value to select result
		apicall    deferred API call
		"""
		r: Result = apicall()
		return self.safely(r, lambda: self.select(r, key, value))


	def dump_null(self, apicall: Callable, replace: str) -> str:
		"""Call API and get stringified JSON result, but replaces nulls.

		apicall    deferred API call
		replace    string to replace nulls with

		Returns stringified JSON data
		"""
		r: Result = apicall()
		i = 0
		for item in r['data']:
			if item is None:
				r['data'][i] = replace
			i += 1

		return self.safely(r, lambda: json.dumps(r.data, indent = 4, sort_keys = True))


	def create_backup(self, *args: str) -> str:
		"""Create a backup tarball and store it on a remote server.

		args	variable argument list with username, password, host,
				optional directory and optional confirmation email

		Returns "OK" or prints error
		"""
		# kwargs for CPanelAPi call to Backup.fullbackup_to_*().
		parameters: Dict[str, NullableStr] = {}

		if len(args) < 1:
			raise CPanelError("missing arguments for create backup")

		try:
			if args[0] == 'ftp' or args[0] == 'scp':
				parameters['username'] = args[1]
				parameters['password'] = args[2]
				parameters['host'] = args[3]
				if len(args) > 4:
					parameters['directory'] = args[4]
				if len(args) > 5:
					parameters['email'] = args[5]
			elif args[0] == 'home':
				if len(args) > 1:
					parameters['email'] = args[1]
			else:
				raise CPanelError("create backup target must be ftp, home or scp")

			log.debug(str(args))

			if args[0] == 'ftp':
				return self.check(
					lambda: self.client.uapi.Backup.fullbackup_to_ftp(**parameters))
			elif args[0] == 'scp':
				return self.check(
					lambda: self.client.uapi.Backup.fullbackup_to_scp_with_password(**parameters))

			return self.check(
				lambda: self.client.uapi.Backup.fullbackup_to_homedir(**parameters))

		except IndexError:
			raise CPanelError("missing arguments for create backup")


	def set_log_settings(self, flag: int, *args: str) -> str:
		"""Enable or disable log archival settings.

		flag        0 to enable, 1 to disable
		args        List of archival settings to enable or disable

		Returns "OK" or prints error
		"""
		parameters: Dict[str, NullableStr] = {}

		log.debug(str(args))

		if len(args) == 0:
			raise CPanelError("missing arguments for set log settings")
		if 'archive' in args:
			parameters['archive_logs'] = str(flag)
		if 'prune' in args:
			parameters['prune_archive'] = str(flag)
		if len(parameters) == 0:
			raise CPanelError("unrecognized arguments for set log settings")

		return self.check(
			lambda: self.client.uapi.LogManager.set_settings(**parameters))


	def get_file_contents(self, filepath: str) -> bytes:
		"""Return the contents of remote filepath encoded using UTF-8.

		filepath    path to remote file
		"""
		dirname: str = os.path.dirname(filepath)
		if len(dirname) == 0:
			dirname = "/"
		basename: str = os.path.basename(filepath)

		r: Result = self.client.uapi.Fileman.get_file_content(
			dir = dirname, file = basename, to_charset = 'utf-8')
		if r.status != 1 or r.errors is not None:
			raise CPanelError(r['errors'][0])

		return r['data'].content.encode('utf-8')


	def write_file(self, filepath: str, content: str) -> str:
		"""Write a remote filepath with provided content.

		filepath    path to remote file
		content     content string encoded using UTF-8

		Returns "OK" or prints error
		"""
		dirname: str = os.path.dirname(filepath)
		if len(dirname) == 0:
			dirname = "/"
		basename: str = os.path.basename(filepath)

		# Unescape backslash-escaped codes.
		content = content.encode('raw_unicode_escape').decode('unicode_escape')

		return self.check(lambda: self.client.uapi.Fileman.save_file_content(
			dir = dirname, file = basename, content = content, fallback = 0))


	def set_mail_autoresponder(self, *args: str) -> str:
		"""Create an autoresponder for an email account.

		args	variable argument list with email, and optional
				from, subject, body, start time and stop time

		Returns "OK" or prints error
		"""
		log.debug(str(args))

		# kwargs for CPanelAPI call to Email.add_auto_responder().
		parameters: Dict[str, StringOrInteger] = {}

		default_subject: str = "This is an automatic message"
		default_body: str = "I’m currently unavailable."

		try:
			email: str = args[0]
			parameters['email'] = email
			parameters['domain'] = email[email.find("@") + 1:]
			parameters['from'] = len(args) > 1 and args[1] or email
			parameters['subject'] = len(args) > 2 and args[2] or default_subject
			parameters['body'] = len(args) > 3 and args[3] or default_body
			parameters['interval'] = 24
			parameters['is_html'] = 1
		except IndexError:
			raise CPanelError("missing arguments for create mail autoresponder")

		cal: parsedatetime.Calendar = parsedatetime.Calendar()

		s: str
		t: time.struct_time
		parsed: int
		starttime: datetime
		endtime: datetime

		s = len(args) > 4 and args[4] or "now"
		# parsed is an int, because of the VERSION_FLAG_STYLE flag.
		t, parsed = cal.parse(s, version = parsedatetime.VERSION_FLAG_STYLE)  # type: ignore [reportAssignmentType]
		if parsed > 0:
			log.debug(str(t))
			starttime = datetime(*t[:6], tzinfo = timezone(timedelta(seconds = -time.timezone)))
		else:
			raise CPanelError("error parsing start time")

		s = len(args) > 5 and args[5] or "December 24, 2099 11:59 PM"
		# parsed is an int, because of the VERSION_FLAG_STYLE flag.
		t, parsed = cal.parse(s, version = parsedatetime.VERSION_FLAG_STYLE)  # type: ignore [reportAssignmentType]
		if parsed > 0:
			log.debug(str(t))
			endtime = datetime(*t[:6], tzinfo = timezone(timedelta(seconds = -time.timezone)))
		else:
			raise CPanelError("error parsing end time")

		parameters['start'] = int(starttime.timestamp())
		parameters['stop'] = int(endtime.timestamp())

		log.debug(str(parameters))
		return self.check(
			lambda: self.client.uapi.Email.add_auto_responder(**parameters))


	def upload_file(self, directory: str, filename: str) -> str:
		"""Upload a local file to a remote directory.

		directory   remote path to directory
		filename    local file name

		Returns "OK" or prints error
		"""
		if not os.path.isfile(filename):
			raise CPanelError("missing file {}".format(filename))

		url: str = urljoin(self.client.base_url, '/execute/Fileman/upload_files')
		permissions: str = "0{}".format(oct(os.stat(filename).st_mode)[-3:])

		# Upload the actual file contents as multipart-encoded form data.
		with open(filename, 'rb') as stream:
			response: requests.Response = self.client.session.post(
				url, {
					'dir': directory,
					'file': filename,
					'overwrite': 1,
					'permissions': permissions
				},
				files = { filename: stream },
				allow_redirects = False,
				headers = { 'Authorization': self.client.auth },
				timeout = self.client.timeout,
				verify = self.client.verify)

		if response.status_code == 401:
			raise CPanelError("Unauthorized")

		r: Result = Result({})
		try:
			r = response.json(object_hook = Result)
		except ValueError:
			raise CPanelError("Bad response")
		finally:
			return self.safely(r, lambda: "OK")


	def set_mail_filter(self, account: str, filterfile: str) -> str:
		"""Set filter for email account.

		account     email account identifier, usually in the form 'name@example.com'
		filterfile  JSON file with filter rule definitions

		Returns "OK" or prints error
		"""
		if not os.path.isfile(filterfile):
			raise CPanelError("missing JSON filter file {}".format(filterfile))

		try:
			# Check if filterfile is a valid JSON file.
			with open(filterfile, 'r') as stream:
				filters: JSONType = json.loads(stream.read())
		except (IOError, JSONDecodeError) as e:
			raise CPanelError("error parsing JSON filter file {}, {}".format(filterfile, str(e)))

		# kwargs for CPanelAPi call to Email.store_filter().
		parameters: Dict[str, NullableStr] = {}

		try:
			parameters['filtername'] = filters['filtername']
			parameters['account'] = account

			action: JSONType
			i: int = 1
			for action in filters['actions']:
				parameters['action' + str(i)] = action['action']
				parameters['dest' + str(i)] = action['dest']
				i += 1

			rule: JSONType
			i: int = 1
			for rule in filters['rules']:
				parameters['match' + str(i)] = rule['match']
				parameters['opt' + str(i)] = rule['opt']
				parameters['part' + str(i)] = rule['part']
				parameters['val' + str(i)] = rule['val']
				i += 1

		except KeyError as e:
			raise CPanelError("missing key in JSON filter file {}, {}".format(filterfile, str(e)))

		log.debug(str(parameters))
		return self.check(
			lambda: self.client.uapi.Email.store_filter(**parameters))


	def get_mail_forwarder(self, email: str, domain: str) -> NullableStr:
		"""Return the forwarder address for email, or None if mail has no forwarders."""

		r: Result = self.client.uapi.Email.list_forwarders(domain = domain)

		log.debug(str(r['data']))

		for forwarder in r['data']:
			if forwarder['dest'] == email:
				return forwarder['forward']

		return None


	def move_mail_filter(self, *args: str) -> str:
		"""Move a mail filter up, down, to the top, or to the bottom.
		(Filters are executed in order from top to bottom.)

		args	variable argument list with account name (arg[0]),
				filter name (arg[1]), "up", "down", "top" or "bottom" (arg[2])
				and optionally a numeric argument (arg[3])

		Returns "OK" or prints error
		"""
		if len(args) < 1:
			raise CPanelError("missing arguments for move mail filter")

		# Get filter list as data
		data: list = self.client.uapi.Email.list_filters(account = args[0])['data']
		n: int = len(data)

		try:
			# Find the index x of the filter to move
			x: int | None  = next((i for i, kv in enumerate(data) if kv['filtername'] == args[1]), None)
			if x is None:
				raise CPanelError("filter not found, {}".format(args[1]))

			# Find the index y of the destination
			y: int
			if args[2] in ("up", "down", "top", "bottom"):
				m: int = 1
				if len(args) > 3:
					m = int(args[3])
				y = x + { "up": -m, "down": m, "top": -x, "bottom": -x + n - 1}[args[2]]  # type: ignore [index]
			else:
				y = int(args[2]) - 1  # From 1-based to 0-based

			if y < 0:
				y = 0
			elif y >= n:
				y = n - 1

		except IndexError:
			raise CPanelError("missing arguments for move mail filter")

		if x == y:
			return "OK"

		# Build a reordered filters dict, with the affected filter reinserted from index x to index y

		i: int = 0
		j: int = 0
		filters: Dict[str, NullableStr] = {}

		while j < n:
			if x > y and i == y or x < y and i == y + 1:
				filters[f'filter{j + 1}'] = data[x]['filtername']
				if i < n:
					filters[f'filter{j + 2}'] = data[i]['filtername']
				i += 1
				j += 2
				continue
			if i == x:
				i += 1
				continue
			filters[f'filter{j + 1}'] = data[i]['filtername']
			i += 1
			j += 1

		filters['mailbox'] = args[0]

		log.debug(str(filters))

		return self.check(lambda: self.client.uapi.Email.reorder_filters(filters))


	def update_spam_list(self, add: bool, spam_list: str, *args: str) -> str:
		"""Add/delete email addresses to/from a spam list.

		add        True to add, False to delete
		spam_list  'blacklist_from', 'whitelist_from'
		args       variable argument list with email addresses

		Returns "OK" or prints error
		"""

		preferences: Result = self.client.uapi.SpamAssassin.get_user_preferences()
		current: list[str] = preferences['data'][spam_list] if spam_list in preferences['data'] else []

		log.debug(str(current))

		for email in args:
			if add and email not in current or not add and email in current:
				if add:
					current.append(email)
				else:
					current.remove(email)

		kwargs: dict = {'preference': spam_list}
		for i, email in enumerate(current):
			kwargs[f'value-{i}'] = email

		log.debug(str(current))

		return self.check(
			lambda: self.client.uapi.SpamAssassin.update_user_preference(**kwargs))


def endpoint(hostname: str, username: str, utoken: str) -> CPanelEndpoint:
	"""CPanelEndpoint factory."""
	return CPanelEndpoint(CPanelApi(hostname, username, utoken, auth_type = 'utoken'))
