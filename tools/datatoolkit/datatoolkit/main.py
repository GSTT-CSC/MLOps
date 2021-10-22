import argparse
import sys
import traceback


from datatoolkit.init import init
from datatoolkit.view import view
from datatoolkit.error import print_error


def main():
    try:
        exit_code = cli(sys.argv[1:])
        sys.exit(exit_code)
    except Exception:
        print_error(traceback.format_exc())
        sys.exit(1)


def cli(raw_arguments):
    exit_code = 0
    args = parse_arguments(raw_arguments)
    if args.command is None:
        parse_arguments(['-h'])
    elif args.command == 'init':
        init()
    elif args.command == 'view':
        view()
    return exit_code


def parse_arguments(arguments):
    parser = argparse.ArgumentParser(prog='datatoolkit')
    subparsers = parser.add_subparsers(dest='command', metavar='<command>')

    init_help = 'generate yaml file for a given MLOps project'
    init_parser = subparsers.add_parser('init', help=init_help)
    init_output_help = 'Path where templates are copied'
    init_parser.add_argument('-o', '--output', default='regulatory', help=init_output_help)


    view_help = 'data frame of the yaml files for different projects'
    view_parser = subparsers.add_parser('view', help=view_help)
    view_output_help = 'Path where templates are copied'
    view_parser.add_argument('-o', '--output', default='regulatory', help=view_output_help)

    return parser.parse_args(arguments)


if __name__ == '__main__':
    main()
