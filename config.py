import sys
from argparse import ArgumentParser
from pathlib import Path

from pydantic import BaseConfig


class Config(BaseConfig):
    host: str = "https://consumer-api.leafly.com"
    strain_url: str = "/api/strain_playlists/v2"
    comment_url: str = "/api/strains/v1"
    request_attempts: int = 5
    items_per_page: int = 50
    pages_one_time: int = 4
    comments_one_time: int = 50
    update_strains = False
    dump_strains: Path = Path("data/strains.pickle")

    def __init__(self):
        super().__init__()
        self.parse_args()

        data_path = self.dump_strains.parent
        if not data_path.exists():
            data_path.mkdir(exist_ok=True)

    def parse_args(self):
        parser = ArgumentParser()
        parser.add_argument(
            "--update", "-u",
            action="store_true",
            help="Update strains",
            default=False
        )
        args = parser.parse_args(sys.argv[1:])

        if args.update:
            self.update = True


cfg = Config()
