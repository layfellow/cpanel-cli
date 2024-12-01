import os
import unittest
from unittest import TestResult
import json
import random
from typing import List
from cpanel.cli import configuration
from cpanel.core import JSONType, CPanelEndpoint, endpoint
from cpanel.__main__ import dispatch
import urllib3
from urllib3.exceptions import InsecureRequestWarning


class TestCore(unittest.TestCase):

	def setUp(self) -> None:
		_, hostname, username, utoken = configuration([], {}, './test/cpanelrc.test')
		urllib3.disable_warnings(category = InsecureRequestWarning)
		self.host: CPanelEndpoint = endpoint(str(hostname), str(username), str(utoken))


	def run(self, result: TestResult | None = None) -> None:
		"""Stop after first error."""
		if result is None:
			result = self.defaultTestResult()
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


	def test_get_quota(self) -> None:
		quota: JSONType = json.loads(dispatch(self.host, ["get", "quota"]))
		print(quota)

		self.assertTrue(quota['inodes_used'] >= 0)
		self.assertTrue(quota['megabytes_used'] >= 0)


	def test_get_usage(self) -> None:
		usage: List[JSONType] = json.loads(dispatch(self.host, ["get", "usage"]))
		print(usage)

		self.assertTrue(len(usage) > 0)
		item: JSONType
		for item in usage:
			self.assertTrue(len(item['id']) > 0)
			self.assertTrue(int(item['usage']) >= 0)


	def test_get_stats(self) -> None:
		display: List[str] = ["hostname", "machinetype", "cpanelversion"]
		stats: List[JSONType] = json.loads(dispatch(self.host, ["get", "stats"] + display))
		print(stats)

		self.assertTrue(len(stats) > 0)
		stat: JSONType
		for stat in stats:
			self.assertTrue(stat['id'] in display)
			self.assertTrue(len(stat['value']) > 0)


	def test_list_accounts(self) -> None:
		accounts: List[JSONType] = json.loads(dispatch(self.host, ["list", "accounts"]))
		print(accounts)

		self.assertTrue(len(accounts[0]['user']) > 0)


	def test_get_account(self) -> None:
		account: JSONType = json.loads(dispatch(self.host, ["get", "account"]))
		print(account)

		self.assertTrue(len(account['user']) > 0)


	def test_subaccounts(self) -> None:
		subaccounts: List[JSONType] = json.loads(dispatch(self.host, ["list", "subaccounts"]))
		print(subaccounts)

		self.assertTrue(len(subaccounts) > 0)
		subaccount: JSONType
		for subaccount in subaccounts:
			self.assertTrue(len(subaccount['guid']) > 0)

		user: str = ""
		for subaccount in subaccounts:
			if 'enabled' in subaccount['services']['email']:
				if subaccount['services']['email']['enabled'] == 1:
					user = subaccount['full_username']
					break
		if user:
			service: JSONType = json.loads(dispatch(self.host, ["get", "service", "subaccount", user, "email"]))
			print(service)
			self.assertTrue('guid' in service)
			self.assertEqual("service", service['type'])


	def test_cache(self) -> None:
		update: JSONType = json.loads(dispatch(self.host, ["update", "cache"]))
		print(update)
		self.assertTrue(update['cache_id'] > 0)

		read: JSONType = json.loads(dispatch(self.host, ["read", "cache"]))
		print(read)
		self.assertTrue(read['cache_id'] > 0)
		self.assertEqual(read['cache_id'], update['cache_id'])


	def test_locales(self) -> None:
		original: JSONType = json.loads(dispatch(self.host, ["get", "locale"]))
		print(original)
		self.assertTrue(len(original['locale']) > 0)

		locales: List[JSONType] = json.loads(dispatch(self.host, ["list", "locales"]))
		locale: JSONType = locales[0]
		print(locale)
		self.assertTrue(len(locale['locale']) > 0)

		r: str = dispatch(self.host, ["set", "locale", locale['locale']])
		self.assertEqual(r, "OK")

		temporary: JSONType = json.loads(dispatch(self.host, ["get", "locale"]))
		print(temporary)
		self.assertEqual(temporary['locale'], locale['locale'])

		r: str = dispatch(self.host, ["set", "locale", original['locale']])
		self.assertEqual(r, "OK")


	def test_get_theme(self) -> None:
		themes: List[JSONType] = json.loads(dispatch(self.host, ["list", "themes"]))
		print(themes)

		theme: JSONType = json.loads(dispatch(self.host, ["get", "theme"]))
		print(theme)

		self.assertTrue(theme in themes)


	def test_list_dir_indexing(self) -> None:
		indexing: JSONType = json.loads(dispatch(self.host, ["list", "dir", "indexing", "/.cpanel"]))
		print(indexing)

		self.assertTrue(indexing['current']['state']['index_type'] in ("inherit",  "disabled", "standard", "fancy"))


	def test_set_dir_indexing(self) -> None:
		original: JSONType = json.loads(dispatch(self.host, ["get", "dir", "indexing", "/.cpanel"]))
		print(original)

		self.assertTrue(original in ("inherit",  "disabled", "standard", "fancy"))

		r: str = dispatch(self.host, ["set", "dir", "indexing", "/.cpanel", str(original)])
		self.assertEqual(r, "OK")


	def test_list_dir_privacy(self) -> None:
		privacy: JSONType = json.loads(dispatch(self.host, ["list", "dir", "privacy", "/.cpanel"]))
		print(privacy)

		self.assertTrue(privacy['current']['state']['protected'] in (0, 1))


	def test_enable_disable_dir_privacy(self) -> None:
		original: JSONType = json.loads(dispatch(self.host, ["get", "dir", "privacy", "/.cpanel"]))
		print(original)

		self.assertTrue(original['protected'] in (0, 1))

		r: str = dispatch(self.host, ["enable", "dir", "privacy", "/.cpanel"])
		self.assertEqual(r, "OK")

		r = dispatch(self.host, ["disable", "dir", "privacy", "/.cpanel"])
		self.assertEqual(r, "OK")

		if original['protected'] == 0:
			r = dispatch(self.host, ["disable", "dir", "privacy", "/.cpanel"])
			self.assertEqual(r, "OK")
		else:
			r = dispatch(self.host, ["enable", "dir", "privacy", "/.cpanel"])
			self.assertEqual(r, "OK")


	def test_add_list_delete_dir_user(self) -> None:
		user: str = 'tmp-{}'.format(hex(random.randrange(0, 2 ** 32))[2:])
		print(user)

		r: str = dispatch(self.host, ["add", "dir", "user", "/.cpanel", user, "twypjaspAsAc1"])
		self.assertEqual(r, "OK")

		users: List[JSONType] = json.loads(dispatch(self.host, ["list", "dir", "users", "/.cpanel"]))
		print(users)

		created: bool = False
		for u in users:
			created = created or u == user
		self.assertTrue(created)

		r = dispatch(self.host, ["delete", "dir", "user", "/.cpanel", user])
		self.assertEqual(r, "OK")

		users = json.loads(dispatch(self.host, ["list", "dir", "users", "/.cpanel"]))
		print(users)

		deleted: bool = True
		for u in users:
			deleted = deleted and u != user
		self.assertTrue(deleted)


	def test_list_dir_protection(self) -> None:
		protection: JSONType = json.loads(dispatch(self.host, ["list", "dir", "protection", "/.cpanel"]))
		print(protection)

		self.assertTrue(protection['current']['state']['has_leech_protection'] in (0, 1))


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

		r = dispatch(self.host, ["delete", "mail", "filter", emails[0]['email'], name])
		self.assertEqual(r, "OK")

		os.remove(filterfile)


	def test_move_mail_filter(self) -> None:
		emails: List[JSONType] = self.list_mail_accounts()
		if len(emails) == 0: return

		filters: List[JSONType] = self.list_mail_filters(emails[0]['email'])
		n: int = len(filters)
		if n == 0: return

		print(filters)

		account: str = emails[0]['email']
		first_filtername: str = filters[0]['filtername']

		r: str = dispatch(self.host, ["move", "mail", "filter", account, first_filtername, "bottom"])
		self.assertEqual(r, "OK")

		filters = self.list_mail_filters(account)
		m: int = len(filters)
		self.assertTrue(m == n)

		last_filtername: str = filters[m - 1]['filtername']
		self.assertTrue(last_filtername == first_filtername)

		r = dispatch(self.host, ["move", "mail", "filter", account, last_filtername, "top"])
		self.assertEqual(r, "OK")

		filters = self.list_mail_filters(account)
		n = len(filters)
		self.assertTrue(n == m)

		first_filtername = filters[0]['filtername']
		self.assertTrue(first_filtername == last_filtername)


	def test_list_filter_domains(self) -> None:
		domains: List[JSONType] = json.loads(dispatch(self.host, ["list", "filter", "domains"]))
		if len(domains) == 0: return

		print(domains)

		domain: JSONType
		for domain in domains:
			self.assertTrue(len(domain['domain']) > 0)


	def test_get_spam_settings(self) -> None:
		settings: JSONType = json.loads(dispatch(self.host, ["get", "spam", "settings"]))
		if len(settings) == 0: return

		print(settings)

		self.assertTrue('spam_enabled' in settings)
		self.assertTrue(settings['spam_enabled'] >= 0)


	def test_add_then_remove_from_spam_allowlist(self) -> None:
		settings: JSONType = json.loads(dispatch(self.host, ["get", "spam", "settings"]))
		if len(settings) == 0: return

		r: str = dispatch(self.host, ["add", "spam", "allowlist", "scott@example.com"])
		self.assertEqual(r, "OK")

		settings = json.loads(dispatch(self.host, ["get", "spam", "settings"]))
		print(settings)
		self.assertTrue("scott@example.com" in settings['whitelist_from'])

		r = dispatch(self.host, ["delete", "spam", "allowlist", "scott@example.com"])
		self.assertEqual(r, "OK")

		settings = json.loads(dispatch(self.host, ["get", "spam", "settings"]))
		self.assertTrue(
			'whitelist_from' not in settings or
			"scott@example.com" not in settings['whitelist_from'])


	def test_suspend_then_unsuspend_mail(self) -> None:
		emails: List[JSONType] = self.list_mail_accounts()
		if len(emails) == 0: return

		r: str = dispatch(self.host, ["suspend", "mail", "incoming", emails[0]['email']])
		self.assertEqual(r, "OK")

		r: str = dispatch(self.host, ["unsuspend", "mail", "incoming", emails[0]['email']])
		self.assertEqual(r, "OK")
		
		r: str = dispatch(self.host, ["suspend", "mail", "outgoing", emails[0]['email']])
		self.assertEqual(r, "OK")

		r: str = dispatch(self.host, ["unsuspend", "mail", "outgoing", emails[0]['email']])
		self.assertEqual(r, "OK")
		
		r: str = dispatch(self.host, ["suspend", "mail", "login", emails[0]['email']])
		self.assertEqual(r, "OK")

		r: str = dispatch(self.host, ["unsuspend", "mail", "login", emails[0]['email']])
		self.assertEqual(r, "OK")
		
	def test_domain_stats(self) -> None:
		domains: List[str] = json.loads(dispatch(self.host, ["list", "stats", "domains"]))	
		if len(domains) == 0: return
		
		print(domains)
		
		html: str = dispatch(self.host, ["get", "stats", "domain", domains[0]])
		self.assertTrue(len(html) > 800)
		
		print(html[:800])
