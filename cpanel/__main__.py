import sys
import cpanel_api
from typing import List
from .core import version

def main() -> None:
	args: List[str] = sys.argv[1:]
	if args[0] == 'version':
		print(version())

if __name__ == '__main__':
	main()
