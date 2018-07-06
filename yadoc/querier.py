import requests
import json
import semantic_version
from typing import Dict, List, Tuple
from abc import abstractmethod, ABCMeta


class IQuerier(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def list_tags(host: str, name: str, limit: int=None) -> List[str]:
        raise NotImplementedError("list_tags is not implemented")


class Querier(IQuerier):
    @staticmethod
    def get_auth_info(host: str) -> Tuple[str, Dict[str, str]]:
        r = requests.get(f'https://{host}/v2/')
        www_auth = r.headers['WWW-Authenticate'].split(" ")
        assert len(www_auth) == 2, www_auth
        scheme, params_tmp = www_auth
        params: Dict[str, str] = dict(
            map(
                lambda s: (s.split("=")[0], s.split("=")[1]),
                params_tmp.replace("\"", "").split(",")
            )
        )
        assert "realm" in params, params
        return scheme, params

    @staticmethod
    def get_token(host: str, scope: str) -> str:
        scheme, params = Querier.get_auth_info(host)
        auth_url = \
            f'{params["realm"]}?service={params["service"]}&scope={scope}'
        r = requests.get(auth_url)
        body: Dict[str, str] = json.loads(r.text)
        assert "token" in body, body
        return body["token"]

    @staticmethod
    def sort_tags(tags: List[str], reverse: bool=True) -> List[str]:
        filtered_tags = filter(
            lambda tag: semantic_version.validate(tag), tags
        )
        return sorted(
            filtered_tags,
            key=lambda tag: semantic_version.Version(tag),
            reverse=reverse
        )

    @staticmethod
    def list_tags(host: str, name: str, limit: int=None) -> List[str]:
        """
        List the list of tags for a repository from the newer versions

        Parameters
        ----------
        name : string
            Image name (username/image)
        """

        scope = f"repository:{name}:pull"
        token = Querier.get_token(host, scope)
        headers = {
            'Authorization': f'Bearer {token}'
        }

        r = requests.get(
            f'https://{host}/v2/{name}/tags/list',
            headers=headers
        )
        if r.status_code != 200:
            raise RuntimeError(
                f'Failed to fetch data. Status code {r.status_code}'
            )

        body = json.loads(r.text)
        return Querier.sort_tags(body["tags"])[:limit]
