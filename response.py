from typing import Dict

from request import Request

DEFAULT_HEADERS = {
    "Server": "Pepuv super server",
    "Content-Length": 0,
    "Content-Type": "text/html",
    "Connection": "Closed"
}

DEFAULT_STATUS_MESSAGE = ""
STATUS_CODE_TO_STATUS_MESSAGE = {200: "OK", 404: "NOT_FOUND"}


class Response(object):
    def __init__(self, content: str, request: Request,
                 headers: Dict[str, str] = None,
                 status_code: int = 200):  # TODO: add request as a parameter and access socket through that
        self._content = content
        self._request = request
        self._headers = headers
        self._status_code = status_code

    @property
    def client_socket(self):
        return self._request._socket

    def serialize(self):
        content = self._content
        bytes_html = content.encode("utf-8")
        http_version = "HTTP/1.1"
        status_code = str(self._status_code)
        status_message = STATUS_CODE_TO_STATUS_MESSAGE[self._status_code]
        headers = DEFAULT_HEADERS
        headers["Content-Length"] = len(bytes_html)
        if self._headers is not None:
            for header_name, header_value in self._headers:
                headers[header_name] = header_value

        first_line = " ".join([http_version, status_code, status_message])
        next_lines = [str(name) + ":" + str(content) for name, content in headers.items()]
        header = first_line + "\n" + "\n".join(next_lines) + "\n\r\n"
        return header.encode("utf-8") + bytes_html
