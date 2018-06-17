import argparse
import querier

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Get tags from docker repository'
    )
    parser.add_argument(
        'name',
        help="name of a docker image including repository name"
    )
    parser.add_argument(
        '-r', '--registry',
        default="registry-1.docker.io",
        help="Host name of the registry"
    )

    args = parser.parse_args()
    tags = querier.list_tags(args.registry, args.name)
    for tag in tags:
        print(tag)
