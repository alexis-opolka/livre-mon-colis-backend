import logging
from datetime import datetime

### We configure the logging util
logging.basicConfig(filename="./livre-mon-colis.log", encoding="utf-8", level=logging.DEBUG)

def logRoute(route: str, type: str):
    logging.debug(f"[{datetime.now()}] - ROUTE [{type}]: `{route}`")

### Two `logRoute` wrappers
def logGETRoute(route: str) -> None:
    logRoute(route, type="GET")

def logPOSTRoute(route: str) -> None:
    logRoute(route, type="POST")

def log(msg: str) -> None:
    logging.info(f"[{datetime.now()}]: {msg}")

def warn(msg: str) -> None:
    logging.warning(f"[{datetime.now()}]: {msg}")

def error(msg: str) -> None:
    logging.error(f"[{datetime.now()}]: {msg}")