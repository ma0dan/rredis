import sys


def bulk_string(args):
    body = ' '.join(args)
    length = len(body)
    return f"${length}\r\n{body}\r\n"

def cmd_ping(args):
    """Process a Redis command and return the RESP response."""
    if args:
        return bulk_string(args)
    return "+PONG\r\n"

def cmd_echo(args):
    if args:
        return bulk_string(args)

HANDLERS = {'PING': cmd_ping, 'ECHO': cmd_echo}

def handle_command(args):
    cmd = args[0].upper()
    handler = HANDLERS.get(cmd)
    if handler:
        return handler(args[1:])
    return "-ERR unknown command\r\n"


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
