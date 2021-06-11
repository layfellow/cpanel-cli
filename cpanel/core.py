import cpanel

def version() -> str:
	return "{} client version {}".format(cpanel.__description__, cpanel.__version__)
