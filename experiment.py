import socket
import threading
from typing import Optional, Tuple

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Aby se mohl hned znovupouzit kdyz se na nem ukonci spojeni
s.bind(("0.0.0.0", 9494))  # Porty nizsi nez 1024 muzou chtit root
s.listen()  # Call na system, kdyz tam neco prijde tak to preda


# Prijme klienta kdyz se pripoji, client_socket je takovy network stream
# address -- slozitejsi struktura, obsahuje ip uzivatele

# Socket = data ve spravnym poradi a bez der.


def _safe_index(string: str, substring: str) -> Optional[int]:
    try:
        index = string.index(substring)
        return index
    except ValueError:
        return None


def socket_worker(client_socket: socket.socket):
    max_bytes_received = 32
    data_buffer = ""
    header_separators = ["\n\n", "\n\r\n"]

    while True:
        raw_new_data = client_socket.recv(max_bytes_received)
        new_data = str(raw_new_data, "ascii")
        data_buffer += new_data
        if any([header_separator in data_buffer for header_separator in header_separators]):
            break

    separator_to_index = {header_separator: _safe_index(data_buffer, header_separator)
                          for header_separator in header_separators}
    activated_separators = [header_separator for header_separator, index
                            in separator_to_index.items() if index is not None]
    assert len(activated_separators) == 1
    activated_separator = activated_separators[0]
    header = data_buffer.split(activated_separator)[0]

    _, relative_url, _, _ = parse_header(header)

    response = generate_response(relative_url)
    bytes_sent = client_socket.send(response)
    # TODO: Has to handle the case when not all bytes are sent
    client_socket.close()


def parse_header(request_header: str):
    request_header_lines = request_header.split("\n")
    http_method, relative_url, http_version = parse_first_request_header_line(request_header_lines[0])
    if len(request_header_lines) > 1:
        request_headers = request_header_lines[1:]

    header_name_to_header_content = dict()
    for header in request_headers:
        splitted_header = header.split(":")
        header_name = splitted_header[0]
        header_content = ":".join(splitted_header[1:])
        header_name_to_header_content[header_name] = header_content

    return http_method, relative_url, http_version, header_name_to_header_content


def generate_response(payload: str):
    html = payload_to_html(payload)
    bytes_html = html.encode("utf-8")
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


def payload_to_html(payload: str):
    return f"<!DOCTYPE html>" \
           f"<html lang=\"en\">" \
           f"<head>" \
           f"<meta charset=\"UTF-8\">" \
           f"<title>Title</title>" \
           f"</head>" \
           f"<body>{payload}</body>" \
           f"</html>"


def parse_first_request_header_line(first_header: str) -> Tuple[str, str, str]:
    http_method, relative_url, http_version = first_header.split(" ")
    return http_method, relative_url, http_version


while True:
    client_socket, address = s.accept()  # socket.socket.accept() vraci socket.socket

    threading.Thread(target=socket_worker, args=(client_socket,)).start()

    # client_socket.recv()
    # client_socket.send()
