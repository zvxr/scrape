from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    db_file: str
    fetcher_base_url: str
    fetcher_relative_urls: List[str] = []
    fetcher_max_resources: int = 100
    fercher_max_depth: int = 2
    db_resources_path: str = "src/scrape/db/data"

    class Config:
        env_prefix = "scrape_"
