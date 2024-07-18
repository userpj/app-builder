# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import json
from urllib.parse import urlparse
from requests import Response

from appbuilder.utils.logger_util import logger
from appbuilder.utils.trace.tracer_wrapper import session_post
from baidubce.http import (
    bce_http_client,
    handler,
    http_methods,
)

from baidubce import bce_client_configuration


def sign(
    credentials,
    http_method,
    path,
    headers,
    params,
    timestamp=0,
    expiration_in_seconds=1800,
    headers_to_sign=None,
):
    return headers.get("Authorization")


class InnerSession(requests.sessions.Session):

    def __init__(self, *args, **kwargs):
        """
        Initialize inner session.
        """
        super(InnerSession, self).__init__(*args, **kwargs)

    def build_curl(self, request: requests.PreparedRequest) -> str:
        """
        Generate cURL command from prepared request object.
        """
        curl = "curl -X {0} -L '{1}' \\\n".format(request.method, request.url)
        headers = [
            "-H '{0}: {1}' \\".format(k, v)
            for k, v in request.headers.items()
            if k != "Content-Length"
        ]
        if headers:
            headers[-1] = headers[-1].rstrip(" \\")
        curl += "\n".join(headers)
        if request.body:
            try:
                body = json.loads(request.body)
                body = "'{0}'".format(json.dumps(body, ensure_ascii=False))
                curl += " \\\n-d {0}".format(body)
            except:
                curl += " \\\n-d '{0}'".format(request.body)
        return curl

    def send(self, request, **kwargs):
        """
        Send request using inner session.
        """
        logger.debug("Curl Command:\n" + self.build_curl(request) + "\n")
        return super(InnerSession, self).send(request, **kwargs)

    def _send_request(
        self,
        http_method,
        url,
        body=None,
        data=None,
        headers=None,
        params=None,
        config=None,
        body_parser=None,
        timeout=None,
    ):
        """ """
        if config is None:
            config = bce_client_configuration.DEFAULT_CONFIG
        if body_parser is None:
            body_parser = handler.parse_json
        if timeout is not None:
            config.connection_timeout_in_mills = timeout * 1000
        if url is not None:
            parsed_url = urlparse(url)
            config.endpoint = (parsed_url.scheme + "://" + parsed_url.netloc).encode()
            path = parsed_url.path
        if data is not None:
            body = data
        resp = bce_http_client.send_request(
            config,
            sign,
            [handler.parse_error, body_parser],
            http_method,
            path,
            body,
            headers,
            params,
        )
        print(resp)
        return resp

    @session_post
    def post(self, url, **kwargs):
        # return super().post(url=url, **kwargs)
        return self._send_request(http_methods.POST, url, **kwargs)

    @session_post
    def delete(self, url, **kwargs):
        return self._send_request(http_methods.POST, url, **kwargs)

    @session_post
    def get(self, url, **kwargs):
        return self._send_request(http_methods.GET, url, **kwargs)

    @session_post
    def put(self, url, data=None, **kwargs):
        return super().put(url=url, data=data, **kwargs)
