import httpx
from bs4 import BeautifulSoup

from src.scrape.settings import Settings
from src.scrape.console import console


class Scraper:
    def __init__(self, settings: Settings):
        self.base_url = settings.fetcher_base_url
        self.relative_urls = settings.fetcher_relative_urls
        self.resources_path = settings.db_resources_path
        self.resources_left = settings.fetcher_max_resources
        self.max_depth = settings.fetcher_max_depth

    async def crawl(self, client, relative_url, depth=0):
        if not self.resources_left:
            console.log(f"No more resources to process. Aborting {relative_url}.")
            return

        if depth > self.max_depth:
            console.log(f"Maximum depth reached. Aborting {relative_url}.")
            return

        resp = await client.get(f"{self.base_url}{relative_url}")
        html = resp.content
        soup = BeautifulSoup(html)

        # Check if resource is a table.
        table = soup.find_all("table")
        if len(table) > 0:
            console.log(f"Table detected in {relative_url}: processing {len(table)} items.")
            for link in table[0].find_all("a"):
                link_url = link.get("href")
                if link_url.split("/")[-1].split(".")[-1] == "html":
                    await self.crawl(client, f"{relative_url}/{link_url}", depth=depth + 1)
                # TODO -- handle non html/href?
        else:
            await self.process(relative_url, html)
            self.resources_left -= 1

    async def process(self, relative_url, html):
        console.log(f"process {relative_url}.")

    async def execute(self) -> bool:
        async with httpx.AsyncClient() as client:
            for relative_url in self.relative_urls:
                if not self.resources_left:
                    console.log("No more resources to process. Ending execute.")
                    return True
                await self.crawl(client, relative_url)

