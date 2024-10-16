import cpanel
from sphinx.locale import get_translation

_ = get_translation('index')

project = cpanel.__description__
copyright = cpanel.__copyright__
author = cpanel.__author__
release = cpanel.__version__
extensions = []
templates_path = []
exclude_patterns = ['build', 'Thumbs.db', '.DS_Store']
html_static_path = ['_static/']
html_title = cpanel.__description__
locale_dirs = ['locale/']
gettext_compact = False

html_theme = 'sphinx_book_theme'
html_logo = '_static/cpanel-cli-salmon.png'
html_theme_options = {
	# If False, expand all TOC entries
	'globaltoc_collapse': True,

	# If True, show hidden TOC entries
	'globaltoc_includehidden': False,

    "repository_url": cpanel.__url__,
    "use_repository_button": True,
}
suppress_warnings = ["config.cache"]
