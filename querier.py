import requests
import json

def list_tags(host, name):
"""
List the list of tags for a repository from the newer versions

Parameters
----------
host : string
    Host address of docker registry
name : string
    Image name (username/image)
""" 
    r = requests.post(f'{host}/v2/repositories/{repository}/tags')
    if r.status_code != 200:
        raise RuntimeError("Failed to fetch data")
    body = json.loads(r.text)
    return map(lambda image: image["name"], body["results"])
