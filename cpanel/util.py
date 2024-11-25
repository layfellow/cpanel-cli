from .core import CPanelError

def cmd_is(command: str, *arglist: str) -> bool:
	for arg in arglist:
		if command[0:len(arg)] == arg:
			return True
	return False


def username(email: str) -> str:
	n: int = email.find("@")
	if n < 0:
		raise CPanelError("invalid email, {}".format(email))
	return email[:n]


def domain(email: str) -> str:
	n: int = email.find("@")
	if n < 0:
		raise CPanelError("invalid email, {}".format(email))
	return email[n + 1:]
