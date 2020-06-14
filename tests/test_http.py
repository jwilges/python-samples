from dataclasses import dataclass
from unittest import TestCase
from unittest.mock import MagicMock, patch

from samples._http import ContentType, HttpClient


class TestContentType(TestCase):
    def test_from_response(self):
        @dataclass
        class SubTest:
            content_type: str
            expected: ContentType

        subtests = [
            SubTest('text/plain', ContentType(type='text', subtype='plain')),
            SubTest('application/json', ContentType(type='application', subtype='json')),
            SubTest('application/json; charset=UTF-8', ContentType(type='application', subtype='json', attribute='charset', value='UTF-8')),
        ]
        for subtest in subtests:
            with self.subTest(subtest=subtest):
                mock_response = MagicMock(getheader=MagicMock(return_value=subtest.content_type))
                assert ContentType.from_response(mock_response) == subtest.expected

    def test_str(self):
        @dataclass
        class SubTest:
            content_type: ContentType
            expected: str

        subtests = [
            SubTest(ContentType(type='text', subtype='plain'), 'text/plain'),
            SubTest(ContentType(type='application', subtype='json'), 'application/json'),
            SubTest(ContentType(type='application', subtype='json', attribute='charset', value='UTF-8'), 'application/json; charset=UTF-8'),
        ]
        for subtest in subtests:
            with self.subTest(subtest=subtest):
                assert str(subtest.content_type) == subtest.expected

    def test_is_json(self):
        @dataclass
        class SubTest:
            content_type: ContentType
            expected: bool

        subtests = [
            SubTest(ContentType(type='text', subtype='plain'), 'text/plain'),
            SubTest(ContentType(type='application', subtype='json'), 'application/json'),
            SubTest(ContentType(type='application', subtype='json', attribute='charset', value='UTF-8'), 'application/json; charset=UTF-8'),
        ]
        for subtest in subtests:
            with self.subTest(subtest=subtest):
                assert str(subtest.content_type) == subtest.expected


class TestHttpClient(TestCase):
    def test_get(self):
        mock_response = MagicMock()
        with patch.object(HttpClient, '_request', return_value=mock_response) as mock_request:
            expected_url = MagicMock(name='url')
            expected_query = MagicMock(name='query')
            expected_headers = MagicMock(name='headers')
            response = HttpClient.get(expected_url, query=expected_query, headers=expected_headers)
            assert response == mock_response
            mock_request.assert_called_with(expected_url, method='GET', query=expected_query, headers=expected_headers)

    def test_patch(self):
        mock_response = MagicMock()
        with patch.object(HttpClient, '_request', return_value=mock_response) as mock_request:
            expected_url = MagicMock(name='url')
            expected_query = MagicMock(name='query')
            expected_headers = MagicMock(name='headers')
            expected_encoded_data = MagicMock(name='encoded-data')
            expected_data = MagicMock(name='data', spec=str, encode=MagicMock(return_value=expected_encoded_data))
            expected_encoding = MagicMock(name='utf-8')
            response = HttpClient.patch(expected_url, query=expected_query, headers=expected_headers, data=expected_data, encoding=expected_encoding)
            assert response == mock_response
            mock_request.assert_called_with(expected_url, method='PATCH', query=expected_query, headers=expected_headers, data=expected_encoded_data)

    def test_post(self):
        mock_response = MagicMock()
        with patch.object(HttpClient, '_request', return_value=mock_response) as mock_request:
            expected_url = MagicMock(name='url')
            expected_query = MagicMock(name='query')
            expected_headers = MagicMock(name='headers')
            expected_encoded_data = MagicMock(name='encoded-data')
            expected_data = MagicMock(name='data', spec=str, encode=MagicMock(return_value=expected_encoded_data))
            expected_encoding = MagicMock(name='utf-8')
            response = HttpClient.post(expected_url, query=expected_query, headers=expected_headers, data=expected_data, encoding=expected_encoding)
            assert response == mock_response
            mock_request.assert_called_with(expected_url, method='POST', query=expected_query, headers=expected_headers, data=expected_encoded_data)
