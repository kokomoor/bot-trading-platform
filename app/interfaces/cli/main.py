"""CLI placeholder entrypoint."""

from app.core.logging import get_logger

logger = get_logger(interface="cli")


def main() -> None:
    logger.info("cli.startup")


if __name__ == "__main__":
    main()
