import os
import unittest
from unittest import TestResult
import json
import random
from typing import List, Union
from cpanel.cli import configuration
from cpanel.core import JSONType, CPanelEndpoint, endpoint
from cpanel.__main__ import dispatch
from cpanel_api import Api


class TestCore(unittest.TestCase):

	def setUp(self) -> None:
		_, hostname, username, utoken = configuration([], {}, './test/cpanelrc.test')
		self.host: CPanelEndpoint = endpoint(hostname, username, utoken)


	def run(self, result: TestResult) -> None:
		"""Stop after first error."""
		if not result.errors:
			super(TestCore, self).run(result)


	def list_mail_accounts(self) -> List[JSONType]:
		return json.loads(dispatch(self.host, ["list", "mail", "accounts"]))


	def list_mail_filters(self, account: str) -> List[JSONType]:
		return json.loads(dispatch(self.host, ["list", "mail", "filters", account]))


	def get_mail_filter(self, account: str, filtername: str) -> JSONType:
		return json.loads(dispatch(self.host, ["get", "mail", "filter", account, filtername]))


	# Actual tests below.

	def test_list_features(self) -> None:
		features: JSONType = json.loads(dispatch(self.host, ["list", "features"]))
		print(features)

		key: str
		value: int
		for key, value in features.items():
			self.assertTrue(value in (0, 1))


	def test_list_mail_accounts(self) -> None:
		emails: List[JSONType] = self.list_mail_accounts()
		print(emails)

		email: JSONType
		for email in emails:
			self.assertTrue(len(email['email']) > 0)


	def test_list_mail_filters(self) -> None:
		emails: List[JSONType] = self.list_mail_accounts()
		if len(emails) == 0: return

		filters: List[JSONType] = self.list_mail_filters(emails[0]['email'])
		print(filters)

		filter: JSONType
		for filter in filters:
			self.assertTrue(len(filter['filtername']) > 0)


	def test_get_mail_filter(self) -> None:
		emails: List[JSONType] = self.list_mail_accounts()
		if len(emails) == 0: return

		filters: List[JSONType] = self.list_mail_filters(emails[0]['email'])
		if len(filters) == 0: return

		filter: JSONType = self.get_mail_filter(emails[0]['email'], filters[0]['filtername'])
		print(filter)

		actions: List[JSONType] = filter['actions']
		action: JSONType
		for action in actions:
			self.assertTrue(len(action['action']) > 0)
			if action['dest'] is not None: self.assertTrue(len(action['dest']) > 0)
			self.assertTrue(int(action['number']) > 0)

		rules: List[JSONType] = filter['rules']
		rule: JSONType
		for rule in rules:
			self.assertTrue(len(rule['match']) > 0)
			self.assertTrue(len(rule['part']) > 0)
			self.assertTrue(len(rule['val']) > 0)
			self.assertTrue(int(rule['number']) > 0)


	def test_set_then_delete_mail_filter(self) -> None:
		emails: List[JSONType] = self.list_mail_accounts()
		if len(emails) == 0: return

		filters: List[JSONType] = self.list_mail_filters(emails[0]['email'])
		if len(filters) == 0: return

		filter: JSONType = self.get_mail_filter(emails[0]['email'], filters[0]['filtername'])
		if len(filter) == 0: return

		name: str = 'tmp-{}'.format(hex(random.randrange(0, 2 ** 32))[2:])
		filter['filtername'] = name
		filterfile: str = './test/{}.json'.format(name)

		with open(filterfile, 'w', encoding = 'utf-8') as stream:
			stream.write(json.dumps(filter, indent = 4, sort_keys = True))

		r: str = dispatch(self.host, ["set", "mail", "filter", emails[0]['email'], filterfile])
		self.assertEqual(r, "OK")

		r: str = dispatch(self.host, ["delete", "mail", "filter", emails[0]['email'], name])
		self.assertEqual(r, "OK")

		os.remove(filterfile)
