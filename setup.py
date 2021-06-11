from setuptools import setup

setup(
	name = 'cpanel-cli',
	version = '0.1.0',
	packages = ['cpanel'],
	entry_points = {
		'console_scripts': [
			'cpanel = cpanel.__main__:main'
		]
	})
