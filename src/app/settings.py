import re
from typing import List

from pydantic import BaseSettings, validator


RELATIVE_DIR_REGEX = re.compile(r"^\/[\w\-_]+\/$")
SETTINGS = None


class Settings(BaseSettings):
    db_file: str
    fetcher_base_url: str
    fetcher_fernet_secret: str
    fetcher_offset: int = 0
    fetcher_relative_urls: str|List[str] = []
    fetcher_max_resources: int = 10
    fetcher_max_depth: int = 2
    db_resources_path: str = "src/data"

    @validator("fetcher_relative_urls", pre=True, always=True)
    def split_relative_urls_verify_format(cls, v):
        if not v:
            return []
        urls = v.split(",")
        for url in urls:
            if not re.match(RELATIVE_DIR_REGEX, url):
                raise ValueError(f"{url} does not match pattern.")
        return urls

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "scrape_"


def get_settings():
    global SETTINGS
    if not SETTINGS:
        SETTINGS = Settings()
    return SETTINGS
