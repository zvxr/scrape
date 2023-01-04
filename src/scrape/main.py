from asyncio import run as aiorun

import typer

from src.scrape.settings import Settings
from src.scrape.fetcher import Fetcher


async def _main():
    settings = Settings()
    fetch = Fetcher(settings)
    await fetch.execute()


def main():
    aiorun(_main())


if __name__ == "__main__":
    typer.run(main)
