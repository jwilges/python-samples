from __future__ import annotations

import http.client
import json
import logging
import re

from collections import namedtuple
from dataclasses import dataclass
from typing import ClassVar, Mapping, Optional, Pattern
from urllib.parse import urlencode
from urllib.request import urlopen, Request


@dataclass(frozen=True)
class ContentType:
    '''An HTTP Content Type based on the RFC 1521 definition in Section 4: The Content-Type Header Field

    See: <https://tools.ietf.org/html/rfc1521#page-9>'''
    FORMAT: ClassVar[Pattern] = re.compile(r'^(?P<type>[^/\s]+)/(?P<subtype>[^;\s]+)(?:\s*;\s*(?P<attribute>[^=]+)=(?P<value>.+))?$')

    type: str
    subtype: str
    attribute: Optional[str] = None
    value: Optional[str] = None

    def __str__(self) -> str:
        mime_type = f'{self.type}/{self.subtype}'
        if self.attribute or self.value:
            return f'{mime_type}; {"=".join((self.attribute, self.value))}'
        return mime_type

    def is_json(self) -> bool:
        return f'{self.type}/{self.subtype}'.lower() == 'application/json'

    @classmethod
    def from_response(cls, response: http.client.HTTPResponse) -> ContentType:
        content_type = response.getheader('Content-Type', '')
        content_type_match = cls.FORMAT.match(content_type)
        if not content_type_match:
            return ContentType(type='text', subtype='plain')
        return ContentType(**content_type_match.groupdict())


@dataclass
class HttpResponse:
    raw: http.client.HTTPResponse
    content_type: ContentType
    data: object


class HttpClient:
    LOGGER: ClassVar[logging.Logger] = logging.getLogger(__qualname__)

    @classmethod
    def _request(cls, url: str, method: str, query: Mapping[str, str] = {}, data: bytes = None, **kwargs) -> HttpResponse:
        if query:
            url += f'?{urlencode(query)}'
        request = Request(url=url, data=data, method=method, **kwargs)
        cls.LOGGER.debug('%s: %s', method, request.full_url)

        response: http.client.HTTPResponse
        with urlopen(request) as response:
            content_type = ContentType.from_response(response)
            content_length = response.getheader('Content-Length')
            content_bytes = response.read(int(content_length)) if content_length else response.read()
            if content_type.is_json():
                return HttpResponse(raw=response, content_type=content_type, data=json.loads(content_bytes))
            return HttpResponse(raw=response, content_type=content_type, data=content_bytes)

    @classmethod
    def get(cls, url: str, query: Mapping[str, str] = {}, headers: Mapping[str, str] = {}) -> HttpResponse:
        return cls._request(url, method='GET', query=query, headers=headers)

    @classmethod
    def patch(cls, url: str, query: Mapping[str, str] = {}, headers: Mapping[str, str] = {},
              data: Optional[bytes] = None, encoding: Optional[str] = 'utf-8') -> HttpResponse:
        data = data.encode(encoding) if isinstance(data, str) else data
        return cls._request(url, method='PATCH', query=query, data=data, headers=headers)

    @classmethod
    def post(cls, url: str, query: Mapping[str, str] = {}, headers: Mapping[str, str] = {},
             data: Optional[bytes] = None, encoding: Optional[str] = 'utf-8') -> HttpResponse:
        data = data.encode(encoding) if isinstance(data, str) else data
        return cls._request(url, method='POST', query=query, data=data, headers=headers)
