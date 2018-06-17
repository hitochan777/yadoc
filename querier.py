import requests
import json

def get_auth_info(host):
    r = requests.get(f'https://{host}/v2/')
    www_auth = r.headers['WWW-Authenticate'].split(" ")
    assert(len(www_auth) == 2)
    scheme, params_tmp = www_auth
    params = dict(map(lambda s: s.split("="), params_tmp.replace("\"", "").split(",")))
    assert("realm" in params)
    return scheme, params

def get_token(host, scope):
    scheme, params = get_auth_info(host)
    auth_url = f'{params["realm"]}?service={params["service"]}&scope={scope}'
    r = requests.get(auth_url)
    body = json.loads(r.text)
    assert("token" in body)
    return body["token"]

def list_tags(host, name):
    """
    List the list of tags for a repository from the newer versions
    
    Parameters
    ----------
    name : string
        Image name (username/image)
    """ 

    scope = f"repository:{name}:pull"
    token = get_token(host, scope)
    headers = {
        'Authorization': f'Bearer {token}'
    }

    r = requests.get(f'https://{host}/v2/{name}/tags/list', headers=headers)
    if r.status_code != 200:
        print(r.text)
        raise RuntimeError(f'Failed to fetch data. Status code {r.status_code}')

    body = json.loads(r.text)
    return body["tags"]
