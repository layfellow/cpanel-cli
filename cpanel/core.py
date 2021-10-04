import os
import sys
import json
import logging
from logging import Logger
from json import JSONDecodeError
import cpanel
from cpanel_api import CPanelApi, Result, ClientError
from typing import cast, Any, Union, Dict, List, Mapping, Callable

NullableStr = Union[str, None]
JSONType = Dict[str, Any]

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
		if r.status == 1 and r.errors is None:
			return method()
		else:
			raise CPanelError(r.errors[0])
		return ""


	def extract(self, r: Result, key: str) -> str:
		"""Get r['data'] values corresponding to key.

		r          API call result
		key        key name

		Returns stringified JSON array with key: value pairs
		"""
		data: List[Mapping[str, str]] = []
		for datum in r.data:
			data.append({ key: datum[key] })
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
		parameters: Mapping[str, NullableStr] = {}

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
		return self.check(lambda: self.client.uapi.Email.store_filter(**parameters))


def endpoint(hostname: NullableStr, username: NullableStr, utoken: NullableStr) -> CPanelEndpoint:
	"""CPanelEndpoint factory."""
	return CPanelEndpoint(CPanelApi(hostname, username, utoken, auth_type = 'utoken'))
