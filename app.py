from server import Server

server = Server()


def _payload_to_html(payload: str):
    return f"<!DOCTYPE html>" \
           f"<html lang=\"en\">" \
           f"<head>" \
           f"<meta charset=\"UTF-8\">" \
           f"<title>Title</title>" \
           f"</head>" \
           f"<body>{payload}</body>" \
           f"</html>"


@server.web
def index(x, y):
    return _payload_to_html(str(int(x) ** 2 + int(y) ** 2))


server.start()
