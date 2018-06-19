import argparse
import querier

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Get tags from docker repository'
    )
    parser.add_argument(
        '-r', '--registry',
        default="registry-1.docker.io",
        help="Host name of the registry"
    )
    subparsers = parser.add_subparsers(help='List of subcommands', dest="subcommand_name")

    parser_tag = subparsers.add_parser('tag', help='tag help')
    parser_tag.add_argument(
        'name',
        help="name of a docker image including repository name"
    )

    args = parser.parse_args()

    if args.subcommand_name == "tag":
        tags = querier.list_tags(args.registry, args.name)
        for tag in tags:
            print(tag)

    else:
        raise ValueError(f"Unexpected subcommand {args.subcommand_name}")
