import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s : %(message)s",
    stream=sys.stdout
)

logger = logging.getLogger("ai-music-perception")


def info(message: str) -> None:
    logger.info(message)


def error(message: str) -> None:
    logger.error(message)


def debug(message: str) -> None:
    logger.debug(message)


def warn(message: str) -> None:
    logger.warning(message)