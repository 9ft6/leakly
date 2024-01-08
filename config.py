from pathlib import Path

from pydantic import BaseConfig


class Config(BaseConfig):
    host: str = "https://consumer-api.leafly.com"
    api: str = "/api/strain_playlists/v2"
    request_attempts: int = 5
    items_per_page: int = 20
    pages_one_time: int = 10
    dump_name: Path = Path("data/strains.json")

    def __init__(self):
        super().__init__()


cfg = Config()
