from typing import Dict
import socket


class Request(object):
    def __init__(self, http_method: str, relative_url: str, http_version: str,
                 header_name_to_header_content: Dict[str, str], socket: socket.socket):
        self._http_method = http_method
        self._relative_url = relative_url
        self._http_version = http_version
        self._header_name_to_header_content = header_name_to_header_content
        self._socket = socket

    def __str__(self) -> str:
        representation = f"{self._http_method} {self._relative_url} {self._http_version}\n"
        for header_name, header_content in self._header_name_to_header_content.items():
            representation += f"{header_name}: {header_content}\n"

        return representation

    @property
    def client_socket(self) -> socket.socket:
        return self._socket
