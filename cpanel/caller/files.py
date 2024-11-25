from typing import List
from cpanel_api import Api
from ..core import CPanelEndpoint
from ..util import cmd_is


def call(host: CPanelEndpoint, cmd: str, args: List[str]) -> str:
	r: str = ""
	uapi: Api = host.client.uapi

	if cmd_is(cmd, "list files"):
		r = host.dump(lambda: uapi.Fileman.list_files(
			dirs = args[2] if len(args) > 2 else '/', include_mime = 1, include_permissions = 1, show_hidden = 1))

	elif cmd_is(cmd, "glob files"):
		r = host.dump(lambda: uapi.Fileman.autocompletedir(path = args[2], html = 0))

	elif cmd_is(cmd, "get file info"):
		r = host.dump(lambda: uapi.Fileman.get_file_information(
			path = args[3], include_mime = 1, include_permissions = 1, show_hidden = 1))

	elif cmd_is(cmd, "cat file"):
		r = host.get_file_contents(args[2]).decode('utf-8')

	elif cmd_is(cmd, "write file"):
		r = host.write_file(args[2], args[3])

	elif cmd_is(cmd, "upload file"):
		r = host.upload_file(args[2], args[3])

	elif cmd_is(cmd, "delete file trash", "rm file trash", "remove file trash"):
		r = host.check(lambda: uapi.Fileman.empty_trash(older_than = int(args[3]) if len(args) > 3 else 0))

	return r
