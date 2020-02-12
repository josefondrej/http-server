from server import Server

# Test: go to browser http://0.0.0.0:9494/index?x=2&y=4
host = "0.0.0.0"
port = 9494

server = Server(host, port)

STATIC_PATH = "./static/"
TEMPLATES_PATH = "./templates/"


def _render_template(template_name: str = "index.html", **kwargs):
    template_path = TEMPLATES_PATH + template_name
    with open(template_path, "r") as template:
        template_lines = template.readlines()

    template_str = "\n".join(template_lines)
    rendered_template = template_str

    for key, value in kwargs.items():
        rendered_template = rendered_template.replace("{" + key + "}", value)

    return rendered_template

@server.web
def index(x, y):
    payload = str(int(x) ** 2 + int(y) ** 2)
    return _render_template("index.html", payload=payload)


server.start()
