import socket


class Response(object):
    def __init__(self, content: str, client_socket: socket.socket): # TODO: add request as a parameter and access socket through that
        self._content = content
        self._client_socket = client_socket

    @property
    def client_socket(self):
        return self._client_socket

    def serialize(self):
        content = self._content
        bytes_html = content.encode("utf-8")
        http_version, status_code, status_message = "HTTP/1.1", "200", "OK"
        headers = {
            "Server": "Pepuv super server",
            "Content-Length": len(bytes_html),
            "Content-Type": "text/html",
            "Connection": "Closed"
        }
        first_line = " ".join([http_version, status_code, status_message])
        next_lines = [str(name) + ":" + str(content) for name, content in headers.items()]
        header = first_line + "\n" + "\n".join(next_lines) + "\n\r\n"
        return header.encode("utf-8") + bytes_html
