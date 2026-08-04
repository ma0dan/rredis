import sys


def simple_string(s):
    return f"+{s}\r\n"

def error(msg):
    return f"-{msg}\r\n"

def integer(n):
    return f":{n}\r\n"

def bulk_string(s):
    if s is None:
        return "$-1\r\n"
    return f"${len(s)}\r\n{s}\r\n"


def cmd_ping(args):
    """Process a Redis command and return the RESP response."""
    s = ' '.join(args)
    if s:
        return bulk_string(s)
    return "+PONG\r\n"

def cmd_echo(args):
    s = ' '.join(args)
    return bulk_string(s)

def cmd_commnad(args):
    s = ' '.join(args)
    if s.upper() == 'DOCS':
        return simple_string("OK")
    return error(f"ERR unknown command COMMAND")

ARITY = {
    "PING": (0, 1),
    "ECHO": (1, 1),
    "COMMAND": (1, 2)
}

HANDLERS = {'PING': cmd_ping, 'ECHO': cmd_echo, 'COMMAND': cmd_commnad}

def check_artiy(cmd, args):
    lo, hi = ARITY[cmd]
    if not (lo <= len(args) <= hi):
        return error(f"ERR wrong number of arguments for '{cmd.upper()}' command")
    return None

def handle_command(args):
    cmd = args[0].upper()
    handler = HANDLERS.get(cmd)
    if handler:
        err = check_artiy(cmd, args[1:])
        return err if err else handler(args[1:])
    return error(f"ERR unknown command '{cmd}'")


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        args = parse_args(line)
        response = handle_command(args)
        sys.stdout.write(response)
        sys.stdout.flush()

def parse_args(line):
    """Split a command line into arguments, handling quoted strings."""
    args = []
    current = ""
    in_quotes = False
    for ch in line:
        if ch == '"' and not in_quotes:
            in_quotes = True
        elif ch == '"' and in_quotes:
            in_quotes = False
        elif ch == ' ' and not in_quotes:
            if current:
                args.append(current)
                current = ""
        else:
            current += ch
    if current:
        args.append(current)
    return args

if __name__ == "__main__":
    main()
