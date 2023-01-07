import httpx
from bs4 import BeautifulSoup

from src.scrape.db import db_session
from src.scrape.console import console
from src.scrape.settings import Settings
from src.scrape.data_mappers.documents import get_document


class Fetcher:
    def __init__(self, settings: Settings):
        self.base_url = settings.fetcher_base_url
        self.relative_urls = settings.fetcher_relative_urls
        self.resources_path = settings.db_resources_path
        self.resources_left = settings.fetcher_max_resources
        self.max_depth = settings.fetcher_max_depth
        console.log(f"Loaded {self}")

    def __repr__(self):
        return f"Fetcher(base_url={self.base_url} resources_left={self.resources_left}"

    async def crawl(self, client, relative_url, depth=0):
        if not self.resources_left:
            console.log(f"No more resources to process. Aborting {relative_url}.")
            return

        if depth > self.max_depth:
            console.log(f"Maximum depth reached. Aborting {relative_url}.")
            return

        url = f"{self.base_url}{relative_url}"
        resp = await client.get(url)
        if not 200 <= resp.status_code < 300:
            console.log(f"Non 2xx response from {url}: {resp.content}")
            return

        html = resp.content
        soup = BeautifulSoup(html, features="html.parser")

        if len(soup.find_all("table")) == 1:
            urls = [row.text for row in soup.find_all("table")[0].find_all('a', href=True)]
        else:
            # TODO clean-up, maybe use function
            urls = [row.find("a").text for row in soup.find_all("div", {"class": "ftr"})]

        for url in urls:
            if not self.resources_left:
                console.log(f"No more resources to process. Aborting {relative_url}.")
                return
            resource_path = f"{relative_url}{url}"
            if resource_path.endswith("/"):
                await self.crawl(client, resource_path, depth=depth+1)
            elif resource_path.endswith(".html"):
                console.log(f"Ignoring {resource_path} (HTML not supported)")
            else:
                await self.process(resource_path)

    async def process(self, resource_path):
        console.log(f"process {resource_path}")
        async with db_session() as session:
            document = await get_document(resource_path, session)
            console.log(f"results for {resource_path}: {document}")
            if document:
                self.resources_left -= 1

    async def execute(self) -> bool:
        async with httpx.AsyncClient() as client:
            for relative_url in self.relative_urls:
                if not self.resources_left:
                    console.log("No more resources to process. Ending execute.")
                    return True
                await self.crawl(client, relative_url)

    async def test_process(self):
        for r in ('a', 'b'):
            await self.process(r)
