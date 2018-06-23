import unittest
import responses
from .querier import Querier


class TestQuerier(unittest.TestCase):
    def test_sort_tags(self):
        tags = [
            "2.1.14", "3.0.0", "3.0.3", "3.0.2", "3.0.4",
            "1.0.0", "1.0.2", "3.0.10-alpha", "3.0.10", "3.0.5"
        ]

        expected_tags = [
            '3.0.10', '3.0.10-alpha', '3.0.5', '3.0.4',
            '3.0.3', '3.0.2', '3.0.0', '2.1.14', '1.0.2',
            '1.0.0'
        ]

        self.assertEqual(Querier.sort_tags(tags), expected_tags)

    def test_sort_tags_from_old_ones(self):
        tags = [
            "2.1.14", "3.0.0", "3.0.3", "3.0.2", "3.0.4",
            "1.0.0", "1.0.2", "3.0.10-alpha", "3.0.10", "3.0.5"
        ]

        expected_tags = [
            '1.0.0', '1.0.2', '2.1.14', '3.0.0', '3.0.2',
            '3.0.3', '3.0.4', '3.0.5', '3.0.10-alpha', '3.0.10',
        ]

        self.assertEqual(Querier.sort_tags(tags, reverse=False), expected_tags)

    @responses.activate
    def test_list_tags_returns_5_tags_from_the_new_ones(self):
        returnedTags = [
            "2.1.14", "3.0.0", "3.0.3", "3.0.2", "3.0.4",
            "1.0.0", "1.0.2", "3.0.10-alpha", "3.0.10", "3.0.5"
        ]

        expected_tags = [
            '3.0.10', '3.0.10-alpha', '3.0.5', '3.0.4', '3.0.3'
        ]

        responses.add(**{
            'method': responses.GET,
            'url': 'https://hitochan777.registry.io\
                   /v2/hitochan777/sample-repo/tags/list',
            'json': {
                'tags': returnedTags
            },
            'status': 200,
        })
        responses.add(**{
            'method': responses.GET,
            'url': 'https://hitochan777.registry.io/v2/',
            'headers': {
                'WWW-Authenticate': 'Bearer\
                    realm="https://hitochan777.docker.io/token",\
                    service="hitochan777.registry.io"'
            },
            'status': 200
        })
        responses.add(**{
            'method': responses.GET,
            'url': 'https://hitochan777.docker.io/token',
            'json': {
                'token': "THIS IS A DUMMY TOKEN"
            },
            'status': 200
        })

        tags = Querier.list_tags(
            "hitochan777.registry.io",
            "hitochan777/sample-repo",
            limit=5
        )
        self.assertEqual(tags, expected_tags)


if __name__ == '__main__':
    unittest.main()
