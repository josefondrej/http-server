import socket
from threading import Thread
from typing import Optional, Tuple

from request import Request

HEADER_SEPARATORS = ["\n\n", "\n\r\n"]


class Downloader(Thread):
    def __init__(self, client_socket: socket.socket, address: str, max_bytes_received: int = 32):
        self._client_socket = client_socket
        self._address = address
        self._max_bytes_received = max_bytes_received

        super().__init__()

    def _on_request_accepted(self, request: Request):
        pass

    def run(self):
        data_buffer = ""

        while True:  # Tady naparsuju headery, kdyz bych chtel parsovat body, tak si z headeru prectu content length a cekam az naparsuju celou tu lenght
            raw_new_data = self._client_socket.recv(self._max_bytes_received)
            new_data = str(raw_new_data, "ascii")
            data_buffer += new_data
            if any([header_separator in data_buffer for header_separator in HEADER_SEPARATORS]):
                break

        separator_to_index = {header_separator: self._safe_index(data_buffer, header_separator)
                              for header_separator in HEADER_SEPARATORS}
        activated_separators = [header_separator for header_separator, index
                                in separator_to_index.items() if index is not None]
        assert len(activated_separators) == 1
        activated_separator = activated_separators[0]
        header = data_buffer.split(activated_separator)[0]

        http_method, relative_url, http_version, header_name_to_header_content = self._parse_header(header)
        request = Request(http_method, relative_url, http_version, header_name_to_header_content, self._client_socket)
        self._on_request_accepted(request)

    def _safe_index(self, string: str, substring: str) -> Optional[int]:
        try:
            index = string.index(substring)
            return index
        except ValueError:
            return None

    def _parse_header(self, request_header: str):
        request_header_lines = request_header.split("\n")
        http_method, relative_url, http_version = self._parse_first_request_header_line(request_header_lines[0])
        if len(request_header_lines) > 1:
            request_headers = request_header_lines[1:]

        header_name_to_header_content = dict()
        for header in request_headers:
            splitted_header = header.split(":")
            header_name = splitted_header[0]
            header_content = ":".join(splitted_header[1:])
            header_name_to_header_content[header_name] = header_content

        return http_method, relative_url, http_version, header_name_to_header_content

    def _parse_first_request_header_line(self, first_header: str) -> Tuple[str, str, str]:
        http_method, relative_url, http_version = first_header.split(" ")
        return http_method, relative_url, http_version
