import logging
import sys

LOG_FORMAT = "[%(asctime)s.%(msecs)03d] [%(levelname)s] [%(filename)s:%(lineno)d] : %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    stream=sys.stdout,
    force=True
)

def info(msg: str, *args, **kwargs) -> None:
    logging.info(msg, *args, **kwargs, stacklevel=2)


def error(msg: str, *args, **kwargs) -> None:
    logging.error(msg, *args, **kwargs, stacklevel=2)


def debug(msg: str, *args, **kwargs) -> None:
    logging.debug(msg, *args, **kwargs, stacklevel=2)


def warn(msg: str, *args, **kwargs) -> None:
    logging.warning(msg, *args, **kwargs, stacklevel=2)
    

# test
if __name__ == "__main__":
    info("Starting service...")