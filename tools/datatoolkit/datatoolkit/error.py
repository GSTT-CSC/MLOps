import sys 

RED_ANSI = '\033[31m'
END_COLOR_ANSI = '\033[0m'

def print_error(message):
    print(RED_ANSI + message + END_COLOR_ANSI, file=sys.stderr)
