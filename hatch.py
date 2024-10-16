from hatchling.metadata.plugin.interface import MetadataHookInterface

def parse_init(src):
	metadata = {}
	with open(src, 'r') as stream:
		for line in stream:
			pair = line.split(" = ")
			metadata[pair[0]] = pair[1][pair[1].find("'") + 1:pair[1].find("'", 2)]  # Remove quotes
	return metadata


class JSONMetaDataHook(MetadataHookInterface):
	def update(self, metadata):
		cpanel_init = parse_init('cpanel/__init__.py')
		metadata['version'] = cpanel_init['__version__']
		metadata['authors'] = [{
			'name': cpanel_init['__author__'],
			'email': cpanel_init['__email__']
		}]
		metadata['description'] = cpanel_init['__description__']
		metadata['urls'] = {
			'Homepage': cpanel_init['__url__'],
			'Documentation': "https://cpanel-cli.readthedocs.io/",
			'Repository': cpanel_init['__url__'],
			'Bug Tracker': cpanel_init['__url__'] + '/issues'
		}
