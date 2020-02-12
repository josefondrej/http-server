from server import Server, response_from_file_name, render_template

# Test: go to browser http://0.0.0.0:9494/index?x=2&y=4
#                     http://0.0.0.0:9494/static?path=img/img_lights.jpg
#                     http://0.0.0.0:9494/static?path=example.html

host = "0.0.0.0"
port = 9494

server = Server(host, port)

@server.web
def index(x, y):
    payload = str(int(x) ** 2 + int(y) ** 2)
    return render_template("index.html", payload=payload)

@server.web
def static(path: str):
    return response_from_file_name(path)

server.start()
