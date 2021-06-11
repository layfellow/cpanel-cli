import cpanel

project = cpanel.__description__
copyright = cpanel.__copyright__
author = cpanel.__author__
release = cpanel.__version__
extensions = []
templates_path = []
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']
html_static_path = []
html_title = cpanel.__description__
html_theme = 'sphinx_material'
html_theme_options = {
	# Set the name of the project to appear in the navigation.
	'nav_title': cpanel.__description__,

	# Set you GA account ID to enable tracking.
	# 'google_analytics_account': 'UA-XXXXX',

	# Specify a base_url used to generate sitemap.xml.
	# 'base_url': 'https://project.github.io/project',

	# Set the color and the accent color.
	'color_primary': 'orange',
	'color_accent': 'teal',

	# Set the repo location to get a badge with stats
	'repo_url': cpanel.__url__,
	'repo_name': cpanel.__description__,

	# Visible levels of the global TOC; -1 means unlimited
	'globaltoc_depth': 3,
	# If False, expand all TOC entries
	'globaltoc_collapse': False,
	# If True, show hidden TOC entries
	'globaltoc_includehidden': False
}
