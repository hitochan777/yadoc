import argparse
# import querier

# curl https://auth.docker.io/token?service=registry.docker.io&scope=repository:weseek/growi:pull
# curl -i -H "Authorization: Bearer $TOKEN" https://registry-1.docker.io/v2/weseek/growi/tags/list

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get tags from docker repository')
    parser.add_argument('name', help="name of a docker image including repository name")
    parser.add_argument('-r', '--registry', default="registry-1.docker.io", help="Host name of the registry")
    args = parser.parse_args()
    print(args)
    # tags = querier.listTags("weseek/growi")
    # print(list(tags))
