from setuptools import setup
import cpanel

with open('README.rst', 'r', encoding = 'utf-8') as stream:
	long_description = stream.read()

setup(
	name = 'cpanel-cli',
	version = cpanel.__version__,
	author = cpanel.__author__,
	author_email = cpanel.__email__,
	description = cpanel.__description__,
	long_description = long_description,
	url = cpanel.__url__,
	project_urls = {
		'Bug Tracker': cpanel.__url__ + '/issues'
	},
	classifiers = [
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Operating System :: OS Independent'
	],
	include_package_data = True,
	packages = ['cpanel'],
	python_requires = '>=3.9',
	install_requires = [
		'cpanel-api>=0.3.0',
		'parsedatetime>=2.6'
	],
	entry_points = {
		'console_scripts': [
			'cpanel = cpanel.__main__:main'
		]
	}
)
