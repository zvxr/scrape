from asyncio import run as aiorun

import typer

from src.app.settings import get_settings
from src.app.fetcher import Fetcher


async def _main():
    settings = get_settings()
    fetch = Fetcher(settings)
    await fetch.execute()


def main():
    aiorun(_main())


if __name__ == "__main__":
    typer.run(main)
