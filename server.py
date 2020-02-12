from typing import Callable

from listener import Listener
from logging import log_request
from processor import Processor
from response import Response
from response_queue import ResponseQueue

STATIC_PATH = "./static/"
TEMPLATES_PATH = "./templates/"

SUFFIX_TO_CONTENT_TYPE = {"jpg": "text/html", "html": "text/html", "js": "application/javascript"}
DEFAULT_CONTENT_TYPE = "text/html"


def render_template(template_name: str = "index.html", **kwargs):
    template_path = TEMPLATES_PATH + template_name
    with open(template_path, "r") as template:
        template_lines = template.readlines()

    template_str = "\n".join(template_lines)
    rendered_template = template_str

    for key, value in kwargs.items():
        rendered_template = rendered_template.replace("{" + key + "}", value)

    return rendered_template


def response_from_file_name(file_name: str) -> Response:
    absolute_path = STATIC_PATH + file_name

    with open(absolute_path, "rb") as file:
        payload = file.read()

    file_extension = file_name.split(".")[-1]
    content_type = SUFFIX_TO_CONTENT_TYPE.get(file_extension, DEFAULT_CONTENT_TYPE)

    return Response(payload, headers={"Content-Type": content_type})

class Server(object):
    def __init__(self, host: str = "0.0.0.0", port: int = 9494):
        self._processor = Processor()
        self._response_queue = ResponseQueue()
        self._listener = Listener(host, port)

        self._init()

    def _init(self):
        self._listener.add_subscriber(self._processor.enqueue)
        self._listener.add_subscriber(log_request)
        self._processor.add_subscriber(self._response_queue.enqueue)

    def start(self):
        self._processor.start()
        self._response_queue.start()
        self._listener.listen()

    def web(self, action: Callable):
        action_name = action.__name__
        self._processor.add_action(action_name, action)
