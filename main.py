import argparse
from querier import IQuerier, Querier


def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Get tags from docker repository'
    )
    parser.add_argument(
        '-r', '--registry',
        default="registry-1.docker.io",
        help="Host name of the registry"
    )
    subparsers = parser.add_subparsers(
        help='List of subcommands',
        dest="subcommand_name"
    )

    parser_tag = subparsers.add_parser('tag', help='tag help')
    parser_tag.add_argument(
        'name',
        help="name of a docker image including repository name"
    )
    parser_tag.add_argument(
        '-l', '--limit',
        type=int,
        default=None,
        help="Number of tags to print"
    )
    args = parser.parse_args()
    return args


def run(querier: IQuerier):
    args = parse_cli()
    if args.subcommand_name == "tag":
        tags = querier.list_tags(args.registry, args.name, args.limit)
        for tag in tags:
            print(tag)

    else:
        raise ValueError(f"Unexpected subcommand {args.subcommand_name}")


if __name__ == "__main__":
    run(Querier())
