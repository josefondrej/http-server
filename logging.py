from request import Request
from colorama import Fore, Style


def log_request(request: Request):
    print(f"{Fore.GREEN}[INFO]{Style.RESET_ALL} New request.")
    print(str(request))
