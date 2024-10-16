import cpanel

from hatchling.metadata.plugin.interface import MetadataHookInterface

class JSONMetaDataHook(MetadataHookInterface):
	def update(self, metadata):
		metadata['version'] = cpanel.__version__
		metadata['authors'] = [{ 'name': cpanel.__author__, 'email': cpanel.__email__ }]
		metadata['description'] = cpanel.__description__
		metadata['urls'] = {
			'Homepage': cpanel.__url__,
			'Documentation': "https://cpanel-cli.readthedocs.io/",
			'Repository': cpanel.__url__,
			'Bug Tracker': cpanel.__url__ + '/issues'
		}
