import cpanel
from sphinx.locale import get_translation

_ = get_translation('index')

def setup(app):
	app.add_css_file('custom.css')

project = cpanel.__description__
copyright = cpanel.__copyright__
author = cpanel.__author__
release = cpanel.__version__
extensions = []
templates_path = []
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']
html_static_path = ['_static/']
html_title = cpanel.__description__ + " (v" + cpanel.__version__ + ")"
locale_dirs = ['locale/']
gettext_compact = False
html_sidebars = {
    "**": ['logo-text.html', 'globaltoc.html', 'localtoc.html', 'searchbox.html']
}
html_theme = 'sphinx_material'
html_logo = '_static/cpanel-cli-white.svg'
html_theme_options = {
	# Set the name of the project to appear in the navigation.
	'nav_title': _("cPanel CLI"),

	# Set you GA account ID to enable tracking.
	# 'google_analytics_account': 'UA-XXXXX',

	# Specify a base_url used to generate sitemap.xml.
	# 'base_url': 'https://project.github.io/project',

	# Set the color and the accent color.
	'color_primary': 'salmon',
	'color_accent': 'teal',

	# Set the repo location to get a badge with stats
	'repo_url': cpanel.__url__,
	'repo_name': "cpanel-cli",

	# Visible levels of the global TOC; -1 means unlimited
	'globaltoc_depth': 2,
	# If False, expand all TOC entries
	'globaltoc_collapse': True,
	# If True, show hidden TOC entries
	'globaltoc_includehidden': True,

	'version_dropdown': True
}
